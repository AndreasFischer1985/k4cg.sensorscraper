#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os, tkinter, requests, time, pandas

db1="https://graphs.k4cg.org/api/datasources/proxy/1/query?db=sensors"
db2="https://graphs.k4cg.org/api/datasources/proxy/8/query?db=homeassi"
db3="https://graphs.k4cg.org/api/datasources/proxy/4/query?db=wip"
        
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
    print("visitors:\t\t "+str(l.cget("text")))
    
    # db=sensors
    #-------------    
    print("\n**********\ndb=sensors\n**********\n")
    door_status=requests.get(db1+"&q=SELECT last(\"value\") FROM \"door_status\"").json()["results"][0]["series"][0]["values"][0]
    print("door_status:\t\t "+str(door_status))
    irc=requests.get(db1+"q=SELECT last(\"value\") FROM \"irc\"").json()["results"][0]["series"][0]["values"][0]
    print("irc:\t\t\t "+str(irc))
    network_hosts=requests.get(db1+"&q=SELECT last(\"value\") FROM \"network_hosts\"").json()["results"][0]["series"][0]["values"][0]
    print("network_hosts:\t\t "+str(network_hosts))
    mqtt_consumer=requests.get(db1+"&q=SELECT last(\"value\") FROM \"mqtt_consumer\"").json()
    if(len(mqtt_consumer)>1): mqtt_consumer=mqt_consumer["results"][0]["series"][0]["values"][0] # sensor tends to be offline
    else: mqtt_consumer=[timestamp,-1]
    print("mqtt_consumer:\t\t "+str(mqtt_consumer))
    humidity=requests.get(db1+"&q=SELECT last(\"value\") FROM \"humidity\"").json()["results"][0]["series"][0]["values"][0]
    print("humidity:\t\t "+str(humidity))
    tinker_noise=requests.get(db1+"&q=SELECT last(\"value\") FROM \"tinker_noise\"").json()["results"][0]["series"][0]["values"][0]
    print("tinker_noise:\t\t "+str(tinker_noise))
    tinker_temp=requests.get(db1+"&q=SELECT last(\"value\") FROM \"tinker_temp\"").json()["results"][0]["series"][0]["values"][0]
    print("tinker_temp:\t\t "+str(tinker_temp))
    darksky_ext_temp=requests.get(db1+"&q=SELECT last(\"value\") FROM \"darksky_ext_temp\"").json()["results"][0]["series"][0]["values"][0]
    print("darksky_ext_temp:\t "+str(darksky_ext_temp))
    openweathermap_ext_temp=requests.get(db1+"&q=SELECT last(\"value\") FROM \"openweathermap_ext_temp\"").json()["results"][0]["series"][0]["values"][0]
    print("openweathermap_ext_temp\t:"+str(openweathermap_ext_temp))

    # db=homeassi
    #-------------
    print("\n***********\ndb=homeassi\n***********\n")
    temp_ttennis=requests.get(db2+"&q=SELECT last(\"value\") FROM \"sensor.temp_ttennis\"").json()["results"][0]["series"][0]["values"][0]
    print("temp_ttennis:\t\t "+str(temp_ttennis))
    temp_co2=requests.get(db2+"&q=SELECT last(\"value\") FROM \"sensor.temp_co2\"").json()["results"][0]["series"][0]["values"][0]
    print("temp_co2:\t\t "+str(temp_co2))
    temp_c=requests.get(db2+"&q=SELECT last(\"value\") FROM \"C\"").json()["results"][0]["series"][0]["values"][0]
    print("temp_c:\t\t\t "+str(temp_c))
    sound_intensity=requests.get(db2+"&q=SELECT last(\"value\") FROM \"sensor.sound_intensity\"").json()["results"][0]["series"][0]["values"][0]
    print("sound_intensity:\t "+str(sound_intensity))
    light=requests.get(db2+"&q=SELECT last(\"value\") FROM \"sensor.light\"").json()["results"][0]["series"][0]["values"][0]
    print("light:\t\t\t "+str(light))
    co2=requests.get(db2+"&q=SELECT last(\"value\") FROM \"sensor.co2\"").json()["results"][0]["series"][0]["values"][0]
    print("co2:\t\t\t "+str(co2))
    bier=requests.get(db2+"&q=SELECT last(\"value\") FROM \"sensor.bier\"").json()["results"][0]["series"][0]["values"][0]
    print("bier:\t\t\t "+str(bier))
    apfelschorle=requests.get(db2+"&q=SELECT last(\"value\") FROM \"sensor.apfelschorle\"").json()["results"][0]["series"][0]["values"][0]
    print("apfelschole:\t\t "+str(apfelschorle))
    mate_cola=requests.get(db2+"&q=SELECT last(\"value\") FROM \"sensor.mate_cola\"").json()["results"][0]["series"][0]["values"][0]
    print("mate_cola:\t\t "+str(mate_cola))
    club_mate=requests.get(db2+"&q=SELECT last(\"value\") FROM \"sensor.club_mate\"").json()["results"][0]["series"][0]["values"][0]
    print("club_mate:\t\t "+str(club_mate)+"\n\n")

    p=pandas.DataFrame([l.cget("text"),timestamp,door_status[1],door_status[0],irc[1],irc[0],network_hosts[1],network_hosts[0],mqtt_consumer[1],mqtt_consumer[0],humidity[1],humidity[0],tinker_noise[1],tinker_noise[0],tinker_temp[1],tinker_temp[0],darksky_ext_temp[1],darksky_ext_temp[0],openweathermap_ext_temp[1],openweathermap_ext_temp[0],temp_ttennis[1],temp_ttennis[0],temp_co2[1],temp_co2[0],temp_c[1],temp_c[0],sound_intensity[1],sound_intensity[0],light[1],light[0],co2[1],co2[0],bier[1],bier[0],apfelschorle[1],apfelschorle[0],mate_cola[1],mate_cola[0],club_mate[1],club_mate[0]]).transpose()
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

p=pandas.DataFrame(["visitors","localtime","door_status","t0","irc","t1","network_hosts","t2","mqtt_consumer","t3","humidity","t4","tinker_noise","t5","tinker_temp","t6","darksky_ext_temp","t7","openweathermap_ext_temp","t8","temp_ttennis","t9","temp_co2","t10","temp_c","t11","sound_intensity","t12","light","t13","co2","t14","bier","t15","apfelschorle","t16","mate_cola","t17","club_mate","t18"]).transpose()
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
