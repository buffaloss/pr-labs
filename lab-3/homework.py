import requests
import bs4 as BeautifulSoup

def get_product(url):
    page = requests.get(url) 
    soup = BeautifulSoup.BeautifulSoup(page.content, "html.parser")
    characteristics = []
    values = []
    product = {}

    characteristics_tags = soup.find_all("span", class_="adPage__content__features__key")
    for key in characteristics_tags:
        characteristics.append(key.text)

    values_tags = soup.find_all("span", class_="adPage__content__features__value")
    for value in values_tags:
        values.append(value.text)

    for i in range(len(characteristics)):
        if i < len(values):
            product[characteristics[i]] = values[i]
        else:
            product[characteristics[i]] = "Yes"
    return product

def main():
    product = get_product("https://999.md/ro/84220635")
    for key, value in product.items():
        print(key, ":", value)

if __name__ == '__main__':
    main()
