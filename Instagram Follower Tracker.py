import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_data(): #Logs in and scrapes your list of follower and following accounts.

    username = str(input("Enter your Instagram username: "))
    password = str(input("Enter your Instagram password: "))
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.instagram.com/" + username + "/followers/")
    driver.implicitly_wait(30)
    time.sleep(2)
    username_login = driver.find_element(by=By.NAME, value='username')
    username_login.send_keys(username)
    password_login = driver.find_element(by=By.NAME, value='password')
    password_login.send_keys(password)
    login_button = driver.find_element(by=By.CLASS_NAME, value="sqdOP.L3NKy.y3zKF")
    login_button.click()
    time.sleep(4)
    not_now_button = driver.find_element(by=By.CLASS_NAME, value="sqdOP.yWX7d.y3zKF")
    not_now_button.click()
    time.sleep(4)
    
    followers_button = driver.find_element(by=By.PARTIAL_LINK_TEXT, value=(" followers"))
    follower_num = int(followers_button.text.strip(" followers").replace(',', ''))
    followers_button.click()
    time.sleep(4)
    followers_window = driver.find_element(by=By.CLASS_NAME, value="isgrP")

    for x in range(follower_num//3):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', followers_window)
        time.sleep(0.5)
        
    follower_usernames = driver.find_elements(by=By.CLASS_NAME, value="_7UhW9.xLCgt.qyrsm.KV-D4.se6yk.T0kll")
    follower_counter = 0
    
    with open("FollowersUsernames.txt", 'w', encoding='UTF-8') as f1:
        for names in follower_usernames:
            if follower_counter < follower_num:
                f1.write(names.text)
                f1.write('\n')
                follower_counter += 1
            else:
                follower_counter == follower_num
                break
    f1.close()

    with open("FollowersUsernames.txt", 'a', encoding='UTF-8') as f1:
        last_user = driver.find_elements(by=By.CLASS_NAME, value="_7UhW9.xLCgt.qyrsm.KV-D4.se6yk.T0kll")[-1]
        f1.write(last_user.text)
    
    f1.close()

    exit = driver.find_element(by=By.CSS_SELECTOR, value="svg[aria-label='Close']")
    exit.click()
    time.sleep(1)
    
    following_button = driver.find_element(by=By.PARTIAL_LINK_TEXT, value=(" following"))
    following_num = int(following_button.text.strip(" following").replace(',', ''))
    following_button.click()
    time.sleep(4)
    following_window = driver.find_element(by=By.CLASS_NAME, value="isgrP")

    for x in range(following_num//3):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', following_window)
        time.sleep(0.5)
        
    following_usernames = driver.find_elements(by=By.CLASS_NAME, value="_7UhW9.xLCgt.qyrsm.KV-D4.se6yk.T0kll")
    following_counter = 0

    with open("FollowingUsernames.txt", 'w', encoding='UTF-8') as f2:
        for names in following_usernames:
            if following_counter < following_num:
                f2.write(names.text)
                f2.write('\n')
                following_counter += 1
            else:
                following_counter == following_num
                break
    f2.close()

    with open("FollowingUsernames.txt", 'a', encoding='UTF-8') as f2:
        last_user = driver.find_elements(by=By.CLASS_NAME, value="_7UhW9.xLCgt.qyrsm.KV-D4.se6yk.T0kll")[-1]
        f2.write(last_user.text)
    
    f2.close()

    driver.quit()

def sort_data(): #Compares followers to following accounts to see which do not follow the user back.
    line_list = []

    with open("FollowersUsernames.txt", 'r', encoding='UTF-8') as f1:
        with open("FollowingUsernames.txt", 'r', encoding='UTF-8') as f2:
            with open("UncommonFollowers.txt", 'w', encoding='UTF-8') as f3:
                for line in f1:
                    line_list.append(line.strip('\n'))
                for line in f2:
                    if line.strip('\n') not in line_list:
                        f3.write(line)
    
    f1.close()
    f2.close()
    f3.close()

if __name__ == "__main__":
    get_data()
    sort_data()
    print("COMPLETE: Please view uncommon followers.")
