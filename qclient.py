#!/usr/bin/python
#coding:utf-8
import os
import sys
import win32ras
import threading
import StringIO
import config
import pcap,dpkt,socket
from PyQt4 import QtCore, QtGui, uic
from ui_client import Ui_MainWindow
import res_rc

KEY,KLEN = '!@#$%^',6
def encrypt(src):
    output = StringIO.StringIO()
    for i in range(len(src)):
        key = KEY[i%KLEN]
        ch = ord(src[i]) ^ ord(key)
        ihex = hex(ch).upper()
        if '0X' in ihex:
            ihex = ihex[2:]
        output.write(ihex)
    return output.getvalue()

def decrypt(dest):
    output = StringIO.StringIO()
    if len(dest)%2 != 0:
        dest  = "0" + dest
    for i in range(0,len(dest),2):
        key = KEY[(i/2)%KLEN]
        b = int(dest[i+1],16)
        b = b + 16 * int(dest[i],16)
        b = b ^ ord(key)
        output.write(chr(b))
    return output.getvalue()

RASFILE = 'ras.cfg'
USERDATA = '%s/rasuser.data'%os.path.expanduser('~')


class ConnectThread(QtCore.QThread):

    onConnect = QtCore.pyqtSignal(int,bool,object)

    def __init__(self, userdata,parent=None):
        super(ConnectThread, self).__init__(parent)
        self.userdata = userdata
        self.mutex = QtCore.QMutex()
        self.done = False
        self.start()

    def run(self):
        username,passwd,savepass = self.userdata
        try:
            self.save_user(username,passwd,savepass)
            win32ras.SetEntryDialParams(RASFILE,("pyras", "", "", username, passwd, ""),savepass)
            session = win32ras.Dial(None,RASFILE,("pyras", "", "", username, passwd, ""),None)
            self.onConnect.emit(self,session)
        except:
            self.onConnect.emit(self,None)

        self.mutex.lock()
        self.done = True
        self.mutex.unlock()

class ClientApp(QtGui.QMainWindow):
    def __init__(self, *args):
        super(ClientApp, self).__init__(*args)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        try:
            self.init_config()
        except: pass

    def init_config(self):
        """ 初始化配置数据 """
        rsfile = open(RASFILE,'wb')
        rsfile.write(config.rascfg)
        rsfile.close()

        if os.path.exists(USERDATA):
            udfile = open(USERDATA,'rb')
            content = udfile.read().strip()
            udfile.close()
            if content:
                name,pwd,isave = decrypt(content).split(":")
                self.ui.username.setText(name)
                self.ui.password.setText(pwd)
                self.ui.savepass.setChecked(isave==1)

    def save_user(self,name,pwd,isave):
        """ 保存用户数据 """
        udfile = open(USERDATA,'wb')
        _save = isave and 1 or 0
        udfile.write(encrypt("%s:%s:%s"%(name,pwd,_save)))
        udfile.close()

    def on_connect(self,session):
        pass

    def connect_ras(self):
        """ 认证登录 """
        username = self.ui.username.text()
        passwd = self.ui.password.text()
        savepass = self.ui.savepass.isChecked()
        if not username or not passwd:
            self.info(u"帐号和密码不能为空")
            return
        conn_thd = ConnectThread(username,passwd,savepass)
        conn_thd.onConnect.connect(self.on_connect)

    @QtCore.pyqtSlot()
    def on_connect_clicked(self):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    capp = ClientApp()
    capp.show()
    sys.exit(app.exec_())