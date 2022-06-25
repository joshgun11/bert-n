import pandas as pd 
import csv
from sklearn.model_selection import train_test_split
import numpy as np 
import re
import random
import scipy.sparse as sp
from math import log
import pickle as pkl


class Prepare_Data():
    def __init__(self):
        return 
    
    def read_data(self,path):
        df  = pd.read_csv(path)
        df.drop_duplicates(subset = ["text"],inplace = True)
       
        df["label"] = [x.lower() for x in df["label"]]
        df.reset_index(inplace = True)
        return df

    def clean_text(self,x):
        pattern = r'[^a-zA-z0-9\s]'
    
        text = re.sub(pattern, '', x)
        text = re.sub(r'[^\w\s]', '', text)
        text = " ".join(text.split())
        return text

    def clean_numbers(self,x):
        if bool(re.search(r'\d', x)):
            x = re.sub('[0-9]{5,}', '#####', x)
            x = re.sub('[0-9]**{4}**', '####', x)
            x = re.sub('[0-9]**{3}**', '###', x)
            x = re.sub('[0-9]**{2}**', '##', x)
        return x

    def clean_data(self,df):
        cleaned_text = []
        for i in df["text"]:
            i = self.clean_text(i)
            #i = self.clean_numbers(i)
            cleaned_text.append(i)
        df["text"]=cleaned_text

        return df
    
    
        
    def export_data(self,path,data_path):

        processor = Prepare_Data()
        df = processor.read_data(path+data_path)
        print(df.columns)

        df = processor.clean_data(df)

        train,test = train_test_split(df,test_size = 0.2)
        train_label = []
        for i in range(train.shape[0]):
            train_label.append("Train")
    
        test_label = []
        for i in range(test.shape[0]):
            test_label.append("Test")
        train["split"] = train_label
        test["split"] = test_label
        train_new = train[['index', 'split', 'label','text']]
        test_new = test[['index', 'split', 'label','text']]
        frames = [train_new,test_new]

        result = pd.concat(frames)

        label_data = result[['index', 'split', 'label']]
        text_data = result["text"]

        np.savetxt(path+'/corpus/df_clean.txt', 
        result["text"].values,fmt='%s', delimiter='\t')
        np.savetxt(path+'/df.txt', label_data.values,fmt='%s', delimiter='\t')

processor = Prepare_Data()
processor.export_data('data','/text_data.csv')









        
        
    



    

    