# AINewsPortal

This is a news summarization Django app powered by Pegasus Model. This app scraps news from news website like KathmanduPost and NepalNews and summarizes it in a proper way so that user can save their time when browsing news.

Beside summarization, it also utilizes power of Semantic Textual Similarity to suggest similar news.

It is an ongoing project. Upcoming feature includes, tracking user behavior for proper news suggestion and I'm planning to include question answering system from news articles.


## Motivation

Reading news is a very time consuming process. Most news have filler content that might not be important for the viewers. And the news are cluttered with unwanted ads. Beside that, we can hardly get related news article.

Through this project, I aim to summarize these news in a very short format and use semantic similarity to suggest similar news article.


## Demo

Home page of web app

![alt text](https://github.com/saurabkunwar/AINewsPortal/blob/master/images/1.PNG)


Some examples of summarized News

![alt text](https://github.com/saurabkunwar/AINewsPortal/blob/master/images/2.PNG)


Similar News suggested by using semantic similarity

![alt text](https://github.com/saurabkunwar/AINewsPortal/blob/master/images/3.PNG)

![alt text](https://github.com/saurabkunwar/AINewsPortal/blob/master/images/5.PNG)


## Technical Aspect

1. Crawling of website is done by BeautifulSoup4
2. Summarization of news is done by Pegasus Model by google. Specifically, 'pegasus-cnn_dailymail' checkpoint. No finetuning is done. Hugging face library is used.
3. 'all-MiniLM-L6-v2' model is used to find semantic textual similarity between these news content. Sentence transformers library is used for this purpose.
4. In the end, django is used to deploy the model.


## Directory/File Description

1. NepalNewsCrawler.py and crawler.py are used to crawl the nepalnews and kathmandupost respectively.
2. Summarizer.py looks into database for unsummarized news and summarizes it.
3. Bitesizenews folder consists of django project.

Note: Other files are clutered as it is an ongoing project.

## Futher Improvement

1. User engagement tracking for recommendation system.
2. Question Answering system to quickly find the information.
