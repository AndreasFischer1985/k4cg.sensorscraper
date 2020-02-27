#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import tkinter 
import requests
import time
import pandas
    
def tick(): 
    global stopscraping
    t1  = time.time() #set t1 to now (in seconds since epoch)
    if (t1 % 60 < 1) & (stopscraping==False): # start scraping once if time/60 is approximately 0
        print(time.ctime(t1) + " ; ") # ctime converts seconds to string
        scrape(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.localtime(t1))) # use localtime for timestamps; gmtime converts seconds to UTC time_struct based on UTC
        stopscraping=True # don't start scraping again if you already did so this very second
    if t1 % 60 >= 1:
         stopscraping=False # set "stopscrapings" to False if the first second of the current minute is over
    c1.config(text=time.strftime('%H:%M:%S',time.localtime(t1))) 
    c1.after(200,tick) # trigger tick each 200 ms

def scrape(timestamp):
    print("visitors:\t\t"+str(l.cget("text")))
    door_status=requests.get("https://graphs.k4cg.org/api/datasources/proxy/1/query?db=sensors&q=SELECT last(\"value\") FROM \"door_status\"").json()["results"][0]["series"][0]["values"][0]
    print("door_status:\t\t"+str(door_status))
    irc=requests.get("https://graphs.k4cg.org/api/datasources/proxy/1/query?db=sensors&q=SELECT last(\"value\") FROM \"irc\"").json()["results"][0]["series"][0]["values"][0]
    print("irc:\t\t\t"+str(irc))
    network_hosts=requests.get("https://graphs.k4cg.org/api/datasources/proxy/1/query?db=sensors&q=SELECT last(\"value\") FROM \"network_hosts\"").json()["results"][0]["series"][0]["values"][0]
    print("network_hosts:\t\t"+str(network_hosts))
    mqtt_consumer=requests.get("https://graphs.k4cg.org/api/datasources/proxy/4/query?db=wip&q=SELECT last(\"value\") FROM \"mqtt_consumer\"").json()
    if(len(mqtt_consumer)>1): mqtt_consumer=mqt_consumer["results"][0]["series"][0]["values"][0] # sensor seems to be offline at the moment
    else: mqtt_consumer=[timestamp,-1]
    print("mqtt_consumer:\t\t"+str(mqtt_consumer))
    humidity=requests.get("https://graphs.k4cg.org/api/datasources/proxy/1/query?db=sensors&q=SELECT last(\"value\") FROM \"humidity\"").json()["results"][0]["series"][0]["values"][0]
    print("humidity:\t\t"+str(humidity))
    tinker_noise=requests.get("https://graphs.k4cg.org/api/datasources/proxy/1/query?db=sensors&q=SELECT last(\"value\") FROM \"tinker_noise\"").json()["results"][0]["series"][0]["values"][0]
    print("tinker_noise:\t\t"+str(tinker_noise))
    tinker_temp=requests.get("https://graphs.k4cg.org/api/datasources/proxy/1/query?db=sensors&q=SELECT last(\"value\") FROM \"tinker_temp\"").json()["results"][0]["series"][0]["values"][0]
    print("tinker_temp:\t\t"+str(tinker_temp))
    darksky_ext_temp=requests.get("https://graphs.k4cg.org/api/datasources/proxy/1/query?db=sensors&q=SELECT last(\"value\") FROM \"darksky_ext_temp\"").json()["results"][0]["series"][0]["values"][0]
    print("darksky_ext_temp:\t"+str(darksky_ext_temp))
    openweathermap_ext_temp=requests.get("https://graphs.k4cg.org/api/datasources/proxy/1/query?db=sensors&q=SELECT last(\"value\") FROM \"openweathermap_ext_temp\"").json()["results"][0]["series"][0]["values"][0]
    print("openweathermap_ext_temp\t:"+str(openweathermap_ext_temp)+"\n\n")
    p=pandas.DataFrame([l.cget("text"),timestamp,door_status[1],door_status[0],irc[1],irc[0],network_hosts[1],network_hosts[0],mqtt_consumer[1],mqtt_consumer[0],humidity[1],humidity[0],tinker_noise[1],tinker_noise[0],tinker_temp[1],tinker_temp[0],darksky_ext_temp[1],darksky_ext_temp[0],openweathermap_ext_temp[1],openweathermap_ext_temp[0]]).transpose()
    p.to_csv("./daten.csv", mode='a', header=False)

def minus():
    x=l.cget("text")
    if(x=="NA"):x=0
    x=int(x)-1
    if(x<0):x="NA"
    l.config(text=x)
    
def plus():
    x=l.cget("text")
    if(x=="NA"):x=-1
    x=int(x)+1
    if(x<0):x="NA"
    l.config(text=x)

p=pandas.DataFrame(["visitors","localtime","door_status","t0","irc","t1","network_hosts","t2","mqtt_consumer","t3","humidity","t4","tinker_noise","t5","tinker_temp","t6","darksky_ext_temp","t7","openweathermap_ext_temp","t8"]).transpose()
p.to_csv("./daten.csv", mode='w', header=False)

door_status=requests.get("https://graphs.k4cg.org/api/datasources/proxy/1/query?db=sensors&q=SELECT last(\"value\") FROM \"door_status\"").json()["results"][0]["series"][0]["values"][0]
n=5
if(door_status[1]==0): n="NA"
if(len(sys.argv)>1): n=sys.argv[len(sys.argv)-1]
   
print ("Currently there are assumed to be %s lifeforms present in the K4CG.\nData will be written to ./daten.csv each minute.\n" % n)
       
w=tkinter.Tk()
w.geometry("200x100")
w.title("AF")
stopscraping=False

p = tkinter.Frame(w) 
p.pack(fill = tkinter.BOTH, expand = True)

c1=tkinter.Label(p,font=('arial',15,'bold'),bg='green')
l=tkinter.Label(master=p,text=str(n),bg="ivory",font=("FreeMono",10))
b1=tkinter.Button(master=p,text="-",bg="tan",command=minus,font=("FreeMono",15))
b2=tkinter.Button(master=p,text="+",bg="tan",command=plus,font=("FreeMono",15))

c1.pack(side = tkinter.TOP, expand = True, fill = tkinter.BOTH)
l.pack(side = tkinter.TOP, expand = True, fill = tkinter.BOTH)
b1.pack(side = tkinter.LEFT, expand = True, fill = tkinter.BOTH)
b2.pack(side = tkinter.RIGHT, expand = True, fill = tkinter.BOTH)

w.attributes('-topmost','True')
tick()

w.mainloop()
