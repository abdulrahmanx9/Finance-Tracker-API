import requests
from django.core.cache import cache


def fetch_exchange_rates(base_currency):
    cache_key = f"exchange_rates_{base_currency}"
    rates = cache.get(cache_key)
    if rates is not None:
        return rates

    # Fetch rates from API
    api_key = "47ffd86a0617d87e209f9246"
    url = (
        f"https://api.exchangerate-api.com/v4/latest/{base_currency}?api_key={api_key}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["rates"]
    else:
        raise Exception("Failed to fetch exchange ratese")
