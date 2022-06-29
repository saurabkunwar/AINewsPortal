from django.shortcuts import render
from backendservice.models import Article
from django.db.models import Q
from django.http import JsonResponse

# AI stuff
from sentence_transformers import SentenceTransformer, util
import torch
import pandas as pd

filter = 'content'
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_cosine(target_sentence, target_df):
  target_embedding = model.encode(target_sentence, convert_to_tensor=True)
  title_list = list(target_df[filter])
  list_embedding = model.encode(title_list, convert_to_tensor=True)
  cosine_scores = util.cos_sim(target_embedding, list_embedding)
  cosine_list = torch.squeeze(cosine_scores).tolist()
  target_df['cosine'] = cosine_list
  similar_df = target_df.sort_values(by=['cosine'], ascending=False).head(10)
  return list(similar_df.id)[1:], list(similar_df.cosine)[1:]

def article_to_df():
    df = pd.DataFrame(list(Article.objects.all().values()))
    return df

# Create your views here.

def index(request):

    articles = Article.objects.filter(~Q(summarization='')).order_by('-published_date')

    context = {
        "articles":articles
    }

    return render(request, 'index.html', context)


def explore(request, id):

    article = Article.objects.get(pk=id)

    # Code to find similar articles
    df = article_to_df()
    target_sentence = [article.content]
    ids, cosines = calculate_cosine(target_sentence, df)

    related_articles = []

    for id in ids:
        temp = Article.objects.get(pk=id)
        related_articles.append(temp)

    context = {
        "article":article,
        "related_articles":related_articles
    }


    return render(request, 'explore.html', context)

