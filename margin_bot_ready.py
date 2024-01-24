import requests
import json, time
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
from datetime import date
from pandas import *
import time


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
words_lookup = ['margin','margin trading','cross margin','isolated margin','margin ratio','trading pairs','margin pairs','cross margin pairs','isolated margin pairs','super week', 'isolated margin']
final = []
record = {'old':[]}
file_path = './margin_past.csv'
# df = pd.DataFrame(record)
# df.to_csv(file_path, mode='a', header=True)



while True:
    # set everything empty
    final = []
    record = {'old':[]}
    ## MEXC
    try:
        response = requests.get(
                url = 'https://www.mexc.com/help/announce/api/en-US/section/15425930840735/articles?page=1&perPage=20'
        )
        j = response.json()
        res = {'web':'Mexc', 'detail': {'Title': [], 'Link': []} }
        data = read_csv(file_path)
        data = data['old'].tolist()

        for items in j['data']['results'][0:20]:
            for i in words_lookup:
                if i.lower() in items['title'].lower():
                    if items['title'] in res['detail']['Title']:
                        continue
                    if items['title'].strip() not in data:
                        res['detail']['Title'].append(items['title'])
                        res['detail']['Link'].append('https://www.mexc.com/support/articles/' + str(items['id']))
                        record['old'].append(items['title'].strip())
        final.append(res)
        df = pd.DataFrame(record)
        df.to_csv(file_path, mode='a', header=False)
    except Exception as e:
        send_slack_message(webhook_ur_error, str('Margin_bot missed ' + res['web']  + ' ' + str(date.today())) )
        pass

    ## Huobi
    try:
        res = {'web':'Huobi', 'detail': {'Title': [], 'Link': []} }
        response_announcements = requests.get(url = 'https://www.htx.com/support/en-us/list/900000741690')
        soup = BeautifulSoup(response_announcements.text, features='html.parser')
        listings = soup.findAll("dl", {"class": "list"})[0].findAll("a")[0:10]
        data = read_csv(file_path)
        data = data['old'].tolist()

        for l in listings:
            for i in words_lookup:
                if i in l.text.strip().lower():
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

    ## Binance
#     try:
#         res = {'web':'Binance', 'detail': {'Title': [], 'Link': []} }
#         driver = get_driver()
#         driver.get('https://www.binance.com/en/support/announcement/c-48?navId=48')
#         time.sleep(3)
#         html = driver.page_source
#         soup = BeautifulSoup(html, features='html.parser')
#         listingss = soup.findAll("div", {"class": "css-1txs1yu"})[0].findAll("a")[0:10]

#         data = read_csv(file_path)
#         data = data['old'].tolist()

#         for l in listings:
#             for i in words_lookup:
#                 if i in l.text.strip().lower():
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
#         send_slack_message(webhook_ur_error, str('Earn_bot missed ' + res['web']  + ' ' + str(date.today())) )
#         pass

    ## OKX
    try:
        res = {'web':'OKX', 'detail': {'Title': [], 'Link': []} }
        try:
            response_announcements = requests.get(url = 'https://www.okx.com/help-center/section/announcements-spot-margin-trading')
            soup = BeautifulSoup(response_announcements.text, features='html.parser')
            listings = soup.findAll("div", {"class": "index_listWrap__SlN3t"})[0].findAll("a")[0:12]
        except:
            pass

        try:
            response_announcements = requests.get(url = 'https://www.okx.com/help-center/section/announcements-spot-margin-trading')
            soup = BeautifulSoup(response_announcements.text, features='html.parser')
            listings = soup.findAll("div", {"class": "index_list__yJClY"})[0].findAll("a")[0:12]
        except:
            pass

        data = read_csv(file_path)
        data = data['old'].tolist()


        for l in listings:
            for i in words_lookup:
                if i in l.text.strip().lower():
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

    ## Gate
    try:
        res = {'web':'Gate', 'detail': {'Title': [], 'Link': []} }
        response_announcements = requests.get(url = 'https://www.gate.io/articlelist/ann')
        soup = BeautifulSoup(response_announcements.text, features='html.parser')
        listings = soup.findAll("div", {"class": "article_main flex-max"})[0].findAll("a")[0:12]
        data = read_csv(file_path)
        data = data['old'].tolist()

        for l in listings:
            for i in words_lookup:
                if i in l.text.strip().lower():
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

    ## Bybit
    try:
        res = {'web':'Bybit', 'detail': {'Title': [], 'Link': []} }
        response_announcements = requests.post(url = 'https://api2.bybit.com/announcements/api/search/v1/index/announcement-posts_en')
        j1 = response_announcements.json()
        data = read_csv(file_path)
        data = data['old'].tolist()

        for items in j1['result']['hits']:
            for i in words_lookup:
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

    # Kucoin
    try:
        response = requests.get(
                url = 'https://www.kucoin.com/_api/cms/articles?page=1&pageSize=20&category=announcements&lang=ENG'
        )
        j = response.json()
        res = {'web':'Kucoin', 'detail': {'Title': [], 'Link': []} }
        data = read_csv(file_path)
        data = data['old'].tolist()

        for items in j['items'][0:20]:
            for i in words_lookup:
                if i.lower() in items['title'].lower():
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
        title_slack(webhook_url,'Margin_listing_bot')
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