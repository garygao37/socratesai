import pandas as pd
import numpy as np
from nltk.tokenize import sent_tokenize
from numpy.linalg import norm
from dataset import load_dataset

from sentence_transformers import SentenceTransformer
sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def top_k_indices(cos_similarities, k):
    # Get indices of top 5 highest cosine similarity values
    top_indices = np.argsort(cos_similarities)[::-1][:k]
    print(top_indices)
    return top_indices

def cosine_similarity(query_emb, article_embs, k=1):
    # Compute dot product of query with each article embedding
    print("query;", query_emb.shape)
    print(type(article_embs))
    print("article;", article_embs.shape)
    dot_products = np.dot(article_embs, query_emb)
    
    # Compute norms of query and article embeddings
    query_norm = norm(query_emb)
    article_norms = norm(article_embs, axis=1)
    
    # Compute cosine similarity
    cos_sim = dot_products / (query_norm * article_norms)

    article_index = top_k_indices(cos_sim, k)[0]
    print(article_index)
    return cos_sim, article_index

def getQueryEmbed(query):
    query_vec = sbert_model.encode([query])[0]
    return query_vec

def break_articles_into_sentences(article):
  sentences = sent_tokenize(article)
  return(sentences)

def pipeline(query, article_embs, articles):
    print("type of", type(article_embs))
    print("type of", type(articles))
    print(query)
    #return top article and quotes.
    #but the quotes require ranking - perhaps need more helper functions? 
    """
    the user query, article embeddings(from colab), and the article list are inputted. The selected article and the top 5 quotes are returned. 
    """

    print("in the pipeline")

    query_vec = getQueryEmbed(query)
    print("Got the query vector")
    cos_sim, article_index = cosine_similarity(query_vec, article_embs)
    print("Cosine Similarity")
    print(article_index)

    print("Right after cos")

    selected_article = articles[article_index]
    sentence_list = break_articles_into_sentences(selected_article)
    sentence_sim_list = []
    for sent in sentence_list:
        sim = cosine(query_vec, sbert_model.encode([sent])[0])
        sentence_sim_list.append((sim, sent))
        print(sim, sent)
    print("iterating through the sentences")
    sorted_sentence_sim_list = sorted(sentence_sim_list, key=lambda x: x[0], reverse=True) #Sorting tuples with the lambda function
    top5 = sorted_sentence_sim_list[0:5] #(cos similarity, sentence)
    top5_sentences = [sentence for _, sentence in top5]
    print("getting the top5")
    sentence_embeddings = np.vstack(top5_sentences)
    print("stacking")

    return (articles[article_index], top5_sentences)

if __name__ == "__main__":
    query="who is Daniel Radcliffe?"
    articles, article_embeddings = load_dataset()
    the_article, quotes = pipeline(query, article_embeddings, articles)
    print(quotes)
    print(the_article)
