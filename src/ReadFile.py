# a common file read class for pandas


import pandas as pd
import numpy as np
import json as js
import matplotlib.pyplot as plt

from datetime import datetime

import FitPlot as fp


import sys
import os


class ReadFile(object):

    def __init__(self,config_file=None):


     
        
        # block for default values

        self.csv_delimeter_in       = ','
        self.csv_delimeter_out      = ','
        self.sheetname_in           = 'Sheet1' 
        self.sheetname_out           = 'Sheet1' 

        #generate error list
        self.setup_error()

        #print out program info
        self.header()



        #read configuration file

        if config_file == None:
            print('no config file given, exiting')
            sys.exit(0)
        elif os.path.exists(config_file) :
                self.read_config(config_file)
        else:
            print(" Config file does not exist, exiting     ", config_file)

        # initialize the fitting
        self.fpi = fp.FitPlot()
    
    def drop_my_colums(self):
        "here we drop the colums and create a new data structure"
        
        self.new_data =  self.mydata.drop(columns = self.drop_columns)
        self.pandas_info(self.new_data)
        
    def header(self):

        version = '0.1' 

        print('This is the FitTest program \n written by Andi Klein ')
        print('November 2022 \n \n')  
        print('version:  ', version) 

    def fit_data(self):
        self.fpi.pandas2numpy_nd(self.new_data)
        self.fpi.fit_polynomial(self.new_data)
        return

    def print_error(self,err_number,problem):
        print(self.error_list[err_number],'  ',problem)
        return



    def pandas_info(self,data_frame):
        '''gives info on the current data'''
        data_frame.info(verbose = True)



    def read_config(self,config_file):
        '''Reads configuration file in json format
            allowed formats so far: csv, xls
            if we have an xls file we also need the sheet name
            default is Sheet1   
            '''



        print("reading config file ", config_file)    # WGH mod: clarify which conf json we're actually reading
        with open(config_file, "r") as f:
            
            #output block
            myconf = js.load(f)
            output_path            = myconf['IO']['output_path']
            output_file            = myconf['IO']['output_file']
            self.output_format     = myconf['IO']['output_format']
            self.sheetname_out      = myconf['IO']['sheetname_out']
            self.csv_delimeter_out  = myconf['IO']['csv_delimeter_out']
         
            self.out_file          = output_path+output_file


            #input block
            input_path             = myconf['IO']['input_path']
            input_file             = myconf['IO']['input_file']
            self.input_format      = myconf['IO']['input_format']
            self.sheetname_in     = myconf['IO']['sheetname_in']
            self.csv_delimeter_in  = myconf['IO']['csv_delimeter_in']

            
            self.in_file           = input_path+input_file
    

            #data block
            drop_col                =myconf['DATA']['col']
            # now spit the string into a list
            self.drop_columns = list(drop_col.split(' '))
            print(self.drop_columns)


        # check if input file exists:
        if not os.path.exists(self.in_file):
            self.print_error(1,self.in_file)
            sys.exit(0)
        


        return

    def read_file(self):
        '''read either exel or csv file'''

        if(self.input_format == 'csv'):
            self.read_csv_file()
        elif(self.input_format == 'xls'):
            self.read_excel_file()
        else:
            self.print_error(0,self.input_format)

    def read_csv_file(self):


        #first deal with date in column 1 according to 
        # https://stackoverflow.com/questions/17465045/can-pandas-automatically-read-dates-from-a-csv-file
        dateparse = lambda x: datetime.strptime(x, '%y-%m-%d')


        
        #open input file
        self.mydata = pd.read_csv(self.in_file,self.csv_delimeter_in,parse_dates=['date'], date_parser=dateparse)
        print('\n\n ******************************************\n')
        self.pandas_info(self.mydata)
        print('\n\n ******************************************\n')
        return

    def read_excel_file(self):
        
        xlsx = pd.ExcelFile(self.in_file)
        self.mydata = pd.read_excel(xlsx,self.sheetname_in)

    def setup_error(self):
        '''block of errors'''
        self.error_list = []
        self.error_list.append('input format not known ') #0 counter of error list
        self.error_list.append('input file not found ') #1






if __name__ == "__main__":

    config_file = '/Users/klein/git/FitTest/config/ReadFile.json'


    RF = ReadFile(config_file=config_file)
    RF.read_file()
    RF.drop_my_colums()
    RF.fit_data()
    


