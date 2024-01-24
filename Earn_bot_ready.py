import json, time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
import getopt
from pandas import *
from datetime import datetime
from datetime import date




webhook_url = 'https://hooks.slack.com/services/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'
webhook_ur_error = 'https://hooks.slack.com/services/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'
def send_slack_message(webhook_url, msg):
    try:
        webhook_url = webhook_url
        slack_data = {"text": msg}

        response = requests.post(
            webhook_url, data=json.dumps(slack_data),
            headers={"Content-Type": "application/json"})

        if response.status_code != 200:
            raise ValueError(
                "Request to slack returned an error %s, the response is:\n%s"
                % (response.status_code, response.text))
    except Exception as e:
        print (e)
            
def send_slack_attachment(webhook_url, title, text):
    try:
        webhook_url = webhook_url
        slack_data = {
            "attachments": [{
                "title": title,
                "text": text,
                "mrkdwn_in": ["text", "pretext"]
            }]
        }

        response = requests.post(
            webhook_url, data=json.dumps(slack_data),
            headers={"Content-Type": "application/json"})

        if response.status_code != 200:
            raise ValueError(
                "Request to slack returned an error %s, the response is:\n%s"
                % (response.status_code, response.text))

    except Exception as e:
        print (e)
        
def title_slack(webhook_url, pretext):
    try:
        webhook_url = webhook_url
        slack_data = {
            "attachments": [{
                "pretext": pretext
            }]
        }

        response = requests.post(
            webhook_url, data=json.dumps(slack_data),
            headers={"Content-Type": "application/json"})

        if response.status_code != 200:
            raise ValueError(
                "Request to slack returned an error %s, the response is:\n%s"
                % (response.status_code, response.text))

    except Exception as e:
        print (e)

        
look_up = ['earn','saving','savings','staking','apy','apr','fixed','fixed saving','fixed savings','flexible','flexible saving','flexible savings','fixe promotion','flexible promotion','fixed staking','fixed staking','flexible staking','flexible staking','stake','dual','dual asset','simple earn','dual investment','delisted','subscribe','remove','earn','Earnings']
file_path = './past_earns.csv'
final = []
record = {'old':[]}
# df = pd.DataFrame(record)
# df.to_csv(file_path, mode='a', header=True)


while True:
    # set everything empty
    final = []
    record = {'old':[]}
        
    ## Kucoin announcements and activities
    try:
        res = {'web':'Kucoin', 'detail': {'Title': [], 'Link': []} }
        response_announcements = requests.get(url = 'https://www.kucoin.com/_api/cms/articles?page=1&pageSize=10&category=announcements&lang=ENG')
        response_activities = requests.get(url = 'https://www.kucoin.com/_api/cms/articles?page=1&pageSize=10&category=activities&lang=ENG')
        j1 = response_announcements.json()
        j2 = response_activities.json()
        jf = j1['items']+j2['items']
        data = read_csv(file_path)
        data = data['old'].tolist()
        for items in jf:
            for i in look_up:
                if i.lower() in items['title'].strip().lower().split():
                    if items['title'] in res['detail']['Title']:
                        continue
                    if items['title'].strip() not in data:
                        res['detail']['Title'].append(items['title'])
                        res['detail']['Link'].append('https://www.kucoin.com/news' + items['path'])
                        record['old'].append(items['title'].strip())
        final.append(res)
        df = pd.DataFrame(record)
        df.to_csv(file_path, mode='a', header=False)
    except Exception as e:
        send_slack_message(webhook_ur_error, str('Earn_bot missed ' + res['web']  + ' ' + str(date.today())) )
        pass

    ## bybit announcements and activities
    try:
        res = {'web':'Bybit', 'detail': {'Title': [], 'Link': []} }
        response_announcements = requests.post(url = 'https://api2.bybit.com/announcements/api/search/v1/index/announcement-posts_en-us')
        j1 = response_announcements.json()
        data = read_csv(file_path)
        data = data['old'].tolist()

        for items in j1['result']['hits']:
            for i in look_up:
                if i.lower() in items['title'].strip().lower().split():
                    if items['title'] in res['detail']['Title']:
                        continue
                    if items['title'].strip() not in data:
                        res['detail']['Title'].append(items['title'])
                        res['detail']['Link'].append('https://announcements.bybit.com/en-US' + items['url'])
                        record['old'].append(items['title'].strip())
        final.append(res)
        df = pd.DataFrame(record)
        df.to_csv(file_path, mode='a', header=False)
    except Exception as e:
        send_slack_message(webhook_ur_error, str('Earn_bot missed ' + res['web']  + ' ' + str(date.today())) )
        pass

    ## Gate.io announcements and activities
    try:
        res = {'web':'Gate', 'detail': {'Title': [], 'Link': []} }
        response_announcements = requests.get(url = 'https://www.gate.io/articlelist/ann/0')
        soup = BeautifulSoup(response_announcements.text, features='html.parser')
        listings = soup.findAll("div", {"class": "article_main flex-max"})[0].findAll("a")[0:12]
        data = read_csv(file_path)
        data = data['old'].tolist()

        for l in listings:
            for i in look_up:
                if i.lower() in l.text.strip().lower().split():
                    if l.text.strip() in res['detail']['Title']:
                        continue
                    if l.text.strip() not in data:
                        res['detail']['Title'].append(l.text.strip())
                        res['detail']['Link'].append("https://www.gate.io" + l.get('href').strip())
                        record['old'].append(l.text.strip())
        final.append(res)
        df = pd.DataFrame(record)
        df.to_csv(file_path, mode='a', header=False)
    except Exception as e:
        send_slack_message(webhook_ur_error, str('Earn_bot missed ' + res['web']  + ' ' + str(date.today())) )
        pass

    ## OKX
    try:
        res = {'web':'OKX', 'detail': {'Title': [], 'Link': []} }
        try:
            response_announcements = requests.get(url = 'https://www.okx.com/help-center/section/announcements-latest-announcements')
            soup = BeautifulSoup(response_announcements.text, features='html.parser')
            listings1 = soup.findAll("div", {"class": "index_list__yJClY"})[0].findAll("a")[0:12]
        except:
            pass

        try:
            response_announcements = requests.get(url = 'https://www.okx.com/help-center/section/announcements-latest-announcements')
            soup = BeautifulSoup(response_announcements.text, features='html.parser')
            listings1 = soup.findAll("div", {"class": "index_listWrap__SlN3t"})[0].findAll("a")[0:12]
        except:
            pass

        try:
            response_announcements = requests.get(url = 'https://www.okx.com/help-center/section/announcements-latest-events')
            soup = BeautifulSoup(response_announcements.text, features='html.parser')
            listings2 = soup.findAll("div", {"class": "index_list__yJClY"})[0].findAll("a")[0:12]
        except:
            pass

        try:
            response_announcements = requests.get(url = 'https://www.okx.com/help-center/section/announcements-latest-events')
            soup = BeautifulSoup(response_announcements.text, features='html.parser')
            listings2 = soup.findAll("div", {"class": "index_listWrap__SlN3t"})[0].findAll("a")[0:12]
        except:
            pass

        try:
            response_announcements = requests.get(url = 'https://www.okx.com/help-center/section/announcements-okx-pool-announcement')
            soup = BeautifulSoup(response_announcements.text, features='html.parser')
            listings3 = soup.findAll("div", {"class": "index_list__yJClY"})[0].findAll("a")[0:12]
        except:
            pass

        try:
            response_announcements = requests.get(url = 'https://www.okx.com/help-center/section/announcements-okx-pool-announcement')
            soup = BeautifulSoup(response_announcements.text, features='html.parser')
            listings3 = soup.findAll("div", {"class": "index_listWrap__SlN3t"})[0].findAll("a")[0:12]
        except:
            pass

        listings = listings1 + listings2 + listings3

        data = read_csv(file_path)
        data = data['old'].tolist()


        for l in listings:
            for i in look_up:
                if i.lower() in l.text.strip().lower().split():
                    if l.text.strip() in res['detail']['Title']:
                        continue
                    if l.text.strip() not in data:
                        res['detail']['Title'].append(l.text.strip())
                        res['detail']['Link'].append("https://www.okx.com" + l.get('href').strip())
                        record['old'].append(l.text.strip())

        final.append(res)
        df = pd.DataFrame(record)
        df.to_csv(file_path, mode='a', header=False)
    except Exception as e:
        send_slack_message(webhook_ur_error, str('Earn_bot missed ' + res['web']  + ' ' + str(date.today())) )
        pass

    ## binance
#     try:
#         res = {'web':'Binance', 'detail': {'Title': [], 'Link': []} }
#         driver = get_driver()
#         driver.get('https://www.binance.com/en/support/announcement/latest-binance-news?c=49&navId=49')
#         time.sleep(3)
#         html = driver.page_source
#         soup = BeautifulSoup(html, features='html.parser')
#         listings1 = soup.findAll("div", {"class": "css-1txs1yu"})[0].findAll("a")[0:10]

#         driver.get('https://www.binance.com/en/support/announcement/latest-activities?c=93&navId=93')
#         time.sleep(3)
#         html = driver.page_source
#         soup = BeautifulSoup(html, features='html.parser')
#         listings2 = soup.findAll("div", {"class": "css-1txs1yu"})[0].findAll("a")[0:10]

#         listings = listings1 + listings2

#         data = read_csv(file_path)
#         data = data['old'].tolist()

#         for l in listings:
#             for i in look_up:
#                 if i.lower() in l.text.strip().strip().lower().split():
#                     if l.text.strip() in res['detail']['Title']:
#                         continue
#                     if l.text.strip() not in data:
#                         res['detail']['Title'].append(l.text.strip())
#                         res['detail']['Link'].append("https://www.binance.com" + l.get('href').strip())
#                         record['old'].append(l.text.strip())
#         final.append(res)
#         try:
#             driver.quit()
#         except:
#             pass
#         df = pd.DataFrame(record)
#         df.to_csv(file_path, mode='a', header=False)
#     except Exception as e:
#         # driver.quit()
#         send_slack_message(webhook_ur_error, str('Earn_bot missed ' + res['web']  + ' ' + str(date.today())) )
#         pass


    ## huobi
    try:
        try:
            res = {'web':'Huobi', 'detail': {'Title': [], 'Link': []} }
            response_announcements = requests.get(url = 'https://www.huobi.com/support/en-us/list/900000179026')
            soup = BeautifulSoup(response_announcements.text, features='html.parser')
            listings1 = soup.findAll("div", {"class": "van-list list"})[0].findAll("a")[0:12]
        except:
            pass


        listing = listings1 

        data = read_csv(file_path)
        data = data['old'].tolist()

        for l in listing:
            for i in look_up:
                if i.lower() in l.text.strip().strip().lower().split():
                    if l.text.strip() in res['detail']['Title']:
                        continue
                    if l.text.strip() not in data:
                        res['detail']['Title'].append(l.text.strip())
                        res['detail']['Link'].append("https://www.huobi.com" + l.get('href').strip())
                        record['old'].append(l.text.strip())
        final.append(res)
        df = pd.DataFrame(record)
        df.to_csv(file_path, mode='a', header=False)
    except Exception as e:
        send_slack_message(webhook_ur_error, str('Earn_bot missed ' + res['web']  + ' ' + str(date.today())) )
        pass

    ## bitget
#     try:
#         res = {'web':'bitget', 'detail': {'Title': [], 'Link': []} }
#         driver = get_driver()
#         driver.get('https://www.bitget.com/support/sections/4413127530649')
#         time.sleep(3)
#         html = driver.page_source
#         soup = BeautifulSoup(html, features='html.parser')
#         listings1 = soup.findAll("div", {"class": "index_actice_main__t9LUP"})[0].findAll("a")[0:10]

#         driver.get('https://www.bitget.com/support/sections/4413154768537')
#         time.sleep(3)
#         html = driver.page_source
#         soup = BeautifulSoup(html, features='html.parser')
#         listings2 = soup.findAll("div", {"class": "index_actice_main__t9LUP"})[0].findAll("a")[0:10]

#         driver.get('https://www.bitget.com/support/sections/360007868532')
#         time.sleep(3)
#         html = driver.page_source
#         soup = BeautifulSoup(html, features='html.parser')
#         listings3 = soup.findAll("div", {"class": "index_actice_main__t9LUP"})[0].findAll("a")[0:10]

#         driver.get('https://www.bitget.com/support/sections/6549920308633')
#         time.sleep(3)
#         html = driver.page_source
#         soup = BeautifulSoup(html, features='html.parser')
#         listings4 = soup.findAll("div", {"class": "index_actice_main__t9LUP"})[0].findAll("a")[0:10]
#         driver.quit()

#         listings = listings1 + listings2 + listings3 + listings4

#         data = read_csv(file_path)
#         data = data['old'].tolist()

#         for l in listings:
#             for i in look_up:
#                 if i in l.text.strip().strip().lower().split():
#                     if l.text.strip() in res['detail']['Title']:
#                         continue
#                     if l.text.strip() not in data:
#                         res['detail']['Title'].append(l.text.strip())
#                         res['detail']['Link'].append("https://www.bitget.com/" + l.get('href').strip())
#                         record['old'].append(l.text.strip())
#         try:
#             driver.quit()
#         except:
#             pass
#         final.append(res)
#         df = pd.DataFrame(record)
#         df.to_csv(file_path, mode='a', header=False)
#     except Exception as e:
#         # driver.quit()
#         send_slack_message(webhook_ur_error, str('Earn_bot missed ' + res['web']  + ' ' + str(date.today())) )
#         pass


    try:
        msg_out = []
        for i in final:
            count = 0 
            msg = {'web':'', 'detail' : ''}
            msg['web'] += i['web']
            for j,k in zip(i['detail']['Title'],i['detail']['Link']):
                count +=1 
                msg['detail'] += (str(count) +'.' + ' ' + "<" + k + "|" + '{:15s}'.format(j) + ">")
                msg['detail'] += ",\t"
                msg['detail'] += '\n'
            msg_out.append(msg)
    except Exception as e:
        send_slack_message(webhook_ur_error, str('Failed to convert to msg_out' + ' ' + str(date.today())) )
        pass

    try:
        title_slack(webhook_url,'Earn_bot')
        lenth = 0
        today = date.today()
        now = datetime.now()
        for i in msg_out:
            lenth += len(i['detail'])

        if lenth == 0:
            send_slack_message(webhook_url,'Nothing Special ' + str(today))
        else:
            for i in msg_out:
                send_slack_attachment(webhook_url,i['web'],i['detail'])
    except Exception as e:
        send_slack_message(webhook_ur_error, str('에러 났다' + ' ' + str(now)))
        pass
    time.sleep(86400)