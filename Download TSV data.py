import requests
import bs4 as bs
import re

def scrap_data(url):
    response = requests.get(url)
    print(response.text)

def get_the_last_url(url):
    request =   requests.get(url)
    soup = bs.BeautifulSoup(request.text, "html.parser")

    # find the last a tag which has herf attribute enddig with .tsv.gz
    last_url = soup.find_all("a", attrs={"href": re.compile(".tsv.gz$")})[-1]
    last_url = last_url["href"]
    return last_url


if __name__ == "__main__":
    url = "https://gz.blockchair.com/bitcoin/transactions/"
    url = "https://gz.blockchair.com/bitcoin/transactions/"+get_the_last_url(url)
    print(url)
    scrap_data(url)