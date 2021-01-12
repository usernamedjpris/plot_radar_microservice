# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 14:37:57 2020

@author: Jérémie
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from servinglayer import dataaccess




def convert(thetas):
    """Convert Theta (North Origin to Trigo Origin)"""
    teth = []    
    for theta in thetas:
        
        if (theta <= 270):
            teth.append(90 - theta)
        else:
            teth.append(90 + 360 - theta)
    return np.array(teth)
    


def angle2xy(theta,rho):
    """Convert polar coordinate into cartesian coordinate"""
    x = rho*np.cos(np.radians(theta))
    y = -rho*np.sin(np.radians(theta))
    return (x,y)



def format_date(date):
    date = date[:2]+"/"+date[3:5]+"/"+date[6:]
    return date



def read_data(datedebut,datefin):  
    """read data from a csv file (soon : from a database)"""
    #os.chdir("E:/eDocuments/projet intégrateur/asterix_big_data/parser_tests/")
    #df = pd.read_csv('../../data/new_data.csv', delimiter=';')
    df = dataaccess.query_range_date_df(format_date(datedebut),format_date(datefin))
    #df = dataaccess.query_range_date_df("20/07/29-10:00","20/07/29-12:00") #("29/07/20-10:00","29/07/20-12:00")
    return df
    

def plot_flight(df,identification,datedebut,datefin):
    """plot and save figure of the given flight (identification) among the flights of the dataset (df)"""
    # plot configuration
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111)
    
    # ploting all flights of the dataset
    for i in range(df.shape[0]):
        plt.plot(df.iloc[i]["X"],df.iloc[i]["Y"],color='#444')
    df = df.set_index('ID')
     #print(df.head())
    
    # ploting the desired flight
    flight = df.loc[identification]     
    plt.plot(flight["X"],flight["Y"],"-",color="#FF7A86", linewidth=3)
    ax.add_artist(plt.Circle((flight["X"][-1],flight["Y"][-1] ), 1.5, color='#FFBAC6', linewidth=1,zorder=10))
    ax.add_artist(plt.Circle((flight["X"][-1],flight["Y"][-1] ), 3, color='#FFBAC6', fill=None, linewidth=1,zorder=10))
    
    # adding some cool style 
    for spine in ['bottom','top','right','left']:
        ax.spines[spine].set_color('#444')
    plt.axis("equal")
    plt.grid(color='#444', linewidth=0.7)
    frame1 = plt.gca()
    frame1.axes.get_yaxis().set_visible(False)
    plt.xticks([-150,-100,-50,0,50,100,150], ('$-150km$', '$-100km$', '$-50km$', '$0km$', '$50km$', '$100km$', '$150km$'))      
    plt.title("AI: "+identification.split(" ")[0]+"    AA:"+identification.split(" ")[-1])  
    
    # saving file and returning PATH
    RELATIVE_PATH = "/plots/"+identification.replace(" ","_")+"_"+datedebut.replace(":","-")+"_"+datefin.replace(":","-")+".png"    
    plt.savefig("."+RELATIVE_PATH)
    print(os.getcwd()+RELATIVE_PATH)
    #plt.show()
    




def main(argv):
    """plot radar and return path of the image"""

    # Deal with args
    if len(sys.argv) == 5:
        radar, datedebut, identification = int(sys.argv[1]), sys.argv[2],str(sys.argv[3])+" "+str(sys.argv[4])
        datefin = datedebut[:-5]+"23:59" #a changer : il faut mettre jusqu'a la fin de la journee
    elif len(sys.argv) == 6:
        radar, datedebut,datefin, identification = int(sys.argv[1]), sys.argv[2], sys.argv[3], str(sys.argv[4])+" "+str(sys.argv[5])
        #radar, datedebut,datefin, identification = sys.argv[1], sys.argv[2], sys.argv[3], str(sys.argv[4])

    else:
        print('usage: python plotRadar.py @radar YY-MM-DD-HH:mm YY-MM-DD-HH:mm AI AA\nusage: python3 plotRadar.py @radar YY-MM-DD-HH:mm AI AA\nexample: python plotRadar.py 25 20-07-29-10:00 20-07-29-12:00 EVX02EK 38173A')
        sys.exit(12)
        #datedebut, datefin, identification= "12-12-2020", "12-12-2020", "TRA39U 4841AA"#"FPO6610 39666F"VS"JAF7FE 44A835" #"VLG8191 343194"(landed)#"TAR724 02A194"#"AFR1390 3991E1" #"AAF525 398005"
        
    # Read Data    
    try:
        df2 = read_data(datedebut,datefin)  
    except:
        print("no data available")
    # ID
    df2["ID"] = [str(tid).replace(" ","")+" "+str(aa).replace(" ","") for tid, aa in zip(df2["tid"],df2["aa"])]
    #df2["ID"] = df2["aa"]
    
    try:
         df2 = df2[df2["sic"]==25]
         print("sic =",25)
         print(df2.shape)
    except:
         df2 = df2[df2["sic"]==df2.iloc[1]["sic"]]
         print("sic[1] =",df2.iloc[1]["sic"])
         print(df2.iloc[1])
    
    
    # X, Y
    df2["X"],df2["Y"]=angle2xy(convert(df2["theta"]),df2["rho"])
    
    # Aggregation on ID
    df3 = df2.groupby('ID')['X'].apply(list).reset_index(name='X')
    df3['Y'] = df2.groupby('ID')['Y'].apply(list).reset_index(name='Y')['Y']
    
    #print(df2.iloc[1])
    #print(df3.iloc[1])
    print(df3.shape)

    # Plot radar
    try:
        plot_flight(df3,identification,datedebut,datefin)
    except:
        identification = df2.iloc[1]["tid"]+" "+df2.iloc[1]["aa"]  
        plot_flight(df3,identification,datedebut,datefin)





if __name__ == "__main__":
    main(sys.argv)



