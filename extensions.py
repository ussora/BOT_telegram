import requests
import json
from config import keys

class ConvertionException(Exception):
    pass
class CursConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if amount < '0':
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = list(keys.values())[list(map(lambda x: x.lower(), keys.keys())).index(quote)]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = list(keys.values())[list(map(lambda x: x.lower(), keys.keys())).index(base)]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')

        total_base = json.loads(r.content)[list(keys.values())[list(map(lambda x: x.lower(), keys.keys())).index(base)]]
        end_total = total_base * amount

        return end_total