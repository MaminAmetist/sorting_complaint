import requests


def get_location(ip: str) -> str:
    url = f'http://ip-api.com/json/{ip}'
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        data = response.json()
        return f"{data.get('country', '')}, {data.get('regionName', '')}, {data.get('city', '')}"
    else:
        raise Exception('Geolocation API unavailable')
