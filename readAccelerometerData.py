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

def createDatasetFromFiles(directory = u'./dataClean/', id = -1):
    j=1
    data = {}
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
                            measure = int(f[0])

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
                                    " - File: " + str(measure))

                            # read file
                            fp = open(fname,'r')
                            datafile = fp.readlines()[5:1821]
                            matrix = []
                            for d in datafile:
                                obs = [x.strip() for x in d.split(',')]
                                matrix.append(np.asarray(obs, dtype=float))

                            matrix = np.array(matrix)

                            ts1 = np.sqrt(matrix[:,0]**2 + matrix[:,2]**2 + matrix[:,2]**2)
                            ts2 = np.sqrt(matrix[:,3]**2 + matrix[:,4]**2 + matrix[:,5]**2)
				
			    #data standarization/normalization z-score
                            ts1 = (ts1 - np.mean(ts1)) / np.std(ts1)
                            ts2 = (ts2 - np.mean(ts2)) / np.std(ts2)

                            if name not in data:
                                data[name] = {}
                            
                            if drug not in data[name]:
                                data[name][drug] = {}

                            if evalno not in data[name][drug]:
                                data[name][drug][measure] = {}

                            data[name][drug][measure] = [ts1, ts2]

    return pd.DataFrame(data)
                        

def plotParticipant(dataf, name, ts=0, pdfsave=False):
    """Plot the 8 measures for a participant
       given some time series
       :param dataf: Dataframe where data is stored
       :param name: Participant name
       :param ts: Time series 0=accelerometer, 1=gyroscope (default=0)
       :param pdfsave: saves PDF file with name (default=False)
       """
    fig = plt.figure()

    j = 1
    for i in np.arange(1,16,2):
        ax1 = fig.add_subplot(8,2,i)
        ax1.plot(dataf[name][1][j][ts])
        
        ax2 = fig.add_subplot(8,2,i+1)
        ax2.plot(dataf[name][2][j][ts],'r')

        j = j + 1

    if pdfsave:
        filename = name.split()[0].lower() + str(ts) + '.pdf'
        ppdf = PdfPages(filename)
        ppdf.savefig(fig)
        ppdf.close()

    fig.show()


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def featPFreq( ts, fs, order=6, a=5 ):
    """Return frequency features
       :param fs: frequency sampling
       :param order: Butterworth filter order
       :param ts: Time series 0=accelerometer, 1=gyroscope (default=0)
    """

    ts_f = butter_lowpass_filter(ts, fs/5 , fs, order)
    print(ts_f.size)
    ts_f = ts_f[a:-a]
    ts   = ts[a:-a]
    print(ts_f.size)

    fft_ts = scipy.fft(ts)
    fft_ts_f = scipy.fft(ts_f)
    FFT1 = np.square(abs(fft_ts))
    FFT2 = np.square(abs(fft_ts_f))
    freqs = scipy.fftpack.fftfreq(ts.size)

    plt.subplot(2,1,1)
    plt.plot(ts)
    plt.plot(ts_f)

    plt.subplot(2,1,2)
    plt.plot(FFT1[2:30])
    plt.plot(FFT2[2:30])
    plt.show()
    


def featarticipant(dataf, name, nof=0, ts=0):
    """Extract features for the 8 measures for a participant
       given some time series
       :param dataf: Dataframe where data is stored
       :param name: Participant name
       :param nof: Number of features (
       """

    feats = {}
    feats[1] = {}
    feats[2] = {}

    for j in np.arange(1,9):
        ax1.plot(dataf[name][1][j][ts])
        ax2.plot(dataf[name][2][j][ts], 'r-')

        feats[1][j] = featPFreq( dataf[name][1][j][ts] )
        feats[2][j] = featPFreq( dataf[name][2][j][ts] )

    return feats


def saveDataFrame(dataf, filename):

    if filename[-3:] != ".pkl":
        filename = filename + ".pkl"

    dataf.to_pickle(filename)



def loadDataFrame(filename):

    dataf = pd.read_pickle(filename)
    return dataf
