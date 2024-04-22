import pandas as pd
import numpy as np
import nltk
import networkx as nx
from nltk.tokenize import sent_tokenize
from numpy.linalg import norm
from dataset import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


from sentence_transformers import SentenceTransformer
sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Download required NLTK resources
nltk.download("punkt") 

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
    article_embs = np.array(article_embs)  # Convert list to numpy array
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


def custom_cosine_similarity(vectors):
    similarity_matrix = np.zeros((vectors.shape[0], vectors.shape[0]))

    # Compute cosine similarity between each pair of sentence vectors
    for i in range(vectors.shape[0]):
        for j in range(vectors.shape[0]):
            dot_product = np.dot(vectors[i], vectors[j])
            norm_i = norm(vectors[i])
            norm_j = norm(vectors[j])
            similarity_matrix[i, j] = dot_product / (norm_i * norm_j)

    return similarity_matrix

def getQueryEmbed(query):
    query_vec = sbert_model.encode([query])[0]
    return query_vec

def generate_key_terms(articles, top_n=5):
    vectorizer = TfidfVectorizer(stop_words='english')

    tfidf_matrix = vectorizer.fit_transform(articles)

    feature_names = vectorizer.get_feature_names_out()

    key_terms = []
    for i in range(tfidf_matrix.shape[0]):
        # Extract the TF-IDF scores for the article
        tfidf_scores = tfidf_matrix[i].tocoo()

        scores_df = pd.DataFrame({
            'term': [feature_names[j] for j in tfidf_scores.col],
            'tfidf_score': tfidf_scores.data
        })

        scores_df = scores_df.sort_values(by='tfidf_score', ascending=False)

        key_terms.append(scores_df['term'].head(top_n).tolist())

    return key_terms #key_terms is a list

def text_rank_summarizer(articles, top_n=5):
    bullet_points = []

    for text in articles:
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)

        # Create a TF-IDF matrix for the sentences
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)

        # Calculate the similarity matrix using custom cosine similarity
        similarity_matrix = custom_cosine_similarity(tfidf_matrix.toarray())

        # Create a graph where nodes are sentences and edges represent similarity
        graph = nx.from_numpy_array(similarity_matrix)

        # Use the PageRank algorithm to rank the sentences based on TextRank
        scores = nx.pagerank(graph)

        # Sort the sentences by their scores in descending order
        sorted_sentences = sorted(
            ((scores[i], s) for i, s in enumerate(sentences)),
            reverse=True
        )

        # Extract the top N sentences
        top_sentences = [s[1] for s in sorted_sentences[:top_n]]

        # Add to the bullet points list
        bullet_points.extend(top_sentences)

    return bullet_points

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

    key_terms1 = generate_key_terms(articles, top_n=7)

    key_terms = [item for sublist in key_terms1 for item in sublist]
    combined_key_terms = " ".join(key_terms)
    key_terms1_embs = sbert_model.encode([combined_key_terms])[0]

    for sent in sentence_list:

        similarity_to_key_terms = cosine(key_terms1_embs, sbert_model.encode([sent])[0])
        print(type(key_terms1_embs))
        similarity_to_query = cosine(query_vec, sbert_model.encode([sent])[0])

        beta = 0.3

        alpha = 0.7

        combined_similarity = (similarity_to_key_terms*beta + similarity_to_query*alpha) / 2

        sentence_sim_list.append((combined_similarity, sent))

    sorted_sentence_sim_list = sorted(sentence_sim_list, key=lambda x: x[0], reverse=True) 

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
