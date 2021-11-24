#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob, os


dataset_path = r'C:/Users/90505/Desktop/resimseti'

# Percentage of images to be used for the test set


counter=0
 
for pathAndFilename in glob.iglob(os.path.join(dataset_path, "*.png")):  
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    
    try:
        datas=(r"C:/Users/90505/Desktop/resimseti/"+str(title)+".txt")
            
        file_train = open(datas,'r') 
    except:
        os.remove((r"C:/Users/90505/Desktop/resimseti/"+str(title)+".png")) 
        print("silindi")
    
