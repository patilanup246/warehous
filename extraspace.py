import requests
from bs4 import BeautifulSoup as soup
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
        page_soup = soup(req.content, "html.parser")
        return page_soup
    except:
        pass


def main(zip_code_lst, unique_url_lst):
    x = "https://www.extraspace.com"
    for zip in zip_code_lst:
        try:
            url = "https://www.extraspace.com/querysearch/?searchTerm=" + str(zip)
            page_soup = html_parser(url)

            link_lst = []
            url_lst = page_soup.findAll("a", {"class": "address-link"})
            for links in url_lst:
                try:
                    lnk = x + str(links['href'])
                    if lnk in unique_url_lst:
                        continue
                    else:
                        unique_url_lst.append(lnk)
                        link_lst.append(lnk)
                except:
                    pass

            for i in range(0, len(link_lst)):
                try:
                    storage_link = link_lst[i]

                    page_soup = html_parser(storage_link)

                    addr_container = page_soup.find("div", {"class": "fac-info middle-col"}).findAll("div")

                    addr_lst = addr_container[1].findAll('span')
                    addr = ''
                    for addr_txt in addr_lst:
                        try:
                            addr = addr + " " + addr_txt.text.strip()
                        except:
                            pass
                    address = addr.strip()
                    addr_zip_code = address.split(" ")[-1]

                    all_lst = page_soup.findAll("div", {"class": "makes-offer"})
                    for txt in all_lst:
                        try:
                            size_txt = txt.findAll("div", {"class": "size RamaGothicSemiBold"})
                            size_type = size_txt[0].findAll("div")[0].text.replace(" ", "")

                            price_txt = txt.findAll("div", {"class": "rate"})
                            if len(price_txt)>1:
                                price = price_txt[1].findAll("div")[0].contents[0].strip()
                            else:
                                price = price_txt[0].findAll("div")[0].text.strip()

                            isexit = False
                            sql = "SELECT * FROM tbl_extraspace WHERE address = %s  AND price = %s AND size = %s AND link = %s"
                            adr = (address, str(price), str(size_type), storage_link)
                            mycursor.execute(sql, adr)
                            myresult = mycursor.fetchall()
                            for x in myresult:
                                isexit = True

                            if isexit == False:
                                sql = "INSERT INTO tbl_extraspace (address, price,size,zipcode,link) VALUES (%s, %s,%s, %s,%s)"
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
    print("start")
    zip_code_lst = []
    unique_url_lst = []

    with open("zip_code.txt", "r") as f:
        file = f.read()
        zip_codes = file.split(",")
        for code in zip_codes:
            if len(code.strip()) > 0:
                zip_code_lst.append(code.strip())
    main(zip_code_lst, unique_url_lst)
    print("End")

