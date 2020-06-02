from config import *
import pandas as pd
import requests
import os
import time
import json
from module import check_path_and_mkdir, read_log, write_log

def matchlist():
    files=os.listdir('./data/summoner')
    for file in files:
        df=pd.read_csv('./data/summoner/{}'.format(file),index_col=0)
        accountIds=df['accountId'].tolist()
        for i,accountId in enumerate(accountIds):
            if os.path.exists('./log/match/list/{}'.format(file)):
                logIndex=read_log('./log/match/list/{}'.format(file))
                if i<logIndex:
                    #print('{}:{} skipped'.format(file,i))
                    continue
            response=requests.get('https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?queue=420&season={}'.format(accountId,SEASON),headers=headers)
            while response.status_code!=200:
                time.sleep(5)
                response=requests.get('https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?queue=420&season={}'.format(accountId,SEASON),headers=headers)
            results=json.loads(response.text)
            check_path_and_mkdir('./data/match/list')
            if os.path.exists('./data/match/list/{}'.format(file)):
                df2=pd.read_csv('./data/match/list/{}'.format(file),index_col=0)
            else:
                df2=pd.DataFrame(columns=['gameId','season'])
            for result in results['matches']:
                df2=df2.append({'gameId':result['gameId'],'season':result['season']},ignore_index=True)
            df2=df2.drop_duplicates(df2.columns.tolist(),keep='first')
            df2.reset_index(drop=True,inplace=True)
            df2.to_csv('./data/match/list/{}'.format(file),encoding='utf-8-sig')
            check_path_and_mkdir('./log/match/list')
            write_log('./log/match/list/{}'.format(file),i+1)
            print('{}: ({}/{})'.format(file.split('.')[0],i+1,len(accountIds)))

def matches():
    files=os.listdir('./data/match/list')
    for file in files:
        df=pd.read_csv('./data/match/list/{}'.format(file),index_col=0)
        df=df.sort_values(by=['gameId'],axis=0,ascending=False)
        gameIds=df['gameId'].tolist()
        for idx,gameId in enumerate(gameIds):
            if os.path.exists('./log/match/game/{}'.format(file)):
                logIndex=read_log('./log/match/game/{}'.format(file))
                if idx<logIndex:
                    #print('{}:{} skipped'.format(file,i))
                    continue
            URL='https://kr.api.riotgames.com/lol/match/v4/matches/{}'.format(gameId)
            response=requests.get(URL,headers=headers)
            while response.status_code!=200:
                #print(response.status_code)
                time.sleep(5)
                response=requests.get(URL,headers=headers)
            result=json.loads(response.text)
            if (int(VERSION.split('.')[0]) > int(result['gameVersion'].split('.')[0])) or ((int(VERSION.split('.')[0])==int(result['gameVersion'].split('.')[0])) and int(VERSION.split('.')[1])>int(result['gameVersion'].split('.')[1])):
                if not os.path.exists('./log'):
                    os.mkdir('./log')
                if not os.path.exists('./log/match'):
                    os.mkdir('./log/match')
                if not os.path.exists('./log/match/game'):
                    os.mkdir('./log/match/game')
                write_log('./log/match/game/{}'.format(file),idx+1)
                #print('SKIP: Old Version!!')
                break
            if not VERSION in result['gameVersion']:
                check_path_and_mkdir('./log/match/game')
                write_log('./log/match/game/{}'.format(file),idx+1)
                continue
            check_path_and_mkdir('./data/match/game')
            if os.path.exists('./data/match/game/{}'.format(file)):
                df2=pd.read_csv('./data/match/game/{}'.format(file),index_col=0)
            else:
                df2=pd.DataFrame(columns=['AD_championId','SUP_championId','AD_csPerMin','AD_KDA','SUP_KDA','firstDragon','firstTower','AD_DPM','SUP_DPM','AD_CC','SUP_CC','win'])
            team={}
            try:
                team['1']={'firstDragon':1 if result['teams'][0]['firstDragon'] else 0,'win':1 if result['teams'][0]['win']=="Win" else 0}
                team['2']={'firstDragon':1 if result['teams'][1]['firstDragon'] else 0,'win':1 if result['teams'][1]['win']=="Win" else 0}
                FTFlag=False
                for i in range(0,10):
                    if result['participants'][i]['timeline']['role']=='DUO_CARRY':
                        team['{}'.format(i//5+1)]['AD_csPerMin']=round(result['participants'][i]['stats']['totalMinionsKilled']/result['gameDuration']*60,1)
                        team['{}'.format(i//5+1)]['AD_DPM']=result['participants'][i]['stats']['totalDamageDealtToChampions']//result['gameDuration']*60
                        try:
                            team['{}'.format(i//5+1)]['AD_KDA']=round((result['participants'][i]['stats']['kills']+result['participants'][i]['stats']['assists'])/result['participants'][i]['stats']['deaths'],2)
                        except ZeroDivisionError:
                            team['{}'.format(i//5+1)]['AD_KDA']=round((result['participants'][i]['stats']['kills']+result['participants'][i]['stats']['assists'])/1,2)
                        team['{}'.format(i//5+1)]['AD_CC']=result['participants'][i]['stats']['totalTimeCrowdControlDealt']
                        team['{}'.format(i//5+1)]['AD_championId']=result['participants'][i]['championId']
                        if result['participants'][i]['stats']['firstTowerKill'] or result['participants'][i]['stats']['firstTowerAssist']:
                            FTFlag=True
                    elif result['participants'][i]['timeline']['role']=='DUO_SUPPORT':
                        team['{}'.format(i//5+1)]['SUP_DPM']=result['participants'][i]['stats']['totalDamageDealtToChampions']//result['gameDuration']*60
                        try:
                            team['{}'.format(i//5+1)]['SUP_KDA']=round((result['participants'][i]['stats']['kills']+result['participants'][i]['stats']['assists'])/result['participants'][i]['stats']['deaths'],2)
                        except ZeroDivisionError:
                            team['{}'.format(i//5+1)]['SUP_KDA']=round((result['participants'][i]['stats']['kills']+result['participants'][i]['stats']['assists'])/1,2)
                        team['{}'.format(i//5+1)]['SUP_CC']=result['participants'][i]['stats']['totalTimeCrowdControlDealt']
                        team['{}'.format(i//5+1)]['SUP_championId']=result['participants'][i]['championId']
                        if result['participants'][i]['stats']['firstTowerKill'] or result['participants'][i]['stats']['firstTowerAssist']:
                            FTFlag=True
                    if i==4 or i==9:
                        if FTFlag:
                            team['{}'.format(i//5+1)]['firstTower']=1
                        else:
                            team['{}'.format(i//5+1)]['firstTower']=0
                        FTFlag=False
                if 'AD_championId' in list(team['1'].keys()):
                    df2=df2.append(team['1'],ignore_index=True)
                if 'AD_championId' in list(team['2'].keys()):
                    df2=df2.append(team['2'],ignore_index=True)
                df2.to_csv('./data/match/game/{}'.format(file),encoding='utf-8-sig')
                check_path_and_mkdir('./log/match/game')
                write_log('./log/match/game/{}'.format(file),idx+1)
                print('{}: ({}/{})'.format(file.split('.')[0],idx+1,len(gameIds)))
            except KeyError:
                check_path_and_mkdir('./log/match/game')
                write_log('./log/match/game/{}'.format(file),idx+1)
                continue
        
if __name__=="__main__":
    #matchlist()
    matches()