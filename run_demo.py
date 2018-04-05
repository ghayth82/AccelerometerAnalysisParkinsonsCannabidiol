
dataf = createDatasetFromFiles()

# extracts from accelerometer data (0) and maximum frequency 32, without filtering
feats0_32 = featuresFromDataframe(dataf, 0, maxfr=32, filtering=False)


