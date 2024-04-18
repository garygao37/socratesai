import numpy as np
import pandas as pd

def load_dataset():
    stacked_embeddings = np.load('./stacked_embeddings.npy')
    df = pd.read_csv('./articles.csv') 
    articles = df['articles'].tolist()
    return articles, stacked_embeddings


