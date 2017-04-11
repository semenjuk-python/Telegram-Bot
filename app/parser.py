from urllib2 import urlopen
from bs4 import BeautifulSoup

def minfin_get_html():
    headers = {
                '''User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0)
                Gecko/20100101 Firefox/45.0'''
             }
    try:
        htmlcash=urlopen('http://minfin.com.ua/currency/').read()
        htmlbank=urlopen('http://minfin.com.ua/currency/mb/').read()

    except ValueError:
        html='We regret but something went wrong...Try later.'
        success=False
    except TypeError:
        html='We regret but something went wrong...Try later.'
        success=False
    else:
        success=True
        htmlcash=htmlcash[180000:]
        start=htmlcash.find('<td class="mfcur-table-cur">')
        end=htmlcash.find('<h4 class="mfm-h4 mfcur-news-h">')
        htmlcash=htmlcash[start:end]
    return htmlcash, success, htmlbank

def minfin_init_cash(values):
    numbers=values
    numbers=numbers.split(' ')
    dollar=(numbers[0],numbers[3])
    euro=(numbers[8],numbers[11])
    ruble=(numbers[16],numbers[19])
    return dollar, euro, ruble

def minfin_init_bank(htmlbank):
    start=htmlbank.find('<table class="mb-table-currency">')
    end=htmlbank.find('<div class="mb-interbank-graph--body">')
    htmlbank=htmlbank[start:end]
    soup=BeautifulSoup(htmlbank,'html.parser')
    pure=soup.get_text()
    numbers=str()
    for i in range(len(pure)):
        if pure[i].isdigit() and pure[i+1].isdigit():
            numbers=numbers+pure[i]
        elif pure[i].isdigit() and (pure[i+1]==',' or pure[i+1]=='.'):
            numbers+=pure[i]+pure[i+1]
            i+=1
        elif pure[i].isdigit() and not pure[i+1].isdigit() and pure[i+1] not in (',','.'):
            numbers=numbers+pure[i]+' '
    numbers=numbers.split(' ')
    dollar=(numbers[0],numbers[6])
    euro=(numbers[2],numbers[8])
    ruble=(numbers[4],numbers[10])
    return dollar, euro, ruble

def minfin_parse(htmlcash,htmlbank):
    soup=BeautifulSoup(htmlcash,'html.parser')
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

    (dollar_bank, euro_bank, ruble_bank)=minfin_init_bank(htmlbank)
    (dollar_cash, euro_cash, ruble_cash)=minfin_init_cash(numbers)
    currencies=(
                dollar_cash,
                euro_cash,
                ruble_cash,
                dollar_bank,
                euro_bank,
                ruble_bank
                )
    return currencies

from requests import get
from json import loads
from requests.exceptions import ConnectionError

def obmenka_parse():
    try:
        r=get('https://obmenka.kharkov.ua/api/rates/020016')
        data=loads(r.text)
    except ValueError:
        full_set=None
        date=None
        return full_set, date

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
