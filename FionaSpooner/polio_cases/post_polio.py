import requests
from requests import Request, Session
from bs4 import BeautifulSoup

item_request_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}

url = "https://extranet.who.int/polis/public/CaseCount.aspx"

s = requests.Session()
s.headers.update(item_request_headers)

fr_soup = s.get(url)
soup = BeautifulSoup(fr_soup.content, "lxml")

soup.select("#__VIEWSTATE")[0]["value"]
soup.select("#__EVENTVALIDATION")[0]["value"]
r = s.get("https://extranet.who.int/polis/public/CaseCount.aspx")

select_object = soup.find("select", {"id": "ListBox1"})
select_object


soup.select("#ListBox1")

data = {i["name"]: i.get("value", "") for i in soup.select("input[name]")}

soup.find_all("option", selected=True)

subject_options = [
    i.findAll("option") for i in soup.findAll("select", attrs={"name": "ListBox1"})
]

subject_options[0] = '<option selected="selected" value="Glo"> World</option>'


s.post("https://prod.ceidg.gov.pl/CEIDG/CEIDG.Public.UI/Search.aspx", data=data)
