import pandas as pd
import numpy as np
from nltk.tokenize import sent_tokenize
from numpy.linalg import norm
from dataset import load_dataset
from inference import generate_key_terms
from inference import text_rank_summarizer

OPENAI_API_KEY="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"

import os
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

def openai(top5_quotes, value, index, articles):

    bullet_points = text_rank_summarizer(articles, top_n=3)

    key_terms = generate_key_terms(articles, top_n=5)

    quote = top5_quotes[index]

    query = value

    context = key_terms
    print("These are the key terms", key_terms)

    model_output = []
    # for idx, (sentence) in enumerate(quote):

    model_input = f"My user has asked the following question {query} to which I have found this quote {quote}.  Please provide a veryshort response (2 short sentences) heavily focusing on this lens: {context}. Please do not use any of your knowledge or facts other than: {bullet_points} "

    message=[ {"role": "user", "content": model_input}]
    temperature=0.2
    max_tokens=512
    frequency_penalty=0.0
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages = message,
        temperature=temperature,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty
    )
    model_output.append(response.choices[0].message.content)

    return model_output


if __name__ == "__main__":
    query="who is Daniel Radcliffe?"
    top5_quotes = ["Top 1 Sentence: LONDON, England (Reuters) -- Harry Potter star Daniel Radcliffe gains access to a reported £20 million ($41.1 million) fortune as he turns 18 on Monday, but he insists the money won't cast a spell on him. ", 
    "Top 2 Sentence: Radcliffe's earnings from the first five Potter films have been held in a trust fund which he has not been able to touch. ",
"Top 3 Sentence: Daniel Radcliffe as Harry Potter in Harry Potter and the Order of the Phoenix To the disappointment of gossip columnists around the world, the young actor says he has no plans to fritter his cash away on fast cars, drink and celebrity parties. ",
"Top 4 Sentence: At 18, Radcliffe will be able to gamble in a casino, buy a drink in a pub or see the horror film ostel: Part II, currently six places below his number one movie on the UK box office chart. ",
"Top 5 Sentence: There is life beyond Potter, however. "]
    print(openai(top5_quotes, query))
