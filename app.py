from flask import Flask, render_template, request, redirect, url_for
from Covid19India import CovidIndia
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from gnewsclient import gnewsclient
app = Flask(__name__)

@app.route("/backup")
def hellworld():
    obj = CovidIndia()
    stats = obj.getstats()
    sort = sorted(stats['states'].items(),
                  key=lambda x: x[1]['confirmed'], reverse=True)
    to = obj._CovidIndia__gettotalstats()
    return render_template("index.html", result=sort, total=to, t=stats)



@app.route("/news/<t>")
def news(t):
    cat = t
    print(cat)
    
    client = gnewsclient.NewsClient(
        language='english', location='india', topic=cat, use_opengraph=True, max_results=10)
    client1 = gnewsclient.NewsClient(
        language='hindi', location='india', topic=cat, use_opengraph=True, max_results=5)
    n1 = client.get_news()
    n2 = client1.get_news()
    return render_template("newsdata.html", data=n1, data1=n2)

@app.route('/bar')
def bar():
    bar_labels = labels
    bar_values = values
    return render_template('bar_chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=bar_labels, values=bar_values)


@app.route('/youtube', methods=["POST", "GET"])
def tool():
    if request.method == 'POST':
        url = request.form["url"]
        size = request.form["size"]
        try:
            from pytube import YouTube
            from pytube import Playlist
        except Exception as e:
            print("Few modules are missing {}".format(e))
        ytd = YouTube(url).streams.first().download()
        print(ytd)
        print(url)
        return redirect(url_for('thankyou'))
    else:
        return render_template('youtube-search.html')

#backup home
@app.route("/backupanother")
def globalData():
    url = "https://api.covid19india.org/data.json"
    resp = requests.get(url)
    d = resp.json()
    obj = statedata("TT")
    
    client = gnewsclient.NewsClient(
        language='english', location='india', topic="All", use_opengraph=True, max_results=10)
    n1 = client.get_news()
    return render_template("index_new.html", result=d, total=obj, data=n1)


#Testing for Graph
@app.route("/")
def home():
    url = "https://api.covid19india.org/data.json"
    resp = requests.get(url)
    d = resp.json()
    obj = statedata("TT")
    # client = gnewsclient.NewsClient(
    #     language='english', location='india', topic="All", use_opengraph=True, max_results=10)
    # n1 = client.get_news()
    return render_template("index_responsive.html", result=d, total=obj)

@app.route('/mpdata/<stateCode>')
def mpstatus(stateCode):
    url = "https://api.covid19india.org/state_district_wise.json"
    resp = requests.get(url)
    d = resp.json()
    for i, j in d.items():
        if j['statecode'] == stateCode:
            n = j
    newDict = {}
    for i, j in n.items():
        for a, b in j.items():
            newDict[a] = b
        break
    obj = statedata(stateCode)  
    # client = gnewsclient.NewsClient(
    # language='english', location='india', topic="All", use_opengraph=True, max_results=10)
    # n1 = client.get_news()
    return render_template('mpdata.html', j=newDict, ob=obj)

@app.route('/mp')
def madhya():
    url = "https://api.covid19india.org/state_district_wise.json"
    resp = requests.get(url)
    d = resp.json()
    for i, j in d.items():
        if i == "Madhya Pradesh":
            n = j
    newDict = {}
    for i, j in n.items():
        for a, b in j.items():
            newDict[a] = b
        break
    confirm = 0
    active = 0
    recover = 0
    death = 0
    for i, j in newDict.items():
        confirm += j['confirmed']
        active += j['active']
        recover += j['recovered']
        death += j['deceased']
    t = {}
    t['c'] = confirm
    t['a'] = active
    t['r'] = recover
    t['d'] = death
    tc = 0
    ta = 0
    tr = 0
    td = 0
    a = {}
    for i, j in newDict.items():
        newd = j['delta']
        for i, j in newd.items():
            if i == 'confirmed':
                tc += j
            if i == 'deceased':
                td += j
            if i == 'recovered':
                tr += j
    a['c'] = tc
    a['d'] = td
    a['r'] = tr
    a['a'] = abs(tc-tr)
    obj = statedata('MP')
    
    client = gnewsclient.NewsClient(
    language='english', location='india', topic="All", use_opengraph=True, max_results=10)
    n1 = client.get_news()
    return render_template('mp.html', j=newDict, total=t, inc=a, ob=obj,data=n1)

#try to explored Graph
@app.route('/test')
def chartTest():
    url = "https://api.covid19india.org/state_district_wise.json"
    resp = requests.get(url)
    # print(resp)
    # print(dir(resp))
    d = resp.json()
    for i, j in d.items():
        if i == "Madhya Pradesh":
            n = j
    li = [i for i in n.values()]
    temp = li[0]
    DistrictName = [i for i in temp.keys()]

    # Fetch the  active case number
    activeCase = []
    for i, j in temp.items():
        activeCase.append(j['active'])
    data = {
        "Name": DistrictName,
        "case": activeCase
    }
    # print(data)
    # Create the dataFrame object
    df = pd.DataFrame(data, index=DistrictName)
    df.plot(kind='barh', figsize=(20, 10))
    return render_template('chart.html', name=plt.show())


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")
@app.route("/about")
def aboutpage():
    return render_template("about.html")    
@app.route("/check")
def check():
    return render_template("index_responsive.html")

def statedata(name):
    url = "https://api.covid19india.org/data.json"
    resp = requests.get(url)
    d = resp.json()
    for i in d['statewise']:
        if i['statecode'] == name:
            return (i['confirmed'], i['deaths'], i['active'], i['recovered'], i['deltaconfirmed'], i['deltadeaths'], i['deltarecovered'], i['lastupdatedtime'])


if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug=True)
