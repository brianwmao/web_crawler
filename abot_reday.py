import json, time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
import getopt
from pandas import *
from datetime import datetime
from datetime import date
from lookupwords import words



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

look_up = ['token swap','contract swap','contract upgrade','upgrade the contract','smart contract migration','attack','attacked','the token ticker will remain unchanged','hack','hacked','suspension','suspend','compromised', 'revised']
coin_list = words
final = []
record = {'old':[]}
file_path = './alignment_past.csv'
# df = pd.DataFrame(record)
# df.to_csv(file_path, mode='a', header=True)


while True:
    # set everything empty
    final = []
    record = {'old':[]}
    try:
        response = requests.get(
                url = 'https://www.kucoin.com/_api/cms/articles?category=others&lang=en_US&page=1&pageSize=10'
        )
        j = response.json()
        res = {'web':'Kucoin', 'detail': {'Title': [], 'Link': []} }
        data = read_csv(file_path)
        data = data['old'].tolist()

        for items in j['items'][0:10]:
            for i in look_up:
                if i.lower() in items['title'].lower().split():
                    for j in [x.lower() for x in coin_list]:
                        if j.lower() in items['title'].lower().split():
                            if items['title'] in res['detail']['Title']:
                                continue
                            if items['title'] not in data:
                                res['detail']['Title'].append(items['title'])
                                res['detail']['Link'].append('https://www.kucoin.com/news' + items['path'])
                                record['old'].append(items['title'])
        df = pd.DataFrame(record)
        df.to_csv(file_path, mode='a', header=False)
        final.append(res)
    except Exception as e:
        send_slack_message(webhook_ur_error, str('Margin_bot missed ' + res['web']  + ' ' + str(date.today())) )
        pass

    # Huobi
    try:
        res = {'web':'Huobi', 'detail': {'Title': [], 'Link': []} }
        response_activities = requests.get(url = 'https://www.huobi.com/support/en-us/list/360000039982')
        soup = BeautifulSoup(response_activities.text, features='html.parser')
        listings = soup.findAll("div", {"class": "van-list list"})[0].findAll("a")
        data = read_csv(file_path)
        data = data['old'].tolist()
        for l in listings:
            for i in look_up:
                if i in l.text.strip().lower():
                    for j in [x.lower() for x in coin_list]:
                        if j.lower() in l.text.strip().lower().split():
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

    # Binance
    # try:
    #     res = {'web':'Binance', 'detail': {'Title': [], 'Link': []} }
    #     driver = get_driver()
    #     driver.get('https://www.binance.com/en/support/announcement/latest-binance-news?c=49&navId=49')
    #     time.sleep(3)
    #     html = driver.page_source
    #     soup = BeautifulSoup(html, features='html.parser')
    #     listings = soup.findAll("div", {"class": "css-1q4wrpt"})[0].findAll("a")
    #     res = {'web':'Binance', 'detail': {'Title': [], 'Link': []} }
    #     data = read_csv(file_path)
    #     data = data['old'].tolist()
    #     for l in listings:
    #         for i in look_up:
    #             if i in l.text.strip().lower():
    #                 for j in [x.lower() for x in coin_list]:
    #                     if j.lower() in l.text.strip().lower().split():
    #                         if l.text.strip() in res['detail']['Title']:
    #                             continue
    #                         if l.text.strip() not in data:
    #                             res['detail']['Title'].append(l.text.strip())
    #                             res['detail']['Link'].append("https://www.binance.com" + l.get('href').strip())
    #                             record['old'].append(l.text.strip())
    #     final.append(res)
    #     df = pd.DataFrame(record)
    #     df.to_csv(file_path, mode='a', header=False)
    # except Exception as e:
    #     send_slack_message(webhook_ur_error, str('Earn_bot missed ' + res['web']  + ' ' + str(date.today())) )
    #     pass

    # OKX



    # Gate
    try:
        res = {'web':'Gate', 'detail': {'Title': [], 'Link': []} }
        response_announcements = requests.get(url = 'https://www.gate.io/articlelist/ann/0')
        soup = BeautifulSoup(response_announcements.text, features='html.parser')
        listings = soup.findAll("div", {"class": "article_main flex-max"})[0].findAll("a")[0:12]
        data = read_csv(file_path)
        data = data['old'].tolist()
        # listing_new 
        res = {'web':'GATE', 'detail': {'Title': [], 'Link': []} }
        for l in listings:
            for i in look_up:
                if i in l.text.strip().lower():
                    for j in [x.lower() for x in coin_list]:
                        if j.lower() in l.text.strip().lower().split():
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

    # mexc
    try:
        response = requests.get(
                url = 'https://www.mexc.com/help/announce/api/en-US/section/15425930840733/articles?page=1&perPage=20'
        )
        j = response.json()
        res = {'web':'Mexc', 'detail': {'Title': [], 'Link': []} }
        data = read_csv(file_path)
        data = data['old'].tolist()

        for items in j['data']['results'][0:10]:
            for i in look_up:
                if i.lower() in items['title'].lower().split():
                    for j in [x.lower() for x in coin_list]:
                        if j.lower() in items['title'].lower().split():
                            if items['title'] in res['detail']['Title']:
                                continue
                            if items['title'] not in data:
                                res['detail']['Title'].append(items['title'])
                                res['detail']['Link'].append('https://www.mexc.com/support/articles/' + str(items['id']))
                                record['old'].append(items['title'])
        df = pd.DataFrame(record)
        df.to_csv(file_path, mode='a', header=False)
        final.append(res)
    except Exception as e:
        send_slack_message(webhook_ur_error, str('Earn_bot missed ' + res['web']  + ' ' + str(date.today())) )
        pass

    #convert to slack msg
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
        title_slack(webhook_url,'Alignment_listing_bot')
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
    # gc authorize
    except Exception as e:
        pass
    time.sleep(86400)