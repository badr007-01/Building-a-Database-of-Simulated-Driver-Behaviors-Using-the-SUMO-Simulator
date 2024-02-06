
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


def get_x_step_DS(df, features_to_keep ,features_to_sum,steps):
    
    # Round down the "Step" column to the nearest multiple of 5
    df["Step"] = df["Step"].apply(lambda n: ((n // steps) + 1) * steps)

    # Group by "VehicleID" and "Step" and calculate the sum for specified features
    features = features_to_sum
    #grouped_df = df.groupby(["VehicleID", "Step"])[features].sum()
    
    #grouped_df = df.groupby(["VehicleID", "Step"]).agg({"Distance_driven": "first", **{feature: "sum" for feature in features}})
    grouped_df = df.groupby(["VehicleID", "Step"]).agg({**{feature: "max" for feature in features_to_keep},
                                                        **{feature: "sum" for feature in features_to_sum}})
    
    #garder on tete que les valuers sont


    return grouped_df



def Data_Base2(df,step ,label, vehicleID, Distance_driven, speed_respect, secure_dist, ttc_respect, safe_dist, emergency_brake):
      #temporary_df = pd.DataFrame([Id], columns=['id_voiture',  'time', 'acceleration', "Distance"])
      #df.loc[ str(Type)+"_"+str(Distance_driven) ,:] = [ label, VehiceID, Distance_driven, Sum_warning]
      #if speed_respect  != 0 or secure_dist != 0 or ttc_respect != 0 or safe_dist != 0 or emergency_brake != 0:
      df = df._append({
                'Step': step,
                'Label': label,
                'VehicleID': vehicleID,
                'Distance_driven': Distance_driven,
                'Speed_respect': speed_respect,
                "secure_dist": secure_dist,
                'TTC_respect': ttc_respect,
                'safe_dist': safe_dist,
                'Emergency_Brake': emergency_brake,
            }, ignore_index=True)
      
      return df

#Create a Data Base for the simmulation for plotting
def Data_Base1(df,Time, Type , v, Distance_driven, acceleration, Speed ,id_edge, Allowed_Speed):
      #temporary_df = pd.DataFrame([Id], columns=['id_voiture',  'time', 'acceleration', "Distance"])
      df.loc[ str(v)+"_"+str(Time) ,:] = [ Time,Type , v, Distance_driven, acceleration, Speed, id_edge,Allowed_Speed]
      return df  

#Create a Data Base for the simmulation for plotting
def Data_Base0(df, v,Time, position, Distance_driven, acceleration, Deceleration, Speed, MaxSpeed,Allowed_Speed):
      #temporary_df = pd.DataFrame([Id], columns=['id_voiture',  'time', 'acceleration', "Distance"])
      df.loc[ str(v)+"_"+str(Time) ,:] = [v, Time, position, Distance_driven, acceleration, Deceleration, Speed, MaxSpeed,Allowed_Speed]
      return df 


def Add_warnings(df, label ,vehicleID, distance_driven, speed_respect, secure_dist,ttc_respect, safe_dist, emergency_brake ):
    # Si le véhicule est déjà présent dans le DataFrame, ajoute les alertes
    Sum_warning = speed_respect + secure_dist +ttc_respect + safe_dist + emergency_brake

    if vehicleID in df['VehicleID'].values:
        #print("__________________________________________")
       
        df.loc[df['VehicleID'] == vehicleID, 'Distance_driven'] = distance_driven
        df.loc[df['VehicleID'] == vehicleID, 'Sum_warning'] += Sum_warning
       
        df.loc[df['VehicleID'] == vehicleID, 'Sum_warning_speed'] += speed_respect
        df.loc[df['VehicleID'] == vehicleID, 'Sum_secure_dist'] += secure_dist
        df.loc[df['VehicleID'] == vehicleID, 'Sum_TTC_respect'] += ttc_respect
        df.loc[df['VehicleID'] == vehicleID, 'Sum_safe_dist'] += safe_dist
        df.loc[df['VehicleID'] == vehicleID, 'Sum_Emergency_Brake'] += emergency_brake

        

        #df.loc[df['VehicleID'] == vehicleID, 'Warning_SUM'] += warning_3 + warning_1 + warning_2 + warning_4 + warning_5
    else:
        # Sinon, ajoute une nouvelle ligne au DataFrame
        df = df._append({
            "Label": label,
            'VehicleID': vehicleID,
            'Distance_driven':distance_driven,
            'Sum_warning': Sum_warning,
            'Sum_warning_speed': speed_respect,
            'Sum_secure_dist' :secure_dist,
            'Sum_TTC_respect' : ttc_respect,
            'Sum_safe_dist' : safe_dist,
            'Sum_Emergency_Brake' : emergency_brake
            

            #'Warning_SUM': warning_1 + warning_2 + warning_3 + warning_4 + warning_5
        }, ignore_index=True)

        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    return df
