import requests
from bs4 import BeautifulSoup

def print_all():
    return duckduckgo_urls, google_urls

def getLinks(phone_number):
    global duckduckgo_urls, google_urls
    duckduckgo_urls = []
    google_urls = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
    }

    phone_number = phone_number.split("+")[1]

    # DuckDuckGo search
    duckduckgo_page = requests.get(f'https://duckduckgo.com/html/?q={phone_number}', headers=headers).text
    duckduckgo_soup = BeautifulSoup(duckduckgo_page, 'html.parser').find_all("a", class_="result__url", href=True)

    for link in duckduckgo_soup:
        if link['href'] == "":
            duckduckgo_urls.append("not found")
        else:
            duckduckgo_urls.append(link['href'])

    # Google search
    google_page = requests.get(f'https://www.google.com/search?q={phone_number}', headers=headers).text
    google_soup = BeautifulSoup(google_page, 'html.parser').find_all("a", href=True)

    for link in google_soup:
        url = link.get('href')
        if url.startswith('/url?q='):
            google_urls.append(url[7:])

# if __name__ == "__main__":
#     phone_number = "+1234567890"
#     get_links(phone_number)
#     duckduckgo_results, google_results = print_all()
#     print("DuckDuckGo results:")
#     print(duckduckgo_results)
#     print("\nGoogle results:")
#     print(google_results)
