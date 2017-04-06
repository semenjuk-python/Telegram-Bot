from urllib2 import urlopen
from bs4 import BeautifulSoup

def minfin_get_html():
    headers = {
                '''User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0)
                Gecko/20100101 Firefox/45.0'''
             }
    try:
        html=urlopen('http://minfin.com.ua/currency/').read()
    except ValueError:
        html='We regret but something went wrong...Try later.'
        success=False
    except TypeError:
        html='We regret but something went wrong...Try later.'
        success=False
    else:
        success=True
        html=html[180000:]
        start=html.find('<td class="mfcur-table-cur">')
        end=html.find('<h4 class="mfm-h4 mfcur-news-h">')
        html=html[start:end]
    return html, success

def minfin_init_cash(values):
    numbers=values
    numbers=numbers.split(' ')
    dollar=(numbers[0],numbers[3])
    euro=(numbers[8],numbers[11])
    ruble=(numbers[16],numbers[19])
    return dollar, euro, ruble

def minfin_init_bank(values):
    numbers=values
    numbers=numbers.split(' ')
    dollar=(numbers[50],numbers[51])
    euro=(numbers[54],numbers[55])
    date=(numbers[52],numbers[53])
    return dollar, euro, date

def minfin_parse(html):
    soup=BeautifulSoup(html,'html.parser')
    pure=soup.get_text()
    numbers=str()
    words=str()
    for i in range(len(pure)):
        if pure[i].isalpha() and pure[i+1].isalpha():
            words=words+pure[i]
        elif pure[i].isalpha() and (pure[i+1].isalpha()==False):
            words=words+pure[i]+' '

        if pure[i].isdigit() and pure[i+1].isdigit():
            numbers=numbers+pure[i]
        elif pure[i].isdigit() and (pure[i+1]==',' or pure[i+1]=='.'):
            numbers+=pure[i]+pure[i+1]
            i+=1
        elif pure[i].isdigit() and not pure[i+1].isdigit() and pure[i+1] not in (',','.'):
            numbers=numbers+pure[i]+' '
    l=len(words)-2
    month=str()
    while words[l]!=' ':
        month=words[l]+month
        l-=1
    (dollar_bank, euro_bank, date)=minfin_init_bank(numbers)
    (dollar_cash, euro_cash, ruble_cash)=minfin_init_cash(numbers)
    currencies=(
                dollar_cash,
                euro_cash,
                ruble_cash,
                dollar_bank,
                euro_bank
                )
    return currencies, month, date

from requests import get
from json import loads

def obmenka_parse():
    r=get('https://obmenka.kharkov.ua/api/rates/020016')
    data=loads(r.text)
    full_set=list()
    date=data[0].get('latestRates').get('createdAt')
    date=date.replace('T',' ')
    for i in range(len(data)):
        curr_from=data[i].get('from')
        curr_to=data[i].get('to')
        buy=data[i].get('latestRates').get('wholeBuy')
        sale=data[i].get('latestRates').get('wholeSale')
        full_set.append((curr_from,curr_to,buy,sale))
    return full_set, date
