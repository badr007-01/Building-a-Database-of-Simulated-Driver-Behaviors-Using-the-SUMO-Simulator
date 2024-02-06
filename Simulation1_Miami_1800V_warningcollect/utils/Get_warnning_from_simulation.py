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




def get_DistanceV(v,n):
    Leader = traci.vehicle.getLeader(v)
    Distance_interV = None
    if Leader != None:
        Distance_interV = Leader[n]
    return Distance_interV 
        
def gap_interV(v, vehicles_IDList):
    LaneID = traci.vehicle.getLaneID(v)
    #Leader = traci.vehicle.getLeader(v)
    Distance_interV = None

    LeaderID = get_DistanceV(v,0)
    
    for vs in vehicles_IDList:
         LaneID_v = traci.vehicle.getLaneID(vs)   #the ID lane of othe vehicles
         
         if  vs != v and LaneID_v == LaneID and LeaderID is not None:
            
            Distance_interV = get_DistanceV(v,1) + traci.vehicle.getMinGap(v)

    return Distance_interV 
        

def Break_speed(v,n):
    LaneID = traci.vehicle.getLaneID(v)

    speed_limit = traci.lane.getMaxSpeed(LaneID)

    if speed_limit <n:
        traci.vehicle.setAcceleration(v,4,200)


# function to compute the if the non respect of the speed limite. return  0 or 1

def Speed_respect(speed_v,LaneID):
    speed_limit = traci.lane.getMaxSpeed(LaneID)
    if speed_v > (speed_limit + 0.3):
       #print ("speed_v.>>>>>>>>>>>>>>>", speed_v )
       #print ("speed_limit.............................", speed_limit )
    
       return 1
    
    return 0


# function to verify if the secure distance <2s. return 0 or 1
def Secure_dist(v, Distance_interv):
    
    speed_v = traci.vehicle.getSpeed(v)

    if speed_v != 0 and Distance_interv is not None:
        sec = Distance_interv/speed_v

        if sec < 1.5 and Distance_interv is not None:
            #print ("Distance_interv.____", Distance_interv )
            #print ("speed_v =============================", speed_v )
            #print ("Secure_dist.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", sec )
            #print ("name ....................................../..........", v )
            return 1
    return 0

# how to calibrat the TTC limit
def set_ttc_limit(simulation_context):
    # Define TTC limit based on safety requirements and simulation context
    if simulation_context == "highway":
        ttc_limit = 3.0 
    elif simulation_context == "urban":
        ttc_limit = 2.0#0.6  
    else:
        ttc_limit = 4.0  # Default TTC limit if context is not specified

    return ttc_limit


# Function to verify if TTC < 5s. return 0 or 1. cuz A shorter TTC indicates a higher risk of collision, while a longer TTC suggests a lower risk. 
def TTC_respect(v,Leader, Distance_interv, Distance_interv_threshold=3):
    
    speed_interV = 0 
    speed_v = traci.vehicle.getSpeed(v)

    if Distance_interv is not None and Leader is not None:
        speed_leader = traci.vehicle.getSpeed(Leader)
        if speed_leader < speed_v:
           speed_interV = speed_leader - speed_v
        else:
           return 0
        
        if speed_interV != 0:
            result = -Distance_interv / speed_interV
            
            if 0 < result < Distance_interv_threshold: #  and Distance_interv is not None:
                #print ("TTC_respect.......", result )
                #print ("Distance_interv. _________________", Distance_interv )
                #print ("speed_interV.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", speed_interV )
                #print ("name ................................................./..........", v )
                return 1
    
    return 0

#respect of the safe distance 
def Safe_dist(Distance_interv,v):
    #print ("Safe_dist._____________________", Distance_interv )
    if  Distance_interv is not None and Distance_interv < 2.5:
        #print ("Distance_interv.>>>>>>>>>>>>>", Distance_interv )
        #print ("name ................................................./..........", v )
        return 1
    
    return 0


# function to verify the braking < -4 m^2/s. return 0 or 1 
def Emergency_brake(v):
    TypeID= traci.vehicle.getTypeID(v)
    if  traci.vehicle.getAcceleration(v)*(-1) > traci.vehicletype.getDecel(TypeID):
        #print ("Distance_interv.>>>>>>>>>>>>>", Distance_interv )
        #print ("name ................................................./..........", v )
        return 1
    
    return 0

#Transformer unne base de donnes en faisant la somme de tout les warning pour chaques  
# def get_x_step_DS (df, steps):
    
#     df["Step"] = df["Step"].apply(lambda n: (n//steps)*steps)
#     df1=df.groupby(["VehicleID","Step"]).sum(["Speed_respect","secure_dist","TTC_respect","safe_dist","Emergency_Brake"])
    
#     return df1 

#def Create_df_warning(vehicleID, speed_respect, secure_dist, TTC_respect, safe_dist):
   

    # Ajoute des exemples d'alertes pour quelques véhicules
    #df1 = Add_warnings(df, vehicleID, speed_respect, secure_dist, TTC_respect, safe_dist)

    #return df1


#sortie nombre globale de 