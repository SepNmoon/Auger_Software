import tkinter
import numpy as np
from tkinter import ttk
from tkinter import Scrollbar
from tkinter.filedialog import askdirectory,askopenfilename
import itertools
import shlex
from decimal import Decimal
from tabulate import tabulate
import webbrowser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import matplotlib.pyplot as plt


'''-------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------
read Auger data from EADL_database'''
#get atomic number and atomic name 
def get_atom():
    number_name=dict()
    with open('EADL_database/atom.txt','r') as f: 
        for line in f.readlines(): #read each line
            curLine=line.strip().split(" ")
            number_name[int(curLine[0])]=curLine[1]
    return number_name

#get electron configuration
def get_shell():
    number_shell=dict()
    with open('EADL_database/shell.txt','r') as f:
        for line in f.readlines():        
            curLine=line.strip().split(" ")
            curLine=['0' if i=='' else i for i in curLine]    
            if len(curLine)==30:
                pass
            else:
                for i in range(30-len(curLine)):
                    curLine.append('0') #add 0 for empty space
            temp=dict()
            temp['K']=float(curLine[1])
            temp['L1'],temp['L2'],temp['L3']=float(curLine[2]),float(curLine[3]),float(curLine[4])
            temp['M1'],temp['M2'],temp['M3'],temp['M4'],temp['M5']=float(curLine[5]),float(curLine[6]),float(curLine[7]),float(curLine[8]),float(curLine[9])
            temp['N1'],temp['N2'],temp['N3'],temp['N4'],temp['N5'],temp['N6'],temp['N7']=float(curLine[10]),float(curLine[11]),float(curLine[12]),float(curLine[13]),float(curLine[14]),float(curLine[15]),float(curLine[16])
            temp['O1'],temp['O2'],temp['O3'],temp['O4'],temp['O5'],temp['O6'],temp['O7']=float(curLine[17]),float(curLine[18]),float(curLine[19]),float(curLine[20]),float(curLine[21]),float(curLine[22]),float(curLine[23])
            temp['P1'],temp['P2'],temp['P3'],temp['P4'],temp['P5']=float(curLine[24]),float(curLine[25]),float(curLine[26]),float(curLine[27]),float(curLine[28])
            temp['Q1']=float(curLine[29])
            for key in temp:
                if temp[key]==0:
                    temp[key]=None #replace 0 with None 
            number_shell[int(curLine[0])]=temp
    return number_shell

#get electrons energies
def get_energies():  
    number_energies=dict()
    with open('EADL_database/energies.txt','r') as f:
        for line in f.readlines():        
            curLine=line.strip().split(" ")
            curLine=['0' if i=='' else i for i in curLine]         
            if len(curLine)==30:
                pass
            else:
                for i in range(30-len(curLine)):
                    curLine.append('0')
            temp=dict()
            temp['K']=float(curLine[1])
            temp['L1'],temp['L2'],temp['L3']=float(curLine[2]),float(curLine[3]),float(curLine[4])
            temp['M1'],temp['M2'],temp['M3'],temp['M4'],temp['M5']=float(curLine[5]),float(curLine[6]),float(curLine[7]),float(curLine[8]),float(curLine[9])
            temp['N1'],temp['N2'],temp['N3'],temp['N4'],temp['N5'],temp['N6'],temp['N7']=float(curLine[10]),float(curLine[11]),float(curLine[12]),float(curLine[13]),float(curLine[14]),float(curLine[15]),float(curLine[16])
            temp['O1'],temp['O2'],temp['O3'],temp['O4'],temp['O5'],temp['O6'],temp['O7']=float(curLine[17]),float(curLine[18]),float(curLine[19]),float(curLine[20]),float(curLine[21]),float(curLine[22]),float(curLine[23])
            temp['P1'],temp['P2'],temp['P3'],temp['P4'],temp['P5']=float(curLine[24]),float(curLine[25]),float(curLine[26]),float(curLine[27]),float(curLine[28])
            temp['Q1']=float(curLine[29])
            for key in temp:
                if temp[key]==0:
                    temp[key]=None
            number_energies[int(curLine[0])]=temp
    return number_energies

#get barkla and orbital notation
def get_notation():
    barkla_orbital=dict()
    with open('EADL_database/notation.txt','r') as f:
        for line in f.readlines():
            curLine=line.strip().split(" ")
            barkla_orbital[curLine[0]]=curLine[1]+' '+curLine[2]
    return barkla_orbital

#get the max and min Auger energies for each element
def get_range():
    number_range=dict()
    with open('EADL_database/energies_range.txt','r') as f:
        for line in f.readlines():
            curLine=line.strip().split(" ")
            temp=dict()
            temp['Max']=float(curLine[1])
            temp['Min']=float(curLine[2])
            number_range[int(curLine[0])]=temp
    return number_range

'''----------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------
read cross section data from Scofield_csv_database'''
#get cross section data for specified photon and number
def get_cross_section(number,photon_energy):
    photon_shell_cross=dict()
    shell_cross=dict()
    with open('Scofield_csv_database/%d.csv'%number,'r') as f: 
        f.readline()
        for line in f.readlines():
        # store all cross section for different photon energies
            if number<=4:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                photon_shell_cross[float(curLine[0])]=temp  
            elif number<=10:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                photon_shell_cross[float(curLine[0])]=temp  
            elif number<=12:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                photon_shell_cross[float(curLine[0])]=temp
            elif number<=18:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                photon_shell_cross[float(curLine[0])]=temp
            elif number<=20:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['4s1/2']=float(curLine[8])
                photon_shell_cross[float(curLine[0])]=temp
            elif number<=30:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['3d3/2']=float(curLine[8])
                temp['3d5/2']=float(curLine[9])
                temp['4s1/2']=float(curLine[10])
                photon_shell_cross[float(curLine[0])]=temp
            elif number<=36:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['3d3/2']=float(curLine[8])
                temp['3d5/2']=float(curLine[9])
                temp['4s1/2']=float(curLine[10])
                temp['4p1/2']=float(curLine[11])
                temp['4p3/2']=float(curLine[12])
                photon_shell_cross[float(curLine[0])]=temp
            elif number<=38:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['3d3/2']=float(curLine[8])
                temp['3d5/2']=float(curLine[9])
                temp['4s1/2']=float(curLine[10])
                temp['4p1/2']=float(curLine[11])
                temp['4p3/2']=float(curLine[12])
                temp['5s1/2']=float(curLine[13])
                photon_shell_cross[float(curLine[0])]=temp
            elif number==46:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['3d3/2']=float(curLine[8])
                temp['3d5/2']=float(curLine[9])
                temp['4s1/2']=float(curLine[10])
                temp['4p1/2']=float(curLine[11])
                temp['4p3/2']=float(curLine[12])
                temp['4d3/2']=float(curLine[13])
                temp['4d5/2']=float(curLine[14])
                photon_shell_cross[float(curLine[0])]=temp
            elif number<=48:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['3d3/2']=float(curLine[8])
                temp['3d5/2']=float(curLine[9])
                temp['4s1/2']=float(curLine[10])
                temp['4p1/2']=float(curLine[11])
                temp['4p3/2']=float(curLine[12])
                temp['4d3/2']=float(curLine[13])
                temp['4d5/2']=float(curLine[14])
                temp['5s1/2']=float(curLine[15])
                photon_shell_cross[float(curLine[0])]=temp
            elif number<=54:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['3d3/2']=float(curLine[8])
                temp['3d5/2']=float(curLine[9])
                temp['4s1/2']=float(curLine[10])
                temp['4p1/2']=float(curLine[11])
                temp['4p3/2']=float(curLine[12])
                temp['4d3/2']=float(curLine[13])
                temp['4d5/2']=float(curLine[14])
                temp['5s1/2']=float(curLine[15])
                temp['5p1/2']=float(curLine[16])
                temp['5p3/2']=float(curLine[17])
                photon_shell_cross[float(curLine[0])]=temp
            elif number<=56:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['3d3/2']=float(curLine[8])
                temp['3d5/2']=float(curLine[9])
                temp['4s1/2']=float(curLine[10])
                temp['4p1/2']=float(curLine[11])
                temp['4p3/2']=float(curLine[12])
                temp['4d3/2']=float(curLine[13])
                temp['4d5/2']=float(curLine[14])
                temp['5s1/2']=float(curLine[15])
                temp['5p1/2']=float(curLine[16])
                temp['5p3/2']=float(curLine[17])
                temp['6s1/2']=float(curLine[18])
                photon_shell_cross[float(curLine[0])]=temp
            elif number==57:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['3d3/2']=float(curLine[8])
                temp['3d5/2']=float(curLine[9])
                temp['4s1/2']=float(curLine[10])
                temp['4p1/2']=float(curLine[11])
                temp['4p3/2']=float(curLine[12])
                temp['4d3/2']=float(curLine[13])
                temp['4d5/2']=float(curLine[14])
                temp['5s1/2']=float(curLine[15])
                temp['5p1/2']=float(curLine[16])
                temp['5p3/2']=float(curLine[17])
                temp['5d3/2']=float(curLine[18])
                temp['5d5/2']=float(curLine[19])
                temp['6s1/2']=float(curLine[20])
                photon_shell_cross[float(curLine[0])]=temp
            elif number<=70 and number!=64:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['3d3/2']=float(curLine[8])
                temp['3d5/2']=float(curLine[9])
                temp['4s1/2']=float(curLine[10])
                temp['4p1/2']=float(curLine[11])
                temp['4p3/2']=float(curLine[12])
                temp['4d3/2']=float(curLine[13])
                temp['4d5/2']=float(curLine[14])
                temp['4f5/2']=float(curLine[15])
                temp['4f7/2']=float(curLine[16])
                temp['5s1/2']=float(curLine[17])
                temp['5p1/2']=float(curLine[18])
                temp['5p3/2']=float(curLine[19])
                temp['6s1/2']=float(curLine[20])   
                photon_shell_cross[float(curLine[0])]=temp
            elif number==64 or (number<=80 and number!=77):
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['3d3/2']=float(curLine[8])
                temp['3d5/2']=float(curLine[9])
                temp['4s1/2']=float(curLine[10])
                temp['4p1/2']=float(curLine[11])
                temp['4p3/2']=float(curLine[12])
                temp['4d3/2']=float(curLine[13])
                temp['4d5/2']=float(curLine[14])
                temp['4f5/2']=float(curLine[15])
                temp['4f7/2']=float(curLine[16])
                temp['5s1/2']=float(curLine[17])
                temp['5p1/2']=float(curLine[18])
                temp['5p3/2']=float(curLine[19])
                temp['5d3/2']=float(curLine[20])
                temp['5d5/2']=float(curLine[21])
                temp['6s1/2']=float(curLine[22])
                photon_shell_cross[float(curLine[0])]=temp
            elif number==77:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['3d3/2']=float(curLine[8])
                temp['3d5/2']=float(curLine[9])
                temp['4s1/2']=float(curLine[10])
                temp['4p1/2']=float(curLine[11])
                temp['4p3/2']=float(curLine[12])
                temp['4d3/2']=float(curLine[13])
                temp['4d5/2']=float(curLine[14])
                temp['4f5/2']=float(curLine[15])
                temp['4f7/2']=float(curLine[16])
                temp['5s1/2']=float(curLine[17])
                temp['5p1/2']=float(curLine[18])
                temp['5p3/2']=float(curLine[19])
                temp['5d3/2']=float(curLine[20])
                temp['5d5/2']=float(curLine[21])
                photon_shell_cross[float(curLine[0])]=temp
            elif number<=86:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['3d3/2']=float(curLine[8])
                temp['3d5/2']=float(curLine[9])
                temp['4s1/2']=float(curLine[10])
                temp['4p1/2']=float(curLine[11])
                temp['4p3/2']=float(curLine[12])
                temp['4d3/2']=float(curLine[13])
                temp['4d5/2']=float(curLine[14])
                temp['4f5/2']=float(curLine[15])
                temp['4f7/2']=float(curLine[16])
                temp['5s1/2']=float(curLine[17])
                temp['5p1/2']=float(curLine[18])
                temp['5p3/2']=float(curLine[19])
                temp['5d3/2']=float(curLine[20])
                temp['5d5/2']=float(curLine[21])
                temp['6s1/2']=float(curLine[22])
                temp['6p1/2']=float(curLine[23])
                temp['6p3/2']=float(curLine[24])
                photon_shell_cross[float(curLine[0])]=temp
            elif number==87 or number==88:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['3d3/2']=float(curLine[8])
                temp['3d5/2']=float(curLine[9])
                temp['4s1/2']=float(curLine[10])
                temp['4p1/2']=float(curLine[11])
                temp['4p3/2']=float(curLine[12])
                temp['4d3/2']=float(curLine[13])
                temp['4d5/2']=float(curLine[14])
                temp['4f5/2']=float(curLine[15])
                temp['4f7/2']=float(curLine[16])
                temp['5s1/2']=float(curLine[17])
                temp['5p1/2']=float(curLine[18])
                temp['5p3/2']=float(curLine[19])
                temp['5d3/2']=float(curLine[20])
                temp['5d5/2']=float(curLine[21])
                temp['6s1/2']=float(curLine[22])
                temp['6p1/2']=float(curLine[23])
                temp['6p3/2']=float(curLine[24])
                temp['7s1/2']=float(curLine[25])
                photon_shell_cross[float(curLine[0])]=temp
            elif number==89 or number==90:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['3d3/2']=float(curLine[8])
                temp['3d5/2']=float(curLine[9])
                temp['4s1/2']=float(curLine[10])
                temp['4p1/2']=float(curLine[11])
                temp['4p3/2']=float(curLine[12])
                temp['4d3/2']=float(curLine[13])
                temp['4d5/2']=float(curLine[14])
                temp['4f5/2']=float(curLine[15])
                temp['4f7/2']=float(curLine[16])
                temp['5s1/2']=float(curLine[17])
                temp['5p1/2']=float(curLine[18])
                temp['5p3/2']=float(curLine[19])
                temp['5d3/2']=float(curLine[20])
                temp['5d5/2']=float(curLine[21])
                temp['6s1/2']=float(curLine[22])
                temp['6p1/2']=float(curLine[23])
                temp['6p3/2']=float(curLine[24])
                temp['6d3/2']=float(curLine[25]) 
                temp['6d5/2']=float(curLine[26])
                temp['7s1/2']=float(curLine[27]) 
                photon_shell_cross[float(curLine[0])]=temp
            elif number<=93:
                curLine=line.strip().split(",")
                temp=dict()
                temp['1s1/2']=float(curLine[1])
                temp['2s1/2']=float(curLine[2])
                temp['2p1/2']=float(curLine[3])
                temp['2p3/2']=float(curLine[4])
                temp['3s1/2']=float(curLine[5])
                temp['3p1/2']=float(curLine[6])
                temp['3p3/2']=float(curLine[7])
                temp['3d3/2']=float(curLine[8])
                temp['3d5/2']=float(curLine[9])
                temp['4s1/2']=float(curLine[10])
                temp['4p1/2']=float(curLine[11])
                temp['4p3/2']=float(curLine[12])
                temp['4d3/2']=float(curLine[13])
                temp['4d5/2']=float(curLine[14])
                temp['4f5/2']=float(curLine[15])
                temp['4f7/2']=float(curLine[16])
                temp['5s1/2']=float(curLine[17])
                temp['5p1/2']=float(curLine[18])
                temp['5p3/2']=float(curLine[19])
                temp['5d3/2']=float(curLine[20])
                temp['5d5/2']=float(curLine[21])
                temp['5f5/2']=float(curLine[22])
                temp['5f7/2']=float(curLine[23])  
                temp['6s1/2']=float(curLine[24])
                temp['6p1/2']=float(curLine[25])
                temp['6p3/2']=float(curLine[26])
                temp['6d3/2']=float(curLine[27]) 
                temp['6d5/2']=float(curLine[28])
                temp['7s1/2']=float(curLine[29])
                photon_shell_cross[float(curLine[0])]=temp

    '''To get the cross section for different photon, if the selected photon is one of the standard photon recorded in file,
     get the cross section from the table directly. If not, use linear interpolation to calculate cross section'''                                    
    if photon_energy in photon_shell_cross: 
        shell_cross=photon_shell_cross[photon_energy]
    elif photon_energy>1 and photon_energy<1.5: 
        start_cross=photon_shell_cross[1]
        end_cross=photon_shell_cross[1.5]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-1)/(1.5-1))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>1.5 and photon_energy<2:
        start_cross=photon_shell_cross[1.5]
        end_cross=photon_shell_cross[2]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-1.5)/(2-1.5))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>2 and photon_energy<3:
        start_cross=photon_shell_cross[2]
        end_cross=photon_shell_cross[3]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-2)/(3-2))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>3 and photon_energy<4:
        start_cross=photon_shell_cross[3]
        end_cross=photon_shell_cross[4]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-3)/(4-3))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>4 and photon_energy<5:
        start_cross=photon_shell_cross[4]
        end_cross=photon_shell_cross[5]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-4)/(5-4))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>5 and photon_energy<6:
        start_cross=photon_shell_cross[5]
        end_cross=photon_shell_cross[6]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-5)/(6-5))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>6 and photon_energy<8:
        start_cross=photon_shell_cross[6]
        end_cross=photon_shell_cross[8]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-6)/(8-6))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>8 and photon_energy<10:
        start_cross=photon_shell_cross[8]
        end_cross=photon_shell_cross[10]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-8)/(10-8))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>10 and photon_energy<15:
        start_cross=photon_shell_cross[10]
        end_cross=photon_shell_cross[15]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-10)/(15-10))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>15 and photon_energy<20:
        start_cross=photon_shell_cross[15]
        end_cross=photon_shell_cross[20]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-15)/(20-15))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>20 and photon_energy<30:
        start_cross=photon_shell_cross[20]
        end_cross=photon_shell_cross[30]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-20)/(30-20))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>30 and photon_energy<40:
        start_cross=photon_shell_cross[30]
        end_cross=photon_shell_cross[40]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-30)/(40-30))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>40 and photon_energy<50:
        start_cross=photon_shell_cross[40]
        end_cross=photon_shell_cross[50]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-40)/(50-40))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>50 and photon_energy<60:
        start_cross=photon_shell_cross[50]
        end_cross=photon_shell_cross[60]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-50)/(60-50))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>60 and photon_energy<80:
        start_cross=photon_shell_cross[60]
        end_cross=photon_shell_cross[80]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-60)/(80-60))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>80 and photon_energy<100:
        start_cross=photon_shell_cross[80]
        end_cross=photon_shell_cross[100]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-80)/(100-80))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>100 and photon_energy<150:
        start_cross=photon_shell_cross[100]
        end_cross=photon_shell_cross[150]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-100)/(150-100))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>150 and photon_energy<200:
        start_cross=photon_shell_cross[150]
        end_cross=photon_shell_cross[200]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-150)/(200-150))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>200 and photon_energy<300:
        start_cross=photon_shell_cross[200]
        end_cross=photon_shell_cross[300]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-200)/(300-200))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>300 and photon_energy<400:
        start_cross=photon_shell_cross[300]
        end_cross=photon_shell_cross[400]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-300)/(400-300))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>400 and photon_energy<500:
        start_cross=photon_shell_cross[400]
        end_cross=photon_shell_cross[500]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-400)/(500-400))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>500 and photon_energy<600:
        start_cross=photon_shell_cross[500]
        end_cross=photon_shell_cross[600]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-500)/(600-500))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>600 and photon_energy<800:
        start_cross=photon_shell_cross[600]
        end_cross=photon_shell_cross[800]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-600)/(800-600))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>800 and photon_energy<1000:
        start_cross=photon_shell_cross[800]
        end_cross=photon_shell_cross[1000]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-800)/(1000-800))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>1000 and photon_energy<1500:
        start_cross=photon_shell_cross[1000]
        end_cross=photon_shell_cross[1500]
        for shell in start_cross:
            shell_cross[shell]=((photon_energy-1000)/(1500-1000))*(end_cross[shell]-start_cross[shell])+start_cross[shell]
    elif photon_energy>1500:
        start_cross=photon_shell_cross[1000]
        end_cross=photon_shell_cross[1500]
        for shell in start_cross:
            shell_cross[shell]=((end_cross[shell]-start_cross[shell])/(1500-1000))*(photon_energy-1500)+end_cross[shell]
        
    norm_shell_cross=dict() #norm the cross section for each single element
    for shell in shell_cross:
        norm_shell_cross[shell]=(shell_cross[shell]/max(shell_cross.values()))*100
            
    return norm_shell_cross,shell_cross


'''-------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------
All about Auger Transition window'''

#Calculate Auger energies for specified element
def calculate_auger(number):    
    number_shell=get_shell() #read from database
    shell_electrons=number_shell[number] #shell configuration for specfied element
    number_energies=get_energies()
    currentEnergies=number_energies[number] #core energies for current element with atomic number Z
    nextEnergies=number_energies[number+1]  #core configuration for element with atomic number Z+1
    
    nonNoneEnergies=dict() #delete subshell without energies
    for energy in currentEnergies:
        if currentEnergies[energy]!=None:
            nonNoneEnergies[energy]=currentEnergies[energy]
    
    #get Auger transition and energies of current element
    transitionArray=[]
    for i in itertools.combinations_with_replacement(nonNoneEnergies.keys(), 3): #permutation and combination
        temp=','.join(i)
        transitionArray.append(temp)
    transitionArrayCopy=transitionArray.copy()
    for transition in transitionArrayCopy:
        #delete impossible combination 
        temp=shlex.shlex(transition,posix=True)
        temp.whitespace += ','
        temp.whitespace_split = True
        temp=list(temp)
        if temp[0]==temp[1]:
            transitionArray.remove(transition)
        elif number<=10:
            if temp[0]=='L1' or temp[0]=='L2' or temp[0]=='L3':
                transitionArray.remove(transition)
        elif number<=18:
            if temp[0]=='M1' or temp[0]=='M2' or temp[0]=='M3':
                transitionArray.remove(transition)
        elif number<=36:
            if temp[0]=='N1' or temp[0]=='N2' or temp[0]=='N3':
                transitionArray.remove(transition)
        elif number<=54:
            if number==45 and (temp[0]=='O1' or temp[1]=='O1' or temp[2]=='O1'):
                transitionArray.remove(transition)                
            if temp[0]=='O1' or temp[0]=='O2' or temp[0]=='O3':
                transitionArray.remove(transition)
        elif number<=86:
            if number==76 and (temp[0]=='P1' or temp[1]=='P1' or temp[2]=='P1'):
                transitionArray.remove(transition)
            if number==57 and (temp[0]=='O4' or temp[1]=='O4' or temp[2]=='O4' or temp[0]=='O5' or temp[1]=='O5' or temp[2]=='O5'):
                transitionArray.remove(transition)
            if number==64 and (temp[0]=='O4' or temp[1]=='O4' or temp[2]=='O4' or temp[0]=='O5' or temp[1]=='O5' or temp[2]=='O5'):
                transitionArray.remove(transition)
            if temp[0]=='P1' or temp[0]=='P2' or temp[0]=='P3':
                transitionArray.remove(transition)
        elif number==93 and (temp[0]=='P4' or temp[1]=='P4' or temp[2]=='P4' or temp[0]=='P5' or temp[1]=='P5' or temp[2]=='P5'):
            transitionArray.remove(transition)
    
    transition_energies=dict()
    for transition in transitionArray:
        temp=shlex.shlex(transition,posix=True)
        temp.whitespace += ','
        temp.whitespace_split = True
        temp=list(temp)
        vacancy=temp[0]
        inter1=temp[1]
        inter2=temp[2]
        
        #calculate Auger energies 
        energies=currentEnergies[vacancy]-0.5*(currentEnergies[inter1]+nextEnergies[inter1])-0.5*(currentEnergies[inter2]+nextEnergies[inter2])
        energies=Decimal(energies).quantize(Decimal('0.00'))
        if energies>0: #delete impossible transition whose energies is less than 0
           transition_energies[transition]=energies
    
    #get Auger Intensity
    multArray=[]
    for transition in transition_energies:
        temp=shlex.shlex(transition,posix=True)
        temp.whitespace += ','
        temp.whitespace_split = True
        temp=list(temp)
        
        #calculate multplicity
        mult=shell_electrons[temp[0]]*shell_electrons[temp[1]]*shell_electrons[temp[2]]      
        mult=Decimal(mult).quantize(Decimal('0.0000'))
        multArray.append(mult)
    maxMult=max(multArray)
    
    normArray=[]
    for mult in multArray:
        #calculate norm mult
        norm=(100*mult)/maxMult
        norm=Decimal(norm).quantize(Decimal('0.0'))
        normArray.append(norm)
        
    return transition_energies,normArray
        
#Click plot button on Auger Transition window                                 
def click_plot_for_elment_button(selectPlotV,selectPlotPhotonButton,inputPlotEntry,augerWindow,transition_energies,normArray,atomNumber,nonNoneValue):
    continuePlot=False
    
    #message box for error user inputs or selects
    if (selectPlotPhotonButton.get()=='No selection' and  inputPlotEntry.get()=='') or (selectPlotPhotonButton.get()!='No selection' and  inputPlotEntry.get()!=''):
        tkinter.messagebox.showinfo(title='ERROR',message='Please input or select',parent=augerWindow)
    elif selectPlotPhotonButton.get()=='No selection' and inputPlotEntry.get()!='':
        try:                  
            selectPhoton=float(inputPlotEntry.get())            
        except:
            tkinter.messagebox.showinfo(title='ERROR',message='Please input valid value',parent=augerWindow)
        else:
            continuePlot=True
    elif selectPlotPhotonButton.get()!='No selection' and inputPlotEntry.get()=='':
        continuePlot=True
        if selectPlotPhotonButton.get()=='Mg 1253.6(eV)':           
            selectPhoton=1253.6
        elif selectPlotPhotonButton.get()=='Al 1486.7(eV)':
            selectPhoton=1486.7
        elif selectPlotPhotonButton.get()=='Ag 2984.3(eV)':
            selectPhoton=2984.3
        elif selectPlotPhotonButton.get()=='Cr 5414.9(eV)':
            selectPhoton=5414.9
        elif selectPlotPhotonButton.get()=='Ga 9251.74(eV)':
            selectPhoton=9251.74
    
    #user selects all the options, program plots the figure
    if continuePlot==True:
        if selectPlotV.get()==1: #select plot binding energies
            if len(transition_energies)<=10:
                fontSize=10
            else:
                fontSize=7
            plotWindow=tkinter.Toplevel()
            plotWindow.geometry("680x680")
            plotWindow.title('Plot for each element')
            transitionXValue=[]
            transitionYHeight=[]
            positiveTransitions=[]
            
            index=0
            for transition in transition_energies:
                #calculate binding energies of Auger transitions
                if (selectPhoton-float(transition_energies[transition]))>=0:                
                    transitionXValue.append(Decimal(selectPhoton-float(transition_energies[transition])).quantize(Decimal('0.00')))
                    transitionYHeight.append(normArray[index])
                    positiveTransitions.append(transition)
                index+=1
            figure, ax = plt.subplots(1,1)
            transitionYMin=np.zeros(len(transitionXValue))
            plt.vlines(transitionXValue,transitionYMin,transitionYHeight) #plot Auger lines
            index=0
            for transition in positiveTransitions:
                transitionText=transition.replace(',','')
                plt.text(transitionXValue[index],transitionYHeight[index],transitionText,size=fontSize,rotation=90)
                index+=1
            
            norm_shell_cross,shell_cross=get_cross_section(atomNumber,selectPhoton)
            coreXValues=list(nonNoneValue.values())
            coreYHeight=list(norm_shell_cross.values())
            coreYMin=np.zeros(len(coreXValues))
            plt.vlines(coreXValues,coreYMin,coreYHeight,color='red') #plot core lines
            index=0
            for shell in norm_shell_cross:
                plt.text(coreXValues[index],coreYHeight[index],shell,rotation=90)
                index+=1
            plt.gca().invert_xaxis() 
            plt.xlabel('Binding Energy')
            plt.ylabel('Normalized Intensity')
            plt.close()      
            canvas =FigureCanvasTkAgg(figure, master=plotWindow)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES)        
            toolbar = NavigationToolbar2Tk(canvas, plotWindow)
            toolbar.update()
            canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH,expand=tkinter.YES)
            plotWindow.mainloop()
        elif selectPlotV.get()==2: #select plot kinetic energies
            if len(transition_energies)<=10:
                fontSize=10
            else:
                fontSize=7
            plotWindow=tkinter.Toplevel()
            plotWindow.geometry("680x680")
            plotWindow.title('Plot for each element')
            figure, ax = plt.subplots(1,1)
            transitionXValue=transition_energies.values()
            transitionYHeight=normArray
            transitionYMin=np.zeros(len(transitionXValue))
            plt.vlines(transitionXValue,transitionYMin,transitionYHeight)
            index=0
            for transition in transition_energies:
                newTransition=transition.replace(',','')
                plt.text(transition_energies[transition],normArray[index],newTransition,size=fontSize,rotation=90)
                index+=1
                
            norm_shell_cross,shell_cross=get_cross_section(atomNumber,selectPhoton)
            coreKineticEnergy=[]
            for shell in nonNoneValue:
                coreKineticEnergy.append(selectPhoton-nonNoneValue[shell]) #calculte kinetic energies of core state energies
                
            shell_list=list(norm_shell_cross.keys())
            norm_cross_list=list(norm_shell_cross.values())           
            coreXValues=[]
            coreYHeight=[]            
            coreText=[]
            
            index=0
            for value in coreKineticEnergy:
                if value>0:
                    coreXValues.append(value)
                    coreYHeight.append(norm_cross_list[index])
                    coreText.append(shell_list[index])
                index+=1
            
            coreYMin=np.zeros(len(coreXValues))
            plt.vlines(coreXValues,coreYMin,coreYHeight,color='red') #plot core lines
            index=0
            for text in coreText:
                plt.text(coreXValues[index],coreYHeight[index],text,rotation=90)
                index+=1
            plt.xlabel('Kinetic Energy')
            plt.ylabel('Normalized Intensity')
            plt.close()        
            canvas =FigureCanvasTkAgg(figure, master=plotWindow)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES)       
            toolbar = NavigationToolbar2Tk(canvas, plotWindow)
            toolbar.update()
            canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH,expand=tkinter.YES)
            plotWindow.mainloop()
        else:
            tkinter.messagebox.showinfo(title='ERROR',message='Please select BE or KE',parent=augerWindow)
            

#window of Auger transitions for corresponding element
def element_transition_window(index):
    global lastChoice # last computed photon energy
    lastChoice=''
    atomNumber=index+3
    augerWindow=tkinter.Toplevel()
    augerWindow.geometry("1200x680")
    number_name=get_atom()
    atomName=number_name[atomNumber]
    augerWindow.title('Auger Transitions for %s'%atomName)
    augerWindow.focus_force()
    
    #read from database
    number_energies=get_energies()
    barkla_orbital=get_notation()
    
    #nonNone energies for this atom
    currentEnergies=number_energies[atomNumber]
    nonNoneValue=dict()
    nonNoneOrbital=[]
    for shell in currentEnergies:
        if currentEnergies[shell]!=None:
            nonNoneValue[shell]=currentEnergies[shell]
            nonNoneOrbital.append(barkla_orbital[shell])
    length=len(nonNoneValue)
    
    #binding energies table
    coreTable = ttk.Treeview(augerWindow,height=length,columns=['1','2','3'],show='headings')
    coreTable.column('1', width=150) 
    coreTable.column('2', width=150) 
    coreTable.column('3', width=150) 
    coreTable.heading('1', text='Barkla Notation')
    coreTable.heading('2', text='Orbital Notation')
    coreTable.heading('3', text='Binding Energies')
    index=0
    for item in nonNoneValue:
        coreTable.insert('',index,values=(item,nonNoneOrbital[index],nonNoneValue[item]))
        index+=1
    coreTable.place(relx=10/1200,rely=60/680)
    
    #calculate energies and norm mult for transitions
    transition_energies,normArray=calculate_auger(atomNumber)
    
    #transition table
    if len(transition_energies)<=28:
        tableRow=len(transition_energies)
    else:
        tableRow=28
    
    transitionTable=ttk.Treeview(augerWindow,height=tableRow,columns=['1','2','3','4'],show='headings')
    transitionTable.column('1', width=150) 
    transitionTable.column('2', width=150) 
    transitionTable.column('3', width=150) 
    transitionTable.column('4', width=150) 
    transitionTable.heading('1', text='Auger Transition')
    transitionTable.heading('2', text='Auger Energies (KE)')
    transitionTable.heading('3', text='Auger Energies (BE)')
    transitionTable.heading('4', text='Norm Mult')
    
    position=0
    for t in transition_energies:
        transitionTable.insert('',position,iid=position+1,values=(t,transition_energies[t],'',normArray[position]))
        position+=1
    transitionTable.place(relx=550/1200,rely=70/680)
    ybar=Scrollbar(transitionTable,orient='vertical', command=transitionTable.yview,bg='Gray')
    transitionTable.configure(yscrollcommand=ybar.set)
    ybar.place(relx=0.95, rely=0.02, relwidth=0.035, relheight=0.958)
    
    #add convert function componetns
    selectConvertPhotonButton=ttk.Combobox(augerWindow)    
    selectConvertPhotonButton.place(relx=550/1200,rely=20/680)
    selectConvertPhotonButton['value']=('Mg 1253.6(eV)','Al 1486.7(eV)','Ag 2984.3(eV)','Cr 5414.9(eV)','Ga 9251.74(eV)','No selection')
    selectConvertPhotonButton.current(5)
    orConvertLabel=tkinter.Label(augerWindow,text='or')
    orConvertLabel.place(relx=750/1200,rely=20/680)
    inputConvertEntry=tkinter.Entry(augerWindow)
    inputConvertEntry.place(relx=800/1200,rely=20/680)    
    unitConvertLabel=tkinter.Label(augerWindow,text='(eV)')
    unitConvertLabel.place(relx=950/1200,rely=20/680)
    lastConvertLabel=tkinter.Label(augerWindow,text='Values in table calculated for: %s'%lastChoice)
    lastConvertLabel.place(relx=930/1200,rely=50/680)
    
    #Click convert button
    def _click_convert_button(selectConvertPhotonButton,transitionTable,position,inputConvertEntry,augerWindow,lastConvertLabel):
        def _update_table(transitionTable,inputValue,position):
            for index in range(position):
                index+=1
                ke_result=transitionTable.set(index,'#2')
                ke_result=float(ke_result)
                result=Decimal(inputValue-ke_result).quantize(Decimal('0.00'))
                if result<0:
                    transitionTable.set(index,'#3','Not Accessible')
                else:
                    transitionTable.set(index,'#3',result)
            
        global lastChoice
        lastConvertLabel['text']='Values in table calculated for: %s'%lastChoice
        inputValue=inputConvertEntry.get()  
        selectChoice=selectConvertPhotonButton.get()
        
        #Check user selection and input
        if (selectChoice=='No selection' and inputValue=='') or (selectChoice!='No selection' and inputValue!=''):
            tkinter.messagebox.showinfo(title='ERROR',message='Please input or select',parent=augerWindow)
        elif selectChoice=='No selection' and inputValue!='':
            try:           
                inputValue=float(inputValue)            
            except:
                tkinter.messagebox.showinfo(title='ERROR',message='Please input valid value',parent=augerWindow)
            else:
                _update_table(transitionTable,inputValue,position)
                lastChoice=inputValue
        elif selectChoice!='No selection' and inputValue=='':
            if selectChoice=='Mg 1253.6(eV)':           
                selectValue=1253.6
                lastChoice='Mg 1253.6(eV)'
            elif selectChoice=='Al 1486.7(eV)':
                selectValue=1486.7
                lastChoice='Al 1486.7(eV)'
            elif selectChoice=='Ag 2984.3(eV)':
                selectValue=2984.3
                lastChoice='Ag 2984.3(eV)'
            elif selectChoice=='Cr 5414.9(eV)':
                selectValue=5414.9
                lastChoice='Cr 5414.9(eV)'
            elif selectChoice=='Ga 9251.74(eV)':
                selectValue=9251.74   
                lastChoice='Ga 9251.74(eV)'
            _update_table(transitionTable,selectValue,position)
        
    convertButton=tkinter.Button(augerWindow,text='Convert',bg='Orange',command=lambda: _click_convert_button(selectConvertPhotonButton,transitionTable,position,inputConvertEntry,augerWindow,lastConvertLabel))
    convertButton.place(relx=1000/1200,rely=20/680)    
    
    #Click clear button
    def _click_clear_convert_button(inputConvertEntry,selectConvertPhotonButton,transitionTable,position):
        #Clear selection and entry
        inputConvertEntry.delete(0,'end')
        selectConvertPhotonButton.current(5)
        for index in range(position):
            index+=1
            transitionTable.set(index,'#3','') 
    clearButton=tkinter.Button(augerWindow,text='Clear',command=lambda: _click_clear_convert_button(inputConvertEntry,selectConvertPhotonButton,transitionTable,position))
    clearButton.place(relx=1065/1200,rely=20/680)
    
    #Click export button
    def _click_export_convert_button(augerWindow,transitionTable,position,atomName):
        reminderBox=tkinter.messagebox.askquestion('Confirmation','Do you want to continue?',parent=augerWindow)
        if reminderBox=='yes':
            selectValue='None'
            filePath=askdirectory(parent=augerWindow)
            if filePath!='':
                tableHeader = ['Auger Transition', 'Auger Energies (KE)', 'Auger Energies (BE)','Norm Mult']
                tableData=[]
                for p in range(position):
                    temp=[]
                    temp.append(transitionTable.set(p+1,'#1'))
                    temp.append(transitionTable.set(p+1,'#2'))
                    temp.append(transitionTable.set(p+1,'#3'))
                    temp.append(transitionTable.set(p+1,'#4'))
                    tableData.append(temp)
                for p in range(position):
                    try:
                        selectValue=float(transitionTable.set(p+1,'#2'))+float(transitionTable.set(p+1,'#3'))
                    except:
                        pass
                    else:                        
                        break
                if selectValue!='None':
                    selectValue=Decimal(selectValue).quantize(Decimal('0.00'))
                    selectValue=str(selectValue)
                    filePath=filePath+'/'+'auger_transition_'+atomName+'_'+selectValue+'.txt' 
                    with open(filePath,"w") as f:
                        f.write(tabulate(tableData, headers=tableHeader))
                else:
                    filePath=filePath+'/'+'auger_transition_'+atomName+'_'+selectValue+'.txt' 
                    with open(filePath,"w") as f:
                        f.write(tabulate(tableData, headers=tableHeader))
            else:
                pass
        else:
            pass
        
        
    exportConvertButton=tkinter.Button(augerWindow,text='Export',bg='LightBlue',command=lambda: _click_export_convert_button(augerWindow,transitionTable,position,atomName))
    exportConvertButton.place(relx=1140/1200,rely=20/680)
    
    #Plot function components
    selectPlotPhotonButton=ttk.Combobox(augerWindow,width=11)
    selectPlotPhotonButton['value']=('Mg 1253.6(eV)','Al 1486.7(eV)','Ag 2984.3(eV)','Cr 5414.9(eV)','Ga 9251.74(eV)','No selection')
    selectPlotPhotonButton.current(5)
    selectPlotPhotonButton.place(relx=20/1200,rely=20/680)
    orPlotLabel=tkinter.Label(augerWindow,text='or')
    orPlotLabel.place(relx=125/1200,rely=20/680)
    inputPlotEntry=tkinter.Entry(augerWindow,width=10)
    inputPlotEntry.place(relx=145/1200,rely=20/680)
    
    selectPlotV=tkinter.IntVar()
    selectBePlotButton=tkinter.Radiobutton(augerWindow,text='Binding Energies',value=1,variable=selectPlotV)
    selectBePlotButton.place(relx=230/1200,rely=5/680)
    selectKePlotButton=tkinter.Radiobutton(augerWindow,text='Kinetic Energies',value=2,variable=selectPlotV)
    selectKePlotButton.place(relx=230/1200,rely=30/680)
    
    plotButton=tkinter.Button(augerWindow,text='Plot',bg='Pink',command=lambda: click_plot_for_elment_button(selectPlotV,selectPlotPhotonButton,inputPlotEntry,augerWindow,transition_energies,normArray,atomNumber,nonNoneValue))
    plotButton.place(relx=380/1200,rely=15/680)
    
    def _click_clear_plot_button(selectPlotPhotonButton,inputPlotEntry,selectPlotV):
        selectPlotPhotonButton.current(5)
        inputPlotEntry.delete(0,'end')
        selectPlotV.set(0)
    clearPlotButton=tkinter.Button(augerWindow,text='Clear',command=lambda: _click_clear_plot_button(selectPlotPhotonButton,inputPlotEntry,selectPlotV))
    clearPlotButton.place(relx=430/1200,rely=15/680)
    
    augerWindow.mainloop()




'''-------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------
All about root window'''

#Click plot button on root window
def click_plot_data_button(importFilePath,root,showPlotPathText,selectPlotPhotonButton,plotXV):
    #Check user selection and input, pop up message box to catch error
    if selectPlotPhotonButton.get()=='':
        tkinter.messagebox.showinfo(title='ERROR',message='Please select photon energy',parent=root)
    elif len(uniqueArray2)==0:
        tkinter.messagebox.showinfo(title='ERROR',message='Please select element',parent=root)
    elif plotXV.get()==0:
        tkinter.messagebox.showinfo(title='ERROR',message='Please select range of x axis',parent=root)
    else:
        number_energies=get_energies()
        number_name=get_atom()
        selectPhoton=selectPlotPhotonButton.get()
        selectPhoton=float(selectPhoton.replace('keV',''))
        bindingData=[]
        intensityData=[]
        normalIntensityData=[]
        
        #user import file
        if importFilePath!='':           
            with open(importFilePath,'r') as f:            
                for line in f.readlines():
                    curLine=line.strip().split(" ")
                    bindingData.append(float(curLine[0]))
                    intensityData.append(float(curLine[1]))
            for intensity in intensityData:
                normalIntensityData.append((intensity/max(intensityData))*100)
        else:
            pass
        
        plotWindow=tkinter.Toplevel()
        plotWindow.geometry('680x680')
        plotWindow.title('Plot imported dataset')
        
        figure,ax=plt.subplots(1,1)
        
        maxCrossEachElement=[] #max cross section for each element
        for number in uniqueArray2:
            norm_shell_cross,shell_cross=get_cross_section(number,selectPhoton)
            maxCrossEachElement.append(max(shell_cross.values()))
        
        maxCrossAllElement=max(maxCrossEachElement) #max cross section for selected elements
        
        #define a set of colors to plot different elements
        plotColor=['red','green','yellow','purple','c',
                   'lightcoral','olivedrab','darkorange','mediumorchid','aquamarine',
                   'indianred','greenyellow','orange','thistle','turquoise',
                   'brown','chartreuse','antiquewhite','plum','lightseagreen',
                   'firebrick','lawngreen','tan','violet','mediumturquoise',
                   'maroon','b','navajowhite','darkmagenta','lightcyan',
                   'darkred','indigo','blanchedalmond','m','paleturquoise',
                   'r','lavender','moccasin','fuchsia','darkslategray',
                   'salmon','honeydew','burlywood','orchid','teal',
                   'tomato','darkseagreen','wheat','mediumvioletred','cyan',
                   'coral','palegreen','darkgoldenrod','deeppink','cadetblue',
                   'orangered','lightgreen','goldenrod','hotpink','powderblue',
                   'lightsalmon','forestgreen','gold','palevioletred','lightblue',
                   'sienna','limegreen','khaki','crimson','deepskyblue',
                   'chocolate','darkgreen','darkkhaki','pink','skyblue',
                   'sandybrown','g','olive','lightpink','steelblue',
                   'peru','lime','y','darkviolet','aliceblue',
                   'black','seagreen','springgreen','mediumspringgreen','royalblue',
                   'grey']
        colorIndex=0
        
        #plot reference lines for each element
        for number in uniqueArray2:
            norm_shell_cross,shell_cross=get_cross_section(number,selectPhoton)
            currentEnergies=number_energies[number]
            nonNoneValue=dict()
            for shell in currentEnergies:
                if currentEnergies[shell]!=None:
                    nonNoneValue[shell]=currentEnergies[shell]
            norm_cross_section=dict()
            for shell in shell_cross:
                norm_cross_section[shell]=(shell_cross[shell]/maxCrossAllElement)*100
            coreXValues=list(nonNoneValue.values())
            coreYHeight=list(norm_cross_section.values())
            coreYMin=np.zeros(len(coreXValues))
            plt.vlines(coreXValues,coreYMin,coreYHeight,color=plotColor[colorIndex]) #plot core lines
            index=0
            for shell in norm_shell_cross:
                plt.text(coreXValues[index],coreYHeight[index],number_name[number]+''+shell,rotation=90) #add core label
                index+=1
            transition_energies,normArray=calculate_auger(number)
            
            augerValues=[]
            normMults=[]
            shellText=[]
            index=0
            for shell in transition_energies:
                augerValues.append(selectPhoton-float(transition_energies[shell]))
                normMults.append(normArray[index])
                shell=shell.replace(',','')
                shellText.append(shell)
                index+=1
                
            transitionXValues=[]
            transitionYHeight=[]
            transitiontext=[]
            index=0
            for value in augerValues:
                if value>0:
                    transitionXValues.append(value)
                    transitionYHeight.append(normMults[index])
                    transitiontext.append(shellText[index])
                index+=1
            transitionYMin=np.zeros(len(transitionYHeight))
            plt.vlines(transitionXValues,transitionYMin,transitionYHeight,color=plotColor[colorIndex]) #plot transition lines
            
            index=0
            for t in transitiontext:
                plt.text(transitionXValues[index],transitionYHeight[index],number_name[number]+t,rotation=90) #add transition label
                index+=1
            colorIndex+=1
        
        if importFilePath!='':
            plt.plot(bindingData,normalIntensityData) #plot dataset if user imports file
        else:
            pass
        
        plt.gca().invert_xaxis() 
        if importFilePath!='':
            if plotXV.get()==2:
                plt.xlim([max(bindingData),0])
        
                       
        plt.xlabel('Binding Energy')
        plt.ylabel('Normalized Intensity')
        plt.close()        
        canvas =FigureCanvasTkAgg(figure, master=plotWindow)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES)
        
        toolbar = NavigationToolbar2Tk(canvas, plotWindow)
        toolbar.update()
        canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH,expand=tkinter.YES)
        plotWindow.mainloop()
  

#click descending or ascending button on search window          
def click_sort_search_button(table,position,descending,auger_range,core_state):   
    global sortOrder #descending, ascending or sort by number
    position_energies=dict() 
    
    if auger_range==True and core_state==False: #search Auger transition
        for p in range(position):
            p+=1
            position_energies[p]=float(table.set(p,'#3'))          
    elif auger_range==False or (auger_range==True and core_state==True): #search core energies or both
        for p in range(position):
            p+=1
            position_energies[p]=float(table.set(p,'#4'))

    #sort the table by energies    
    if descending==True: 
        sortOrder='descending'
        sort_position=sorted(position_energies.items(),key=lambda x:x[1],reverse=True)
    else:
        sortOrder='ascending'
        sort_position=sorted(position_energies.items(),key=lambda x:x[1],reverse=False)
    
    
    new_table=[]
    if auger_range==True and core_state==False: #search Auger        
        for i in sort_position:
            p=i[0]
            temp=[]
            temp.append(table.set(p,'#1'))
            temp.append(table.set(p,'#2'))
            temp.append(table.set(p,'#3'))
            temp.append(table.set(p,'#4'))
            new_table.append(temp)
        
        for p in range(position):
            p+=1              
            table.set(p,'#1',new_table[p-1][0])
            table.set(p,'#2',new_table[p-1][1])
            table.set(p,'#3',new_table[p-1][2])
            table.set(p,'#4',new_table[p-1][3])
    elif auger_range==False: #search core state
        for i in sort_position:
            p=i[0]
            temp=[]
            temp.append(table.set(p,'#1'))
            temp.append(table.set(p,'#2'))
            temp.append(table.set(p,'#3'))
            temp.append(table.set(p,'#4'))
            new_table.append(temp)
            
        for p in range(position):
            p+=1              
            table.set(p,'#1',new_table[p-1][0])
            table.set(p,'#2',new_table[p-1][1])
            table.set(p,'#3',new_table[p-1][2])
            table.set(p,'#4',new_table[p-1][3])
            
    elif (auger_range==True and core_state==True): #search both
        for i in sort_position:
            p=i[0]
            temp=[]
            temp.append(table.set(p,'#1'))
            temp.append(table.set(p,'#2'))
            temp.append(table.set(p,'#3'))
            temp.append(table.set(p,'#4'))
            temp.append(table.set(p,'#5'))
            new_table.append(temp)
            
        for p in range(position):
            p+=1              
            table.set(p,'#1',new_table[p-1][0])
            table.set(p,'#2',new_table[p-1][1])
            table.set(p,'#3',new_table[p-1][2])
            table.set(p,'#4',new_table[p-1][3])
            table.set(p,'#5',new_table[p-1][4])
    
#click sort by number button on search window
def click_sort_number_search_button(correct_energies,table,position,orbitalNotationList,normColumnList,auger_range,core_state):
    global sortOrder
    barkla_orbital=get_notation()
    sortOrder='by_number'
    new_table=[]

    if auger_range==True and core_state==False: #search Auger
        index=0
        for atom_name in correct_energies: 
            current_transitions=correct_energies[atom_name]
            for transition in current_transitions:
                temp=[]
                temp.append(atom_name)
                temp.append(transition)
                temp.append(current_transitions[transition])
                temp.append(normColumnList[index])
                new_table.append(temp)
                index+=1
                
        for p in range(position):
            p+=1
            table.set(p,'#1',new_table[p-1][0])
            table.set(p,'#2',new_table[p-1][1])
            table.set(p,'#3',new_table[p-1][2])
            table.set(p,'#4',new_table[p-1][3])
            
            
    elif auger_range==False:  #search core state
        for atom_name in correct_energies:
            current_energies=correct_energies[atom_name]
            for shell in current_energies:
                temp=[]
                temp.append(atom_name)
                temp.append(shell)
                temp.append(barkla_orbital[shell])
                temp.append(current_energies[shell])
                new_table.append(temp)
        

        for p in range(position):
            p+=1               
            table.set(p,'#1',new_table[p-1][0])
            table.set(p,'#2',new_table[p-1][1])
            table.set(p,'#3',new_table[p-1][2])
            table.set(p,'#4',new_table[p-1][3])
            
    elif auger_range==True and core_state==True:  #search both
        index=0
        for atom_name in correct_energies: 
            current_transitions=correct_energies[atom_name]
            for transition in current_transitions:
                temp=[]
                temp.append(atom_name)
                temp.append(transition)
                temp.append(orbitalNotationList[index])
                temp.append(current_transitions[transition]) 
                temp.append(normColumnList[index])
                new_table.append(temp)
                index+=1
                
        for p in range(position):
            p+=1
            table.set(p,'#1',new_table[p-1][0])
            table.set(p,'#2',new_table[p-1][1])
            table.set(p,'#3',new_table[p-1][2])
            table.set(p,'#4',new_table[p-1][3])
            table.set(p,'#5',new_table[p-1][4])

#click export button on search window
def click_export_search_data_button(rangeWindow,table,position,selectTranCoreV,selectAtomV,selectEnergyV,rangeMin,rangeMax,selectPhoton):
    number_name=get_atom()
    reminderBox=tkinter.messagebox.askquestion('Confirmation','Do you want to continue?',parent=rangeWindow)
    rangeMin=str(rangeMin)
    rangeMax=str(rangeMax)
    if reminderBox=='yes':
        filePath=askdirectory(parent=rangeWindow)
        if filePath!='':
            if selectTranCoreV.get()==1: #search Auger
                tableHeader=['Atom','Auger Transition','Auger Energy','Norm Mult'] #define the table header
                tableData=[]
                for p in range(position):
                    temp=[]
                    temp.append(table.set(p+1,'#1'))
                    temp.append(table.set(p+1,'#2'))
                    temp.append(table.set(p+1,'#3'))
                    temp.append(table.set(p+1,'#4'))
                    tableData.append(temp)
                if selectAtomV.get()==1: #select all elements
                    if selectEnergyV.get()==1:
                        filePath=filePath+'/'+'Auger_transitions_'+'from_'+rangeMin+'_to_'+rangeMax+'_KE_'+sortOrder+'.txt'
                    elif selectEnergyV.get()==2:
                        selectPhoton=str(selectPhoton)
                        filePath=filePath+'/'+'Auger_transitions_'+'from_'+rangeMin+'_to_'+rangeMax+'_BE_'+selectPhoton+'_'+sortOrder+'.txt'
                    with open(filePath,'w') as f: #write data to file
                        f.write(tabulate(tableData,headers=tableHeader))
                elif selectAtomV.get()==2: #select some elements
                    nameStr=''
                    for number in uniqueArray:
                        nameStr=nameStr+number_name[number]
                    if selectEnergyV.get()==1:
                        filePath=filePath+'/'+'Auger_transitions_'+'from_'+rangeMin+'_to_'+rangeMax+'_KE_'+sortOrder+'_'+nameStr+'.txt'
                    elif selectEnergyV.get()==2:
                        selectPhoton=str(selectPhoton)
                        filePath=filePath+'/'+'Auger_transitions_'+'from_'+rangeMin+'_to_'+rangeMax+'_BE_'+selectPhoton+'_'+sortOrder+'_'+nameStr+'.txt'
                    with open(filePath,'w') as f:
                        f.write(tabulate(tableData,headers=tableHeader))
            elif selectTranCoreV.get()==2: #search core state
                tableHeader=['Atom','Barkla Notation','Orbital Notation','Binding Energies']
                tableData=[]
                for p in range(position):
                    temp=[]
                    temp.append(table.set(p+1,'#1'))
                    temp.append(table.set(p+1,'#2'))
                    temp.append(table.set(p+1,'#3'))
                    temp.append(table.set(p+1,'#4'))
                    tableData.append(temp)
                if selectAtomV.get()==1: #select all elements
                    if selectEnergyV.get()==1:
                        selectPhoton=str(selectPhoton)
                        filePath=filePath+'/'+'Core_State_Energies_'+'from_'+rangeMin+'_to_'+rangeMax+'_KE_'+selectPhoton+'_'+sortOrder+'.txt'
                    elif selectEnergyV.get()==2:
                        filePath=filePath+'/'+'Core_State_Energies_'+'from_'+rangeMin+'_to_'+rangeMax+'_BE_'+sortOrder+'.txt'
                    with open(filePath,'w') as f:
                        f.write(tabulate(tableData,headers=tableHeader))
                elif selectAtomV.get()==2: #select some elements
                    nameStr=''
                    for number in uniqueArray:
                        nameStr=nameStr+number_name[number]
                    if selectEnergyV.get()==1:
                        selectPhoton=str(selectPhoton)
                        filePath=filePath+'/'+'Core_State_Energies_'+'from_'+rangeMin+'_to_'+rangeMax+'_KE_'+selectPhoton+'_'+sortOrder+'_'+nameStr+'.txt'
                    elif selectEnergyV.get()==2:
                        filePath=filePath+'/'+'Core_State_Energies_'+'from_'+rangeMin+'_to_'+rangeMax+'_BE_'+sortOrder+'_'+nameStr+'.txt'
                    with open(filePath,'w') as f:
                        f.write(tabulate(tableData,headers=tableHeader))
            elif selectTranCoreV.get()==3: #search both
                tableHeader=['Atom','Auger Transition/Notation(Barkla)','Auger Transition/Notation(Orbital)','Auger Energies/Core State Energies','Norm Mult']
                tableData=[]
                for p in range(position):
                    temp=[]
                    temp.append(table.set(p+1,'#1'))
                    temp.append(table.set(p+1,'#2'))
                    temp.append(table.set(p+1,'#3'))
                    temp.append(table.set(p+1,'#4'))
                    temp.append(table.set(p+1,'#5'))
                    tableData.append(temp)
                if selectAtomV.get()==1:
                    if selectEnergyV.get()==1:
                        selectPhoton=str(selectPhoton)
                        filePath=filePath+'/'+'Search_Both_'+'from_'+rangeMin+'_to_'+rangeMax+'_KE_'+selectPhoton+'_'+sortOrder+'.txt'
                    elif selectEnergyV.get()==2:
                        selectPhoton=str(selectPhoton)
                        filePath=filePath+'/'+'Search_Both_'+'from_'+rangeMin+'_to_'+rangeMax+'_BE_'+selectPhoton+'_'+sortOrder+'.txt'
                    with open(filePath,'w') as f:
                        f.write(tabulate(tableData,headers=tableHeader))
                elif selectAtomV.get()==2:
                    nameStr=''
                    for number in uniqueArray:
                        nameStr=nameStr+number_name[number]
                    if selectEnergyV.get()==1:
                        selectPhoton=str(selectPhoton)
                        filePath=filePath+'/'+'Search_Both_'+'from_'+rangeMin+'_to_'+rangeMax+'_KE_'+selectPhoton+'_'+sortOrder+'_'+nameStr+'.txt'
                    elif selectEnergyV.get()==2:
                        selectPhoton=str(selectPhoton)
                        filePath=filePath+'/'+'Search_Both_'+'from_'+rangeMin+'_to_'+rangeMax+'_BE_'+selectPhoton+'_'+sortOrder+'_'+nameStr+'.txt'
                    with open(filePath,'w') as f:
                        f.write(tabulate(tableData,headers=tableHeader))
        else:
            pass
        
    else:
        pass



#click search button on root window            
def click_search_button(root, searchFromEntry,searchToEntry,selectTranCoreV,selectAtomV,selectEnergyV,selectSearchPhotonButton,searchInputEntry):
    fromValue=searchFromEntry.get()
    toValue=searchToEntry.get()
    continueSearch=False
    selectPhoton=0
    
    #check user selection and input
    if fromValue=='' or toValue=='':
        tkinter.messagebox.showinfo(title='ERROR',message='Please input values',parent=root)
    else:
        try:
            fromValue=float(fromValue)
            toValue=float(toValue)
        except:
            tkinter.messagebox.showinfo(title='ERROR',message='Please input valid values',parent=root)
        else:
            if selectTranCoreV.get()==0:
                tkinter.messagebox.showinfo(title='ERROR',message='Please select Auger Transitions or core state energies',parent=root)
            elif selectAtomV.get()==0:
                tkinter.messagebox.showinfo(title='ERROR',message='Please select from all elements or from some elements',parent=root)
            elif selectAtomV.get()==2 and len(uniqueArray)==0:
                tkinter.messagebox.showinfo(title='ERROR',message='Please select elements',parent=root)
            elif selectEnergyV.get()==0:
                tkinter.messagebox.showinfo(title='ERROR',message='Please select by KE or BE',parent=root)
            elif (selectTranCoreV.get()==1 and selectEnergyV.get()==2) or (selectTranCoreV.get()==2 and selectEnergyV.get()==1) or selectTranCoreV.get()==3:
                if (selectSearchPhotonButton.get()=='No selection' and searchInputEntry.get()=='') or (selectSearchPhotonButton.get()!='No selection' and searchInputEntry.get()!=''):
                    tkinter.messagebox.showinfo(title='ERROR',message='Please input or select photon energy',parent=root)
                elif searchInputEntry.get()!='':
                    try:
                        selectPhoton=float(searchInputEntry.get())
                    except:
                        tkinter.messagebox.showinfo(title='ERROR',message='Please input valid values',parent=root)
                    else:
                        continueSearch=True
                elif selectSearchPhotonButton.get()!='No selection':
                    continueSearch=True
                    if selectSearchPhotonButton.get()=='Mg 1253.6(eV)':                              
                        selectPhoton=1253.6   
                    elif selectSearchPhotonButton.get()=='Al 1486.7(eV)':
                        selectPhoton=1486.7  
                    elif selectSearchPhotonButton.get()=='Ag 2984.3(eV)':
                        selectPhoton=2984.3  
                    elif selectSearchPhotonButton.get()=='Cr 5414.9(eV)':
                        selectPhoton=5414.9 
                    elif selectSearchPhotonButton.get()=='Ga 9251.74(eV)':
                        selectPhoton=9251.74 
            else:
                continueSearch=True
    
    #user selects and inpus correct options, execute search algorithm
    if continueSearch==True:
        rangeWindow=tkinter.Tk()
        rangeWindow.geometry("1200x680")
        rangeWindow.title('Search range')
        
        number_range=get_range()
        number_name=get_atom()
        number_energies=get_energies()
        barkla_orbital=get_notation()
        orbitalNotationList=[]
        normColumnList=[]
        
        rangeMin=min(float(searchFromEntry.get()),float(searchToEntry.get()))
        rangeMax=max(float(searchFromEntry.get()),float(searchToEntry.get()))
        correctAtom=[]
        if selectTranCoreV.get()==1:    #Search Auger
            if selectAtomV.get()==1:    #from all elements
                if selectEnergyV.get()==1:    #search ke
                    for number in number_range:                       
                        temp=number_range[number]
                        if temp['Max']<rangeMin or temp['Min']>rangeMax:                           
                            pass
                        else:
                            correctAtom.append(number)    #all elements whose range is in the specfied range   
                    correctAtomTransitions=dict()  
                    transitionsNumber=0
                    normArrayList=[]
                    for number in correctAtom: #check all transitions for correct atom
                        temp=dict()
                        atom_name=number_name[number]
                        current_transitions_energies,normArray=calculate_auger(number)
                        index=0
                        for transition in current_transitions_energies:
                            if current_transitions_energies[transition]>=rangeMin and current_transitions_energies[transition]<=rangeMax:
                                transitionsNumber+=1
                                temp[transition]=current_transitions_energies[transition]
                                correctAtomTransitions[atom_name]=temp #add correct transitions
                                normArrayList.append(normArray[index])
                            index+=1

                elif selectEnergyV.get()==2:  #search be
                    for number in number_range:
                        temp=number_range[number]
                        tempMin=selectPhoton-temp['Max']
                        tempMax=selectPhoton-temp['Min']
                        if tempMax<rangeMin or tempMin>rangeMax:
                            pass
                        else:
                            correctAtom.append(number)
                    correctAtomTransitions=dict()  
                    transitionsNumber=0
                    normArrayList=[]
                    for number in correctAtom:
                        temp=dict()
                        atom_name=number_name[number]
                        current_transitions_energies,normArray=calculate_auger(number)
                        index=0
                        for transition in current_transitions_energies:
                            if (selectPhoton-float(current_transitions_energies[transition]))>=rangeMin and (selectPhoton-float(current_transitions_energies[transition]))<=rangeMax:
                                transitionsNumber+=1
                                temp[transition]=Decimal(selectPhoton-float(current_transitions_energies[transition])).quantize(Decimal('0.00'))
                                correctAtomTransitions[atom_name]=temp
                                normArrayList.append(normArray[index])
                            index+=1
            elif selectAtomV.get()==2:  #from some elements
                correctAtom=uniqueArray
                if selectEnergyV.get()==1:
                    correctAtomTransitions=dict()  
                    transitionsNumber=0
                    normArrayList=[]
                    for number in correctAtom:
                        temp=dict()
                        atom_name=number_name[number]
                        current_transitions_energies,normArray=calculate_auger(number)
                        index=0
                        for transition in current_transitions_energies:
                            if current_transitions_energies[transition]>=rangeMin and current_transitions_energies[transition]<=rangeMax:
                                transitionsNumber+=1
                                temp[transition]=current_transitions_energies[transition]
                                correctAtomTransitions[atom_name]=temp
                                normArrayList.append(normArray[index])
                            index+=1
                elif selectEnergyV.get()==2:
                    correctAtomTransitions=dict()  
                    transitionsNumber=0
                    normArrayList=[]
                    for number in correctAtom:
                        temp=dict()
                        atom_name=number_name[number]
                        current_transitions_energies,normArray=calculate_auger(number)
                        index=0
                        for transition in current_transitions_energies:
                            if (selectPhoton-float(current_transitions_energies[transition]))>=rangeMin and (selectPhoton-float(current_transitions_energies[transition]))<=rangeMax:
                                transitionsNumber+=1
                                temp[transition]=Decimal(selectPhoton-float(current_transitions_energies[transition])).quantize(Decimal('0.00'))
                                correctAtomTransitions[atom_name]=temp
                                normArrayList.append(normArray[index])
                            index+=1

            if transitionsNumber>0:
                if transitionsNumber<=32:
                    tableRow=transitionsNumber
                else:
                    tableRow=32
                #table displays all transitions with the energies in the range
                transitionTable=ttk.Treeview(rangeWindow,height=tableRow,columns=['1','2','3','4'],show='headings')
                transitionTable.column('1',width=100) 
                transitionTable.column('2',width=200) 
                transitionTable.column('3',width=200) 
                transitionTable.column('4',width=150) 
                transitionTable.heading('1', text='Atom')
                transitionTable.heading('2', text='Auger Transition')
                transitionTable.heading('3', text='Auger Energies')
                transitionTable.heading('4', text='Norm Mult')
                transitionTable.pack() 
                    
                position=0
                for name in correctAtomTransitions:
                    current_transitions=correctAtomTransitions[name]
                    for t in current_transitions:                        
                        transitionTable.insert('',position,iid=position+1,values=(name,t,current_transitions[t],normArrayList[position]))
                        position+=1
                ybar=Scrollbar(transitionTable,orient='vertical', command=transitionTable.yview,bg='Gray')
                transitionTable.configure(yscrollcommand=ybar.set)
                ybar.place(relx=0.95, rely=0.02, relwidth=0.035, relheight=0.958)
                
                #add sort and export button
                descendingButton=tkinter.Button(rangeWindow,text='Descending order (energies)',bg='LightPink',command=lambda: click_sort_search_button(transitionTable,position,descending=True,auger_range=True,core_state=False))
                descendingButton.place(relx=950/1200,rely=50/680)
                ascendingButton=tkinter.Button(rangeWindow,text='Ascending order (energies)',bg='LightBlue',command=lambda: click_sort_search_button(transitionTable,position,descending=False,auger_range=True,core_state=False))
                ascendingButton.place(relx=950/1200,rely=100/680)
                numberButton=tkinter.Button(rangeWindow,text='Sort by atomic number',bg='LightGreen',command=lambda: click_sort_number_search_button(correctAtomTransitions,transitionTable,position,orbitalNotationList,normArrayList,auger_range=True,core_state=False))
                numberButton.place(relx=950/1200,rely=150/680)
                exportButton=tkinter.Button(rangeWindow,text='Export',bg='Yellow',command=lambda: click_export_search_data_button(rangeWindow,transitionTable,position,selectTranCoreV,selectAtomV,selectEnergyV,rangeMin,rangeMax,selectPhoton))
                exportButton.place(relx=950/1200,rely=300/680)

            else:
                tkinter.messagebox.showinfo(title='REMINDER',message='No relevant results',parent=rangeWindow)
        
        elif selectTranCoreV.get()==2:    #search core state
            correctCore={}
            correctCoreNumber=0
            if selectAtomV.get()==1:    #from all elements
                if selectEnergyV.get()==1:    #search ke
                    for number in number_energies:
                        temp=number_energies[number]
                        temp2=dict()
                        for key,value in temp.items():
                            if value!=None: 
                                if (selectPhoton-value)<=rangeMax and (selectPhoton-value)>=rangeMin:
                                    temp2[key]=Decimal(selectPhoton-value).quantize(Decimal('0.00'))
                                    correctCoreNumber+=1
                            else:
                                pass
                        if temp2!={} and number!=94:
                            atom_name=number_name[number]
                            correctCore[atom_name]=temp2
                elif selectEnergyV.get()==2:   #search be
                    for number in number_energies:
                        temp=number_energies[number]
                        temp2=dict()
                        for key,value in temp.items():
                            if value!=None: 
                                if value<=rangeMax and value>=rangeMin:
                                    temp2[key]=value
                                    correctCoreNumber+=1 
                            else:
                                pass
                        if temp2!={} and number!=94:
                            atom_name=number_name[number]
                            correctCore[atom_name]=temp2
            elif selectAtomV.get()==2:    #from some elements
                if selectEnergyV.get()==1:
                    for number in uniqueArray:
                        temp=number_energies[number]
                        temp2=dict()
                        for key,value in temp.items():
                            if value!=None: 
                                if (selectPhoton-value)<=rangeMax and (selectPhoton-value)>=rangeMin:
                                    temp2[key]=Decimal(selectPhoton-value).quantize(Decimal('0.00'))
                                    correctCoreNumber+=1
                            else:
                                pass
                        if temp2!={} and number!=94:
                            atom_name=number_name[number]
                            correctCore[atom_name]=temp2
                elif selectEnergyV.get()==2:
                    for number in uniqueArray:
                        temp=number_energies[number]
                        temp2=dict()
                        for key,value in temp.items():
                            if value!=None: 
                                if value<=rangeMax and value>=rangeMin:
                                    temp2[key]=value
                                    correctCoreNumber+=1 
                            else:
                                pass
                        if temp2!={} and number!=94:
                            atom_name=number_name[number]
                            correctCore[atom_name]=temp2
            if len(correctCore)!=0:
                if correctCoreNumber<=32:
                    tableRow=correctCoreNumber
                else:
                    tableRow=32
                coreTable=ttk.Treeview(rangeWindow,height=tableRow,columns=['1','2','3','4'],show='headings')
                coreTable.column('1',width=100) 
                coreTable.column('2',width=150) 
                coreTable.column('3',width=150) 
                coreTable.column('4',width=160) 
                coreTable.heading('1', text='Atom')
                coreTable.heading('2', text='Barkla Notation')
                coreTable.heading('3', text='Orbital Notation')
                coreTable.heading('4', text='Binding Energies')
                coreTable.pack()
                position=0 
                for name in correctCore:
                    temp=correctCore[name]
                    for shell in temp:
                        coreTable.insert('',position,iid=position+1,values=(name,shell,barkla_orbital[shell],temp[shell]))
                        position+=1
                ybar=Scrollbar(coreTable,orient='vertical', command=coreTable.yview,bg='Gray')
                coreTable.configure(yscrollcommand=ybar.set)
                ybar.place(relx=0.95, rely=0.02, relwidth=0.035, relheight=0.958)
                
                descendingButton=tkinter.Button(rangeWindow,text='Descending order (energies)',bg='LightPink',command=lambda: click_sort_search_button(coreTable,position,descending=True,auger_range=False,core_state=True))
                descendingButton.place(relx=900/1200,rely=50/680)
                ascendingButton=tkinter.Button(rangeWindow,text='Ascending order (energies)',bg='LightBlue',command=lambda: click_sort_search_button(coreTable,position,descending=False,auger_range=False,core_state=True))
                ascendingButton.place(relx=900/1200,rely=100/680)
                numberButton=tkinter.Button(rangeWindow,text='Sort by atomic number',bg='LightGreen',command=lambda: click_sort_number_search_button(correctCore,coreTable,position,orbitalNotationList,normColumnList,auger_range=False,core_state=True))
                numberButton.place(relx=900/1200,rely=150/680)
                exportButton=tkinter.Button(rangeWindow,text='Export',bg='Yellow',command=lambda: click_export_search_data_button(rangeWindow,coreTable,position,selectTranCoreV,selectAtomV,selectEnergyV,rangeMin,rangeMax,selectPhoton))
                exportButton.place(relx=900/1200,rely=300/680)

            else:
                tkinter.messagebox.showinfo(title='REMINDER',message='No relevant results',parent=rangeWindow)
                
        elif selectTranCoreV.get()==3:     #search both
            correctCore=dict()
            correctCoreNumber=0
            if selectAtomV.get()==1:    #from all elements         
                if selectEnergyV.get()==1:    #search ke     
                    for number in number_energies:
                        temp=number_energies[number]
                        temp2=dict()
                        for key,value in temp.items():
                            if value!=None: 
                                if (selectPhoton-value)<=rangeMax and (selectPhoton-value)>=rangeMin:
                                    temp2[key]=Decimal(selectPhoton-value).quantize(Decimal('0.00'))
                                    correctCoreNumber+=1
                            else:
                                pass
                        if temp2!={} and number!=94:
                            atom_name=number_name[number]
                            correctCore[atom_name]=temp2
                    
                    for number in number_range:                       
                        temp=number_range[number]
                        if temp['Max']<rangeMin or temp['Min']>rangeMax:                           
                            pass
                        else:
                            correctAtom.append(number)
                            
                    correctAtomTransitions=dict()  
                    transitionsNumber=0
                    normArrayList=[]
                    for number in correctAtom:
                        temp=dict()
                        atom_name=number_name[number]
                        current_transitions_energies,normArray=calculate_auger(number)
                        index=0
                        for transition in current_transitions_energies:
                            if current_transitions_energies[transition]>=rangeMin and current_transitions_energies[transition]<=rangeMax:
                                transitionsNumber+=1
                                temp[transition]=current_transitions_energies[transition]
                                correctAtomTransitions[atom_name]=temp
                                normArrayList.append(normArray[index])
                            index+=1                    
                elif selectEnergyV.get()==2:
                    for number in number_energies:
                        temp=number_energies[number]
                        temp2=dict()
                        for key,value in temp.items():
                            if value!=None: 
                                if value<=rangeMax and value>=rangeMin:
                                    temp2[key]=value
                                    correctCoreNumber+=1 
                            else:
                                pass
                        if temp2!={} and number!=94:
                            atom_name=number_name[number]
                            correctCore[atom_name]=temp2
                                       
                    for number in number_range:
                        temp=number_range[number]
                        tempMin=selectPhoton-temp['Max']
                        tempMax=selectPhoton-temp['Min']
                        if tempMax<rangeMin or tempMin>rangeMax:
                            pass
                        else:
                            correctAtom.append(number)
                    correctAtomTransitions=dict()  
                    transitionsNumber=0
                    normArrayList=[]
                    for number in correctAtom:
                        temp=dict()
                        atom_name=number_name[number]
                        current_transitions_energies,normArray=calculate_auger(number)
                        index=0
                        for transition in current_transitions_energies:
                            if (selectPhoton-float(current_transitions_energies[transition]))>=rangeMin and (selectPhoton-float(current_transitions_energies[transition]))<=rangeMax:
                                transitionsNumber+=1
                                temp[transition]=Decimal(selectPhoton-float(current_transitions_energies[transition])).quantize(Decimal('0.00'))
                                correctAtomTransitions[atom_name]=temp
                                normArrayList.append(normArray[index])                                
                            index+=1
                                                      
            elif selectAtomV.get()==2:    #search some elements                
                if selectEnergyV.get()==1:    #search ke 
                    for number in uniqueArray:
                        temp=number_energies[number]
                        temp2=dict()
                        for key,value in temp.items():
                            if value!=None: 
                                if (selectPhoton-value)<=rangeMax and (selectPhoton-value)>=rangeMin:
                                    temp2[key]=Decimal(selectPhoton-value).quantize(Decimal('0.00'))
                                    correctCoreNumber+=1
                            else:
                                pass
                        if temp2!={} and number!=94:
                            atom_name=number_name[number]
                            correctCore[atom_name]=temp2
                    correctAtom=uniqueArray
                    correctAtomTransitions=dict()  
                    transitionsNumber=0
                    normArrayList=[]
                    for number in correctAtom:
                        temp=dict()
                        atom_name=number_name[number]
                        current_transitions_energies,normArray=calculate_auger(number)
                        index=0
                        for transition in current_transitions_energies:
                            if current_transitions_energies[transition]>=rangeMin and current_transitions_energies[transition]<=rangeMax:
                                transitionsNumber+=1
                                temp[transition]=current_transitions_energies[transition]
                                correctAtomTransitions[atom_name]=temp
                                normArrayList.append(normArray[index])
                            index+=1
                elif selectEnergyV.get()==2:
                    for number in uniqueArray:
                        temp=number_energies[number]
                        temp2=dict()
                        for key,value in temp.items():
                            if value!=None: 
                                if value<=rangeMax and value>=rangeMin:
                                    temp2[key]=value
                                    correctCoreNumber+=1 
                            else:
                                pass
                        if temp2!={} and number!=94:
                            atom_name=number_name[number]
                            correctCore[atom_name]=temp2
                    correctAtom=uniqueArray
                    correctAtomTransitions=dict()  
                    transitionsNumber=0
                    normArrayList=[]
                    for number in correctAtom:
                        temp=dict()
                        atom_name=number_name[number]
                        current_transitions_energies,normArray=calculate_auger(number)
                        index=0
                        for transition in current_transitions_energies:
                            if (selectPhoton-float(current_transitions_energies[transition]))>=rangeMin and (selectPhoton-float(current_transitions_energies[transition]))<=rangeMax:
                                transitionsNumber+=1
                                temp[transition]=Decimal(selectPhoton-float(current_transitions_energies[transition])).quantize(Decimal('0.00'))
                                correctAtomTransitions[atom_name]=temp
                                normArrayList.append(normArray[index])
                            index+=1
            tableLength=transitionsNumber+correctCoreNumber
                 
            
            if tableLength>0:
                if tableLength<=32:
                    tableRow=tableLength
                else:
                    tableRow=32
                table=ttk.Treeview(rangeWindow,height=tableRow,columns=['1','2','3','4','5'],show='headings')
                table.column('1',width=50) 
                table.column('2',width=180) 
                table.column('3',width=180)
                table.column('4',width=250) 
                table.column('5',width=120) 
                table.heading('1', text='Atom')
                table.heading('2', text='Auger Transition / Notation')
                table.heading('3', text='Auger Transition / Notation')
                table.heading('4', text='Auger Energies / Core State Energies')
                table.heading('5', text='Norm Mult')
                table.pack()
                two_tables=dict() #combine the core energies and Auger together
                for number in number_name:
                    name=number_name[number]
                    if name in correctCore.keys() and name in correctAtomTransitions.keys():
                        temp1=correctCore[name]
                        temp2=correctAtomTransitions[name]
                        temp3=dict()
                        for key1 in temp1:
                            temp3[key1]=temp1[key1]
                        for key2 in temp2:
                            temp3[key2]=temp2[key2]
                        two_tables[name]=temp3
                    elif name in correctCore.keys():
                        two_tables[name]=correctCore[name]
                    elif name in correctAtomTransitions.keys():
                        two_tables[name]=correctAtomTransitions[name]
                position=0
                orbitalNotation=''
                orbitalNotationList=[]
                normColumn=''
                normColumnList=[]
                index=0
                for name in two_tables:
                    current_transitions=two_tables[name]
                    for t in current_transitions:
                        if len(t)==2 or len(t)==1:
                            orbitalNotation=barkla_orbital[t]
                            orbitalNotationList.append(orbitalNotation)
                            normColumn=''
                            normColumnList.append(normColumn)
                        elif len(t)==8 or len(t)==7:
                            splitTransition=t.split(',')
                            orbitalTransition=barkla_orbital[splitTransition[0]].replace(' ','')+' '+barkla_orbital[splitTransition[1]].replace(' ','')+' '+barkla_orbital[splitTransition[2]].replace(' ','')
                            orbitalNotation=orbitalTransition
                            orbitalNotationList.append(orbitalNotation)
                            normColumn=normArrayList[index]    
                            normColumnList.append(normColumn)
                            index+=1


                        table.insert('',position,iid=position+1,values=(name,t,orbitalNotation,current_transitions[t],normColumn))
                        position+=1

                ybar=Scrollbar(table,orient='vertical', command=table.yview,bg='Gray')
                table.configure(yscrollcommand=ybar.set)
                ybar.place(relx=0.95, rely=0.02, relwidth=0.025, relheight=0.958)
                descendingButton=tkinter.Button(rangeWindow,text='Descending order (energies)',bg='LightPink',command=lambda: click_sort_search_button(table,position,descending=True,auger_range=True,core_state=True))
                descendingButton.place(relx=1000/1200,rely=50/680)
                ascendingButton=tkinter.Button(rangeWindow,text='Ascending order (energies)',bg='LightBlue',command=lambda: click_sort_search_button(table,position,descending=False,auger_range=True,core_state=True))
                ascendingButton.place(relx=1000/1200,rely=100/680)
                numberButton=tkinter.Button(rangeWindow,text='Sort by atomic number',bg='LightGreen',command=lambda: click_sort_number_search_button(two_tables,table,position,orbitalNotationList,normColumnList,auger_range=True,core_state=True))
                numberButton.place(relx=1000/1200,rely=150/680)
    
                exportButton=tkinter.Button(rangeWindow,text='Export',bg='Yellow',command=lambda: click_export_search_data_button(rangeWindow,table,position,selectTranCoreV,selectAtomV,selectEnergyV,rangeMin,rangeMax,selectPhoton))
                exportButton.place(relx=1000/1200,rely=300/680)
                
            else:
                tkinter.messagebox.showinfo(title='REMINDER',message='No relevant results',parent=rangeWindow)

        rangeWindow.mainloop()

#root window
def root_window():
    root=tkinter.Tk() 
    root.geometry("1000x680")
    root.title('SpeedyAuger')
    
    #define buttons for corresponding elements 3-93
    tkinter.Button(root,text='1 H',width=5,height=2,bg='Gray').place(relx=30/1000,rely=10/680) #1
    tkinter.Button(root,text='2 He',width=5,height=2,bg='Gray').place(relx=880/1000,rely=10/680) #18
    uncover_atom=dict()
    uncover_atom[94],uncover_atom[95],uncover_atom[96],uncover_atom[97],uncover_atom[98],uncover_atom[99],uncover_atom[100],uncover_atom[101],uncover_atom[102]='Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No'
    uncover_atom[103],uncover_atom[104],uncover_atom[105],uncover_atom[106],uncover_atom[107]='Lr','Rf','Db','Sg','Bh'
    uncover_atom[108],uncover_atom[109],uncover_atom[110],uncover_atom[111],uncover_atom[112]='Hs','Mt','Ds','Rg','Cn'
    uncover_atom[113],uncover_atom[114],uncover_atom[115],uncover_atom[116],uncover_atom[117],uncover_atom[118]='Nh','Fl','Mc','Lv','Ts','Og'
    for i in range(25):
        if i<=8:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+94,'name':uncover_atom[i+94]},width=5,height=2,bg='Gray').place(relx=(380+i*50)/1000, rely=490/680)
        else:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+94,'name':uncover_atom[i+94]},width=5,height=2,bg='Gray').place(relx=(130+(i-9)*50)/1000, rely=370/680)  
    number_name=get_atom()    
    for i in range(91):
        atom_name=number_name[i+3]
        if i==0 or i==1:     
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='Salmon').place(relx=(30+i*50)/1000, rely=70/680)
        elif i<=7:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='Yellow').place(relx=(630+(i-2)*50)/1000, rely=70/680)
        elif i==8 or i==9:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='Salmon').place(relx=(30+(i-8)*50)/1000, rely=130/680)
        elif i<=15:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='Yellow').place(relx=(630+(i-10)*50)/1000, rely=130/680)
        elif i==16 or i==17:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='Salmon').place(relx=(30+(i-16)*50)/1000, rely=190/680)
        elif i<=27:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='PowderBlue').place(relx=(30+(i-16)*50)/1000, rely=190/680)
        elif i<=33:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='Yellow').place(relx=(30+(i-16)*50)/1000, rely=190/680)
        elif i==34 or i==35:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='Salmon').place(relx=(30+(i-34)*50)/1000, rely=250/680)
        elif i<=45:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='PowderBlue').place(relx=(30+(i-34)*50)/1000, rely=250/680)
        elif i<=51:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='Yellow').place(relx=(30+(i-34)*50)/1000, rely=250/680)
        elif i==52 or i==53:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='Salmon').place(relx=(30+(i-52)*50)/1000, rely=310/680)
        elif i>=54 and i<=67:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='LightGreen').place(relx=(30+(i-52)*50)/1000, rely=430/680)
        elif i<=77:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='PowderBlue').place(relx=(130+(i-68)*50)/1000, rely=310/680)
        elif i<=83:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='Yellow').place(relx=(130+(i-68)*50)/1000, rely=310/680)
        elif i==84 or i==85:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='Salmon').place(relx=(30+(i-84)*50)/1000, rely=370/680)
        else:
            tkinter.Button(root,text='%(number)d %(name)s'%{'number':i+3,'name':atom_name},command = lambda text=i: element_transition_window(text),width=5,height=2,bg='LightGreen').place(relx=(30+(i-84)*50)/1000, rely=490/680)
    
    #components of search function
    searchFromLabel=tkinter.Label(root,text='from')
    searchFromLabel.place(relx=200/1000,rely=10/680)
    searchFromEntry=tkinter.Entry(root,width=13)
    searchFromEntry.place(relx=240/1000,rely=10/680)
    searchToLabel=tkinter.Label(root,text='(eV)  to')
    searchToLabel.place(relx=340/1000,rely=10/680)
    searchToEntry=tkinter.Entry(root,width=13)
    searchToEntry.place(relx=400/1000,rely=10/680)
    searchUnitLabel=tkinter.Label(root,text='(eV)')
    searchUnitLabel.place(relx=500/1000,rely=10/680)
    
    selectSearchPhotonButton=ttk.Combobox(root,width=11)
    selectSearchPhotonButton['value']=('Mg 1253.6(eV)','Al 1486.7(eV)','Ag 2984.3(eV)','Cr 5414.9(eV)','Ga 9251.74(eV)','No selection')
    selectSearchPhotonButton.current(5)
    searchOrLabel=tkinter.Label(root,text='or')
    searchInputEntry=tkinter.Entry(root,width=10)
    
    selectTranCoreV=tkinter.IntVar()
    selectEnergyV=tkinter.IntVar()

    
    '''user needs to select or input photon energy with 3 conditions:
    1. Select Auger and search by binding energies
    2. Select core state and search by kinetic energies
    3. select search both'''
    def _click_tran_core_radiobutton(selectTranCoreV,selectEnergyV,selectSearchPhotonButton,searchOrLabel,searchInputEntry):
        if selectTranCoreV.get()==3:
            selectSearchPhotonButton.place(relx=490/1000,rely=48.5/680)
            searchOrLabel.place(relx=600/1000,rely=48/680)
            searchInputEntry.place(relx=620/1000,rely=48.5/680)
        elif selectTranCoreV.get()==1 and selectEnergyV.get()==2:
            selectSearchPhotonButton.place(relx=490/1000,rely=48.5/680)
            searchOrLabel.place(relx=600/1000,rely=48/680)
            searchInputEntry.place(relx=620/1000,rely=48.5/680)
        elif selectTranCoreV.get()==2 and selectEnergyV.get()==1:
            selectSearchPhotonButton.place(relx=490/1000,rely=48.5/680)
            searchOrLabel.place(relx=600/1000,rely=48/680)
            searchInputEntry.place(relx=620/1000,rely=48.5/680)
        else:
            selectSearchPhotonButton.place_forget()
            searchOrLabel.place_forget()
            searchInputEntry.place_forget()
    
    
    transitionRadiobutton=tkinter.Radiobutton(root,text='Auger Transitions',value=1,variable=selectTranCoreV,command=lambda: _click_tran_core_radiobutton(selectTranCoreV,selectEnergyV,selectSearchPhotonButton,searchOrLabel,searchInputEntry))
    transitionRadiobutton.place(relx=150/1000,rely=30.5/680)
    coreRadiobutton=tkinter.Radiobutton(root,text='Core State Energies',value=2,variable=selectTranCoreV,command=lambda: _click_tran_core_radiobutton(selectTranCoreV,selectEnergyV,selectSearchPhotonButton,searchOrLabel,searchInputEntry))
    coreRadiobutton.place(relx=150/1000,rely=52/680)
    bothRadiobutton=tkinter.Radiobutton(root,text='Both',value=3,variable=selectTranCoreV,command=lambda: _click_tran_core_radiobutton(selectTranCoreV,selectEnergyV,selectSearchPhotonButton,searchOrLabel,searchInputEntry))
    bothRadiobutton.place(relx=150/1000,rely=73.5/680)
    
    sep1 = ttk.Separator(root, orient='vertical')
    sep1.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.0005)
    
    #select elements for search function
    def _click_elements_checkbutton(element,elementArray):
        elementArray.append(element)
        elementArray=sorted(elementArray)
        uniqueElement=np.unique(elementArray)
        resdata = []
        for ii in uniqueElement:
            resdata.append(elementArray.count(ii))                
        newArray=[]
        index=0
        for d in resdata:
            if d%2==0:
                pass
            else:
                newArray.append(uniqueElement[index])
            index+=1
        global uniqueArray
        uniqueArray=newArray
        
    #select elements for plot function    
    def _click_elements_checkbutton2(element,elementArray2):
        elementArray2.append(element)
        elementArray2=sorted(elementArray2)
        uniqueElement=np.unique(elementArray2)
        resdata = []
        for ii in uniqueElement:
            resdata.append(elementArray2.count(ii))                
        newArray=[]
        index=0
        for d in resdata:
            if d%2==0:
                pass
            else:
                newArray.append(uniqueElement[index])
            index+=1
        global uniqueArray2
        uniqueArray2=newArray
    
    #click search elements
    def _click_select_elements(root,searchFunction,plotFunction): 
        #click clear button for search function    
        def _click_clear_elements_button(elementArray,elementBox):
            for number in elementBox:
                elementBox[number].deselect()
    
            for element in uniqueArray:
                _click_elements_checkbutton(element,elementArray)
                
        #click clear button for plot function         
        def _click_clear_elements_button2(elementArray2,elementBox):
            for number in elementBox:
                elementBox[number].deselect()
    
            for element in uniqueArray2:
                _click_elements_checkbutton2(element,elementArray2)
            
        selectAtomWindow=tkinter.Tk()
        selectAtomWindow.geometry("1200x300")
        selectAtomWindow.title('Select Elements')
        selectAtomWindow.resizable(0,0)
        number_name=get_atom()
        global elementArray
        global uniqueArray
        global elementArray2
        global uniqueArray2
        elementBox={}
        H_Label=tkinter.Label(selectAtomWindow,text='1 H')
        H_Label.place(x=20,y=10)
        He_Label=tkinter.Label(selectAtomWindow,text='2 He')
        He_Label.place(x=1125,y=10)
        
        #organize the check button 
        for number in number_name:
            v=tkinter.IntVar()
            atomName=number_name[number]      
            if searchFunction==True:               
                elementBox[number]=tkinter.Checkbutton(selectAtomWindow,text='%(number)d %(name)s'%{'number':number,'name':atomName},variable=v,command=lambda element=number: _click_elements_checkbutton(element,elementArray))  
            elif plotFunction==True:
                elementBox[number]=tkinter.Checkbutton(selectAtomWindow,text='%(number)d %(name)s'%{'number':number,'name':atomName},variable=v,command=lambda element=number: _click_elements_checkbutton2(element,elementArray2))  
            if searchFunction==True:                
                if number in uniqueArray:
                    elementBox[number].select()     
            elif plotFunction==True:
                if number in uniqueArray2:
                    elementBox[number].select() 
            if number==3 or number==4:
                elementBox[number].config(fg='red')
                elementBox[number].place(x=20+(number-3)*65,y=35)
            elif number>4 and number<=10:
                elementBox[number].config(fg='Gold')
                elementBox[number].place(x=800+(number-5)*65,y=35)
            elif number==11 or number==12:
                elementBox[number].config(fg='red')
                elementBox[number].place(x=20+(number-11)*65,y=60)
            elif number>12 and number<=18:
                elementBox[number].config(fg='Gold')
                elementBox[number].place(x=800+(number-13)*65,y=60)
            elif number==19 or number==20:
                elementBox[number].config(fg='red')
                elementBox[number].place(x=20+(number-19)*65,y=85)
            elif number>20 and number<=30:
                elementBox[number].config(fg='blue')
                elementBox[number].place(x=150+(number-21)*65,y=85)
            elif number>=31 and number<=36:
                elementBox[number].config(fg='Gold')
                elementBox[number].place(x=800+(number-31)*65,y=85)
            elif number==37 or number==38:
                elementBox[number].config(fg='red')
                elementBox[number].place(x=20+(number-37)*65,y=110)
            elif number>=39 and number<=48:
                elementBox[number].config(fg='blue')
                elementBox[number].place(x=150+(number-39)*65,y=110)
            elif number>=49 and number<=54:
                elementBox[number].config(fg='Gold')
                elementBox[number].place(x=800+(number-49)*65,y=110)
            elif number==55 or number==56:
                elementBox[number].config(fg='red')
                elementBox[number].place(x=20+(number-55)*65,y=135)
            elif number>=71 and number<=80:
                elementBox[number].config(fg='blue')
                elementBox[number].place(x=150+(number-71)*65,y=135)
            elif number>=81 and number<=86:
                elementBox[number].config(fg='Gold')
                elementBox[number].place(x=800+(number-81)*65,y=135)
            elif number==87 or number==88:
                elementBox[number].config(fg='red')
                elementBox[number].place(x=20+(number-87)*65,y=160)
            elif number>=57 and number<=70:
                elementBox[number].config(fg='green')
                elementBox[number].place(x=150+(number-57)*65,y=190)
            else:
                elementBox[number].config(fg='green')
                elementBox[number].place(x=150+(number-89)*65,y=215)
        
        for i in range(25):
            if i<=8:
                tkinter.Label(selectAtomWindow,text='%(number)d %(name)s'%{'number':i+94,'name':uncover_atom[i+94]}).place(x=480+i*65,y=215)
            else:
                tkinter.Label(selectAtomWindow,text='%(number)d %(name)s'%{'number':i+94,'name':uncover_atom[i+94]}).place(x=150+(i-9)*65,y=160)
        if searchFunction==True:            
            clearButton=tkinter.Button(selectAtomWindow,text='Clear',command=lambda:_click_clear_elements_button(elementArray,elementBox))
        elif plotFunction==True:
            clearButton=tkinter.Button(selectAtomWindow,text='Clear',command=lambda:_click_clear_elements_button2(elementArray2,elementBox))
        clearButton.place(x=1100,y=250)


    selectAtomV=tkinter.IntVar()
    selectSearchAtomButton=tkinter.Button(root,text='Select Elements',command=lambda: _click_select_elements(root,searchFunction=True,plotFunction=False))
    def _select_elements_radionbutton(selectAtomV,selectSearchAtomButton):
        if selectAtomV.get()==1:
            selectSearchAtomButton.place_forget()
        elif selectAtomV.get()==2:
            selectSearchAtomButton.place(relx=350/1000,rely=72/680)
        
    allAtomRadiobutton=tkinter.Radiobutton(root, text='From All Elements',value=1,variable=selectAtomV,command=lambda: _select_elements_radionbutton(selectAtomV,selectSearchAtomButton))
    allAtomRadiobutton.place(relx=320/1000,rely=30.5/680)
    someAtomRadiobutton=tkinter.Radiobutton(root,text='From Selected Elements',value=2,variable=selectAtomV,command=lambda: _select_elements_radionbutton(selectAtomV,selectSearchAtomButton))
    someAtomRadiobutton.place(relx=320/1000,rely=52/680)
        
    def _select_ke_be_radionbutton(selectTranCoreV,selectEnergyV,selectSearchPhotonButton,searchOrLabel,searchInputEntry):
        if selectTranCoreV.get()==3:
            selectSearchPhotonButton.place(relx=490/1000,rely=48.5/680)
            searchOrLabel.place(relx=600/1000,rely=48/680)
            searchInputEntry.place(relx=620/1000,rely=48.5/680)
        elif selectTranCoreV.get()==1 and selectEnergyV.get()==2:
            selectSearchPhotonButton.place(relx=490/1000,rely=48.5/680)
            searchOrLabel.place(relx=600/1000,rely=48/680)
            searchInputEntry.place(relx=620/1000,rely=48.5/680)
        elif selectTranCoreV.get()==2 and selectEnergyV.get()==1:
            selectSearchPhotonButton.place(relx=490/1000,rely=48.5/680)
            searchOrLabel.place(relx=600/1000,rely=48/680)
            searchInputEntry.place(relx=620/1000,rely=48.5/680)
        else:
            selectSearchPhotonButton.place_forget()
            searchOrLabel.place_forget()
            searchInputEntry.place_forget()
    
  
    keRadiobutton=tkinter.Radiobutton(root,text='by kinetic energies',value=1,variable=selectEnergyV,command=lambda: _select_ke_be_radionbutton(selectTranCoreV,selectEnergyV,selectSearchPhotonButton,searchOrLabel,searchInputEntry))
    keRadiobutton.place(relx=530/1000,rely=1/680)
    beRadiobutton=tkinter.Radiobutton(root,text='by binding energies',value=2,variable=selectEnergyV,command=lambda: _select_ke_be_radionbutton(selectTranCoreV,selectEnergyV,selectSearchPhotonButton,searchOrLabel,searchInputEntry))
    beRadiobutton.place(relx=530/1000,rely=21.5/680)
    
    searchButton=tkinter.Button(root,text='Search',bg='Orange',command=lambda: click_search_button(root, searchFromEntry,searchToEntry,selectTranCoreV,selectAtomV,selectEnergyV,selectSearchPhotonButton,searchInputEntry))
    searchButton.place(relx=685/1000,rely=10/680)
    
    #click clear button for search function
    def _click_clear_search_button(searchFromEntry,searchToEntry,selectTranCoreV,selectAtomV,selectEnergyV,selectSearchPhotonButton,searchInputEntry,selectAtomButton,searchOrLabel):
        selectAtomButton.place_forget()
        searchFromEntry.delete(0,'end')
        searchToEntry.delete(0,'end')
        selectTranCoreV.set(0)
        selectAtomV.set(0)
        selectEnergyV.set(0)
        searchOrLabel.place_forget()
        selectSearchPhotonButton.place_forget()
        searchInputEntry.place_forget()
        global uniqueArray
        for element in uniqueArray:
            _click_elements_checkbutton(element,elementArray)
        uniqueArray=[]
  
    clearSearchButton=tkinter.Button(root,text='Clear',command=lambda: _click_clear_search_button(searchFromEntry,searchToEntry,selectTranCoreV,selectAtomV,selectEnergyV,selectSearchPhotonButton,searchInputEntry,selectSearchAtomButton,searchOrLabel))
    clearSearchButton.place(relx=750/1000,rely=10/680)
    
    #citation label
    citationLabel1=tkinter.Label(root,text='The listed core level binding energy values are taken from the following reference and were used to compute all possible Auger transition energies:')
    citationLabel1.place(relx=70/1000,rely=540/680)
    citationLabel2=tkinter.Label(root,text='[1] S.T.Perkins, D.E.Cullen, et al.,')
    citationLabel2.place(relx=70/1000,rely=560/680)   
    citationLabel3=tkinter.Label(root,text='Tables and Graphs of Atomic Subshell and Relaxation Data Derived from the LLNL Evaluated Atomic Data Library (EADL),', fg='blue',font=('Times',10,'italic'))
    citationLabel3.place(relx=260/1000,rely=560/680)
    citationLabel4=tkinter.Label(root,text='Z = 1--100', fg='blue',font=('Times',10,'italic'))
    citationLabel4.place(relx=70/1000,rely=580/680)
    citationLabel5=tkinter.Label(root,text='Lawrence Livermore National Laboratory, UCRL-50400, Vol. 30,')
    citationLabel5.place(relx=135/1000,rely=580/680)
    def _open_EADL_url(event):
       webbrowser.open("https://www.osti.gov/biblio/10121422-tables-graphs-atomic-subshell-relaxation-data-derived-from-llnl-evaluated-atomic-data-library-eadl", new=0)    
    citationLabel3.bind("<Button-1>", _open_EADL_url)
    citationLabel4.bind("<Button-1>", _open_EADL_url)
    
    citationLabel6=tkinter.Label(root,text='The digitised version [2] of the Scofield tabulated data [3] was implemented to scale the intensity of the core lines in the plotting function:')
    citationLabel6.place(relx=70/1000,rely=600/680)
    citationLabel7=tkinter.Label(root,text='[2] C. Kalha, N. K. Fernando, A. Regoutz,')
    citationLabel7.place(relx=70/1000,rely=620/680)
    citationLabel8=tkinter.Label(root,text='Digitisation of Scofield Photoionisation Cross Section Tabulated Data, 2020, figshare, Dataset',fg='blue',font=('Times',10,'italic'))
    citationLabel8.place(relx=306/1000,rely=620/680)
    citationLabel9=tkinter.Label(root,text='[3] J.H. Scofield,')
    citationLabel9.place(relx=70/1000,rely=640/680)
    citationLabel10=tkinter.Label(root,text='Theoretical photoionization cross sections from 1 to 1500 keV,',fg='blue',font=('Times',10,'italic'))
    citationLabel10.place(relx=165/1000,rely=640/680)
    citationLabel11=tkinter.Label(root,text='Technical Report UCRL-51326, Lawrence Livermore Laboratory, 1973')
    citationLabel11.place(relx=509/1000,rely=640/680)
    citationLabel12=tkinter.Label(root,text='See README documentation for further information.')
    citationLabel12.place(relx=70/1000,rely=660/680)
    def _open_figshare_url(event):
        webbrowser.open("https://doi.org/10.6084/m9.figshare.12967079.v1", new=0) 
    citationLabel8.bind("<Button-1>", _open_figshare_url)
    def _open_scorfield_url(event):
        webbrowser.open("https://doi.org/10.2172/4545040", new=0)
    citationLabel10.bind("<Button-1>", _open_scorfield_url)

    #click import file button for plot function
    def _click_import_file_button(root,showPlotPathText):
        global importFilePath
        importFilePath=askopenfilename(parent=root)
        if importFilePath!='':            
            splitPath=importFilePath.split('/')
            splitFile=splitPath[-1].split('.')
            if splitFile[-1]!='txt' and splitFile[-1]!='csv':
                tkinter.messagebox.showinfo(title='REMINDER',message='Please import txt or csv',parent=root)
                showPlotPathText.config(state='normal')
                showPlotPathText.delete(0,'end')
                showPlotPathText.config(state='readonly')            
            else: 
                try:
                    bindingData=[]
                    intensityData=[]
                    with open(importFilePath,'r') as f:
                        for line in f.readlines():
                            curLine=line.strip().split(" ")
                            bindingData.append(float(curLine[0]))
                            intensityData.append(float(curLine[1]))
                except:
                    tkinter.messagebox.showinfo(title='REMINDER',message='Please import valid data format',parent=root)
                else:                
                    showPlotPathText.config(state='normal')
                    showPlotPathText.insert(0,importFilePath)
                    showPlotPathText.config(state='readonly')
        else:
            pass
        
    #components of plot function    
    showPlotPathText=tkinter.Entry(root,state='readonly')
    showPlotPathText.place(relx=140/1000,rely=160/680)   
    importFileButton=tkinter.Button(root,text='Import File (.txt or .csv)',bg='Pink',command=lambda: _click_import_file_button(root,showPlotPathText))
    importFileButton.place(relx=140/1000,rely=120/680)
    
    selectPlotPhotonButton=ttk.Combobox(root,width=12)
    selectPlotPhotonButton.set('Select Photon')
    selectPlotPhotonButton['value']=['1keV','1.5keV','2keV','3keV','4keV','5keV','6keV','8keV','10keV','15keV']
    selectPlotPhotonButton.place(relx=292/1000,rely=125/680)
    selectPlotElementButton=tkinter.Button(root,text='Select Elements',command=lambda: _click_select_elements(root,searchFunction=False,plotFunction=True))
    selectPlotElementButton.place(relx=295/1000,rely=155/680)
    rangePlotLabel=tkinter.Label(root,text='Please select range of x axis:')
    rangePlotLabel.place(relx=380/1000,rely=102/680)
    
    def _click_plot_clear_button(showPlotPathText,selectPlotPhotonButton,plotXV):
        showPlotPathText.config(state='normal')
        showPlotPathText.delete(0, 'end')
        showPlotPathText.config(state='readonly')
        selectPlotPhotonButton.set('Select Photon')
        global importFilePath
        importFilePath=''
        global uniqueArray2
        for element in uniqueArray2:
            _click_elements_checkbutton2(element,elementArray2)
        uniqueArray2=[]
        plotXV.set(0)
        
    plotXV=tkinter.IntVar()
    selectPlotReferenceButton=tkinter.Radiobutton(root,text='Range of Reference Lines',variable=plotXV,value=1)
    selectPlotReferenceButton.place(relx=400/1000,rely=125/680)  
    selectPlotDataButton=tkinter.Radiobutton(root,text='Range of Dataset',variable=plotXV,value=2)
    selectPlotDataButton.place(relx=400/1000,rely=155/680)
    plotButton=tkinter.Button(root,text='Plot',bg='Gold',width=5,command=lambda: click_plot_data_button(importFilePath,root,showPlotPathText,selectPlotPhotonButton,plotXV))
    plotButton.place(relx=565/1000,rely=100/680)
    clearPathButton=tkinter.Button(root,text='Clear',width=5,command=lambda: _click_plot_clear_button(showPlotPathText,selectPlotPhotonButton,plotXV))
    clearPathButton.place(relx=565/1000,rely=155/680)

    root.mainloop()




if __name__ == "__main__":   
    lastChoice=''
    elementArray=[]
    uniqueArray=[]
    elementArray2=[]
    uniqueArray2=[]
    importFilePath=''   
    sortOrder='by_number'
    
    root_window()



    