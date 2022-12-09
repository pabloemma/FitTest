import pandas as pd
import numpy as np
import numpy.polynomial.polynomial as poly
import json as js
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import ROOT as ro

import sys
import os


class FitPlot(object):

    def __init__(self,data_x,data_y,config_file=None,data_frame=None,legend_1=None,legend_2=None,title=None):

        
        
        version = 0.1
        self.print_star = '*'*80
        print(self.print_star)
        print("Hello to FitPlot \n\n ")
        print(version)
        print(self.print_star)
         

        self.mydata = data_frame
        global DEBUG
        DEBUG = True

        self.legend_1 = legend_1
        self.legend_2 = legend_2
        self.plot_title = title
        self.data_x = data_x
        self.data_y = data_y

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
        
        data_frame[self.data_x] =  pd.to_numeric(data_frame[self.data_x]) #neede for numpy to be happy
        
        coefs = poly.polyfit(data_frame[self.data_x],data_frame[self.data_y], deg = deg)
        
        if(DEBUG): print("fit coefficiants",coefs)
        
        # get first and last elemnt in the date column
        window = [data_frame[self.data_x].iloc[0],data_frame[self.data_x].iloc[-1]]
        x_model = np.linspace(window[0], window[1], 200)
        
        if(DEBUG): print(window)
        
        ffit = poly.Polynomial(coefs)    # instead of np.poly1d
        if DEBUG: print(ffit)
        
        if(DEBUG): print(data_frame[self.data_x])

        # temporary: plot here
        #fig = plt.figure()
        #ax = fig.add_subplot(1,1,1)
 
        #ax.plot(data_frame['date'],data_frame['weight_kg'],color='green',marker = '*',linestyle ='None')
 
        #ax.plot(x_model, ffit(x_model))
        
        #plt.show()
        self.plot_fit(data_frame,x_model,ffit)
        #self.root_plot(data_frame,x_model,ffit)
        return 

    def plot_fit(self,data_frame,x_model,ffit):

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
 
        ax.plot(data_frame[self.data_x],data_frame[self.data_y],color='green',marker = '*',linestyle ='None')
 
        ax.plot(x_model, ffit(x_model))
        ax.legend([self.legend_1,self.legend_2])
        ax.set_title(self.plot_title)
        
        plt.show()
        self.root_plot(data_frame,x_model,ffit)
        return 

    def root_plot(self,data_frame,x_model,ffit):

        c1 = ro.TCanvas("solveig")
        #c1.SetFillColor( 42 )
        c1.SetGrid()
        c1.cd()

        #c1.Draw()
        # now create a TGraph
        # extracting dataframe into two numpy arrays
        arr0 = data_frame[self.data_x].to_numpy()
        arr1 = arr0.astype(np.float64)
        
        arr2 = data_frame[self.data_y].to_numpy()
        print(arr1.size,arr1.dtype,arr2.dtype)
        gr1 = ro.TGraph(arr1.size,arr1,arr2)
        gr1.Fit('pol2')
        gr1.SetMarkerSize(2.5)
        gr1.SetMarkerColor(4)
        gr1.Draw('AP*')
        c1.Update()
        
        #c1.GetFrame().SetFillColor( 21 )
        #c1.GetFrame().SetBorderSize( 12 )
        #c1.Modified()
        #c1.Update()

        val = input("Enter your value: ")
        return

        #histo1 = ro.TH1D(histo1,'solveig',50,data_frame[self.data_x.loc(0),data_frame[self.data_x.loc(-1)])
