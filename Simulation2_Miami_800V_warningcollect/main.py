#!/usr/bin/env python

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

from utils.Collect_data_from_Simulation import Add_warnings
from utils.Collect_data_from_Simulation  import *
from utils.Get_warnning_from_simulation import *

from utils.Plot_from_Simulation import *
from utils.switch_driver_type import *


# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars



def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options




def run2():
    # vehicles=traci.vehicle.getIDList();
    step = 0;
    Accel= 1.5;
    MaxSpeed = 10; 
    Decel =4; 
    MinGap=2;
    Tau = 1;
    global Collect_DataBase

    NumverVV= 6000


   
     # Crée un DataFrame vide
    
    df = pd.DataFrame(columns=["Label", "VehicleID","Distance_driven", "Sum_warning","Sum_warning_speed", "Sum_secure_dist", "Sum_TTC_respect", "Sum_safe_dist" ,"Sum_Emergency_Brake"])
    df2 = pd.DataFrame( columns=['Step', "Label", "VehicleID", "Distance_driven",'Speed_respect',"secure_dist","TTC_respect", "safe_dist" ,"Emergency_Brake"])
    df3 = pd.DataFrame( columns=['Step', "Label", "VehicleID", "Distance_driven",'Acceleration', "Speed","Allowed_Speed","gap"])

   
   # Run a simulation until all vehicles have arrived
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

    

        vehicles_IDList = traci.vehicle.getIDList() 
        for v in vehicles_IDList:
            #Danger(v,MaxSpeed,Accel,Decel,step) 

            #call the parameters
            VtypeID = traci.vehicle.getTypeID(v)
            GetV_Distance= traci.vehicle.getDistance(v)
            LaneID = traci.vehicle.getLaneID(v)
            speed_v = traci.vehicle.getSpeed(v)
            maxspeed= traci.lane.getMaxSpeed(LaneID) 


            secure_dist = 0
            ttc_respect = 0
            speed_respect = 0
            safe_dist = 0

            Leader = get_DistanceV(v,0)


            # we get the distacne inter Vehicular
            Distance_interv = gap_interV(v, vehicles_IDList)
                
            
            secure_dist = Secure_dist(v, Distance_interv)
            ttc_respect = TTC_respect(v,Leader, Distance_interv, set_ttc_limit("urban"))
            safe_dist = Safe_dist(Distance_interv,v)
        
            speed_respect = Speed_respect(speed_v,LaneID)
            emergency_brake = Emergency_brake(v)



            
            
            
            Collect_DataBase = Add_warnings(df, VtypeID  ,v , GetV_Distance, speed_respect, secure_dist,ttc_respect, safe_dist, emergency_brake ) 
            Collect_DataBase2 =Data_Base2(df2, traci.simulation.getTime(),  VtypeID, v, GetV_Distance, speed_respect, secure_dist, ttc_respect, safe_dist, emergency_brake)
            Collect_DataBase3 =Data_Base1(df3, traci.simulation.getTime(),VtypeID, v , GetV_Distance ,traci.vehicle.getAcceleration(v), speed_v , maxspeed,Distance_interv)

            
            
            #Add_warnings(df, v, 1, 1, 1, step)
       
            df = Collect_DataBase
            df2 = Collect_DataBase2
            df3 = Collect_DataBase3
            
            
            
            
            #Collect_DataBase2 =Data_Base1(df2, traci.simulation.getTime(), v, speed_respect, secure_dist ,ttc_respect, safe_dist ,traci.vehicle.getAcceleration(v),traci.vehicle.getSpeed(v), Leader)
                                                                     


        #Collect_info_plot_1V(VehicleID, accelerations, Decelerations, Distances, Taus,MinGaps)
        
        NumverVV = NumverVV - traci.simulation.getArrivedNumber()
        
        print("The number of vehicles waiting is",NumverVV)
 
        df.to_csv("Output_Dataset\800V_DS_Sum_wornging_NewV.csv")
        df2.to_csv("Output_Dataset\800V_DS_Separated_worning_NewV.csv")
        df3.to_csv("Output_Dataset\800V_DS_Export_dataframe_NewV.csv")
        step +=1
        #print(Collect_DataBase)
        #DataBase.to_csv("export_dataframe_0.csv")
    
    return df , df2, df3
    

 
# main entry point
if __name__ == "__main__":

    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "SUMO_Networks\Miami_Test8_800V_IDM_warningcollect.sumocfg",
                            "-X", "never", 
                            "--collision.stoptime", "40",
                            "--collision.action","warn"])
    #traci.init(9999)

    
    DataBase, DataBase2, DataBase3= run2()
    #print(traci.simulation._getUniversal(tc.VAR_EMERGENCY_DECEL),"222222",traci.simulation.getEmergencyStoppingVehiclesIDList(),"#3333333", traci.simulation.getCollidingVehiclesIDList())

   
    
    DataBase.to_csv("Output_Dataset\800V_DS_Sum_wornging_NewV.csv")
    DataBase2.to_csv("Output_Dataset\800V_DS_Separated_worning_NewV.csv")
    DataBase3.to_csv("Output_Dataset\800V_DS_Export_dataframe_NewV.csv")

    # Feature_to_sum= ['Speed_respect', 'secure_dist', 'TTC_respect', 'safe_dist', 'Emergency_Brake']
    # features_to_keep = ['Distance_driven', 'Label']
    #DataBase2 = get_x_step_DS (DataBase2,features_to_keep, Feature_to_sum, 50)
    #DataBase2.to_csv("DS_sum_each_Xstep_V1.csv")
   

    #List_V = ["Danger1","Normal1","Slow1"]
    #plotting_DB(DataBase,List_V,"Distance_driven","acceleration")
    #plotting_DB(DataBase,List_V,"Distance_driven","speed")

    traci.close()
    sys.stdout.flush()

