#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob, os


dataset_path = r'C:/Users/90505/Desktop/resimseti'

# Percentage of images to be used for the test set





 
for pathAndFilename in glob.iglob(os.path.join(dataset_path, "*.jpg")):  
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    
    if "(" in str(title):

            

        os.remove((r"C:/Users/90505/Desktop/resimseti/"+str(title)+".jpg")) 
        print("silindi")
    
