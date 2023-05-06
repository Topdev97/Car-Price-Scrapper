import requests
import bs4
from requests import models
import yaml
import time

from config import KJ_HEADERS, get_proxy


def kj_scrape_makers():
    url = 'https://www.kijijiautos.ca/'
    makers_dict = {}
    response = requests.session().get(url, headers=KJ_HEADERS, proxies=get_proxy())
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    makers_block = soup.find('div', {'class': 'bpzS6u'})
    makers_id = makers_block.find_all('input')
    for shildik in makers_id:
        name = shildik.get('name')
        _id = shildik.get('id').split(' ')[1].replace('makes-', '')
        makers_dict[name] = _id
    with open('kj_makers.yaml', 'w') as outfile:
        yaml.dump(makers_dict, outfile, default_flow_style=False)


def kj_get_makers():
    with open('kj_makers.yaml', 'r') as r_file:
        makers = yaml.load(r_file, Loader=yaml.FullLoader)
    return makers


def kj_scrape_models():
    models_dict = {}
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=20)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    session.proxies.update(get_proxy())
    # url = 'https://www.kijijiautos.ca/cars/audi/#ms=1900&od=down&sb=relv3'
    for key, val in kj_get_makers().items():
        models_dict[key] = []
        url = 'https://www.kijijiautos.ca/cars/{}/#ms={}&od=down&sb=relv3'.format(key.lower().replace(' ','-'), val)
        response = session.get(url, proxies=get_proxy())
        if response.status_code == 503:
            session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(max_retries=20)
            session.mount('https://', adapter)
            session.mount('http://', adapter)
            session.proxies.update(get_proxy())
            # print('scraper was block')
            # print('waiting for response after 503')
            time.sleep(30)
            response = session.get(url, proxies=get_proxy())
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        models_block = soup.find_all('div', {'class': 'b3Ood7 dpzS6u'})
        try:
            models = models_block[1].find('select').find_all('option')
            for opt in models:
                model_name = opt.text
                model_id = opt.get('value')
                # print(key, model_name, model_id)
                models_dict[key].append({model_name: model_id})
        except IndexError as err:
            print("blank request to Other items")
    
    with open('kj_models.yaml', 'w') as outfile:
        yaml.dump(models_dict, outfile, default_flow_style=False)

# Finds the right code for the selected make & model from yaml file
def kj_get_models(maker, model):
    with open('kj_models.yaml', 'r') as r_file:
        models = yaml.load(r_file, Loader=yaml.FullLoader)

    print(maker)
    print(model)

    #print('Models')
    #print(models)

    #select the correct models based on make
    qs = models[maker]
    #print("QS")
    #print(qs)

    #Find the correct code for the models for that make
    for m in qs:
        for key, val in m.items():
            if key == model:
                qs_id = val

    print('QS_ID')
    print(qs_id)
    return qs_id