#!/usr/bin/python
#coding:utf-8 
from __future__ import unicode_literals  
import os
import win32ras
import threading
import config
from Tkinter import *
from tkMessageBox import askokcancel

RASFILE = 'ras.cfg'

class ClientApp():

    session = None
    rasfile = None

    def __init__(self,master):
        """ init ui """ 
        self.master = master
        photo=PhotoImage(file="logo.gif")
        im = Label(master,image=photo)
        im.image = photo
        im.pack()
        frame = Frame(master)
        frame.config(width=320)
        frame.pack()        

        Label(frame, text="帐号名").grid(row=0,padx=5,pady=10, sticky=W)
        Label(frame, text="密  码").grid(row=1,padx=5,sticky=W)

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
        self.savepass = Checkbutton(master, text="保存密码", variable=self.savepass_val)
        self.connect = Button(master, text=" 连接 ", command=self.connect_ras)
        self.dicconnect = Button(master, text=" 断开 ", command=self.disconnect_ras,state=DISABLED)   
        self.dicconnect.pack(side=RIGHT, padx=5, pady=5)     
        self.connect.pack(side=RIGHT, padx=5, pady=5)
        self.savepass.pack(side=RIGHT, padx=5, pady=5)   

        self.init_config() 

        self.master.protocol("WM_DELETE_WINDOW",self.exit_handle)

    def init_config(self):
        if not os.path.exists(RASFILE):
            with open(RASFILE,'wb') as rsfile:
                rsfile.write(config.rascfg)

    def check_conn(self):
        if self.session is None:
            self.master.after(500, self.check_conn)
        else:
            if self.session[0] == 0:
                self.info("网络连接失败，错误代码：%s"%self.session[0])
                self.connect.config(state=NORMAL)
            else:
                if self.session[1] > 0:
                    self.info("认证失败，错误代码：%s"%self.session[1])
                    self.disconnect_ras()
                    self.connect.config(state=NORMAL)
                    
    def connect_ras(self):
        def _connect():
            username = self.username_val.get()
            passwd = self.password_val.get()
            savepass = self.savepass_val.get()

            try:
                win32ras.SetEntryDialParams(RASFILE,("pyras", "", "", username, passwd, ""),savepass)
                self.session = win32ras.Dial(
                    None, 
                    RASFILE, 
                    ("pyras", "", "", "username", "password", ""), 
                    None
                )
            except Exception, e:
                raise e

        self.info("正在连接，请稍候...")
        self.connect.config(state=DISABLED)
        self.disconnect_ras()
        threading.Thread(target=_connect).start()
        self.check_conn()

    def disconnect_ras(self):
        if self.session:
            try:
                win32ras.HangUp(self.session[0])
            except :
                pass
            self.session = None 

    def info(self,msg):
        self.msg_val.set(msg)

    def exit_handle(self):
        if self.session and askokcancel("退出","退出程序会断开您的网络连接，确认这样做吗？"):
            self.disconnect_ras()
        self.master.destroy()
   
if __name__ == '__main__':
    master = Tk()
    master.title("宽带拨号器")
    master.maxsize(335,280)
    master.minsize(335,280)
    client = ClientApp(master)
    master.mainloop()