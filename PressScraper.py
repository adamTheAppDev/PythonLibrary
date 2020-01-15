# -*- coding: utf-8 -*-
"""
Created on Wed May  3 15:14:55 2017

@author: AmatVictoriaCuramIII
"""

#This is a news scraper, it doesn't work very well. See YahooGrabber.

import newspaper
from newspaper import Article
bbc_paper = newspaper.build('http://bbc.com/news', language = 'en')
npr_paper = newspaper.build('http://npr.org/sections/news', language = 'en')
wsj_paper = newspaper.build('http://wsj.com/', language = 'en')
#for article in bbc_paper.articles:
#     print(article.url)
#for article in npr_paper.articles:
#     print(article.url)
#for article in wsj_paper.articles:
#     print(article.url)
first_article = bbc_paper.article_urls[0]
