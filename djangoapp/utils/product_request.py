import requests
from bs4 import BeautifulSoup

def search_request(value):
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    page = requests.get(f"https://lista.mercadolivre.com.br/{value}", headers=headers)
    
    if page.status_code == 200:

        soup = BeautifulSoup(page.text)
        products_found = []
        products_divs = soup.find_all('div', class_='poly-card__content')
        for div in products_divs:
            try:
                product_title = div.find('a', class_='poly-component__title').text
                product_price = div.find('a', class_='poly-component__title').text
                products_found.append({'title': product_title})
                print(products_found)
            except:
                print('Deu ruim')
                return None

        return products_found
    return None


