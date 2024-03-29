import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_data(): #Logs in and scrapes your list of follower and following accounts.

    username = str(input("Enter your Instagram username: "))
    password = str(input("Enter your Instagram password: "))
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.instagram.com/login")
    driver.implicitly_wait(30)
    time.sleep(2)

    username_login = driver.find_element(by=By.NAME, value='username')
    username_login.send_keys(username)
    password_login = driver.find_element(by=By.NAME, value='password')
    password_login.send_keys(password)
    login_button = driver.find_element(by=By.CLASS_NAME, value="_acan._acap._acas._aj1-")
    time.sleep(1)
    login_button.click()
    time.sleep(4)
    print("Login Clicked")

    not_now_button = driver.find_element(by=By.CLASS_NAME, value="_acan._acao._acas._aj1-")
    if not_now_button:
        time.sleep(1)
        not_now_button.click()
        time.sleep(4)
        print("Not Now Clicked")

    goback = driver.find_element(by=By.CLASS_NAME, value="x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz._a6hd")
    if goback:
        time.sleep(1)
        goback.click()
        time.sleep(4)
        print("Go Back Clicked")
    
    not_now_button_again = driver.find_element(by=By.CLASS_NAME, value="_a9--._a9_1")
    if not_now_button_again:
        time.sleep(1)
        not_now_button_again.click()
        time.sleep(4)
        print("Not Now Clicked")

    driver.get("https://www.instagram.com/" + username + "/followers/")
    time.sleep(4)
    print("Not Now Clicked")

    followers_button = driver.find_element(by=By.PARTIAL_LINK_TEXT, value=(" followers"))
    follower_num = int(followers_button.text.strip(" followers").replace(',', ''))
    time.sleep(4)

    followers_window = driver.find_element(by=By.CLASS_NAME, value="_aano")

    for x in range(follower_num//3):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', followers_window)
        time.sleep(0.5)
        
    follower_usernames = driver.find_elements(by=By.CLASS_NAME, value="_aacl._aaco._aacw._aacx._aad7._aade")
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

    exit = driver.find_element(by=By.CSS_SELECTOR, value="svg[aria-label='Close']")
    exit.click()
    time.sleep(1)
    
    following_button = driver.find_element(by=By.PARTIAL_LINK_TEXT, value=(" following"))
    following_num = int(following_button.text.strip(" following").replace(',', ''))
    following_button.click()
    time.sleep(2)

    following_window = driver.find_element(by=By.CLASS_NAME, value="_aano")

    for x in range(following_num//3):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', following_window)
        time.sleep(0.5)
        
    following_usernames = driver.find_elements(by=By.CLASS_NAME, value="_aacl._aaco._aacw._aacx._aad7._aade")
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
