import requests
import re

def getJSessionId(str):
    try:
        # jsessionid is 73 characters long
        r = re.compile(';jsessionid=(.{73}?)\?')
        m = r.search(str)
        id = m.group(1)
    except:
        id = False

    return id

def getWicketPage(str):
    try:
        # page no is 1-3 characters long.. I think
        r = re.compile('/wicket/page\?(\d{1,3}?)$')
        m = r.search(str)
        no = m.group(1)
    except:
        no = False

    return no


config = {
    'baseUrl': 'https://www.migrationsverket.se/ansokanbokning',
    'formPath': '/valjtyp',
    'officeCodes': {
        'new_york': 'U0766',
        'washington_dc': 'U1075'
    }
}

officeCode = config['officeCodes']['washington_dc']
reqQs = { 'enhet': officeCode }

#### Init and get jsessionid ####
reqUrl = "{}{}".format(config['baseUrl'], config['formPath'])
r = requests.get(reqUrl, params = reqQs)
jSessionId = getJSessionId(r.url)
refererUrl = r.url

reqCookies = {
    'JSESSIONID': jSessionId
}
#### End Init ####

#### Form selection 1 (selects passport appointment type) ####
reqData = {
    'viseringstyp.border:viseringstyp.border_body:viseringstyp': 6
}

reqHeaders = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT': '1',
    'Origin': 'https://www.migrationsverket.se',
    'Referer': refererUrl,
    'Wicket-Ajax': 'true',
    'Wicket-Ajax-BaseURL': 'valjtyp?0&amp;enhet=' + officeCode,
    'Wicket-FocusedElementId': 'viseringstyp',
    'X-Requested-With': 'XMLHttpRequest'
}

reqQF1 = '0-1.IBehaviorListener.0-form-viseringstyp.border-viseringstyp.border_body-viseringstyp'
reqUrl = config['baseUrl'] + config['formPath'] + ';jsessionid=' + jSessionId + '?' + reqQF1
r = requests.post(
    reqUrl,
    params = reqQs,
    data = reqData,
    cookies = reqCookies,
    headers = reqHeaders
)
#### End Form selection 1 ####

#### Form selection 2 (selects number of people) ####
reqData = {
    'antalsokande.border:antalsokande.border_body:antalsokande': 0
}

reqHeaders = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT': '1',
    'Origin': 'https://www.migrationsverket.se',
    'Referer': refererUrl,
    'Sec-Fetch-Dest':'empty',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Site':'same-origin',
    'Wicket-Ajax': 'true',
    'Wicket-Ajax-BaseURL': 'valjtyp?0&amp;enhet=' + officeCode,
    'Wicket-FocusedElementId': 'antalpersoner',
    'X-Requested-With': 'XMLHttpRequest'
}

reqQF2 = '0-1.IBehaviorListener.0-form-antalsokande.border-antalsokande.border_body-antalsokande'
reqUrl = config['baseUrl'] + config['formPath'] + '?' + reqQF2
r = requests.post(
    reqUrl,
    params = reqQs,
    data = reqData,
    cookies = reqCookies,
    headers = reqHeaders
)
#### End Form selection 2 ####

#### Form submit ####
reqData = {
    'id2_hf_0': '',
    'viseringstyp.border:viseringstyp.border_body:viseringstyp': 6,
    'antalsokande.border:antalsokande.border_body:antalsokande': 0,
    'fortsatt': 'Next'
}

reqHeaders = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'www.migrationsverket.se',
    'DNT': '1',
    'Referer': refererUrl,
    'Origin': 'https://www.migrationsverket.se'
}

reqUrl = config['baseUrl'] + config['formPath'] + '?0-1.IFormSubmitListener-form'
r = requests.post(
    reqUrl,
    params = reqQs,
    data = reqData,
    cookies = reqCookies,
    headers = reqHeaders,
    allow_redirects = False
)
#### End Form submit ####

#### Get available slots ####
wicketPage = getWicketPage(r.headers['Location'])

reqHeaders = {
    'DNT': '1',
    'Referer': refererUrl,
    'Origin': 'https://www.migrationsverket.se',
    'Wicket-Ajax': 'true',
    'Wicket-Ajax-BaseURL': 'wicket/page?' + wicketPage
}

reqQs = {
    'start': '2020-10-23T00:00:00+00:00',
    'end': '2020-03-30T00:00:00+00:00'
}

reqUrl = config['baseUrl'] +'/wicket/page?' + wicketPage + '-1.IBehaviorListener.1-form-kalender-kalender'
r = requests.post(
    reqUrl,
    params = reqQs,
    cookies = reqCookies,
    headers = reqHeaders,
    allow_redirects = False
)

#### End Get available slots ####

print(r.text)
