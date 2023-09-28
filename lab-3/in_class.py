import bs4 as BeautifulSoup
import requests
import json

url = "https://999.md/ru/list/real-estate/apartments-and-rooms?o_30_241=894&applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33&o_33_1=776"
max_pages = 3

def get_max_page(link):
    page = requests.get(link) 
    soup = BeautifulSoup.BeautifulSoup(page.text, "html.parser")
    last_page = soup.find('li', class_="is-last-page")
    if last_page:
        last_page_no = int(last_page.find('a').get('href').split('=')[-1])
    else:
        last_page_no = 1
    return last_page_no

def get_urls(link, page_no, read_pages=1, last_page_no=get_max_page(url)):
    if page_no == 1:
        page = requests.get(link)
    else:
        page = requests.get(link + f"&page=" + str(page_no))
    soup = BeautifulSoup.BeautifulSoup(page.text, "html.parser")   
    ad_links = []
    
    for a in soup.find_all('a', class_="js-item-ad"):
        relative_url = a.get('href')
        absolute_url = "https://999.md" + relative_url
        if relative_url.startswith('/ro/') and absolute_url not in ad_links:
            ad_links.append("https://999.md" + relative_url)

    if read_pages < max_pages and page_no < last_page_no:
        return ad_links + get_urls(link, page_no + 1, read_pages + 1, last_page_no)
    else:
        return ad_links

def main():
    links = get_urls(url, 1)
    json_file = open("sites.json", "w")
    json_file.write(json.dumps(links, indent=2))

if __name__ == "__main__":
    main()
