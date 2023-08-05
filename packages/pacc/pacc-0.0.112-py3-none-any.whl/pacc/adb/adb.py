from os import popen, system
from ..tools import findAllWithRe, sleep, EMail
from random import randint
from ..mysql import RetrieveBaseInfo, UpdateBaseInfo
from datetime import datetime
from .uia import UIAutomator


def getOnlineDevices():
    res = popen('adb devices').read()
    res = findAllWithRe(res, r'(.+)\tdevice')
    for i in range(len(res)):
        res[i] = res[i].replace(':5555', '')
    return res


class ADB:
    rebootPerHourRecord = [-1]

    def __init__(self, deviceSN, offlineCnt=1):
        """
        :param deviceSN:
        """
        system('adb reconnect offline')
        self.device = RetrieveBaseInfo(deviceSN)
        if self.device.ID not in getOnlineDevices():
            if not offlineCnt % 20:
                EMail(self.device.SN).sendOfflineError()
            sleep(30)
            self.__init__(deviceSN, offlineCnt+1)
        self.cmd = 'adb -s %s ' % self.device.ID
        if not self.getIPv4Address():
            print(self.getIPv4Address())
            sleep(3)
            self.__init__(deviceSN)
        if not self.getIPv4Address() == self.device.IP:
            UpdateBaseInfo(deviceSN).updateIP(self.getIPv4Address())
            self.device = RetrieveBaseInfo(deviceSN)
        self.tcpip()
        self.reconnect()
        self.cmd = 'adb -s %s ' % self.device.IP
        self.uIA = UIAutomator(deviceSN)
        if not self.getModel() == self.device.Model:
            UpdateBaseInfo(deviceSN).updateModel(self.getModel())
            self.device = RetrieveBaseInfo(deviceSN)
        if 'com.android.settings' in self.getCurrentFocus():
            if self.device.Model == 'M2007J22C':
                self.pressBackKey()

    def getModel(self):
        return popen(self.cmd + 'shell getprop ro.product.model').read()[:-1]

    def getCurrentFocus(self):
        r = popen(self.cmd + 'shell dumpsys window | findstr mCurrentFocus').read()
        print(r)
        return r

    def pressKey(self, keycode):
        print('正在让%s按下%s键' % (self.device.SN, keycode))
        system(self.cmd + 'shell input keyevent ' + keycode)
        sleep(1)

    def pressHomeKey(self):
        self.pressKey('KEYCODE_HOME')

    def pressMenuKey(self):
        self.pressKey('KEYCODE_MENU')

    def pressBackKey(self):
        self.pressKey('KEYCODE_BACK')

    def usb(self, timeout=2):
        """
        restart adbd listening on USB
        :return:
        """
        cmd = self.cmd + 'usb'
        system(cmd)
        print(cmd)
        sleep(timeout)

    def tcpip(self):
        """
        restart adbd listening on TCP on PORT
        :return:
        """
        system(self.cmd + 'tcpip 5555')
        sleep(1)

    def connect(self, timeout=1):
        """
        connect to a device via TCP/IP [default port=5555]
        :return:
        """
        system('adb connect %s' % self.device.IP)
        sleep(timeout)
        if self.device.IP not in getOnlineDevices():
            self.connect(timeout + 1)

    def disconnect(self):
        """
        disconnect from given TCP/IP device [default port=5555], or all
        :return:
        """
        system('adb disconnect %s' % self.device.IP)
        sleep(3)

    def reconnect(self):
        self.disconnect()
        self.connect()

    def taps(self, instructions):
        for x, y, interval, tip in instructions:
            print(tip)
            self.uIA.tap(x, y, interval)

    def start(self, Activity, wait=True):
        cmd = 'shell am start '
        if wait:
            cmd += '-W '
        cmd = self.cmd + cmd + Activity
        system(cmd)
        print(cmd)

    def swipe(self, x1, y1, x2, y2, duration=-1):
        """
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :param duration: the default duration is a random integer from 300 to 500
        :return:
        """
        if duration == -1:
            duration = randint(300, 500)
        cmd = self.cmd + 'shell input swipe %d %d %d %d %d' % (x1, y1, x2, y2, duration)
        system(cmd)
        print(cmd)

    def longPress(self, x, y, duration=-1):
        """
        :param x:
        :param y:
        :param duration: the default duration is a random integer from 1000 to 1500
        :return:
        """
        if duration == -1:
            duration = randint(1000, 1500)
        self.swipe(x, y, x, y, duration)

    def reboot(self):
        self.rebootByIP()

    def rebootByCMD(self, cmd):
        popen(cmd)
        print('已向设备%s下达重启指令' % self.device.SN)
        sleep(69)
        self.__init__(self.device.SN)

    def rebootByIP(self):
        if self.device.IP not in getOnlineDevices():
            self.__init__(self.device.SN)
        self.rebootByCMD('adb -s ' + self.device.IP + ' reboot')

    def rebootPerHour(self, tip='小时'):
        if not datetime.now().hour == self.rebootPerHourRecord[0]:
            self.rebootPerHourRecord = [datetime.now().hour]
        if self.device.SN not in self.rebootPerHourRecord:
            print('按每' + tip + '重启一次的计划重启' + self.device.SN)
            self.reboot()
            self.rebootPerHourRecord.append(self.device.SN)
            return True
        return False

    def rebootPerDay(self, hours=[0]):
        if datetime.now().hour in hours:
            self.rebootPerHour(tip='天')
            return True
        return False

    def getIPv4Address(self):
        rd = popen(self.cmd + 'shell ifconfig wlan0').read()
        IPv4Address = findAllWithRe(rd, r'inet addr:(\d+.\d+.\d+.\d+)  Bcast:.+')
        if len(IPv4Address) == 1:
            IPv4Address = IPv4Address[0]
        return IPv4Address

    def getIPv6Address(self):
        rd = popen(self.cmd + 'shell ifconfig wlan0').read()
        IPv6Address = findAllWithRe(rd, r'inet6 addr: (.+:.+:.+)/64 Scope: Global')
        if 0 < len(IPv6Address) <= 2:
            IPv6Address = IPv6Address[0]
            print('设备%s的公网IPv6地址为：%s' % (self.device, IPv6Address))
        else:
            print('%s的公网IPv6地址数大于2或小于0，正在尝试重新获取')
            self.reboot()
            self.getIPv6Address()
