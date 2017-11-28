# -*- coding: utf-8 -*-
"""
Created on Sun Apr 09 06:46:55 2017

@author: nandankirnesh
"""

from lxml import html
import requests
import pandas as pd




def reclinkedin(url):
    names_dict={}
    response=requests.get(url)
    tree=html.fromstring(response.content)
    links=tree.xpath('//*[@id="seo-dir"]/div/div[3]/div/ul/li/a/@href')
    cnames=tree.xpath('//*[@id="seo-dir"]/div/div[3]/div/ul/li/a/text()')
    v=0
    for i in range(len(links)):
        if links[i].startswith("https://www.linkedin.com/directory/"):
            name=cnames[i]
            rnames=reclinkedin(links[i])
            names_dict[name]=rnames

        else:
            v=v+1
            
    if v==len(cnames):
        return cnames
    else:
        return names_dict
        
url="https://www.linkedin.com/directory/companies-a/"
fnames=reclinkedin(url)

nd=pd.DataFrame(columns={'1st','2nd'})

for i in fnames.keys():
    
    nd=nd.append({'1st':i,'2nd':""},ignore_index=True)   
    if type(fnames[i])==dict:
        for j in fnames[i].keys():
            if len(fnames[i][j])==0:
                nd=nd.append({'1st':j,'2nd':""},ignore_index=True)
            else:
                nd=nd.append({'1st':j,'2nd':fnames[i][j][0]},ignore_index=True)
                for k in fnames[i][j][1:]:
                    nd=nd.append({'1st':"",'2nd':k},ignore_index=True)
      
nd.to_csv("F:/linkedincompanies.csv",sep="\t")