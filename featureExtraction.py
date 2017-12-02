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
import pickle as pkl
import re

from numpy import genfromtxt
from matplotlib.backends.backend_pdf import PdfPages

#directory = u"./dataClean/"

def featuresFromDataframe(df, ts, maxfr=30):
    
    # name/drug/measure/ts-evalno

    # each participant k
    featMat = []
    for k in df:

        print(k)

        # get drug order
        drug_order = int(df[k][1][1][2])
        print("\tFirst Drug: " + str(drug_order))

        # build feature vector
        featVec = [k, drug_order]
 
        # each drug, in order
        for drug in sorted(df[k].keys()):

            print("\t" + str(drug))
            # each measure, compute features
            for measure in sorted(df[k][drug]):

                # Fourier Transform
                tsF  = np.fft.fft(df[k][drug][measure][ts])
                # Power Spectrum within Maximum Frequency
                tfPS = np.abs(tsF[1:maxfr])**2

                # Feature 1: Power Spectrum Entropy
                pse = sum(tfPS * np.log(tfPS))
                # Feature 2: Power Spectrum Frequency Peak
                pspf = np.argmax(tfPS)+1
                # Feature 3: Power Spectrum Peak Value
                psp  = np.max(tfPS)
                # Feature 4: Power Spectrum Weighted Frequency Peak 
                wpsf = psp*pspf

                featVec = featVec + [pse, pspf, psp, wpsf]

        featMat.append(featVec)


    return featMat
    

