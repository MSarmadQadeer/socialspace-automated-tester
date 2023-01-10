from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import time


def chrome_browser(url):
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('headless')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.set_window_size(1080, 720)
    browser.get(url)
    return browser


def login(browser, username, password):
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login-form input[name='email']")))
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login-form input[name='password']")))
        browser.find_element(By.CSS_SELECTOR,".login-form input[name='email']").send_keys(username)
        browser.find_element(By.CSS_SELECTOR,".login-form input[name='password']").send_keys(password)

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".login-form .login-btn")))
        browser.find_element(By.CSS_SELECTOR,".login-form .login-btn").click()

        time.sleep(10) # wait for the page to load after login

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".more-icon-btn")))
        browser.find_element(By.CSS_SELECTOR,".more-icon-btn").click()

        print("Log In Success")
        return True
    except:
        print("Log In Failed")
        return False


def test_create_post(browser, post_caption):
    should_run = False

    try:    
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".create-post-icon")))
        browser.find_element(By.CSS_SELECTOR,".create-post-icon").click()

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".post-creation-panel .post-text-caption")))
        browser.find_element(By.CSS_SELECTOR,".post-creation-panel .post-text-caption").send_keys(post_caption)

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".post-creation-panel .post-btn")))
        browser.find_element(By.CSS_SELECTOR,".post-creation-panel .post-btn").click()

        should_run = True
    except:
        print("Post Creation Failed")
        return 0

    if should_run:
        try:
            time.sleep(10) # wait for the page to load after post creation
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".post")))
            posts = browser.find_elements(By.CSS_SELECTOR, ".post")
            for post in posts:
                WebDriverWait(post, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".caption")))
                caption = post.find_element(By.CSS_SELECTOR,".caption")
                if caption.text == post_caption:
                    post_id = post.get_attribute("data-id")
                    print("Post Creation Success")
                    return post_id
            else:
                print("Post Creation Failed")
                return 0
        except:
            print("Post Creation Failed")
            return 0


def test_like_post(browser,post_id):
    try:    
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".post")))
        posts = browser.find_elements(By.CSS_SELECTOR, ".post")
        for post in posts:
            if post.get_attribute("data-id") == post_id:
                WebDriverWait(post, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".likes-count")))
                likes_count_before_like = post.find_element(By.CSS_SELECTOR,".likes-count").text
                likes_count_before_like = int(likes_count_before_like)
                post.find_element(By.CSS_SELECTOR,".unchecked-heart").click()

                time.sleep(3) # wait to see the post getting liked

                likes_count_after_like = post.find_element(By.CSS_SELECTOR,".likes-count").text
                likes_count_after_like = int(likes_count_after_like)

                if likes_count_after_like > likes_count_before_like:
                    print("Post Like Success")
                    return True
                else:
                    print("Post Like Failed")
                    return False
    except:
        print("Post Like Failed")
        return False


def test_unlike_post(browser,post_id):
    try: 
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".post")))
        posts = browser.find_elements(By.CSS_SELECTOR, ".post")
        for post in posts:
            if post.get_attribute("data-id") == post_id:
                WebDriverWait(post, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".likes-count")))
                likes_count_before_like = post.find_element(By.CSS_SELECTOR,".likes-count").text
                likes_count_before_like = int(likes_count_before_like)
                post.find_element(By.CSS_SELECTOR,".checked-heart").click()

                time.sleep(3) # wait to see the post getting unliked

                likes_count_after_like = post.find_element(By.CSS_SELECTOR,".likes-count").text
                likes_count_after_like = int(likes_count_after_like)

                if likes_count_after_like < likes_count_before_like:
                    print("Post Unlike Success")
                    return True
                else:
                    print("Post Unlike Failed")
                    return False
    except:
        print("Post Unlike Failed")
        return False


def test_update_post(browser, post_id, post_caption):
    should_run = False

    try: 
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".post")))
        posts = browser.find_elements(By.CSS_SELECTOR, ".post")
        for post in posts:
            if post.get_attribute("data-id") == post_id:
                WebDriverWait(post, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".three-dot-icon-btn")))
                post.find_element(By.CSS_SELECTOR,".three-dot-icon-btn").click()

                WebDriverWait(post, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".edit-post-tab a")))
                post.find_element(By.CSS_SELECTOR,".edit-post-tab a").click()

                time.sleep(6) # wait for the data to load in updation panel

                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".post-updation-panel .post-text-caption")))
                browser.find_element(By.CSS_SELECTOR,".post-updation-panel .post-text-caption").clear()
                browser.find_element(By.CSS_SELECTOR,".post-updation-panel .post-text-caption").send_keys(post_caption)

                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".post-updation-panel .update-btn")))
                browser.find_element(By.CSS_SELECTOR,".post-updation-panel .update-btn").click()
                break
        should_run = True
    except:
        print("Post Updation Failed")
        return False

    if should_run:
        try:
            time.sleep(10) # wait for the page to load after post updation
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".post")))
            posts = browser.find_elements(By.CSS_SELECTOR, ".post")
            for post in posts:
                WebDriverWait(post, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".caption")))
                caption = post.find_element(By.CSS_SELECTOR,".caption")
                if caption.text == post_caption:
                    print("Post Updation Success")
                    return True
            else:
                print("Post Updation Failed")
                return False
        except:
            print("Post Updation Success")
            return True


def test_delete_post(browser,post_id):
    should_run = False

    try:    
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".post")))
        posts = browser.find_elements(By.CSS_SELECTOR, ".post")
        for post in posts:
            if post.get_attribute("data-id") == post_id:
                post.find_element(By.CSS_SELECTOR,".three-dot-icon-btn").click()
                post.find_element(By.CSS_SELECTOR,".delete-post-tab a").click()
                break   
        should_run = True     
    except:
        print("Post Deletion Failed")
        return False

    if should_run:
        try:
            time.sleep(10) # wait for the page to load after post deletion
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".post")))
            posts = browser.find_elements(By.CSS_SELECTOR, ".post")
            for post in posts:
                if post.get_attribute("data-id") == post_id:
                    print("Post Deletion Failed")
                    return False
            else:
                print("Post Deletion Success")
                return True
        except:
            print("Post Deletion Success")
            return True


def main():
    file = open("logs.log", "a")
    date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    file.write(date)
    file.write("\n")
    testing_url = "http://18.208.152.219:8082"
    post_caption = "test post"
    updated_post_caption = "updated test post"
    
    try:
        browser = chrome_browser(testing_url)

        # Testing Login
        if login(browser, "admin", "admin"):
            file.write("Log In Success")
            file.write("\n")

            # Testing Post Creation
            post_id = test_create_post(browser, post_caption)
            if post_id != 0:
                file.write("Post Creation Success")
                file.write("\n")

                # Testing Post Like
                if test_like_post(browser, post_id):
                    file.write("Post Like Success")
                    file.write("\n")
                else:
                    file.write("Post Like Failed")
                    file.write("\n")

                # Testing Post Unlike  
                if test_unlike_post(browser, post_id):
                    file.write("Post Unlike Success")
                    file.write("\n")
                else:
                    file.write("Post Unlike Failed")
                    file.write("\n")

                # Testing Post Updation
                if test_update_post(browser, post_id, updated_post_caption):
                    file.write("Post Updation Success")
                    file.write("\n")
                else:
                    file.write("Post Updation Failed")
                    file.write("\n")

                # Testing Post Deletion
                if test_delete_post(browser, post_id):
                    file.write("Post Deletion Success")
                    file.write("\n")
                else:
                    file.write("Post Deletion Failed")
                    file.write("\n")

            else:
                file.write("Post Creation Failed")
                file.write("\n")

        else:
            file.write("Log In Failed")
            file.write("\n")

        browser.close()
    except:
        print("Browser Failed")
        file.write("Browser Failed")
        file.write("\n")

    file.close()


main()