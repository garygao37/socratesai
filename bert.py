import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

#textarea_values is a list of strings - which is what we want. It is essentailly our version of article-list_small (or in this case articles) - If I AM not mistakend. 

def getDataset (textarea_values):
  #Calculate the embeddings for every article
  embeddings = []
  for sent in textarea_values:
    embed = sbert_model.encode([sent])[0]
    embeddings.append(embed)
  stacked_embeddings = np.vstack(embeddings)
  return stacked_embeddings