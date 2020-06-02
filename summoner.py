from config import *
import pandas as pd
import requests
import os
import time
import json
from module import check_path_and_mkdir, read_log, write_log

def summoner_challenger():
    df=pd.read_csv('./data/league/challenger.csv',index_col=0)
    summonerIds=df['summonerId'].tolist()
    URL="https://kr.api.riotgames.com/lol/summoner/v4/summoners"
    for i,summonerId in enumerate(summonerIds):
        if os.path.exists('./log/summoner/challenger.csv'):
            logIndex=read_log('./log/summoner/challenger.csv')
            if i<logIndex:
                continue
        response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
        while response.status_code!=200:
            time.sleep(5)
            response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
        result=json.loads(response.text)
        check_path_and_mkdir('./data/summoner')
        if os.path.exists('./data/summoner/challenger.csv'):
            df2=pd.read_csv('./data/summoner/challenger.csv',index_col=0)
        else:
            df2=pd.DataFrame(columns=list(result.keys()))
        df2=df2.append(result,ignore_index=True)
        df2.to_csv('./data/summoner/challenger.csv',encoding='utf-8-sig')
        check_path_and_mkdir('./log/summoner')
        write_log('./log/summoner/challenger.csv',i+1)
        print('Challenger: ({}/{})'.format(i+1,len(summonerIds)))

def summoner_grandmaster():
    df=pd.read_csv('./data/league/grandmaster.csv',index_col=0)
    summonerIds=df['summonerId'].tolist()
    URL="https://kr.api.riotgames.com/lol/summoner/v4/summoners"
    for i,summonerId in enumerate(summonerIds):
        if os.path.exists('./log/summoner/grandmaster.csv'):
            logIndex=read_log('./log/summoner/grandmaster.csv')
            if i<logIndex:
                continue
        response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
        while response.status_code!=200:
            time.sleep(5)
            response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
        result=json.loads(response.text)
        check_path_and_mkdir('./data/summoner')
        if os.path.exists('./data/summoner/grandmaster.csv'):
            df2=pd.read_csv('./data/summoner/grandmaster.csv',index_col=0)
        else:
            df2=pd.DataFrame(columns=list(result.keys()))
        df2=df2.append(result,ignore_index=True)
        df2.to_csv('./data/summoner/grandmaster.csv',encoding='utf-8-sig')
        check_path_and_mkdir('./log/summoner')
        write_log('./log/summoner/grandmaster.csv',i+1)
        print('Grandmaster: ({}/{})'.format(i+1,len(summonerIds)))

def summoner_master():
    df=pd.read_csv('./data/league/master.csv',index_col=0)
    summonerIds=df['summonerId'].tolist()
    URL="https://kr.api.riotgames.com/lol/summoner/v4/summoners"
    for i,summonerId in enumerate(summonerIds):
        if os.path.exists('./log/summoner/master.csv'):
            logIndex=read_log('./log/summoner/master.csv')
            if i<logIndex:
                continue
        response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
        while response.status_code!=200:
            time.sleep(5)
            response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
        result=json.loads(response.text)
        check_path_and_mkdir('./data/summoner')
        if os.path.exists('./data/summoner/master.csv'):
            df2=pd.read_csv('./data/summoner/master.csv',index_col=0)
        else:
            df2=pd.DataFrame(columns=list(result.keys()))
        df2=df2.append(result,ignore_index=True)
        df2.to_csv('./data/summoner/master.csv',encoding='utf-8-sig')
        check_path_and_mkdir('./log/summoner')
        write_log('./log/summoner/master.csv',i+1)
        print('Master: ({}/{})'.format(i+1,len(summonerIds)))

def summoner_other():
    files=os.listdir('./data/league')
    for file in files:
        if file in ['challenger.csv','grandmaster.csv','master.csv']:
            continue
        else:
            df=pd.read_csv('./data/league/{}'.format(file),index_col=0)
            summonerIds=df['summonerId'].tolist()
            URL="https://kr.api.riotgames.com/lol/summoner/v4/summoners"
            for i,summonerId in enumerate(summonerIds):
                if os.path.exists('./log/summoner/{}'.format(file)):
                    logIndex=read_log('./log/summoner/{}'.format(file))
                    if i<logIndex:
                        continue
                response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
                while response.status_code!=200:
                    time.sleep(5)
                    response=requests.get(URL+'/{}'.format(summonerId),headers=headers)
                result=json.loads(response.text)
                check_path_and_mkdir('./data/summoner')
                if os.path.exists('./data/summoner/{}'.format(file)):
                    df2=pd.read_csv('./data/summoner/{}'.format(file),index_col=0)
                else:
                    df2=pd.DataFrame(columns=list(result.keys()))
                df2=df2.append(result,ignore_index=True)
                df2.to_csv('./data/summoner/{}'.format(file),encoding='utf-8-sig')
                check_path_and_mkdir('./log/summoner')
                write_log('./log/summoner/{}'.format(file),i+1)
                print('{}: ({}/{})'.format(file.split('.')[0],i+1,len(summonerIds)))

def deleteDuplicate():
    files=os.listdir('./data/summoner')
    for file in files:
        df=pd.read_csv('./data/summoner/'+file,index_col=0)
        df=df.drop_duplicates(df.columns.tolist(),keep="first")
        df.reset_index(drop=True,inplace=True)
        df.to_csv('./data/summoner/'+file,encoding='utf-8-sig')   

if __name__=="__main__":
    summoner_challenger()
    summoner_grandmaster()
    summoner_master()
    summoner_other()
    deleteDuplicate()
