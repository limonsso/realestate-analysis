from typing import List
from pandas import json_normalize
import requests
import json
import html

base_url = 'http://127.0.0.1:8001/api/'


def find_properties(cities: List[str], max_price: int = 2000000, min_price: int = 0, only_sales: bool = True):
    url = f'{base_url}properties/find'
    params = {}
    params['localities'] = cities
    params['pageSize'] = 500000
    params['pageNumber'] = 1
    params['maxPrice'] = max_price
    params['minPrice'] = min_price
    params['OnlyOnSale'] = only_sales

    r = requests.get(url, params=params)
    a = json.loads(r.text)

    properties = json_normalize(a['properties'])
    return properties


def get_morgage_payment(price: float, nbr_year: int, nbr_ann_payment: int, interest: float):
    hypoteques = []
    urlpayment = f'{base_url}mortgage/payment'
    data = {
        "montant_pret": price,
        "duree_en_annee": nbr_year,
        "interet_annuel": interest,
        "nbr_vrsmnt_annuel": nbr_ann_payment
    }
    #caluler l'hypothèque mensuel
    r = requests.post(urlpayment, json=data)
    morgage_payment = json.loads(r.text)
    return morgage_payment
