from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

import pandas as pd
import numpy as np
import random


from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def sanitization(web):                      
    web = web.lower()
    token = []
    dot_token_slash = []
    raw_slash = str(web).split('/')
    for i in raw_slash:
        raw1 = str(i).split('-')            
        slash_token = []
        for j in range(0,len(raw1)):
            raw2 = str(raw1[j]).split('.') 
            slash_token = slash_token + raw2
        dot_token_slash = dot_token_slash + raw1 + slash_token # all tokens
    token = list(set(dot_token_slash))      
    if 'com' in token:
        token.remove('com')                 
    return token

def removeAddtionalInfo(s):
    if 'www.' == s[0:4]:
        s=s[4:]
    elif 'http://www.' == s[0:11]:
        s=s[11:]
    elif 'https://www.' == s[0:12]:
        s=s[12:]
        
    #if '/' in s:
    #   s=s[:s.find('/')]
    return s   

url = 'C:\\Users\\sambhu\\Desktop\\programming\\sai_Django\\IrfanSirURLDetect\\basic_app\\dataset.csv'
url_csv = pd.read_csv(url,',',error_bad_lines=False)
url_df = pd.DataFrame(url_csv)                                                                                                
url_df = np.array(url_df)                      
random.shuffle(url_df)
y = [d[1] for d in url_df]                  
urls = [d[0] for d in url_df]              

vectorizer = TfidfVectorizer(tokenizer=sanitization)  
x = vectorizer.fit_transform(urls)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

lgr = LogisticRegression()                  
lgr.fit(x_train, y_train)
score = lgr.score(x_test, y_test)
print("score: {0:.5f} %".format(100 * score))
vectorizer_save = vectorizer


class IndexView(TemplateView):
    template_name = 'index.html'
def URL(request):
    
           
       if request.method=="POST":
           URLForm = request.POST['URL']
           i=removeAddtionalInfo(URLForm)
           print(i)
           i=[i]
           i = vectorizer.transform(i)
           y_predict = lgr.predict(i)
                    
           my_dict={'message':f"""Hi,\n
This is to confirm that the URL {URLForm} you have entered us to check for phishing websites  is {y_predict[0]}.

Prediction Done.

Regards
Fraud Website Dectector

    
    """              }
           return render(request,'URLDetection.html',context=my_dict)
           pass
       else:
            return render(request,'URLDetection.html')
                   
    