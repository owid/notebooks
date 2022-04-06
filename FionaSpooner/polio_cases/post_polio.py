#### A script for messing around with post requests

import requests
from requests import Request, Session
from bs4 import BeautifulSoup
import datetime

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

viewstate = soup.select("#__VIEWSTATE")[0]["value"]
eventvalidation = soup.select("#__EVENTVALIDATION")[0]["value"]
r = s.get("https://extranet.who.int/polis/public/CaseCount.aspx")

select_object = soup.find("select", {"id": "ListBox1"})
select_object


soup.select("#ListBox1")

data = {i["name"]: i.get("value", "") for i in soup.select("input[name]")}

soup.find_all("option", selected=True)

subject_options = [
    i.findAll("option") for i in soup.findAll("select", attrs={"name": "ListBox1"})
]

subject_options[0][0] = '<option selected="selected" value="Glo"> World</option>'


s.post(url, data=subject_options[0])

soup.find_all("input")

selections = soup.find_all("select")

for selection in selections:
    options = selection.find_all("option")
    for option in options:
        str(option).replace("<option", '<option selected="selected"')


post_data2 = {
    "ListBox2": list(["2001", "2020"]),
    "ListBox1": list(["Glo"]),
    "Button1": list(["Show data"]),
}

r = requests.post(url, data=post_data2)

r.content


startDate = datetime.datetime(2016, 1, 1).strftime("%m/%d/%Y")
endDate = datetime.datetime(2016, 2, 20).strftime("%m/%d/%Y")

serviceurl = "https://www.nysaves.org/nytpl/fundperform/fundHistorySearch.do"
payload = {"fundid": 1003022, "startDate": startDate, "endDate": endDate}
r = requests.post(serviceurl, data=payload)
print(r.text)


from selenium import webdriver
