from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from urllib import request
import requests
from itertools import cycle
import traceback
import pandas as pd


# bütün evleri listeyebilen, en filtresiz sayfaya git
# sayfaları döngü ile dolaş (gitmek istediğin sayfanın sayısını sayfa numaraları üstündeki metinden al, döngüye 2.den başla)
# evlerin olduğu elementleri döngü ile gezin
# elementlerin içine gir, özellikleri filtrele
# filtrenen özellikleri al, kaydet

class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome("c:\chromedriver.exe")
        self.url = "http://www.emlakjet.com/satilik-konut/1"  # url dinamik olarak değiştirilirken son karakteri değiştimek için
        self.hrefs = []  # yeni fonksiyon yazılmalı
        self.columns= ['Sehir', 'İlce', 'Mahalle','Fiyat','brüt metrekare', 'Net Metrekare', 'Oda Sayısı', 'Binanın Yaşı',
                             'Bulunduğu Kat']
        self.greatestColumnNumber = 0
        # self.pageNum = 3

    # def set_pageNum(self, i):
    #     self.pageNum = i
    #
    # def get_pageNum(self):
    #     return self.pageNum

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def get_hrefs(self):

        return self.hrefs

    def set_hrefs(self, elem):
        self.hrefs.append(elem)

    def dump_hrefs(self):
        self.hrefs = []

    def set_columns(self, column):
        self.columns.append(column)

    def get_columns(self):
        return self.columns

    def unique_columns(self, list):
        list_set = set(list)
        unique_list = list(list_set)
        return unique_list

    def load_url(self):
        self.driver.get(self.url)

    # def getNum(self):
    #     main = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div[1]/div/div[5]/div[1]/div[2]/div[1]/ul')
    #     soup = bs(main.get_attribute("innerHTML"), "html.parser")
    #     for elem in soup.findAll('div', {'class': 'styles_pagingButton__3HGBl'}):
    #         # self.hrefs.append(elem.a['href'])
    #         self.set_pageNum(elem.a['href'][-2:])

    def read_data(self):

        # main = self.driver.find_element(By.XPATH, "//*[@id='__next']/div[3]/div[1]/div/div[5]/div[1]/div[1]")
        main = WebDriverWait(self.driver, 200).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[3]/div[1]/div/div[5]/div[1]')))
        soup = bs(main.get_attribute("innerHTML"), "html.parser")
        # açılan sayfadaki ilanların class adı
        for elem in soup.findAll('div', {'class': 'styles_listingItem__1asTK'}):
            # self.hrefs.append(elem.a['href'])
            self.set_hrefs(elem.a['href'])

    # def get_proxies(self):
    #     url = 'https://free-proxy-list.net/'
    #
    #     response = requests.get(url)
    #     parser = fromstring(response.text)
    #     proxies = set()
    #     for i in parser.xpath('//tbody/tr')[:5]:
    #         if i.xpath('.//td[7][contains(text(),"yes")]'):
    #             proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
    #             proxies.add(proxy)
    #     return proxies

    def get_columns(self, url):

        self.driver.get(url)

        cf = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="bilgiler"]/div/div[2]/div/div[1]')))
        soup = bs(cf.get_attribute("innerHTML"), "html.parser")

        master = []
        cols = []
        attributes = soup.findAll('div', {'class': 'styles_tableColumn__2x6nG'})

        # if len(attributes) > self.greatestColumnNumber:
        #     self.greatestColumnNumber = len(attributes)
        #     # bilgilerin bulunduğu tablonun classı ve istediğimiz yerin'div' olması
        #     for div in attributes:
        #         text = div.text
        #         master.append(text)

        # for x in range(0, len(master), 2):
        #     # cols.append(master[x])
        #     self.columns = ['Sehir', 'İlce', 'Mahalle', 'brüt metrekare', 'Net Metrekare', 'Oda Sayısı', 'Binanın Yaşı',
        #                     'Bulunduğu Kat', 'Banyo Sayısı', 'WC Sayısı', 'Site İçerisinde']
        #     # if master[x] not in self.columns:
        #     # self.columns.append(master[x])

    def get_info(self, url):

        self.driver.get(url)

        # ilan sayfasındaki bilgiler tablosunun xpathi
        cf = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="bilgiler"]/div/div[2]/div/div[1]')))
        soup = bs(cf.get_attribute("innerHTML"), "html.parser")

        master = []
        master_new = []

        # bilgilerin bulunduğu tablo elementlerinin class'ı ile iterasyon
        for div in soup.findAll('div', {'class': 'styles_tableColumn__2x6nG'}):
            text = div.text
            master.append(text)

        # lokasyon bilgileri
        locElem = self.driver.find_element(By.CLASS_NAME, 'styles_locationInfo__3adCH')
        loc = locElem.text.strip('location_on')
        sehir = loc.split(" - ")[0]
        ilce = loc.split(" - ")[1]
        mahalle = loc.split(" - ")[2] + "i"

        master_new.append(sehir[1:])
        master_new.append(ilce)
        master_new.append(mahalle)



        # fiyat bilgisi
        prcElem = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div[2]/div[2]/div[2]/div[1]/div')
        price = prcElem.text.replace('.', "")[:-2]
        master_new.append(price)

        mb1 = self.driver.find_element(By.XPATH, '//*[@id="bilgiler"]/div/div[2]/div/div[1]/div[1]/div[4]/div[2]')
        mb = mb1.text

        mn1 = self.driver.find_element(By.XPATH, '//*[@id="bilgiler"]/div/div[2]/div/div[1]/div[2]/div[3]/div[2]')
        mn = mn1.text

        os1 = self.driver.find_element(By.XPATH, '//*[@id="bilgiler"]/div/div[2]/div/div[1]/div[2]/div[4]/div[2]')
        os = os1.text

        by1 = self.driver.find_element(By.XPATH, '//*[@id="bilgiler"]/div/div[2]/div/div[1]/div[1]/div[5]/div[2]')
        by = by1.text

        bk1 = self.driver.find_element(By.XPATH, '//*[@id="bilgiler"]/div/div[2]/div/div[1]/div[2]/div[5]/div[2]')
        bk = bk1.text
    #-------------------------------------------------------------------------------


        master_new.append(mb)
        master_new.append(mn)
        master_new.append(os)
        master_new.append(by)
        master_new.append(bk)



        return master_new

