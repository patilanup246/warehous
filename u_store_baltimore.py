from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
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


def uStoreBaltimore_scrap(zip_code_lst, unique_url_lst):
    for zip in zip_code_lst:
        try:
            url = "https://www.u-store.com/locations/?search=" + str(zip)

            t = random.randint(20, 30)
            time.sleep(t)

            options = Options()
            options.headless = True

            root_dir = os.path.dirname(os.path.abspath(__file__))

            try:
                driver = webdriver.Firefox(options=options, executable_path=root_dir + '/geckodriver')

                driver.get(url)
                time.sleep(3)

                content = soup(driver.page_source, 'html.parser')

                link_lst = []
                lst_container = []
                lst_container = content.findAll("div", {"class": "ilf-location-list"})
                url_lst = lst_container[0].findAll("div", {"class": "col-6 col-sm-4"})
                for links in url_lst:
                    try:
                        lnk = links.find("a", {"class": "ilf-permalink"})['href']
                        if lnk in unique_url_lst:
                            continue
                        else:
                            unique_url_lst.append(lnk)
                            link_lst.append(lnk)
                    except:
                        pass

                for i in range(len(link_lst)):
                    try:
                        storage_link = link_lst[i]

                        t = random.randint(10, 15)
                        time.sleep(t)
                        driver.get(storage_link)
                        time.sleep(3)

                        page_soup = soup(driver.page_source, 'html.parser')

                        container = []
                        container = page_soup.findAll('div', attrs={"id": "all-units-table"})

                        lst_small = container[0].findAll("div", {"class": "grid unitGrid Small"})
                        lst_medium = container[0].findAll("div", {"class": "grid unitGrid Medium"})
                        lst_large = container[0].findAll("div", {"class": "grid unitGrid Large"})

                        all_lst = lst_small + lst_medium + lst_large

                        addr_lst = []
                        addr_lst = page_soup.findAll("p", {"class": "singleLocationAddress"})
                        addr = ''
                        for add_txt in addr_lst:
                            try:
                                addr = addr + " " + add_txt.text.strip()
                            except:
                                pass
                        address = addr.strip()
                        addr_zip_code = address.split(" ")[-1]

                        for txt in all_lst:
                            try:
                                size_type = ''
                                size_type = txt.findAll("p", {"class": "unitSize"})[0].text.strip()
                                price = ''
                                price = txt.find("p", {"class": "unitPrice"}).text.strip().split("/")[0]

                                print(size_type + ",  " + price + ",  " + address + ", " + addr_zip_code + ", " + storage_link)

                                isexit = False
                                sql = "SELECT * FROM tbl_ustore WHERE address = %s  AND price = %s AND size = %s AND link = %s"
                                adr = (address, str(price), str(size_type), storage_link)
                                mycursor.execute(sql, adr)
                                myresult = mycursor.fetchall()
                                for x in myresult:
                                    isexit = True

                                if isexit == False:
                                    sql = "INSERT INTO tbl_ustore (address, price,size,zipcode,link) VALUES (%s, %s,%s, %s,%s)"
                                    val = (address, str(price), str(size_type), str(addr_zip_code), storage_link)
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

