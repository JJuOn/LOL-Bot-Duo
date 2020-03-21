from config import *
import pandas as pd
import requests
import os
import time
import json

def summoner_challenger():
    df=pd.read_csv('./data/league/challenger.csv',index_col=0)
    summonerIds=df['summonerId'].tolist()
    URL="https://kr.api.riotgames.com/lol/summoner/v4/summoners"
    for i,summonerId in enumerate(summonerIds):
        response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
        while response.status_code!=200:
            time.sleep(5)
            response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
        result=json.loads(response.text)
        if not os.path.exists('./data'):
            os.mkdir('./data')
        if not os.path.exists('./data/summoner'):
            os.mkdir('./data/summoner')
        if os.path.exists('./data/summoner/challenger.csv'):
            df2=pd.read_csv('./data/summoner/challenger.csv',index_col=0)
        else:
            df2=pd.DataFrame(columns=list(result.keys()))
        df2=df2.append(result,ignore_index=True)
        df2.to_csv('./data/summoner/challenger.csv',encoding='utf-8-sig')
        print('Challenger: ({}/{})'.format(i+1,len(summonerIds)))

def summoner_grandmaster():
    df=pd.read_csv('./data/league/grandmaster.csv',index_col=0)
    summonerIds=df['summonerId'].tolist()
    URL="https://kr.api.riotgames.com/lol/summoner/v4/summoners"
    for i,summonerId in enumerate(summonerIds):
        response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
        while response.status_code!=200:
            time.sleep(5)
            response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
        result=json.loads(response.text)
        if not os.path.exists('./data'):
            os.mkdir('./data')
        if not os.path.exists('./data/summoner'):
            os.mkdir('./data/summoner')
        if os.path.exists('./data/summoner/grandmaster.csv'):
            df2=pd.read_csv('./data/summoner/grandmaster.csv',index_col=0)
        else:
            df2=pd.DataFrame(columns=list(result.keys()))
        df2=df2.append(result,ignore_index=True)
        df2.to_csv('./data/summoner/grandmaster.csv',encoding='utf-8-sig')
        print('Grandmaster: ({}/{})'.format(i+1,len(summonerIds)))

def summoner_master():
    df=pd.read_csv('./data/league/master.csv',index_col=0)
    summonerIds=df['summonerId'].tolist()
    URL="https://kr.api.riotgames.com/lol/summoner/v4/summoners"
    for i,summonerId in enumerate(summonerIds):
        response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
        while response.status_code!=200:
            time.sleep(5)
            response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
        result=json.loads(response.text)
        if not os.path.exists('./data'):
            os.mkdir('./data')
        if not os.path.exists('./data/summoner'):
            os.mkdir('./data/summoner')
        if os.path.exists('./data/summoner/master.csv'):
            df2=pd.read_csv('./data/summoner/master.csv',index_col=0)
        else:
            df2=pd.DataFrame(columns=list(result.keys()))
        df2=df2.append(result,ignore_index=True)
        df2.to_csv('./data/summoner/master.csv',encoding='utf-8-sig')
        print('Master: ({}/{})'.format(i+1,len(summonerIds)))

def summoner_other():
    files=os.listdir('./data/league')
    for file in files:
        if file in ['challenger.csv','grandmaster.csv','master.csv']:
            continue
        else:
            df=pd.read_csv('./data/league/'+file,index_col=0)
            summonerIds=df['summonerId'].tolist()
            URL="https://kr.api.riotgames.com/lol/summoner/v4/summoners"
            for i,summonerId in enumerate(summonerIds):
                response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
                while response.status_code!=200:
                    print(response.status_code)
                    time.sleep(5)
                    response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
                result=json.loads(response.text)
                if not os.path.exists('./data'):
                    os.mkdir('./data')
                if not os.path.exists('./data/summoner'):
                    os.mkdir('./data/summoner')
                if os.path.exists('./data/summoner/{}'.format(file)):
                    df2=pd.read_csv('./data/summoner/{}'.format(file),index_col=0)
                else:
                    df2=pd.DataFrame(columns=list(result.keys()))
                df2=df2.append(result,ignore_index=True)
                df2.to_csv('./data/summoner/{}'.format(file),encoding='utf-8-sig')
                print('{}: ({}/{})'.format(file.split('.')[0],i+1,len(summonerIds)))

if __name__=="__main__":
    #summoner_challenger()
    #summoner_grandmaster()
    #summoner_master()
    summoner_other()