from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re


chrome = webdriver.Chrome()
chrome.minimize_window()
url = "https://tenjo.tw/2016-09-27-954/"
chrome.get(url)
html = chrome.page_source

soup = BeautifulSoup(html, 'html.parser')

strong_tag = []
strong_tag = soup.find_all('p')

name = []
for i in range(len(strong_tag)):
    text = str(strong_tag[i])
    text = re.sub('<p>', '', text)
    text = re.sub('</p>', '', text)
    if text.find('<strong>') == 0:
        text = re.sub('<strong>', '', text)
        if text.find('</strong>') > 0:
            text = re.sub('</strong>', '', text)
            if len(text) < 35:
                name += [text]
            print(len(text))

print(name)
print(len(name))

chrome.close()

path = './data/restaurant.txt'
f = open(path, "w+", encoding='utf-8')
for n in name:
    f.write(n)
    f.write('\n')
f.close()

exit()