from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
# bütün evleri listeyebilen, en filtresiz sayfaya git
# sayfaları döngü ile dolaş (gitmek istediğin sayfanın sayısını sayfa numaraları üstündeki metinden al, döngüye 2.den başla)
# evlerin olduğu elementleri döngü ile gezin
# elementlerin içine gir, özellikleri filtrele
# filtrenen özellikleri al, kaydet

class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome("c:\chromedriver.exe")
        self.url = "https://www.arabam.com/ikinci-el/otomobil?page=38" # url dinamik olarak değiştirilirken son karakteri değiştimek için
        self.hrefs = []  # yeni fonksiyon yazılmalı
        self.columns= ['Fiyat', 'Marka', 'Seri', 'Model', 'Yıl', 'Yakıt Tipi', 'Vites Tipi', 'Motor Hacmi',
                        'Motor Gücü', 'Kilometre', 'Boya-Değişen',"Toplam Tramer Tutarı"]
        self.greatestColumnNumber = 0


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


    def read_data(self):

        # main = self.driver.find_element(By.XPATH, "//*[@id='__next']/div[3]/div[1]/div/div[5]/div[1]/div[1]")
        main = WebDriverWait(self.driver, 200).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main-listing"]/tbody')))
        soup = bs(main.get_attribute("innerHTML"), "html.parser")
        # açılan sayfadaki ilanların class adı
        for elem in soup.findAll('div', {'class': 'pr10 fade-out-content-wrapper'}):

            self.set_hrefs(elem.a['href'])


    def get_columns(self, url):

        self.driver.get(url)

        cf = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="js-hook-for-observer-detail"]/div[2]')))
        soup = bs(cf.get_attribute("innerHTML"), "html.parser")


    def get_info(self, url):

        self.driver.get(url)

        # ilan sayfasındaki bilgiler tablosunun xpathi
        cf = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="js-hook-for-observer-detail"]/div[2]')))
        soup = bs(cf.get_attribute("innerHTML"), "html.parser")

        master = []
        master_new = []

        # bilgilerin bulunduğu tablo elementlerinin class'ı ile iterasyon
        for div in soup.findAll('div', {'//*[@id="js-hook-for-observer-detail"]/div[2]'}):
            text = div.text
            master.append(text)


        # fiyat bilgisi
        prcElem = self.driver.find_element(By.XPATH, '//*[@id="js-hook-for-observer-detail"]/div[2]/div[1]/div/span')
        price = prcElem.text.replace('.', "")[:-2]
        master_new.append(price)

        br = self.driver.find_element(By.XPATH,
                                      '//*[@id="js-hook-for-observer-detail"]/div[2]/ul/li[3]/span[2]')  # marka  //*[@id="js-hook-for-observer-detail"]/div[2]/ul/li[3]/span[2]
        br = br.text

        sr = self.driver.find_element(By.XPATH,
                                      '//*[@id="js-hook-for-observer-detail"]/div[2]/ul/li[4]/span[2]')  # seri
        sr = sr.text

        ml = self.driver.find_element(By.XPATH,
                                      '//*[@id="js-hook-for-observer-detail"]/div[2]/ul/li[5]/span[2]')  # model
        ml = ml.text

        yr = self.driver.find_element(By.XPATH, '//*[@id="js-hook-for-observer-detail"]/div[2]/ul/li[6]/span[2]')  # yıl
        yr = yr.text

        ft = self.driver.find_element(By.XPATH,
                                      '//*[@id="js-hook-for-observer-detail"]/div[2]/ul/li[7]/span[2]')  # yakıt tipi
        ft = ft.text

        gr = self.driver.find_element(By.XPATH,
                                      '//*[@id="js-hook-for-observer-detail"]/div[2]/ul/li[8]/span[2]')  # vites tipi
        gr = gr.text

        ec = self.driver.find_element(By.XPATH,
                                      '//*[@id="js-hook-for-observer-detail"]/div[2]/ul/li[9]/span[2]')  # motor hacmi
        ec = ec.text

        mp = self.driver.find_element(By.XPATH,
                                      '//*[@id="js-hook-for-observer-detail"]/div[2]/ul/li[10]/span[2]')  # motor gücü
        mp = mp.text

        km = self.driver.find_element(By.XPATH,
                                      '//*[@id="js-hook-for-observer-detail"]/div[2]/ul/li[11]/span[2]')  # kilometre
        km = km.text


        pc = self.driver.find_element(By.XPATH,
                                      '//*[@id="js-hook-for-observer-detail"]/div[2]/ul/li[12]/a')
        pc = pc.text  # boya-değişim
        tt = self.driver.find_element(By.XPATH,
                                          '//*[@id="js-hook-for-observer-boyadegisen"]/div/div[3]/div/p/span')  # kilometre
        tt = tt.text


        pc = self.driver.find_element(By.XPATH,
                                      '//*[@id="js-hook-for-observer-detail"]/div[2]/ul/li[12]/span[2]')
        pc = pc.text ###belirtilmemiş



        master_new.append(br)
        master_new.append(sr)
        master_new.append(ml)
        master_new.append(yr)
        master_new.append(ft)
        master_new.append(gr)
        master_new.append(ec)
        master_new.append(mp)
        master_new.append(km)
        master_new.append(pc)
        master_new.append(tt)

        return master_new

