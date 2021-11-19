#This file is merging the csv files
import pandas as pd #here I am importing pandas in order to merge the files            

folder = "C:\\Users\\eser\\Desktop\\sondata" #defining my folder Note: this code should be in the same folder of my csv files.
csv_paths  = ["page{1}.csv".format(folder, ix + 1) for ix in range(530)] #here I am creating paths for each csv files Their name start with page1.csv to page530.csv

all_data_frames = [pd.read_csv(csv_path) for csv_path in csv_paths]
merged_data_frame = pd.concat(all_data_frames) #here I am concatanate the each csv file 
merged_data_frame.to_csv("ZubeyirEser12.csv",index=False) #here I am writing concatanated csv file to ZubeyirEser1 file.
# I need to also comment on the csv file(ZubeyirEser1), when I import the data to stata, I had delimeter problem. In order to solve this problem
# I used excel to import csv and then I deleted the cosponsors(it includes all cosponsors description) and the I import the stata
