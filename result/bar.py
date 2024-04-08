import numpy as np
#the scrip to draw graph
import pandas as pd
import plotly.express as px
#importation to see the check current directory
import os

#line to check the current directory
print("Current working directory:", os.getcwd())

#drawing graph using CSV file
df =pd.read_csv("gw_receiving_tracker.csv")
fig =px.bar(df, x= "sim_time", y= "packet")
fig.show()