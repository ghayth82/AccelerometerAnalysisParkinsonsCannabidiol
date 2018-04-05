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
import scipy
import scipy.fftpack
import pylab
from scipy import pi
from scipy.signal import butter, lfilter, freqz

from numpy import genfromtxt
from matplotlib.backends.backend_pdf import PdfPages

#directory = u"./dataClean/"

def featuresFromDataframe(df, ts, maxfr=20, filtering=False):
    
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

            #print("\t" + str(drug))
            # each measure, compute features
            for measure in sorted(df[k][drug]):

                tsS = df[k][drug][measure][ts]

                if filtering == True:
                    tsS = butter_lowpass_filter(tsS, 3.6667, int(maxfr*0.9), order=6)

                # Fourier Transform
                tsF  = np.fft.fft( tsS[10:-10] )

                # Power Spectrum within Maximum Frequency
                tfPS = np.abs(tsF[0:maxfr])**2

                # Feature 1: Power Spectrum Entropy
                tfPSprob = (tfPS - np.min(tfPS)) / (np.max(tfPS) - np.min(tfPS))
                pse = -sum(tfPSprob * np.log(0.001+tfPSprob))

                print(tfPS)
                tfPS[0] = 0
                # Feature 2a: Power Spectrum Frequency Peak
                pspf1 = np.argmax(tfPS)
                # Feature 3a: Power Spectrum Peak Value
                psp1  = np.max(tfPS)
                print(pspf1)
                tfPS[pspf1-1:pspf1+1+1] = 0

                # Feature 2b: Power Spectrum Frequency Peak
                pspf2 = np.argmax(tfPS)
                # Feature 3b: Power Spectrum Peak Value
                psp2  = np.max(tfPS)
                print(pspf2)
                tfPS[pspf2-1:pspf2+1+1] = 0

                # Feature 2c: Power Spectrum Frequency Peak
                pspf3 = np.argmax(tfPS)
                # Feature 3c: Power Spectrum Peak Value
                psp3  = np.max(tfPS)

                # Feature 4: Power Spectrum Weighted Frequency Peak 
                wpsf = psp1*pspf1

                print([pse, pspf1, pspf2, pspf3, psp1, psp2, psp3, wpsf])
                
                featVec = featVec + [pse, pspf1, pspf2, pspf3, psp1, psp2, psp3, wpsf]

        featMat.append(featVec)


    return featMat


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y




def writeMatrixCSV(featMat, filename):

    with open(filename, 'w', newline='\n') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(featMat)
