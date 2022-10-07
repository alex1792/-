from bs4.dammit import html_meta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from  bs4 import BeautifulSoup
import time
import os
import re
import csv
import numpy as np
import pandas as pd


def refresh_page():
	window_after = chrome.window_handles[0]
	chrome.switch_to_window(window_after)

# return the content of the file and delete it
def open_file():
	file_name = "./data/f.txt"
	txt = open(file_name, "r+", encoding="utf-8")
	content = txt.read()
	txt.close()
	os.remove(file_name)
	return content

# get token of next page
def get_token(contex):
	tk = re.search('data-next-page-token="(.*?)"', contex).group(1)
	return tk

def url_cat(data_id, token):
	url_head = "https://www.google.com/async/reviewDialog?hl=tw&async=feature_id:"
	url_mid = ",sort_by:,next_page_token:"
	url_tail = ",associated_topic:,_fmt:pc"
	url_tmp = url_head + data_id + url_mid + token + url_tail
	return url_tmp

def get_review():
	code = open_file()
	tmp_code = code
	ret = tmp_code.find("review-full-text")
	# print(ret)
	tmp_list = []
	while ret >= 0:
		tmp_code = tmp_code[ret:]
		tmp_code = tmp_code[tmp_code.find('>') + 1:]
		review = tmp_code[:tmp_code.find("</span>")]
		review = review.replace('<br>', '\n')
		tmp_list.append(review)
		ret = tmp_code.find("review-full-text")
	return tmp_list

url = 'https://www.google.com.tw/maps/@25.0919078,121.5401243,12z?hl=zh-TW&authuser=0'
# chrome = webdriver.Chrome()
option = webdriver.ChromeOptions()
download_path = "C:\\Users\\yuhon\\Desktop\\big_data_competition\\data"
prefs = {}
prefs["profile.default_content_settings.popups"]=0
prefs["download.default_directory"]=download_path
option.add_experimental_option("prefs", prefs)
chrome = webdriver.Chrome(chrome_options=option)


with open('./data/reviews.csv', 'w', encoding='utf-8', newline='') as review_csv:
	csv_writer = csv.writer(review_csv)
	header = ["餐廳名稱","評論"]
	csv_writer.writerows([header])
	with open('./data/restaurant.txt', 'r+', encoding='utf-8') as file:
		restaurant_name = file.readlines()
		for name in restaurant_name:
			review_list = []
			# print(name)
			review_list.append(name)
			
			# processing the restaurant name
			restaurant = re.sub('\n', '', name)
			area = ' 中山區\n'
			text = restaurant + area

			# refresh the page and search the restaurant
			chrome.get(url)
			target = chrome.find_element_by_name('q')
			target.send_keys(text)
			time.sleep(3)

			# processing the html source code
			html = chrome.page_source
			soup = BeautifulSoup(html, 'html.parser')
			html = soup.prettify()
			txt = str(html)

			# find reviews button
			while True:
				# the only target we are looking for
				try:
					ret = chrome.find_element_by_class_name('Yr7JMd-pane-hSRGPd')	
					review_cnt = chrome.find_element_by_class_name('Yr7JMd-pane-hSRGPd').text
					review_cnt = re.sub('\D', '',review_cnt)
					# review_cnt = int(review_cnt)
					print(review_cnt)
					current_url = chrome.current_url
					start_idx = current_url.find('0x')
					data_id = current_url[start_idx:start_idx+37]
					
					for i in range(10):
						if i == 0:
							token = ""
						else:
							token = get_token(code)
						url_tmp = url_cat(data_id,token)
						refresh_page()
						chrome.get(url_tmp)
						time.sleep(5)
						
						code = open_file()
						tmp_code = code
						ret = tmp_code.find("review-full-text")
						while ret >= 0:
							tmp_code = tmp_code[ret:]
							tmp_code = tmp_code[tmp_code.find('>') + 1:]
							review = tmp_code[:tmp_code.find("</span>")]
							review = review.replace('<br>', '\n')
							review_list.append(review)
							ret = tmp_code.find("review-full-text")
					csv_writer.writerows([review_list])
					review_list.clear()

					print('found review button')
					break
				# multiple search consequences
				except:
					print('review button not found')
					chrome.get(url)
					break

# close browser and terminate
chrome.close()
exit()