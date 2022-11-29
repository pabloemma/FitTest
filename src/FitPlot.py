import pandas as pd
import numpy as np
import numpy.polynomial.polynomial as poly
import json as js
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import sys
import os


class FitPlot(object):

    def __init__(self,config_file=None,data_frame=None):

        
        
        version = 0.1
        
        print("********************************************* \n\n")
        print("Hello to FitPlot \n\n ")
        print(version)
        print("\n********************************************* \n\n")
         

        self.mydata = data_frame
        global DEBUG
        DEBUG = False

    def pandas2numpy_nd(self,data_frame):
        """ converts the pandas data frame to a numpy ndarray, however before we do this we
        convert the time axis to numbers"""
        num_arr = data_frame.to_numpy()
        print("array type",type(num_arr))
        print("array data type",num_arr.dtype)
        print("the array",num_arr)
        return num_arr



    def fit_polynomial(self ,data_frame = None, deg = 1):
        "fits polynomial of nth degree to data frame"
        
        data_frame['date'] =  pd.to_numeric(data_frame.date) #neede for numpy to be happy
        
        coefs = poly.polyfit(data_frame['date'],data_frame['weight_kg'], deg = deg)
        
        if(DEBUG): print("fit coefficiants",coefs)
        
        # get first and last elemnt in the date column
        window = [data_frame['date'].iloc[0],data_frame['date'].iloc[-1]]
        x_model = np.linspace(window[0], window[1], 200)
        
        if(DEBUG): print(window)
        
        ffit = poly.Polynomial(coefs)    # instead of np.poly1d
        
        if(DEBUG): print(data_frame['date'])

        # temporary: plot here
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
 
        ax.plot(data_frame['date'],data_frame['weight_kg'],color='green',marker = '*',linestyle ='None')
 
        ax.plot(x_model, ffit(x_model))
        
        plt.show()
        return 