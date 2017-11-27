##
# Code for reading files and extract accelerometer features
#
# Moacir Ponti / 2017
##
import csv
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import re

from numpy import genfromtxt
from matplotlib.backends.backend_pdf import PdfPages

#directory = u"./dataClean/"

def createDatasetFromFiles(directory = u'./dataClean/', id = -1):
    j=1
    for path, dirs, files in os.walk(directory):

            #print(dirs)
            apath = path.split(os.sep)
            #print(apath[-1])

            # look for the right folder
            if apath[-1] != 'Medidas acelerômetro' \
               and apath[-1] != 'Medidas Acelerometro' \
               and apath[-1] != 'Acelerometro' \
               and apath[-1] != 'Acelerômetro':
                #print("Skip!")
                continue

            # sort files
            files.sort()

            # for each txt file
            for f in files:
                    if f.endswith(".txt"):
                            fname = path + "/" + f
                      
                            # identify info
                            tags = re.split('/',fname)
                            name = tags[2].title() #participant name
                            drug = int(tags[3][-2]) # drug taken
                            evalname = tags[3].split()[0]

                            # convert evaluation name to number
                            if evalname == "Primeira":
                                evalno = 1
                            elif evalname == "Segunda":
                                evalno = 2
                            else:
                                print("Evaluation name does not match 'Primeira' or 'Segunda'")
                                evalno = 0

                            print(name + " - Drug: " + str(drug) + \
                                    " - Evaluation: "+ str(evalno) +\
                                    " - File: " + f)

                            # read file
                            fp = open(fname,'r')
                            data = fp.readlines()[4:1822]
                            matrix = []
                            for d in data:
                                obs = [x.strip() for x in d.split(',')]
                                matrix.append(obs)

                            matrix = np.array(matrix)


#return dataAcc                          
                        




