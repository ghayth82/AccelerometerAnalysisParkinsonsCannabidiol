##
# Code for reading files and extract accelerometer features
#
# Moacir Ponti / 2017
##
import csv
import numpy as np
import matplotlib.pyplot as plt
import os

from numpy import genfromtxt
from matplotlib.backends.backend_pdf import PdfPages

#directory = u"./data/"

def createDatasetFromFiles(directory = u'./data/', id = -1):
    j=1
    for path, dirs, files in os.walk(directory):

            print(dirs)
            apath = path.split(os.sep)
            print(apath[-1])

            # look for the right folder
            if apath[-1] != 'Medidas acelerômetro' \
               and apath[-1] != 'Medidas Acelerometro' \
               and apath[-1] != 'Acelerometro' \
               and apath[-1] != 'Acelerômetro':
                print("Skip!")
                continue

            # sort files
            files.sort()

            # for each txt file
            for f in files:
                    if f.endswith(".txt"):
                            fname = path + "/" + f
                            print(fname)
                            fp = open(fname,'r')
                            data = fp.readlines()[4:1822]
                            matrix = []
                            for d in data:
                                obs = [x.strip() for x in d.split(',')]
                                matrix.append(obs)

                            matrix = np.array(matrix)


#return dataAcc                          
                        




