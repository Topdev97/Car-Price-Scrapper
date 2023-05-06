import bs4
import requests
import multiprocessing
import datetime
import json
import logging

from multiprocessing.pool import ThreadPool
from config import auth_to_sheet, get_proxy, send_mail, KJ_HEADERS, KIJIJI_AUTO_TABLE, CRITERIES_TABLE
from tools import kj_get_models

logging.basicConfig(
    level=logging.DEBUG,
    filename='kijijiauto.log',
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    )


class KijijiAutoScraper():
    def __init__(self):
        super().__init__()
        self.criteries_sheet = auth_to_sheet().worksheet_by_title(CRITERIES_TABLE)
        self.result_sheet = auth_to_sheet().worksheet_by_title(KIJIJI_AUTO_TABLE)
        self.search_radius = self.criteries_sheet.get_value("B6")
        self.post_code = self.criteries_sheet.get_value("B7")
        self.base_url = 'https://www.kijijiautos.ca/cars' #/ford/f-150/used/#vip=19945602'

    def get_cars(self, start_year, end_year, maker, model, seller_type, condition, keywords=''):
        links = []
        if seller_type == 'Private':
            transform_seller_type = 'FSBO'
        elif seller_type == 'Dealer':
            transform_seller_type = 'DEALER'
        else:
            transform_seller_type = ''


        model_qs = kj_get_models(maker, model)
        url = 'https://www.kijijiautos.ca/consumer/srp/by-params'
        payload = {
            'sb': 'relv3',
            'od': 'down',
            'ms': model_qs,
            'yc': f'{start_year}:{end_year}',
            'st': transform_seller_type,
            'ps': '0',
            'psz': '500',
            'vc': 'Car',
            # 'con': f'{str(condition).upper()}',
            'll': '43.52318260000001,-79.8547073',
            'rd': self.search_radius
        }
        if keywords != '':
            payload['q'] = keywords
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=20)
        session.mount('https://', adapter)
        session.mount('http://', adapter)
        session.proxies.update(get_proxy())
        #print('URL')
        #print(url)
        #print('Headers')
        #print(KJ_HEADERS)
        #print('PayLoad: ')
        #print(payload)
        resp = session.get(url, headers=KJ_HEADERS, params=payload)
        logging.debug('response status code: {}'.format(resp.status_code))
        logging.debug("response url: {}".format(resp.url))
        logging.debug("\n Maker:{} \n Model:{} \n Keyword: {}".format(maker, model, keywords))
        j_data = json.loads(resp.text)
        for i in j_data['listings']['items']:
            link = f'{self.base_url}/{maker.lower().replace(" ","-")}/{model.lower().replace(" ","-")}/{condition.lower()}/#vip={i["id"]}'
            links.append(link)
            print('New Kijiji Listing: ' + link)
        
        return links

    def get_search_settings(self):
        data = self.criteries_sheet.get_values(start='I10', end='O10000')
        return data

    def main(self):
        data = []
        new_links = []
        pool = ThreadPool(multiprocessing.cpu_count())
        result = pool.starmap(self.get_cars, self.get_search_settings())
        for link_list in result:
            for link in link_list:
                if link not in data:
                    data.append(link)

        if len(data):
            current_data = self.result_sheet.get_values(start='A2', end='A10000')
            current_data_list = []
            for d in current_data:
                current_data_list.append(d[0])
            if current_data_list != data:
                for link in data:
                    if link not in current_data_list:
                        new_links.append(link)
                
                now = datetime.datetime.now()
                if len(current_data_list) == 1:
                    self.result_sheet.update_col(index=1, values=new_links, row_offset=1)
                    self.result_sheet.update_col(index=2, values=[f'{now.year}/{now.month}/{now.day}-{now.hour}:{now.minute}' for i in range(len(new_links))], row_offset=1)
                else:
                    link_for_mail = []
                    for link in new_links:
                        if link not in current_data_list:
                            self.result_sheet.insert_rows(1, values=[link, f'{now.year}/{now.month}/{now.day}-{now.hour}:{now.minute}'], inherit=True)
                            link_for_mail.append(link)
                    if link_for_mail:
                        logging.debug(f'New links was found: {len(link_for_mail)}')
                        mail_text = 'New links have been added to the table, please check out:\n' + '\n'.join([f'{ref}\n' for ref in link_for_mail])
                        send_mail('KijijiAutos: ', mail_text)
            else:
                print("nothing new")



if __name__ == "__main__":
    scraper = KijijiAutoScraper()
    scraper.main()