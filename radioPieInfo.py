# -*- coding: utf-8 -*-
"""
Internet radio info app

@author: Polonius
"""

import tkinter as tk
from tkinter import messagebox as msb

from bs4 import BeautifulSoup
import requests

class MainWindow:
    radioTitle='None'
    songInfo='None'
    url=""
    
    def __init__(self,url):
        self.window=tk.Tk()
        self.window.title("Radio Pie Info")
        self.window.geometry("340x70")
        self.url=url
        self.window.after(1,self.createLabels) #Don't know why I need 2x after
        self.window.mainloop()
        
    def createLabels(self):
        for i in range(6):
            try:
                radioInfo=getRadioInfo(self.url)
            #do something
            except:
                print('Error has occured!')
                if i>=5:
                    msb.showerror.showinfo("Error",
                     "An error has occured and the program have to be shout down :(")
                    self.quit()
            else:
                break
            
        self.radioTitle=radioInfo['radio']
        self.songInfo=radioInfo['nowPlaying']
        
        progInfo=tk.Label(self.window,text="Radio Pie Info")
        progInfo2=tk.Label(self.window,text="by Jacek Piłka, 2020")
        progInfo.grid(row=1,column=1)
        progInfo2.grid(row=1,column=2)
        
        radioDesc=tk.Label(self.window,text="Radio: ")
        radio = tk.Entry(self.window,width=40)
        radio.insert(0,self.radioTitle)
        radioDesc.grid(row=2,column=1)
        radio.grid(row=2,column=2)
        
        songDesc=tk.Label(self.window,text="Now playing: ")
        song = tk.Entry(self.window,width=40)
        song.insert(0,self.songInfo)
        songDesc.grid(row=3,column=1)
        song.grid(row=3,column=2)
        
        self.window.after(5000, self.createLabels)
        
    def quit(self):
        self.window.destroy()
        
class SettingWindow:
    
    serverName = ""
    
    def __init__(self):
        self.window=tk.Tk()
        self.window.title("Server Setting")
        self.window.geometry("300x50")
        self.serverName = tk.StringVar(self.window)
        self.serverName.set("radiopi.local")
        self.createControls()
        self.window.mainloop()
        
    def createControls(self):
        serverDesc=tk.Label(self.window,text="Server: ")
        server = tk.Entry(self.window,width=40,textvariable=self.serverName)
        serverDesc.grid(row=2,column=1)
        server.grid(row=2,column=2)
    
        setButt=tk.Button(self.window)
        setButt["text"]="Set"
        setButt["command"]=self.openMainWindow
        setButt.grid(row=3,column=1)
        
        progInfo=tk.Label(self.window,text="Radio Pie Info, by Jacek Piłka, 2020")
        progInfo.grid(row=3,column=2)
        
    def openMainWindow(self):
        url="http://"+self.serverName.get()+":8080/requests/status.xml"
        self.quit()
        MainWindow(url)
        
    def quit(self):
        self.window.destroy()
        
#getInfo function        
def getRadioInfo(url):
    logInfo = ('', 'raspberry') #login+password
    # Send HTTP GET request to server and attempt to receive a response
    response = requests.get(url, auth=logInfo)
      
    # If the HTTP GET request can be served
    if response.status_code == 200:
       xml=response.text
       soup=BeautifulSoup(xml,'xml') #xml parser
       #Return dictionary with radio title and song info
       return {'radio':soup('info',{'name':'title'})[0].text,
               'nowPlaying':soup('info',{'name':'now_playing'})[0].text}
    return{'radio':'No Data','nowPlaying':'No Data'}

#main
SettingWindow()
