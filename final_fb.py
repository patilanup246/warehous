from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
from bs4 import BeautifulSoup as soup
import csv


def fb_post(root_dir, user_id, password, group_id):
    try:
        option = Options()
        # option.add_argument("--headless")

        driver = webdriver.Chrome(options=option, service_log_path="NUL",
                                executable_path=root_dir+"/chromedriver.exe")
        driver.maximize_window()

        driver.get("https://www.facebook.com/")
        time.sleep(8)

        driver.find_element_by_xpath("//input[@id='email']").send_keys(user_id)
        driver.find_element_by_xpath("//input[@id='pass']").send_keys(password)

        driver.find_element_by_xpath("//input[@value='Log In']").click()
        time.sleep(10)

        gp_url = "https://www.facebook.com/groups/" + group_id
        driver.get(gp_url)
        time.sleep(10)

        columns = ["Group Name", "Post Description", "Post Date", "User Id", "Like Count", "Love Count",
                   "Haha Count", "Wow Count", "Sad Count", "Angry Count", "Care Count", "Post Url", "Post Text"]

        f =  open(root_dir + "/"+group_id+".csv", "w", encoding='utf-8', newline='')
        csv_writer = csv.writer(f, delimiter = ',')
        csv_writer.writerow(columns)
        f.close()


        try:
            gp_name = driver.find_element_by_xpath("//div[@class='tr9rh885']//h2").text
        except:
            try:
                gp_name = driver.find_element_by_xpath("//h1[@id='seo_h1_tag']").text.strip()
            except:
                gp_name = "-"
            pass

        posts_lst = []
        old_position = 0
        new_position = None

        i = 0
        while i < 3:
            while new_position != old_position:
                try:
                    page_soup = soup(driver.page_source, "html.parser")
                    # posts = driver.find_elements_by_xpath("//div[@data-testid='Keycommand_wrapper_feed_story']")

                    posts_1 = page_soup.findAll("div", {"data-testid": "Keycommand_wrapper_feed_story"})

                    if len(posts_1) <1:
                        posts_1 = page_soup.findAll("div", {"class": "_3ccb"})

                    for i, data in enumerate(posts_1):
                        try:
                            post_date = data.findAll("span", attrs={"class": "jpp8pzdo"})[0].nextSibling.find("a").text.strip()
                        except:
                            try:
                                post_date = data.findAll("a", {"class": "_5pcq"})[0].find("abbr")["title"]
                            except:
                                post_date = "-"
                                pass
                            pass

                        post_desc = '-'
                        try:
                            post_desc = data.find("div",{
                                "style": "height: 100%; left: 0%; width: calc(100%);"}).find("img")["src"]
                        except:
                            try:
                                post_desc = data.find("a", {"rel": "theater"}).find("img")["src"]
                                #  video src
                                # post_desc = data.findAll("div", {"class": "video"})[0].find("img")["src"]
                            except:
                                try:
                                    post_desc = data.findAll("div", {"dir": "auto"})[0].text.strip()
                                except:
                                    try:
                                        post_desc = data.findAll("div", {"class": "text_exposed_root"})[0].find("p").text
                                    except:
                                        pass
                                    pass
                                pass
                            pass

                        post_dict = {"post_date": post_date, "post_desc": post_desc}

                        if post_dict in posts_lst:
                            continue

                        posts_lst.append(post_dict)


                        posted_by_user_id = "-"
                        try:
                            posted_user = data.findAll("div", {"class": "nc684nl6"})[0].findAll("a")[0]["href"]
                            posted_by_user_id = posted_user.split("?")[0].split("/")[-1]

                            if len(posted_by_user_id.strip()) < 1:
                                posted_by_user_id = posted_user.split("?")[0].split("/")[-2]

                        except:
                            pass

                        try:
                            post_url = data.findAll("span", {"class": "fwb"})[-1].find("a")["href"]
                        except:
                            try:
                                post_url = data.find("div", {"class": "stjgntxs ni8dbmo4"}).find("a")["href"]
                            except:
                                post_url = posted_user
                                pass
                            pass


                        try:
                            post_text = data.find("div", {"class": "text_exposed_root"}).text
                        except:
                            try:
                                post_text = data.find("div", {"style": "text-align: start;"}).text
                            except:
                                post_text = "-"
                                pass
                            pass

                        no_of_like = 0
                        like_love=0
                        like_care=0
                        like_haha=0
                        like_wow=0
                        like_sad=0
                        like_angry=0
                        try:
                            # driver.find_elements_by_xpath('//span[@class="bp9cbjyn j83agx80 b3onmgus"]')[
                            #     i].find_element_by_tag_name("div").click()

                            try:
                                driver.find_elements_by_xpath('//span[@aria-label="See who reacted to this"]')[
                                i].find_element_by_tag_name("div").click()
                            except:
                                driver.find_elements_by_xpath('//span[@aria-label="See who reacted to this"]')[
                                    i].find_element_by_tag_name("a").click()
                                pass

                            time.sleep(4)

                            find_like = 1
                            try:
                                like_soup = soup(driver.page_source, "html.parser")
                                like_data = like_soup.findAll("div", {"class": "bp9cbjyn j83agx80 btwxx1t3 k4urcfbm"})[1]
                                likes = like_data.findAll("div", {"class": "soycq5t1 cgat1ltu"})
                            except:
                                try:
                                    find_like = 2
                                    likes = like_soup.findAll("ul", {"role": "tablist"})[1].findAll("li", {"role": "presentation"})

                                except:
                                    likes = []
                                    pass
                                pass

                            try:
                                driver.find_element_by_xpath("//div[@aria-label='Close']").click()
                            except:
                                try:
                                    driver.find_element_by_xpath("//a[@data-testid='reactions_profile_browser:close']").click()
                                except:
                                    pass
                                pass

                            time.sleep(2)

                            ele = driver.find_elements_by_xpath('//span[@aria-label="See who reacted to this"]')[i]
                            driver.execute_script("arguments[0].scrollIntoView();", ele)
                            time.sleep(1)

                            if find_like == 1:
                                for lk in likes:
                                    try:
                                        like_url = lk.find("img")["src"]
                                        if like_url == "https://static.xx.fbcdn.net/rsrc.php/v3/yU/r/tc5IAx58Ipa.png" or like_url == "https://www.facebook.com/rsrc.php/v3/yH/r/LH87Z6E9R6k.png" :
                                            no_of_like = lk.parent.find("span").text.strip()
                                        elif like_url == "https://static.xx.fbcdn.net/rsrc.php/v3/yK/r/bkP6GqAFgZ_.png" or like_url == "https://www.facebook.com/rsrc.php/v3/y_/r/0j-CFqn6tn2.png":
                                            like_haha = lk.parent.find("span").text.strip()
                                        elif like_url == "https://static.xx.fbcdn.net/rsrc.php/v3/yE/r/MB1XWOdQjV0.png" or like_url == "https://www.facebook.com/rsrc.php/v3/yM/r/uwJNoxxjOjw.png":
                                            like_love = lk.parent.find("span").text.strip()
                                        elif like_url == "https://static.xx.fbcdn.net/rsrc.php/v3/y4/r/1eqxxZX7fYp.png" or "https://www.facebook.com/rsrc.php/v3/yA/r/8gLxrbu8gc7.png":
                                            like_sad = lk.parent.find("span").text.strip()
                                        elif like_url == "https://static.xx.fbcdn.net/rsrc.php/v3/yY/r/PByJ079GWfl.png" or "https://www.facebook.com/rsrc.php/v3/yr/r/II0uCVCHz8X.png":
                                            like_angry = lk.parent.find("span").text.strip()
                                        elif like_url == "https://static.xx.fbcdn.net/rsrc.php/v3/yR/r/QTVmPoFjk5O.png" or "https://www.facebook.com/rsrc.php/v3/ye/r/-p39cn7I6sV.png":
                                            like_care = lk.parent.find("span").text.strip()
                                        elif like_url == "https://static.xx.fbcdn.net/rsrc.php/v3/yS/r/tHO3j6Ngeyx.png" or like_url == "https://www.facebook.com/rsrc.php/v3/y5/r/n7ydRDBQhQx.png":
                                            like_wow = lk.parent.find("span").text.strip()
                                    except:
                                        pass
                            else:
                                try:
                                    for lk in likes:
                                        rect = lk.find("span").find("span")["aria-label"].strip()
                                        if rect.__contains__('with Like'):
                                            no_of_like = rect.split(" ")[0]
                                        elif rect.__contains__('with Haha'):
                                            like_haha = rect.split(" ")[0]
                                        elif rect.__contains__('with Wow'):
                                            like_wow = rect.split(" ")[0]
                                        elif rect.__contains__('with Love'):
                                            like_love = rect.split(" ")[0]
                                        elif rect.__contains__('with Sad'):
                                            like_sad = rect.split(" ")[0]
                                        elif rect.__contains__('with Angry'):
                                            like_angry = rect.split(" ")[0]
                                        elif rect.__contains__('with Care'):
                                            like_care = rect.split(" ")[0]
                                except:
                                    pass
                        except:
                            pass

                        columns = [gp_name, post_desc, post_date, posted_by_user_id, no_of_like, like_love,
                                like_haha, like_wow, like_sad, like_angry, like_care, post_url, post_text]

                        try:
                            driver.find_element_by_xpath("//div[@aria-label='Close']").click()
                        except:
                            try:
                                driver.find_element_by_xpath(
                                    "//a[@data-testid='reactions_profile_browser:close']").click()
                            except:
                                pass
                            pass
                        time.sleep(2)

                        f =  open(root_dir + "/"+group_id+".csv", "a", encoding='utf-8', newline='')
                        csv_writer = csv.writer(f, delimiter=',')
                        csv_writer.writerow(columns)
                        f.close()

                        time.sleep(10)
                except:
                    pass

                # Get old scroll position
                old_position = driver.execute_script(
                    ("return (window.pageYOffset !== undefined) ?"
                     " window.pageYOffset : (document.documentElement ||"
                     " document.body.parentNode || document.body);"))
                # Sleep and Scroll
                time.sleep(3)
                driver.execute_script((
                    "var scrollingElement = (document.scrollingElement ||"
                    " document.body);scrollingElement.scrollTop ="
                    " scrollingElement.scrollHeight;"))
                # Get new position
                new_position = driver.execute_script(
                    ("return (window.pageYOffset !== undefined) ?"
                     " window.pageYOffset : (document.documentElement ||"
                     " document.body.parentNode || document.body);"))

                time.sleep(2)
                i = 0

            time.sleep(10)
            # Get new position
            new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
            i += 1

        print("completed")
        print("completed")

        driver.quit()

    except Exception as e:
        print("error 1: {}".format(str(e)) )
        try:
            driver.quit()
        except:
            pass
        pass






if __name__ == '__main__':
    try:
        root_dir = os.path.dirname(os.path.abspath(__file__))
        user_id = str(input("Enter your User_id: ")).strip()
        password = str(input("Enter your Pasword: ")).strip()

        group_id= str(input("Enter the Group Id: ")).strip()

        fb_post(root_dir, user_id, password, group_id)

    except:
        pass




