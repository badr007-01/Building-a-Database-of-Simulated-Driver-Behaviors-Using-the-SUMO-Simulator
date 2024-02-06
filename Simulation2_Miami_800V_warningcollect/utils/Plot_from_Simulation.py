
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd

def plotting_DB(df1,List_V,X,Y):
  fig, ax = plt.subplots(figsize=(8,6))
  #bp = p_df.groupby('class').plot(x='a', y='b',ax=ax)
  for Id in List_V:
      for label, df in df1.groupby('VehicleID'):
         if Id == label:
              df.plot(x=X, y=Y, kind="line", ax=ax, label=label)
              plt.xlabel(X, size = 20)
              plt.ylabel(Y, size = 20)
              plt.title("Changement of drivers behaviour", size = 25)
  plt.legend()
  plt.show()
