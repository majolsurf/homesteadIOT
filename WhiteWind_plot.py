#this example reads and prints CO2 equiv. measurement, TVOC measurement, and temp every 2 seconds
  
import time
from time import sleep
from datetime import datetime
from Adafruit_CCS811 import Adafruit_CCS811
import matplotlib.pyplot as plt
import numpy as numps
from numpy import median

enableMedianFilter = 1;

ccs =  Adafruit_CCS811()
samples = 256;#1024;
minibuffSamples = 4;
sig_co2 = [0 for i in range(samples)]
sig_tvoc = [0 for i in range(samples)]
sig_temp = [24 for i in range(samples)]
minibuff_co2 = [0 for i in range(minibuffSamples)]
minibuff_tvoc = [0 for i in range(minibuffSamples)]
minibuff_temp = [24 for i in range(minibuffSamples)]

plt.ion()

print "Before While Loop 1"    

while not ccs.available():
        print "Inside While Loop 1"    
	pass
temp = ccs.calculateTemperature()
ccs.tempOffset = temp - 25.0

while(1):
	try:
            ccs_avail = ccs.available();
        except:
            ccs_avail = 0;
	#if ccs.available():
        if ccs_avail:
            try:
                temp = ccs.calculateTemperature()
	    except:
                temp = temp;
            try:
                ccsReadData = ccs.readData();
            except:
                ccsReadData = ccsReadData;
            
	    if not ccsReadData:
              try:  
                  stor_tvoc = ccs.getTVOC();
              except:
                  stor_tvoc = stor_tvoc;
              try:
                  stor_co2 = ccs.geteCO2();
              except:
                  stor_co2 = stor_co2;
                
              if enableMedianFilter == 1:  
                  minibuff_temp = minibuff_temp[1::] + minibuff_temp[:1:];
                  minibuff_tvoc = minibuff_tvoc[1::] + minibuff_tvoc[:1:];
                  minibuff_co2 = minibuff_co2[1::] + minibuff_co2[:1:];
                  minibuff_temp[-1] = temp;
                  minibuff_tvoc[-1] = stor_tvoc;
                  minibuff_co2[-1] = stor_co2;
              
                  temp = median(minibuff_temp);
                  stor_tvoc = median(minibuff_tvoc);
                  stor_co2 = median(minibuff_co2);
            
              stor_datetime = str(datetime.now());
	      print "Time: ",stor_datetime,"  CO2: ", stor_co2, "ppm, TVOC: ", stor_tvoc, " temp: ", temp
	      wfile = open("log_air_quality.txt", "a+")
              wfile.write(str(stor_datetime)+","+str(temp)+","+str(stor_co2)+","+str(stor_tvoc)+"\n")
              wfile.close()
              sig_temp = sig_temp[1::] + sig_temp[:1:];
              sig_tvoc = sig_tvoc[1::] + sig_tvoc[:1:];
              sig_co2 = sig_co2[1::] + sig_co2[:1:];
              sig_temp[-1] = temp;
              if stor_tvoc < 65535:
                  sig_tvoc[-1] = stor_tvoc;
              else:
                  sig_tvoc[-1] = sig_tvoc[-2];
              if stor_co2 < 65535:
                  sig_co2[-1] = stor_co2;
              else:
                  sig_co2[-1] = sig_co2[-2];
              
              plt.clf()
              plt.subplot(3,1,1)
              plt.plot(sig_temp)
              plt.show()
              plt.pause(0.0001)
              #plt.clf()
              
              plt.subplot(3,1,2)
              plt.plot(sig_co2)
              plt.show()
              plt.pause(0.0001)
              #plt.clf()
              
              plt.subplot(3,1,3)
              plt.plot(sig_tvoc)
              plt.show()
              plt.pause(0.0001)
              #plt.clf()
	    else:
	      print "ERROR!"
	      while(1):
	      	pass
	sleep(1)
