from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv
import os
import re



def get_users(new_driver, url_post_lst, root_dir):
    try:
        # Open a new tab-window
        # This does not change focus to the new window for the driver.
        new_driver.execute_script("window.open('');")
        for url in url_post_lst:
            try:
                # Switch to the new tab-window
                new_driver.switch_to.window(new_driver.window_handles[1])

                # open url in new tab window
                new_driver.get(url)

                time.sleep(2)

                try:
                    photo_text = new_driver.find_elements_by_xpath("//h2[@class='_6lAjh ']/following::span")[0].text

                    remove_txt_lst = new_driver.find_elements_by_xpath("//a[@class=' xil3i']")

                    for rmv_txt in remove_txt_lst:
                        try:
                            photo_text = photo_text.replace(rmv_txt.text.strip(), "")
                        except:
                            pass
                    photo_text = photo_text.strip()

                except:
                    photo_text = "-"
                    pass

                try:
                    location = new_driver.find_elements_by_xpath("//a[@class='O4GlU']")[0].text
                    location = location.strip()
                except:
                    location = "-"
                    pass

                data_url = new_driver.find_elements_by_xpath('//*[@class="e1e1d"]/a')[0].get_attribute("href")

                new_driver.get(data_url)
                time.sleep(2)

                followers_lst = new_driver.find_elements_by_xpath('//ul[@class="k9GMp "]/li/a/span')

                if len(followers_lst)<3:
                    followers = new_driver.find_elements_by_xpath('//ul[@class="k9GMp "]/li/a/span')[0].text
                else:
                    followers = new_driver.find_elements_by_xpath('//ul[@class="k9GMp "]/li/a/span')[1].text

                try:
                    name = new_driver.find_element_by_xpath('//h1[@class="rhpdm"]').text
                except:
                    name = "-"
                    pass

                try:
                    bio = new_driver.find_elements_by_xpath('//div[@class="-vDIg"]/span')[0].text
                except:
                    bio='-'
                    pass

                user_name = data_url.split("/")[-2]

                photo_url = url

                driver_source = new_driver.page_source

                try:
                    id = re.findall(r'"owner":{"id":"(.+?)"', driver_source)[0]
                except:
                    id = "-"
                    pass

                try:
                    link_in_bio = re.findall(r'"external_url":"(.+?)"', driver_source)[0]
                except:
                    link_in_bio = "-"

                columns = [id, user_name, name, followers, link_in_bio, bio, photo_url, location, photo_text]

                f = open(root_dir + "/sample.csv", "a", encoding='utf-8', newline='')
                csv_writer = csv.writer(f, delimiter=',')
                csv_writer.writerow(columns)
                f.close()

            except:
                pass

        try:
            # close the active tab
            new_driver.close()

            # Switch back to the first tab
            new_driver.switch_to.window(new_driver.window_handles[0])

        except:
            pass

    except:
        try:
            # close the active tab
            new_driver.close()
            # Switch back to the first tab
            new_driver.switch_to.window(new_driver.window_handles[0])
        except:
            pass
        pass


def instagram_email_scrap(driver, root_dir):
    try:
        columns = ["id", "username", "name", "followers", "link in bio", "bio", "photo URL", "location", "photo text"]

        f =  open(root_dir + "/sample.csv", "w", encoding='utf-8', newline='')
        csv_writer = csv.writer(f, delimiter = ',')
        csv_writer.writerow(columns)
        f.close()

        all_post_lst = []

        ## 3. scroll window (in infinite-loop)
        old_position = 0
        new_position = None
        i = 0
        while i < 3:
            while new_position != old_position:
                try:
                    post_lst = driver.find_elements_by_xpath('//*[@class="v1Nh3 kIKUG  _bz0w"]/a')

                    url_lst = []
                    for a_tag in post_lst:
                        link = a_tag.get_attribute("href")

                        if link in all_post_lst:
                            continue

                        all_post_lst.append(link)
                        url_lst.append(link)

                    get_users(driver, url_lst, root_dir)

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

            time.sleep(5)
            i +=1

        try:
            driver.quit()
        except:
            pass

    except:
        try:
            driver.quit()
        except:
            pass
        pass


def get_driver(root_dir):
    try:
        # open the chrome driver
        options = Options()
       # options.add_argument("--headless")

        driver = webdriver.Chrome(service_log_path='NUL', options=options,
                                  executable_path=root_dir + '/chromedriver.exe')

        driver.maximize_window()
        return driver

    except:
        pass


# open the chrome driver, check the user input validations
def main():
    try:
        # user id  & user password input
        user_id = str(input("Enter the user id: ")).strip()
        user_password = str(input("Enter the user password: ")).strip()

        root_dir = os.path.dirname(os.path.abspath(__file__))

        driver = get_driver(root_dir)

        driver.get("https://www.instagram.com/")
        time.sleep(5)

        driver.find_element_by_name("username").send_keys(user_id)
        driver.find_element_by_name("password").send_keys(user_password)

        # user input length validation
        try:
            driver.find_element_by_css_selector(".L3NKy > div:nth-child(1)").click()
        except:
            print("sorry!!!  invalid credentials")
            driver.quit()
            return

        time.sleep(4)

        # validate the user input
        try:
            if len(driver.find_elements_by_id("slfErrorAlert")) > 0:
                print("sorry!!!  invalid credentials")
                driver.quit()
                return

        except:
            pass
        time.sleep(1)

        try:
            driver.find_element_by_xpath("//div[@class='cmbtv']//button").click()
        except:
            pass
        time.sleep(1)

        try:
            driver.find_elements_by_xpath("//div[@class='mt3GC']//*[contains(text(), 'Not Now')]")[0].click()
        except:
            pass
        time.sleep(1)

        driver.get("https://www.instagram.com/explore/tags/healthychef/")
        time.sleep(4)

        instagram_email_scrap(driver, root_dir)

        try:
            driver.quit()
        except:
            pass

    except:
        try:
            driver.quit()
        except:
            pass
        pass


if __name__ == '__main__':
    main()