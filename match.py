from config import *
import pandas as pd
import requests
import os
import time
import json

def matchlist():
    files=os.listdir('./data/summoner')
    for file in files:
        df=pd.read_csv('./data/summoner/{}'.format(file),index_col=0)
        accountIds=df['accountId'].tolist()
        for i,accountId in enumerate(accountIds):
            if os.path.exists('./log/match/list/{}'.format(file)):
                logFile=open('./log/match/list/{}'.format(file),'r')
                logIndex=int(logFile.readline())
                logFile.close()
                if i<logIndex:
                    #print('{}:{} skipped'.format(file,i))
                    continue
            response=requests.get('https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?queue=420&season={}'.format(accountId,SEASON),headers=headers)
            while response.status_code!=200:
                time.sleep(5)
                response=requests.get('https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?queue=420&season={}'.format(accountId,SEASON),headers=headers)
            results=json.loads(response.text)
            if not os.path.exists('./data/match'):
                os.mkdir('./data/match')
            if not os.path.exists('./data/match/list'):
                os.mkdir('./data/match/list')
            if os.path.exists('./data/match/list/{}'.format(file)):
                df2=pd.read_csv('./data/match/list/{}'.format(file),index_col=0)
            else:
                df2=pd.DataFrame(columns=['gameId','season'])
            for result in results['matches']:
                df2=df2.append({'gameId':result['gameId'],'season':result['season']},ignore_index=True)
            df2=df2.drop_duplicates(df2.columns.tolist(),keep='first')
            df2.reset_index(drop=True,inplace=True)
            df2.to_csv('./data/match/list/{}'.format(file),encoding='utf-8-sig')
            if not os.path.exists('./log'):
                os.mkdir('./log')
            if not os.path.exists('./log/match'):
                os.mkdir('./log/match')
            if not os.path.exists('./log/match/list'):
                os.mkdir('./log/match/list')
            logFile=open('./log/match/list/{}'.format(file),'w')
            logFile.write(str(i+1))
            logFile.close()
            print('{}: ({}/{})'.format(file.split('.')[0],i+1,len(accountIds)))

def matches():
    files=os.listdir('./data/match/list')
    for file in files:
        df=pd.read_csv('./data/match/list/{}'.format(file),index_col=0)
        gameIds=df['gameId'].tolist()
        for idx,gameId in enumerate(gameIds):
            if os.path.exists('./log/match/game/{}'.format(file)):
                logFile=open('./log/match/game/{}'.format(file),'r')
                logIndex=int(logFile.readline())
                logFile.close()
                if idx<logIndex:
                    #print('{}:{} skipped'.format(file,i))
                    continue
            URL='https://kr.api.riotgames.com/lol/match/v4/matches/{}'.format(gameId)
            response=requests.get(URL,headers=headers)
            while response.status_code!=200:
                time.sleep(5)
                response=requests.get(URL,headers=headers)
            result=json.loads(response.text)
            if not VERSION in result['gameVersion']:
                if not os.path.exists('./log'):
                    os.mkdir('./log')
                if not os.path.exists('./log/match'):
                    os.mkdir('./log/match')
                if not os.path.exists('./log/match/game'):
                    os.mkdir('./log/match/game')
                logFile=open('./log/match/game/{}'.format(file),'w')
                logFile.write(str(idx+1))
                logFile.close()
                continue
            if not os.path.exists('./data/match/game'):
                os.mkdir('./data/match/game')
            if os.path.exists('./data/match/game/{}'.format(file)):
                df2=pd.read_csv('./data/match/game/{}'.format(file),index_col=0)
            else:
                df2=pd.DataFrame(columns=['AD_championId','SUP_championId','AD_csPerMin','AD_KDA','SUP_KDA','firstDragon','firstTower','AD_DPM','SUP_DPM','AD_CC','SUP_CC','win'])
            team={}
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
                df2=df2.append(team['2'],ignore_index=True)
            df2.to_csv('./data/match/game/{}'.format(file),encoding='utf-8-sig')
            if not os.path.exists('./log'):
                os.mkdir('./log')
            if not os.path.exists('./log/match'):
                os.mkdir('./log/match')
            if not os.path.exists('./log/match/game'):
                os.mkdir('./log/match/game')
            logFile=open('./log/match/game/{}'.format(file),'w')
            logFile.write(str(i+1))
            logFile.close()
            print('{}: ({}/{})'.format(file.split('.')[0],idx+1,len(gameIds)))
        
if __name__=="__main__":
    matchlist()
    #matches()