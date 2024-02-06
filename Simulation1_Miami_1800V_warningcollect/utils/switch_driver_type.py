import os
import sys

import os
import sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
    
import optparse
import traci
import traci.constants as tc

import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd



#choose a random interval like [a,a+2]
def random_interval(v):
    a=0
    b=0
    random.seed(v)
    a= random.uniform(1000,7000)
    random.seed(v+"_1")
    c= random.uniform(1000,7000)
    b= a+2
    d= c+2
    return a,b,c,d

#Define the random change behavior to danger and to normal
def Random_Behaviour(v):
    (a_toDanger,b_toDanger)=(0,0)
    (a_toNormal,b_Normal)=(0,0)
    (a_toDanger,b_toDanger,a_toNormal,b_Normal)=random_interval(v)
   
    if (a_toDanger,b_toDanger) == (a_toNormal,b_Normal):
        return Random_Behaviour(v)
    if b_toDanger > a_toNormal:
        a_toDanger,b_toDanger,a_toNormal,b_Normal=a_toNormal,b_Normal,a_toDanger,b_toDanger
        
        return  a_toDanger,b_toDanger,a_toNormal,b_Normal
    else :
        return a_toDanger,b_toDanger, a_toNormal,b_Normal


# Pushing a driver to be dangerous
def Make_vehicle_Danger(v,Id,MaxSpeed, Accel,Decel,step):
        
        M = MaxSpeed + np.random.uniform(10,30)
        A= Accel+np.random.uniform(0.5,1)
        D= Decel + np.random.uniform(1,2)
        traci.vehicle.setMaxSpeed(v, M); 
        traci.vehicle.setAccel(v,A);  #set the speed of the vehicle v
        traci.vehicle.setDecel(v,D); 
     
        print(' For {} : The accel is {}. The Decel is {}. The Max Speed is {}'.format(v, A, D, M))
        print(step)
        print(traci.vehicle.getDistance(v))
                
                #Vehicle_Danger(v,Id,M,A,D,G,T,step)

# Pushing a driver to be normal
def Make_vehicle_normal(v,Id,MaxSpeed, Accel,Decel,step):

        traci.vehicle.setAccel(v,Accel);  #set the speed of the vehicle v
        traci.vehicle.setMaxSpeed(v, MaxSpeed); 
        traci.vehicle.setDecel(v,Decel); 
        
        print(' For {} : The accel is {}. The Decel is {}. The Max Speed is {} '.format(v, Accel, Decel, MaxSpeed))
        print(step)
        print(traci.vehicle.getDistance(v))
        #Vehicle_Danger(v)


    


#Function to change behavior randomly       
def Danger(v,MaxSpeed, Accel,Decel,step):

            a_toDanger,b_toDanger, a_toNormal,b_Normal = Random_Behaviour(v)
            
            if b_toDanger > a_toNormal:
                a_toDanger,b_toDanger,a_toNormal,b_Normal=a_toNormal,b_Normal,a_toDanger,b_toDanger
            

            #print("the vehicle {} and when danger between {} and {}. Them went normal Between {} and {}.". format( v,a_toDanger,b_toDanger, a_toNormal,b_Normal) )

            Id = traci.vehicle.getTypeID(v)
            

            if  a_toDanger <= traci.vehicle.getDistance(v) <= b_toDanger and Id == "Dangerous" : #ma khassnich ndir intervale kbir hite kib9a ihssa naffse vehicle f kola metre
                                                                                   
               print("rani fate 10<x<20")
               Make_vehicle_Danger(v,Id,MaxSpeed, Accel,Decel,step)
               print("the vehicle {} became dangerous between {}m and {}m. Then went normal between {}m and {}m.". format( v,a_toDanger,b_toDanger, a_toNormal,b_Normal) )

               #return Danger(MaxSpeed, Accel,Decel,MinGap,Tau,step)

            elif  a_toNormal <= traci.vehicle.getDistance(v) <= b_Normal and Id != "DEFAULT_VEHTYPE" : #makhassnich ndire egale dangereux hire makatakhodhache la condission
                print("rani fate 20")
                Make_vehicle_normal(v,Id,MaxSpeed, Accel,Decel,step)
                print("the vehicle {} became dangerous between {}m and {} m. Then went normal Between {}m and {}m.". format( v,a_toDanger,b_toDanger, a_toNormal,b_Normal) )
