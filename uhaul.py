import requests
from bs4 import BeautifulSoup as soup
import time
import mysql.connector

mydb = mysql.connector.connect(
  host="129.146.46.75",
  user="usselfstorage",
  passwd="aB5HArimKzp6525N",
  database="usselfstorage"
)

mycursor = mydb.cursor()

def html_parser(req_url):
    try:
        req = requests.get(req_url)
        page_soup = soup(req.content, "html5lib")
        time.sleep(2)
        return page_soup
    except:
        pass


def all_addr_url(page_soup, all_url, x, unique_url_lst):
    container_01 = page_soup.findAll("ul", {"class": "no-bullet no-offset collapse-bottom available-services"})

    for link_url in container_01:
        try:
            container_02 = link_url.findAll("li")
            for link_txt in container_02:
                url_txt = link_txt.find("a")

                if url_txt.text.strip().replace(' ', '').lower() == 'selfstorage':
                    url = x + str(url_txt['href'])

                    if url in unique_url_lst:
                        continue
                    else:
                        unique_url_lst.append(url)
                        all_url.append(url)
        except:
            pass


def main(zip_code_lst, unique_url_lst):
    x = "https://www.uhaul.com"
    print("Start")
    for zip in zip_code_lst:
        time.sleep(2)
        try:
            url = "https://www.uhaul.com/Locations/" + str(zip) + "/Results/"

            page_soup = html_parser(url)

            all_url = []
            all_addr_url(page_soup, all_url, x, unique_url_lst)

            for i in range(5):
                try:
                    nxt_urls = page_soup.findAll("a", {"id": "locationSearchNextLocations"})
                    if len(nxt_urls) > 0:
                        url = x + str(nxt_urls[0]['href'])

                        page_soup = html_parser(url)

                        all_addr_url(page_soup, all_url, x, unique_url_lst)
                    else:
                        break
                except:
                    pass

            for i in range(0, len(all_url)):
                try:
                    storage_link = all_url[i]

                    page_soup = html_parser(storage_link)

                    addr_container = []
                    try:
                        addr_container = page_soup.find("div", {"class": "address"}).find("p").text
                    except:
                        addr_content = page_soup.findAll("div", {"class": "flex-cell medium-5"})
                        addr_container = addr_content[0].findAll("address", {"class": "collapse"})[0].text
                        pass
                    addr_lst = addr_container.replace('\n', ' ').split(" ")

                    address = ''
                    for addr in addr_lst:
                        if len(addr.strip()) > 0:
                            address = address + " " + addr.strip()

                    address = address.strip()

                    addr_zip_code = ''
                    addr_zip_code = address.split(" ")[-1]

                    all_lst = []
                    all_lst = page_soup.findAll("div", {"class": "small-7 medium-10 flex-cell"})
                    if len(all_lst) == 0:
                        all_lst = page_soup.findAll("div", {"class": "small-5 medium-10 flex-cell"})

                    for txt in all_lst:
                        try:
                            size_type = ''
                            size_txt = txt.find("div", {"class": "medium-5 flex-cell"})
                            size_type = size_txt.find("h4").text.replace("\n", "").replace(" ", "")
                            price = ''
                            try:
                                price = txt.findAll("b", {"class": "text-callout text-xlarge"})[0].text.strip()
                            except:
                                price_txt = txt.findAll("div", {"class": "medium-3 column"})
                                price = price_txt[0].find("p").find("strong").text.strip()
                                pass

                            isexit = False
                            sql = "SELECT * FROM tlb_uhaul WHERE address = %s  AND price = %s AND size = %s AND link = %s"
                            adr = (address, str(price), str(size_type), storage_link)
                            mycursor.execute(sql, adr)
                            myresult = mycursor.fetchall()
                            for x in myresult:
                                isexit = True

                            if isexit == False:
                                sql = "INSERT INTO tlb_uhaul (address, price,size,zipcode,link) VALUES (%s, %s,%s, %s,%s)"
                                val = (address, str(price), str(size_type), str(addr_zip_code), storage_link)
                                mycursor.execute(sql, val)
                                mydb.commit()

                        except:
                            pass
                except:
                    pass
        except:
            pass
    print("End")

if __name__ == '__main__':
    zip_code_lst = []
    unique_url_lst = []

    with open("zip_code.txt", "r") as f:
        file = f.read()
        zip_codes = file.split(",")
        for code in zip_codes:
            if len(code.strip()) > 0:
                zip_code_lst.append(code.strip())
    main(zip_code_lst, unique_url_lst)