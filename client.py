#!/usr/bin/python
#coding:utf-8 
import os
import win32ras
import threading
import StringIO
import config
from Tkinter import *
from tkMessageBox import askokcancel,showwarning
import pcap,dpkt,socket

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

class ClientApp():

    session = None
    rasfile = None
    ckp_task = None

    def __init__(self,master):
        """ init ui """ 
        self.master = master
        photo=PhotoImage(data=config.logodata)
        im = Label(master,image=photo)
        im.image = photo
        im.pack()

        frame = Frame(master)
        frame.config(width=320)
        frame.pack()        

        Label(frame, text=u"帐号名").grid(row=0,padx=5,pady=10, sticky=W)
        Label(frame, text=u"密  码").grid(row=1,padx=5,sticky=W)

        self.username_val = StringVar()
        self.password_val = StringVar()
        self.username = Entry(frame, textvariable=self.username_val,width=35)
        self.password = Entry(frame, show="*",textvariable=self.password_val,width=35)
        self.username.grid(row=0, column=1,columnspan=3,sticky=W+E)
        self.password.grid(row=1, column=1,columnspan=3,sticky=W)

        self.msg_val = StringVar()
        self.msg = Label(frame,textvariable=self.msg_val)
        self.msg.grid(row=2,columnspan=4,padx=5,pady=5, sticky=W+E)
        
        frame2 = Frame(master, relief=RAISED, borderwidth=1)
        frame2.pack(fill=BOTH, expand=1)
        self.savepass_val = IntVar()
        self.savepass = Checkbutton(master, text=u"保存密码", variable=self.savepass_val)
        self.connect = Button(master, text=u" 连接 ", command=self.connect_ras)
        self.disconnect = Button(master, text=u" 断开 ", command=self.disconnect_ras,state=DISABLED)   
        self.disconnect.pack(side=RIGHT, padx=5, pady=5)     
        self.connect.pack(side=RIGHT, padx=5, pady=5)
        self.savepass.pack(side=RIGHT, padx=5, pady=5)   
        try:
            self.init_config() 
        except:
            pass
    
        self.master.protocol("WM_DELETE_WINDOW",self.exit_handle)

    def init_config(self):
        rsfile = open(RASFILE,'wb')
        rsfile.write(config.rascfg)
        rsfile.close()

        if os.path.exists(USERDATA):
            udfile = open(USERDATA,'rb')
            content = udfile.read().strip()
            udfile.close()
            if content:
                name,pwd,isave = decrypt(content).split(":")
                self.username_val.set(name)
                self.password_val.set(pwd)
                self.savepass_val.set(int(isave))



    def save_user(self,name,pwd,isave):
        udfile = open(USERDATA,'wb')
        if self.savepass_val.get() == 0:
            pwd = ''
        udfile.write(encrypt("%s:%s:%s"%(name,pwd,isave)))  
        udfile.close()   

    def check_proxy(self):
        if not self.ckp_task.is_proxy:
            self.master.after(1000*1, self.check_proxy)
        else:
            self.disconnect_ras()
            showwarning(u"警告",u"检测到您使用了代理软件，网络被断开")



    def check_conn(self):
        if self.session is None:
            self.master.after(500, self.check_conn)
        else:
            if self.session[0] == 0:
                self.info(u"网络连接失败，错误代码：%s"%self.session[0])
                self.connect.config(state=NORMAL)
            else:
                if self.session[1] > 0:
                    self.info(u"认证失败，错误代码：%s"%self.session[1])
                    self._disconnect_ras()
                    self.connect.config(state=NORMAL)
                else:
                    self.info(u"认证成功，连接已经建立")
                    self.connect.config(state=DISABLED)
                    self.disconnect.config(state=NORMAL)

                    #启动代理检测
                    self.ckp_task = ChkProxy()
                    self.check_proxy()

                    
    def connect_ras(self):
        username = self.username_val.get()
        passwd = self.password_val.get()
        savepass = self.savepass_val.get()
        if not username or not passwd:
            self.info(u"帐号和密码不能为空")
            return
        def _connect():
            try:
                self.save_user(username,passwd,savepass)
                win32ras.SetEntryDialParams(RASFILE,("pyras", "", "", username, passwd, ""),savepass)
                self.session = win32ras.Dial(None,RASFILE,("pyras", "", "", username, passwd, ""),None)
            except:
                pass

        self.info(u"正在连接，请稍候...")
        self.connect.config(state=DISABLED)
        self._disconnect_ras()
        threading.Thread(target=_connect).start()
        self.check_conn()

    def _disconnect_ras(self):
        if self.ckp_task:
            self.ckp_task.stop()
        if self.session:
            try:
                win32ras.HangUp(self.session[0])
            except Exception, e:
                print e
            self.session = None

        conns = win32ras.EnumConnections()
        if conns:
            for conn in conns:
                try:
                    win32ras.HangUp(conn[0])
                except:pass
                


    def disconnect_ras(self):
        self._disconnect_ras()
        self.info(u"连接已经断开")
        self.connect.config(state=NORMAL)
        self.disconnect.config(state=DISABLED)

    def info(self,msg):
        self.msg_val.set(msg)

    def exit_handle(self):
        def _exit():
            if os.path.exists(RASFILE):
                os.remove(RASFILE)
            self.master.destroy()
        if self.session:
            if askokcancel(u"退出","退出程序会断开您的网络连接，确认这样做吗？"):
                self._disconnect_ras()
                _exit()
        else:_exit()    

class ChkProxy(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ipaddrs = socket.gethostbyname_ex(socket.gethostname())[2]
        print self.ipaddrs
        self.is_proxy = False
        self.running = True
        self.start()

    def stop(self):
        self.running = False

    def run(self):
        pc = pcap.pcap()
        _get_type = lambda pd: pd.__class__.__name__
        _get_ip = lambda ipdat:'%d.%d.%d.%d' % tuple(map(ord, list(ipdat)))
        while self.running:
            try:
                ptime,pdata=pc.next()
                p = dpkt.ethernet.Ethernet(pdata)
                if _get_type(p.data) == "IP":
                    dstip = _get_ip(p.data.dst)
                    if _get_type(p.data.data)== "TCP":
                        data = p.data.data.data
                        if dstip in self.ipaddrs:
                            if data.startswith("GET") \
                                or data.startswith("POST"):
                                    self.is_proxy = True
            except:
                pass

if __name__ == '__main__':
    master = Tk()
    master.title(u"宽带客户端")
    master.maxsize(335,280)
    master.minsize(335,280)
    client = ClientApp(master)
    master.mainloop()

