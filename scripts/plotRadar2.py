# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 14:37:57 2020

@author: Jérémie
"""
import sys

def plot_flight(df,identification,datedebut,datefin):
    """plot and save figure of the given flight (identification) among the flights of the dataset (df)"""

    # saving file and returning PATH
    PATH = "E:/eDocuments/\"projet intégrateur\"/plot_radar_microservice"
    PATH += "/plots/"+identification.replace(" ","-")+"_"+datedebut+"_"+datefin+".png"    
    print("file:///"+PATH.replace(" ", "%20").replace("é", "%C3%A9").replace("\"", "").replace("\\",""))





def main(argv):
    """plot radar and return path of the image"""
  
    # Deal with args
    if len(sys.argv) == 5:
        radar, datedebut, identification = sys.argv[1], sys.argv[2],str(sys.argv[3])+" "+str(sys.argv[4])
        datefin = datedebut
    elif len(sys.argv) == 6:
        radar, datedebut,datefin, identification = sys.argv[1], sys.argv[1], sys.argv[2], str(sys.argv[4])+" "+str(sys.argv[5])
    else:
        print('usage: python plotRadar.py @radar JJ-MM-YYYY JJ-MM-YYYY AI AA\nusage: python plotRadar.py @radar JJ-MM-YYYY AI AA\nexample: python plotRadar.py 01:00:5e:50:00:26 12-12-2020 TRA39U 4841AA')
        sys.exit(12)
        #datedebut, datefin, identification= "12-12-2020", "12-12-2020", "TRA39U 4841AA"#"FPO6610 39666F"VS"JAF7FE 44A835" #"VLG8191 343194"(landed)#"TAR724 02A194"#"AFR1390 3991E1" #"AAF525 398005"
        
    # Plot radar
    plot_flight("",identification,datedebut,datefin)

    return 0


if __name__ == "__main__":
    main(sys.argv)



