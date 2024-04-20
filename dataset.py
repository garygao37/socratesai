import numpy as np
import pandas as pd
from bert import getDataset

def load_dataset():
    stacked_embeddings = np.load('./stacked_embeddings.npy')
    df = pd.read_csv('./articles.csv') 
    articles = df['articles'].tolist()
    return articles, stacked_embeddings

def load_dataset_2():
    stacked_embeddings = np.load('./stacked_embeddings(2).npy')
    df = pd.read_csv('./articles(2).csv') 
    articles = df['articles'].tolist()
    return articles, stacked_embeddings

def load_data_function(textarea_values):
    stacked_embeddings = getDataset(textarea_values)
    artciles = textarea_values
    return articles, stacked_embeddings
