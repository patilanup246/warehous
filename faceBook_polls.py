from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
from bs4 import BeautifulSoup as soup
import csv


def func_call_1(driver, posts_lst, group_name, group_id, root_dir):
    try:
        post_ele = driver.find_elements_by_xpath("//div[@class='_3ccb']")[-18:]
        # polls_ele = driver.find_elements_by_xpath(".//a[@class='_3coo']")
        for pol_ele in post_ele:
            try:
                ele_1 = pol_ele.find_element_by_xpath(".//a[@class='_3coo']")
                driver.execute_script("arguments[0].scrollIntoView();", pol_ele)
                ele_1.click()
                time.sleep(1)
            except:
                pass

        page_soup = soup(driver.page_source, "html.parser")
        posts_1 = page_soup.findAll("div", {"class": "_3ccb"})[-18:]
        # post_ele = driver.find_elements_by_xpath("//div[@class='_3ccb']")
        print(len(posts_1), len(post_ele))

        # group_name, group_id, Fb_userName, post_date, user_Id, post_url, post_txt, total_comments, share
        for i, data in enumerate(posts_1):
            polls_desc = "-"
            try:
                polls_desc = data.find("div", {"data-testid": "post_message"}).text  # done
            except:
                pass

            polls_options_lst = []

            polls = []
            try:
                polls = data.findAll("div", {"class": "_3cof"})[0].findAll("div", {"class": "_61xb"})
            except:
                pass

            for pol in polls:
                try:
                    pol_txt = pol.find("div", {"class": "_3con"}).text.strip()

                    poll_vote = 0
                    votes = pol.find("div", {"class": "_mb6"}).findAll("li")

                    more_vote = votes[-1].find("a", {"data-hover": "tooltip"})

                    if more_vote:
                        poll_vote = len(votes) - 1 + int(more_vote["data-tooltip-content"].split(" ")[0].strip())

                    polls_options_lst.append({pol_txt + ": " + str(poll_vote)})

                except:
                    pass

            fb_userName = "-"
            try:
                # polls ceated by
                fb_userName = data.findAll("span", {"class": "fwb"})[0].find("a").text
            except:
                pass

            post_dict = {polls_desc[:150], fb_userName}

            if post_dict in posts_lst:
                continue

            posts_lst.append(post_dict)

            total_comments = 0
            share = 0
            try:
                all_comments = data.find("div", {"class": "_3vum"}).findAll("span", {"data-hover": "tooltip"})
                comment = all_comments[-1].text.strip().lower()
                if "share" in comment:
                    share = comment.split(" ")[0].strip()
                    total_comment = all_comments[-2].text.strip().lower()
                    if "comments" in total_comment:
                        total_comments = total_comment.split(" ")[0].strip()

                elif "comments" in comment:
                    total_comments = comment.split(" ")[0].strip()
                    total_comment = all_comments[-2].text.strip().lower()
                    if "share" in total_comment:
                        share = total_comment.split(" ")[0].strip()
            except:
                pass

            fb_userId = "-"
            try:
                fb_userId = data.findAll("span", {"class": "fwb"})[0].find("a")["href"].split("?")[
                    0].split("/")[-1].strip()
                if len(fb_userId) < 1:
                    fb_userId = data.findAll("span", {"class": "fwb"})[0].find("a")["href"].split(
                        "?")[0].split("/")[-2].strip()
            except:
                pass

            likes = 0
            like_love = 0
            like_care = 0
            like_haha = 0
            like_wow = 0
            like_sad = 0
            like_angry = 0
            try:
                driver.execute_script("arguments[0].scrollIntoView();", post_ele[i])
                time.sleep(1)
                try:
                    driver.find_elements_by_xpath('//span[@aria-label="See who reacted to this"]')[
                        i].find_element_by_tag_name("a").click()
                    time.sleep(4)
                except:
                    pass

                likes_lst = []
                try:
                    like_soup = soup(driver.page_source, "html.parser")
                    likes_lst = like_soup.findAll("ul", {"role": "tablist"})[1].findAll("li",
                                                                                        {"role": "presentation"})
                except:
                    pass

                try:
                    driver.find_element_by_xpath("//a[@data-testid='reactions_profile_browser:close']").click()
                    time.sleep(2)
                except:
                    pass

                ele = driver.find_elements_by_xpath('//span[@aria-label="See who reacted to this"]')[i]
                driver.execute_script("arguments[0].scrollIntoView();", ele)
                time.sleep(1)

                try:
                    for lk in likes_lst:
                        rect = lk.find("span").find("span")["aria-label"].strip()

                        if rect.__contains__('with Like'):
                            likes = rect.split(" ")[0]
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

            columns = [group_name, group_id, fb_userName, polls_desc, polls_options_lst,
                       like_haha, likes, like_love, like_wow, like_sad, like_angry, like_care,
                       total_comments, share]

            f = open(root_dir + "/" + group_id + ".csv", "a", encoding='utf-8', newline='')
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(columns)
            f.close()

            try:
                driver.find_element_by_xpath("//a[@data-testid='reactions_profile_browser:close']").click()
                time.sleep(2)
            except:
                pass
    except:
        pass
    return driver


def func_call_2(driver, posts_lst, group_name, group_id, root_dir, ):
    try:
        post_ele = driver.find_elements_by_xpath("//div[@class='_3ccb']")[-18:]
        #polls_ele = driver.find_elements_by_xpath(".//a[@class='_3coo']")
        for pol_ele in post_ele:
            try:
                ele_1 = pol_ele.find_element_by_xpath(".//a[@class='_3coo']")
                driver.execute_script("arguments[0].scrollIntoView();", pol_ele)
                ele_1.click()
                time.sleep(1)
            except:
                pass

        page_soup = soup(driver.page_source, "html.parser")
        posts_1 = page_soup.findAll("div", {"class": "_3ccb"})[-18:]
        # post_ele = driver.find_elements_by_xpath("//div[@class='_3ccb']")
        print(len(posts_1), len(post_ele))

        # group_name, group_id, Fb_userName, post_date, user_Id, post_url, post_txt, total_comments, share
        for i, data in enumerate(posts_1):
            polls_desc = "-"
            try:
                polls_desc = data.find("div", {"data-testid": "post_message"}).text  # done
            except:
                pass

            polls_options_lst = []

            polls = []
            try:
                polls = data.findAll("div", {"class": "_3cof"})[0].findAll("div", {"class": "_61xb"})
            except:
                pass

            for pol in polls:
                try:
                    pol_txt = pol.find("div", {"class": "_3con"}).text.strip()

                    poll_vote = 0
                    votes = pol.find("div", {"class": "_mb6"}).findAll("li")

                    more_vote = votes[-1].find("a", {"data-hover": "tooltip"})

                    if more_vote:
                        poll_vote = len(votes)-1 + int(more_vote["data-tooltip-content"].split(" ")[0].strip())

                    polls_options_lst.append({pol_txt+": "+ str(poll_vote)})

                except:
                    pass

            fb_userName = "-"
            try:
                # polls ceated by
                fb_userName = data.findAll("span", {"class": "fwb"})[0].find("a").text
            except:
                pass

            post_dict = {polls_desc[:150], fb_userName}

            if post_dict in posts_lst:
                continue

            posts_lst.append(post_dict)

            total_comments = 0
            share = 0
            try:
                all_comments = data.find("div", {"class": "_3vum"}).findAll("span", {"data-hover": "tooltip"})
                comment = all_comments[-1].text.strip().lower()
                if "share" in comment:
                    share = comment.split(" ")[0].strip()
                    total_comment = all_comments[-2].text.strip().lower()
                    if "comments" in total_comment:
                        total_comments = total_comment.split(" ")[0].strip()

                elif "comments" in comment:
                    total_comments = comment.split(" ")[0].strip()
                    total_comment = all_comments[-2].text.strip().lower()
                    if "share" in total_comment:
                        share = total_comment.split(" ")[0].strip()
            except:
                pass


            fb_userId = "-"
            try:
                fb_userId = data.findAll("span", {"class": "fwb"})[0].find("a")["href"].split("?")[
                    0].split("/")[-1].strip()
                if len(fb_userId) < 1:
                    fb_userId = data.findAll("span", {"class": "fwb"})[0].find("a")["href"].split(
                        "?")[0].split("/")[-2].strip()
            except:
                pass

            likes = 0
            like_love = 0
            like_care = 0
            like_haha = 0
            like_wow = 0
            like_sad = 0
            like_angry = 0
            try:
                driver.execute_script("arguments[0].scrollIntoView();", post_ele[i])
                time.sleep(1)
                try:
                    driver.find_elements_by_xpath('//span[@aria-label="See who reacted to this"]')[
                        i].find_element_by_tag_name("a").click()
                    time.sleep(4)
                except:
                    pass

                likes_lst = []
                try:
                    like_soup = soup(driver.page_source, "html.parser")
                    likes_lst = like_soup.findAll("ul", {"role": "tablist"})[1].findAll("li", {"role": "presentation"})
                except:
                    pass

                try:
                    driver.find_element_by_xpath("//a[@data-testid='reactions_profile_browser:close']").click()
                    time.sleep(2)
                except:
                    pass

                ele = driver.find_elements_by_xpath('//span[@aria-label="See who reacted to this"]')[i]
                driver.execute_script("arguments[0].scrollIntoView();", ele)
                time.sleep(1)

                try:
                    for lk in likes_lst:
                        rect = lk.find("span").find("span")["aria-label"].strip()

                        if rect.__contains__('with Like'):
                            likes = rect.split(" ")[0]
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

            columns = [group_name, group_id, fb_userName, polls_desc, polls_options_lst,
                       like_haha, likes, like_love, like_wow, like_sad, like_angry, like_care,
                       total_comments, share]

            f = open(root_dir + "/" + group_id + ".csv", "a", encoding='utf-8', newline='')
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(columns)
            f.close()

            try:
                driver.find_element_by_xpath("//a[@data-testid='reactions_profile_browser:close']").click()
                time.sleep(2)
            except:
                pass
    except:
        pass
    return driver



def fb_post(root_dir, user_id, password, group_id):
    try:
        function_1 = True

        option = Options()
        # option.add_argument("--headless")

        driver = webdriver.Chrome(options=option, service_log_path="NUL",
                                  executable_path=root_dir + "/chromedriver.exe")
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

        columns = ["Group Name", "Group ID", "Facebook_UserName", "Poll's Description", "Poll Options",
                   "Haha Reacts", "Likes", "Hearts", "Wow Reacts", "Sad Reacts", "Angry Reacts",
                   "Care Reacts", "Total Comments", "Shares"]

        f = open(root_dir + "/" + group_id + ".csv", "w", encoding='utf-8', newline='')
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(columns)
        f.close()

        try:
            group_name = driver.find_element_by_xpath("//div[@class='tr9rh885']//h2").text
        except:
            try:
                group_name = driver.find_element_by_xpath("//h1[@id='seo_h1_tag']").text.strip()
            except:
                group_name = "-"
            pass

        posts_lst = []
        old_position = 0
        new_position = None

        page_soup = soup(driver.page_source, "html.parser")

        posts_1 = page_soup.findAll("div", {"data-testid": "Keycommand_wrapper_feed_story"})

        if len(posts_1) < 1:
            function_1 = False

        i = 0
        while i < 3:
            while new_position != old_position:
                if function_1 == True:
                    pass
                    #driver = func_call_1(driver, posts_lst, group_name, group_id, root_dir)
                else:
                    driver = func_call_2(driver, posts_lst, group_name, group_id, root_dir)

                time.sleep(5)
                print(len(posts_lst))

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
        print("error 1: {}".format(str(e)))
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

        group_id = str(input("Enter the Group Id: ")).strip()

        fb_post(root_dir, user_id, password, group_id)

    except Exception as e:
        print(e)
        pass
