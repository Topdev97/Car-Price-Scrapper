import pygsheets
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from fp.fp import FreeProxy


SERVICE_FILE = "google_sheet_auth.json"
# SHEET_NAME = "https://docs.google.com/spreadsheets/d/1Qvoee1K5DCJiQCkelZ0L7MQUBV__i9XHQa_3z9IOuA8/edit#gid=0"
SHEET_NAME = "https://docs.google.com/spreadsheets/d/1tyO3xXHcxg1XFxNPKb7m24QdtXnd-ZcA8bRlFloctbA/edit#gid=0"

CRITERIES_TABLE = "SearchCriteriaAll"
KIJIJI_AUTO_TABLE = "KijijiAutoAll"
AUTO_TRADE_TABLE = "AutoTraderAll"

def send_mail(source, mail_text):
    # msg = MIMEMultipart()
    print(f'trying to send mail')
    # pwd = 'lwnz frol gvfa yiqh'
    pwd = 'nyqz ybhz hmqu cqrv'
    msg = EmailMessage()
    # msg['From'] = 'searchautobot.ca@gmail.com'
    msg['From'] = 'akwork099@gmail.com'
    # msg['To'] = 'searchautobot.ca@gmail.com'
    msg['To'] = 'akwork099@gmail.com'
    msg['Subject'] = source + 'Newest listings'
    
    
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    print('before ttls')
    server.starttls()
    print('after ttls')
    server.login(msg['From'], pwd)

    print('after login')
    # msg.attach(MIMEText(mail_text, 'plain'))
    # server.sendmail(msg['From'], msg['To'], msg.as_string())
    msg.set_content(mail_text)
    server.send_message(msg)
    print(f'Mail was send to {msg["To"]}')
    server.quit()


def auth_to_sheet():
    gc = pygsheets.authorize(service_file=SERVICE_FILE)
    sh = gc.open_by_url(SHEET_NAME)
    return sh


def get_proxy():
    """
    host = "hub.zenscrape.com"
    port = "31112"
    username = "81ztb0hcg6er357"
    password = "UlaniAt2YrbGYpbV"
    country_param = "_country-Canada"
    http_proxy = f"http://{username}:{password}{country_param}@{host}:{port}"
    """

    print('Before getting free proxy')
    http_proxy = FreeProxy().get()
    http_proxy = FreeProxy(country_id=['US', 'CA']).get()
    http_proxy = FreeProxy(country_id=['US']).get()
    http_proxy = FreeProxy(country_id=['CA']).get()
    http_proxy = FreeProxy(timeout=1).get()
    http_proxy = FreeProxy(rand=True).get()
    http_proxy = FreeProxy(anonym=True).get()
    http_proxy = FreeProxy(elite=True).get()
    http_proxy = FreeProxy(google=True).get()
    http_proxy = FreeProxy(https=True).get()
    http_proxy = FreeProxy(country_id=['US', 'BR'], timeout=0.3, rand=True).get()    
    print('After getting free proxy')
    proxy_dict = {
        "http": http_proxy #,
        #"https": http_proxy
    }
    return proxy_dict


def random_useragent():
    desktop_agents = \
        ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36']
    agent = random.choice(desktop_agents)
    return agent


HEADERS = {
    'authority': 'www.autotrader.ca',
    'method': 'GET',
    # 'path': '/cars/ram/1500/on/milton/?rcp=15&rcs=0&srt=3&yRng=2015%2C2019&prx=500&prv=Ontario&loc=L9T0B3&kwd=SPORT&hprc=True&wcp=True&sts=Used&adtype=Private&showcpo=1&inMarket=advancedSearch',
    'scheme': 'https',
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,pl-PL;q=0.6,pl;q=0.5,en-US;q=0.4',
    'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': random_useragent()
}

KJ_HEADERS = {
    'authority': 'www.kijijiautos.ca',
    'method': 'GET',
    # 'path': '/consumer/srp/by-params?sb=relv3&od=down&ms=9000%3B16&yc=2015%3A2019&con=USED&st=FSBO&ps=0&psz=20&vc=Car&ll=43.52318260000001%2C-79.8547073&rd=500'
    'scheme': 'https',
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-CA',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'pragma': 'no-cache',
    # 'referer': 'https://www.kijijiautos.ca/cars/',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': random_useragent(),
    'x-client': 'ca.move.web.app',
    # 'x-client-id': '992d2dc3-83f7-4639-9798-969978a552a5',
    'x-client-id': '2cb21cc2-8666-4b51-b184-54a2d8fb318c',
    # 'x-search-source': 'srp',
    # 'x-track-recent-search': 'true'
}

KJ_CAR_MAKERS = {
   "Ford": "",
   "RAM": "267",
   "Chevrolet": "",
   "Cadillac": "",
   "Jeep": "",
   "Dodge": "",
}

KJ_CAR_MODELS = {

}