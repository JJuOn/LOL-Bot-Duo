from config import *
import pandas as pd
import requests
import os
import time
import json

headers={"X-Riot-Token":API_KEY}
tiers=['DIAMOND','PLATINUM','GOLD','SILVER','BRONZE','IRON']
divisions=['I','II','III','IV']

def league_challenger():
    URL="https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/{}".format(QUEUE)
    response=requests.get(URL,headers=headers)
    while response.status_code!=200:
        time.sleep(5)
        response=requests.get(URL,headers=headers)
    users=json.loads(response.text)
    if not os.path.exists('./data'):
        os.mkdir('./data')
    if not os.path.exists('./data/league'):
        os.mkdir('./data/league')
    df=pd.DataFrame(columns=list(users['entries'][0].keys()))
    for user in users['entries']:
        df=df.append(user,ignore_index=True)
    df.to_csv('./data/league/challenger.csv',encoding='utf-8-sig')
    print('Done: CHALLENGER')

def league_grandmaster():
    URL="https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/{}".format(QUEUE)
    response=requests.get(URL,headers=headers)
    while response.status_code!=200:
        time.sleep(5)
        response=requests.get(URL,headers=headers)
    users=json.loads(response.text)
    if not os.path.exists('./data'):
        os.mkdir('./data')
    if not os.path.exists('./data/league'):
        os.mkdir('./data/league')
    df=pd.DataFrame(columns=list(users['entries'][0].keys()))
    for user in users['entries']:
        df=df.append(user,ignore_index=True)
    df.to_csv('./data/league/grandmaster.csv',encoding='utf-8-sig')
    print('Done: GRANDMASTER')

def league_master():
    URL="https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/{}".format(QUEUE)
    response=requests.get(URL,headers=headers)
    while response.status_code!=200:
        time.sleep(5)
        response=requests.get(URL,headers=headers)
    users=json.loads(response.text)
    if not os.path.exists('./data'):
        os.mkdir('./data')
    if not os.path.exists('./data/league'):
        os.mkdir('./data/league')
    df=pd.DataFrame(columns=list(users['entries'][0].keys()))
    for user in users['entries']:
        df=df.append(user,ignore_index=True)
    df.to_csv('./data/league/master.csv',encoding='utf-8-sig')
    print('Done: MASTER')

def league_other(tier,division):
    page=1
    URL="https://kr.api.riotgames.com/lol/league/v4/entries/{}/{}/{}".format(QUEUE,tier,division)
    responseSize=0
    isContinue=True
    while isContinue:
        response=requests.get(URL,headers=headers)
        while response.status_code!=200:
            time.sleep(5)
            response=requests.get(URL+'?page={}'.format(page),headers=headers)
        users=json.loads(response.text)
        if responseSize==0:
            responseSize=len(users)
        if len(users)<responseSize:
            isContinue=False
        if not os.path.exists('./data'):
            os.mkdir('./data')
        if not os.path.exists('./data/league'):
            os.mkdir('./data/league')
        if os.path.exists('./data/league/{}_{}.csv'.format(tier,division)):
            df=pd.read_csv('./data/league/{}_{}.csv'.format(tier,division),index_col=0)
        else:
            df=pd.DataFrame(columns=list(users[0].keys()))
        for user in users:
            df=df.append(user,ignore_index=True)
        df.to_csv('./data/league/{}_{}.csv'.format(tier,division),encoding='utf-8-sig')
        print('Done: {}_{}_{} ({})'.format(tier,division,page,len(users)))
        page+=1
            
            


if __name__=="__main__":
    #league_challenger()
    #league_grandmaster()
    #league_master()
    for tier in tiers:
        for division in divisions:
            league_other(tier,division)