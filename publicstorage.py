from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
from bs4 import BeautifulSoup as soup
import re
import time
import random
import mysql.connector


mydb = mysql.connector.connect(
  host="129.146.46.75",
  user="usselfstorage",
  passwd="aB5HArimKzp6525N",
  database="usselfstorage"
)

mycursor = mydb.cursor()

def publicstorage_scrap(zip_code_lst, unique_url_lst):
    for zip in zip_code_lst:
        try:
            url = "https://www.publicstorage.com/self-storage-search?location=" + str(zip)
            t = random.randint(25, 30)
            time.sleep(t)

            options = Options()
            options.headless = True

            root_dir = os.path.dirname(os.path.abspath(__file__))

            try:
                driver = webdriver.Firefox(options=options, executable_path=root_dir + '/geckodriver')

                driver.get(url)
                time.sleep(3)
                content = soup(driver.page_source, 'html.parser')

                url_lst = content.findAll("a", {"class": "ps-property-v2__view-plp"})

                ur_lst = []
                for urls in url_lst:
                    try:
                        url = "https://www.publicstorage.com" + str(urls['href'])

                        if url in unique_url_lst:
                            continue
                        else:
                            unique_url_lst.append(url)
                            ur_lst.append(url)
                    except:
                        pass

                for i in range(len(ur_lst)):
                    try:
                        storage_link = ur_lst[i]

                        t = random.randint(10, 15)
                        time.sleep(t)
                        driver.get(storage_link)
                        time.sleep(3)

                        content = soup(driver.page_source, 'html.parser')

                        address = ''
                        addr_lst = []
                        addr_lst = re.findall(r'"FormattedAddress":"(.*?)","', content.text)[0].split(" ")

                        for addr in addr_lst:
                            if len(addr.strip()) > 0:
                                address = address + " " + addr.strip()
                        address = address.strip()

                        addr_zip_code = address.split(" ")[-1]

                        dt_lst = content.findAll("div", {"class": "row ps-properties-propertyV2__units__summary"})
                        for index_data in dt_lst:
                            try:
                                size_type = ''
                                size_type = index_data.find("h4", {"class": "ps-properties-propertyV2__units__header"}).text.strip()
                                price_txt = ''
                                price_txt = index_data.find("span",{"class": "ps-properties-propertyV2__units__prices__wrapper"})
                                price = price_txt.text.strip().split('/')[0]

                                print(size_type + ",  " + price + ",  " + address + ", " + addr_zip_code + ", " + storage_link)

                                isexit = False
                                sql = "SELECT * FROM tbl_publicstorage WHERE address = %s  AND price = %s AND size = %s AND link = %s"
                                adr = (address, price, size_type, storage_link)
                                mycursor.execute(sql, adr)
                                myresult = mycursor.fetchall()
                                for x in myresult:
                                    isexit = True

                                if isexit == False:
                                    sql = "INSERT INTO tbl_publicstorage (address, price,size,zipcode,link) VALUES (%s, %s,%s, %s,%s)"
                                    val = (address, price, size_type, addr_zip_code, storage_link)
                                    mycursor.execute(sql, val)
                                    mydb.commit()

                            except:
                                pass
                    except:
                        pass
            except:
                pass

            try:
                driver.quit()
            except:
                pass

        except:
            pass

