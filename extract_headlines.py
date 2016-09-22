#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 15:20:37 2016

@author: dsaunder
"""

from bs4 import BeautifulSoup
import glob
import pandas as pd
import re

#%%

def read_frontpage_by_prefix(prefix, frontpagedir):
    return glob.glob(frontpagedir + prefix + '*')[0]
    
def get_url(tag, url_prefix=None):
    if not 'href' in tag.attrs:
        return None
    url = tag.attrs['href']
    url = url.split('#')[0]
    url = url.split('?')[0]
    if url_prefix:
        if not 'http' in url:
            url = url_prefix + url
    return url
    
def get_contents(tag):
    contents = tag.decode_contents()
    if not contents:
        return ''
        
    if type(contents) == list:
        contents = contents[0]

    contents = contents.strip()

    contents, dummy = re.subn('&amp;apos;','\'',contents)
    return contents

    
def extract_all_headlines(fp_timestamp):
    frontpagedir = '../frontpages/%s/' % fp_timestamp
    frontpage_data = pd.DataFrame()
    
    #%%
    # LA TIMES
    prefix = 'lat'
    url_prefix = 'http://latimes.com'
    with open(read_frontpage_by_prefix(prefix,frontpagedir), 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    headline_selectors = ['a.trb_outfit_primaryItem_article_title_a','a.trb_outfit_relatedListTitle_a']
    
    src_rows = pd.DataFrame()
    for selector in headline_selectors:
        headlines = soup.select(selector)
        
        new_rows = pd.DataFrame({'src':[prefix]*len(headlines), 
         'headline':[get_contents(a) for a in headlines],
         'url':[get_url(a, url_prefix) for a in headlines],
        })
        
        new_rows = new_rows.loc[new_rows.headline != '', :]
        src_rows = src_rows.append(new_rows, ignore_index=True)
    
    src_rows.loc[:,'article_order'] = range(1,len(src_rows)+1)
    frontpage_data = frontpage_data.append(src_rows, ignore_index=True)
    
    #%%
    # New York Times
    prefix = 'nyt'
    url_prefix = None
    
    with open(read_frontpage_by_prefix(prefix,frontpagedir), 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    headline_selectors = ['div.story h3 a','ul.headlinesOnly h6 a']
    
    src_rows = pd.DataFrame()
    for selector in headline_selectors:
        headlines = soup.select(selector)
        
        new_rows = pd.DataFrame({'src':[prefix]*len(headlines), 
         'headline':[get_contents(a) for a in headlines],
         'url':[get_url(a, url_prefix) for a in headlines]
        })
        
        new_rows = new_rows.loc[new_rows.headline != '', :]
        src_rows = src_rows.append(new_rows, ignore_index=True)
    
    src_rows.loc[:,'article_order'] = range(1,len(src_rows)+1)
    frontpage_data = frontpage_data.append(src_rows, ignore_index=True)
        
    
    ##%%
    ## Google News
    #prefix = 'goo'
    #url_prefix = None
    #
    #with open(read_frontpage_by_prefix(prefix,frontpagedir), 'r') as f:
    #    soup = BeautifulSoup(f, 'html.parser')
    #headline_selectors = ['.esc-lead-article-title']
    #
    #src_rows = pd.DataFrame()
    #for selector in headline_selectors:
    #    headlines = soup.select(selector)
    #    headlines = [a.contents[0] for a in headlines]
    #    new_rows = pd.DataFrame({'src':[prefix]*len(headlines), 
    #     'headline':[get_contents(a.contents[0]) for a in headlines],
    #     'url':[get_url(a, url_prefix) for a in headlines]
    #    })
    #    
    #    new_rows = new_rows.loc[new_rows.headline != '', :]
    #    src_rows = src_rows.append(new_rows, ignore_index=True)
    #
    #src_rows.loc[:,'article_order'] = range(1,len(src_rows)+1)
    #frontpage_data = frontpage_data.append(src_rows, ignore_index=True)
    #    
    
    #%%
    # CNN
    prefix = 'cnn'
    url_prefix = 'http://www.cnn.com'
    
    with open(read_frontpage_by_prefix(prefix,frontpagedir), 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    headline_selectors = ['h3.cd__headline']
    
    src_rows = pd.DataFrame()
    for selector in headline_selectors:
        headlines = soup.select(selector)
        headlines = [a.contents[0] for a in headlines]
        new_rows = pd.DataFrame({'src':[prefix]*len(headlines), 
         'headline':[a.contents[0].contents[0] for a in headlines],
         'url':[get_url(a, url_prefix) for a in headlines]
        })
        
        new_rows = new_rows.loc[new_rows.headline != '', :]
        src_rows = src_rows.append(new_rows, ignore_index=True)
    
    src_rows.loc[:,'article_order'] = range(1,len(src_rows)+1)
    frontpage_data = frontpage_data.append(src_rows, ignore_index=True)
    
    #%%
    # Fox
    prefix = 'fox'
    url_prefix = None
    
    with open(read_frontpage_by_prefix(prefix,frontpagedir), 'r') as f:
        soup = BeautifulSoup(f, 'lxml')
    headline_selectors = ['.primary h1 a','.top-stories a']
    
    src_rows = pd.DataFrame()
    for i,selector in enumerate(headline_selectors):
        headlines = soup.select(selector)
        new_rows = pd.DataFrame({'src':[prefix]*len(headlines), 
         'headline':[get_contents(a) for a in headlines],
         'url':[get_url(a, url_prefix) for a in headlines]
        })
        
        new_rows = new_rows.loc[new_rows.headline != '', :]
        src_rows = src_rows.append(new_rows, ignore_index=True)
    
    for j in range(len(src_rows)):
        if '<!--' in src_rows.loc[j,'headline']:
            src_rows.loc[j,'headline'] = re.search('<h3>(.*)</h3>',src_rows.loc[j,'headline']).groups()[0]
        if 'span style' in src_rows.loc[j,'headline']:
            src_rows.loc[j,'headline'] = re.search('>(.*)<',src_rows.loc[j,'headline']).groups()[0]
    
    src_rows.loc[:,'article_order'] = range(1,len(src_rows)+1)
    frontpage_data = frontpage_data.append(src_rows, ignore_index=True)
    
    #%%
    # Washington Post
    prefix = 'wap'
    url_prefix = None
    
    with open(read_frontpage_by_prefix(prefix,frontpagedir), 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    headline_selectors = ['.headline a']
    
    src_rows = pd.DataFrame()
    for i,selector in enumerate(headline_selectors):
        headlines = soup.select(selector)
        
        new_rows = pd.DataFrame({'src':[prefix]*len(headlines), 
         'headline':[get_contents(a) for a in headlines],
         'url':[get_url(a, url_prefix) for a in headlines]
        })
        
        new_rows = new_rows.loc[new_rows.url != None, :]
        
        new_rows = new_rows.loc[new_rows.headline != '', :]
        src_rows = src_rows.append(new_rows, ignore_index=True)
    
    src_rows.loc[:,'article_order'] = range(1,len(src_rows)+1)
    frontpage_data = frontpage_data.append(src_rows, ignore_index=True)
    
    #%%
    # The Guardian
    prefix = 'gua'
    url_prefix = None
    
    with open(read_frontpage_by_prefix(prefix,frontpagedir), 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    headline_selectors = ['a.js-headline-text']
    
    src_rows = pd.DataFrame()
    for i,selector in enumerate(headline_selectors):
        headlines = soup.select(selector)
        new_rows = pd.DataFrame({'src':[prefix]*len(headlines), 
         'headline':[get_contents(a) for a in headlines],
         'url':[get_url(a, url_prefix) for a in headlines]
        })
        
        new_rows = new_rows.loc[new_rows.headline != '', :]
        src_rows = src_rows.append(new_rows, ignore_index=True)
    
    src_rows.loc[:,'article_order'] = range(1,len(src_rows)+1)
    frontpage_data = frontpage_data.append(src_rows, ignore_index=True)
    
    
    
    #%%
    # Wall street journal
    prefix = 'wsj'
    url_prefix = None
    
    with open(read_frontpage_by_prefix(prefix,frontpagedir), 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    headline_selectors = ['.wsj-headline-link']
    
    src_rows = pd.DataFrame()
    for i,selector in enumerate(headline_selectors):
        headlines = soup.select(selector)
        new_rows = pd.DataFrame({'src':[prefix]*len(headlines), 
         'headline':[get_contents(a) for a in headlines],
         'url':[get_url(a, url_prefix) for a in headlines]
        })
        
        new_rows = new_rows.loc[new_rows.headline != '', :]
        src_rows = src_rows.append(new_rows, ignore_index=True)
    
    src_rows.loc[:,'article_order'] = range(1,len(src_rows)+1)
    frontpage_data = frontpage_data.append(src_rows, ignore_index=True)
    #%%
    # BBC news
    prefix = 'bbc'
    url_prefix = 'http://www.bbc.com'
    
    with open(read_frontpage_by_prefix(prefix,frontpagedir), 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    headline_selectors = ['.title-link']
    
    src_rows = pd.DataFrame()
    for i,selector in enumerate(headline_selectors):
        headlines = soup.select(selector)
        new_rows = pd.DataFrame({'src':[prefix]*len(headlines), 
         'headline':[re.sub('\n',' ',a.text.strip()) for a in headlines],
         'url':[get_url(a, url_prefix) for a in headlines]
        })
        
        new_rows = new_rows.loc[new_rows.headline != '', :]
        src_rows = src_rows.append(new_rows, ignore_index=True)
    
    src_rows.loc[:,'article_order'] = range(1,len(src_rows)+1)
    frontpage_data = frontpage_data.append(src_rows, ignore_index=True)
    
    #%%
    # USA Today
    prefix = 'usa'
    url_prefix = 'http://www.usatoday.com'
    
    with open(read_frontpage_by_prefix(prefix,frontpagedir), 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    headline_selectors = ['.hfwmm-primary-hed-link','.hfwmm-list-link','.hgpfm-link']
    
    src_rows = pd.DataFrame()
    for i,selector in enumerate(headline_selectors):
        headlines = soup.select(selector)
        new_rows = pd.DataFrame({'src':[prefix]*len(headlines), 
         'headline':[re.sub('[ \n]+',' ',a.text) for a in headlines],
         'url':[get_url(a, url_prefix) for a in headlines]
        })
        
        new_rows = new_rows.loc[new_rows.headline != '', :]
        src_rows = src_rows.append(new_rows, ignore_index=True)
    
    src_rows.loc[:,'article_order'] = range(1,len(src_rows)+1)
    frontpage_data = frontpage_data.append(src_rows, ignore_index=True)
    
    
    #%%
    # Daily Mail (uk)
    prefix = 'dm'
    url_prefix = 'http://www.dailymail.co.uk'
    
    with open(read_frontpage_by_prefix(prefix,frontpagedir), 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    headline_selectors = ['.article h2 a']
    
    src_rows = pd.DataFrame()
    for i,selector in enumerate(headline_selectors):
        headlines = soup.select(selector)
        new_rows = pd.DataFrame({'src':[prefix]*len(headlines), 
         'headline':[re.sub('[ \n]+',' ',a.text) for a in headlines],
         'url':[get_url(a, url_prefix) for a in headlines]
        })
        
        new_rows = new_rows.loc[new_rows.headline != '', :]
        src_rows = src_rows.append(new_rows, ignore_index=True)
    
    src_rows.loc[:,'article_order'] = range(1,len(src_rows)+1)
    frontpage_data = frontpage_data.append(src_rows, ignore_index=True)

#    #%%
#    # Boston Globe
#    prefix = 'bos'
#    url_prefix = 'http://www.dailymail.co.uk'
#    
#    with open(read_frontpage_by_prefix(prefix,frontpagedir), 'r') as f:
#        soup = BeautifulSoup(f, 'html.parser')
#    headline_selectors = ['.story-title a']
#    
#    src_rows = pd.DataFrame()
#    for i,selector in enumerate(headline_selectors):
#        headlines = soup.select(selector)
#        new_rows = pd.DataFrame({'src':[prefix]*len(headlines), 
#         'headline':[re.sub('[ \n]+',' ',a.text) for a in headlines],
#         'url':[get_url(a, url_prefix) for a in headlines]
#        })
#        print new_rows.headline + " " + new_rows.url
#        new_rows = new_rows.loc[new_rows.headline != '', :]
#        src_rows = src_rows.append(new_rows, ignore_index=True)
#    
#    src_rows.loc[:,'article_order'] = range(1,len(src_rows)+1)
#    frontpage_data = frontpage_data.append(src_rows, ignore_index=True)

    #%%
    frontpage_data.loc[:,'fp_timestamp'] = fp_timestamp

    return frontpage_data
