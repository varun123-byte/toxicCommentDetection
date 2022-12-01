
from sklearn import preprocessing
from sklearn.feature_selection import SelectFromModel


from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import f1_score, precision_score, recall_score, precision_recall_curve, fbeta_score, confusion_matrix
from sklearn.metrics import roc_auc_score, roc_curve

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
import os
from pprint import pprint 
import googleapiclient.discovery
import pickle
import emoji

from flask import Flask, render_template, request
import numpy as np
import json
import urllib
import urllib.request
import jinja2

test = pickle.load(open('model_gb.pkl', 'rb'))
test2 = pickle.load(open('model_gb2.pkl', 'rb'))
AllcommentsGobally=[]
def char_is_emoji(character):
    return character in emoji.UNICODE_EMOJI


def text_has_emoji(text):
    for character in text:
        if character in emoji.UNICODE_EMOJI:
            return True
    return False

app = Flask(__name__)
@app.route('/')
def man():
    return render_template('home.html')

@app.route('/active')
def man1():
    return render_template('active.html')

@app.route('/activeComment',methods=['POST'])
def man4():
    try:
        allcomment=request.form["typtxt"]
        
    except:
        array1=[]
        array1.append("invalid link")
        return render_template('active.html', error=array1)
    return render_template('new.html', answer=AllcommentsGobally)

@app.route('/about')
def man3():
    return render_template('about.html')

@app.route('/activeForm',methods=['POST'])
def man2():
    try:
        youtube_video = request.form["typedText"]
        video_id = youtube_video.split("=")[1]
    except:
        array1=[]
        array1.append("invalid link")
        return render_template('active.html', error=array1)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCFROwksqEH6YZYgwXPPI5w-iPlBeCuFu8"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    rst = youtube.commentThreads().list(
        part="snippet",
        textFormat="plainText",
        videoId=video_id ,
        maxResults=200
        
    )

    try:
        response = rst.execute()
     

        commentList=[]
        for item in response['items'][:100]:
            t=item['snippet']['topLevelComment']['snippet']['textOriginal']
            s=""
            for i in t:
                if(char_is_emoji(i)==False):
                    s=s+i
            l=[]
            l.append(s)
            if(s!=""):
                commentList.append(l)
        
        ary=[]
     
        c=0
        d=0
        for i in commentList:
            comment1_vect = test.transform(i)
            ans1=test2.predict_proba(comment1_vect)[:1]
            k1=ans1[0][1]
            d+=1
            if(k1>0.9):
                ary.append(i)
                c+=1
     
        global AllcommentsGobally
        AllcommentsGobally=commentList
        return render_template('active.html', allcomments=commentList,ans=ary,cc=c,dd=d)
    except:
        array1=[]
        array1.append("comments are deactivated")
        return render_template('active.html', error=array1)
  
if __name__ == "__main__":
    app.run(debug=True)
