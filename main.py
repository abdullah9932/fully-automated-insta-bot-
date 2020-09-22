from selenium import webdriver  
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests as req
from selenium.webdriver.chrome.options import Options
import os
from bs4 import BeautifulSoup as bs
from operator import itemgetter
from datetime import date, datetime
import json,re,lxml,os,random
from langdetect import detect
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


options = Options()
options.add_argument('--headless')
driver=webdriver.Chrome(options=options)
commenttxt="nice"
Username=""
Password=""
data={}
data1={}
data['tags'] = []
data1['inbox']=[]
hashtag_blacklist = [] # list of forbidden hashtags
post_blacklist = [] # list of forbidden catchwords in post text
i=0
like_counter=0
comment_counter=0
follow_counter=0

def login():
    global driver,Username,Password
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    sleep(random.randint(1,10))
    try:
        driver.find_element_by_name('username').send_keys(Username)
        driver.find_element_by_name('password').send_keys(Password)
        driver.find_element_by_name('password').send_keys(Keys.RETURN)
        sleep(random.randint(2,10))
        print("Login successful")
        Username=""
        Password=""
    except:
        pass
    
def loginwrite(U,P):
    try:
        with open("Login.txt",'a') as log:
            log.write(U)
            log.write("\n")
            log.write(P)
            log.write("\n")
            log.close()
    except:
        print("Error in opening file")
        
def loginread():
    global Username,Password,i
    try:
        with open("Login.txt") as log:
            data=log.readlines()
            Username=data[i]
            i+=1
            Password=data[i]
            i=0
            print(Username)
            print(Password)
    except:
        print("Error in opening file")
            

def likepost():
    global driver
    try:
        html_to_parse=str(driver.page_source)
        html=bs(html_to_parse,'lxml')
        div=html.findAll("svg", {"class":"_8-yf5" })
        status=(str(div[0].get("aria-label")))
        if(status =="Like"):
            driver.find_element_by_css_selector('.fr66n .\_8-yf5').click()
            print("liked")
            commentpost()
            savepost()
            like_counter+=1
            comment_counter+=1
        else:
            pass
    except:
        print("Already liked")
        
def commentpost():
    global driver,commenttxt
    try:
        driver.find_element_by_css_selector(".Ypffh").click()
        comment_box = ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Ypffh")))
        comment_box.send_keys(commenttxt)
        sleep(random.randint(1,2))
        comment_box.send_keys(Keys.RETURN)
        sleep(random.randint(1,4))
        
    except:
        print("Commenting is disabled or error")
        
def savepost():
    global driver
    try:
        driver.find_element_by_css_selector(".wmtNn .\_8-yf5").click()
    except:
        print("already saved")
        
def notifications():
    i=0
    global driver,data
    bol=True
    driver.get('https://www.instagram.com/accounts/activity/')
    html_to_parse=str(driver.page_source)
    html=bs(html_to_parse,'lxml')
    div=html.findAll("div", {"class":"YFq-A" })
    time=html.findAll("time", {"class":"HsXaJ Nzb55" })
    usernames=html.findAll("a", {"class":"FPmhX notranslate yrJyr" })
    for i in range (len(div)):
        f= open('data.txt','r+')
        text=div[i].get_text()
        datetime= time[i].get("datetime")
        username= usernames[i].get("title")
        filesize1 = os.path.getsize("data.txt")
        if(re.search('mentioned you in a',text)):
            if filesize1 == 0:
                data['tags'].append({
                'username': username,
                'mentioned': text,
                'datetime': datetime})
                json.dump(data,f,indent=4)
                data.clear()
                i+=1
            else:
                try:
                    mydata = json.load(f)
                    for t in mydata['tags']:
                        if(t['datetime']==datetime):
                            bol=True
                            break
                        else:
                            bol=False
                except:
                    print("file is empty")
            if bol==False:
                    print("Running")
                    mydata['tags'].append({
                    'username': username,
                    'mentioned': text,
                    'datetime': datetime})
                    mydata.update(mydata)
                    f.seek(0)
                    json.dump(mydata,f,indent=4)
                    print("done")
                    data.clear()
                    bol=True
        f.close()
        
def directmessages():
    global driver,data1
    bol=True
    filesize1 = os.path.getsize("directmessage.txt")
    driver.get('https://www.instagram.com/direct/inbox/?hl=en')
    try:
        driver.find_element_by_css_selector(".HoLwm").click()
    except:
        pass
    sleep(5)
    html_to_parse=str(driver.page_source)
    html=bs(html_to_parse,'lxml')
    div=html.findAll("div", {"class":"DPiy6 Igw0E IwRSH eGOV_ _4EzTm" })
    txt=html.findAll("div", {"class": "_7UhW9 xLCgt MMzan KV-D4 fDxYl"})#name
    msg=html.findAll("span",{"class": "_7UhW9 xLCgt qyrsm KV-D4 se6yk"})#text
    time=html.findAll("time", {"class":"W5HcT Nzb55" })#datetime
    j=0
    for i in range (len(div)):
        f= open('directmessage.txt','r+')
        unseen=div[i].findAll("div", {"class":"_41V_T Sapc9 Igw0E IwRSH eGOV_ _4EzTm"})#div with blue marker
        if not unseen:      
            continue
        else:
            msgs=msg[j].get_text()
            print(msgs)
            j+=1
            name=txt[i].get_text()
            datetime= time[i].get("datetime")
            if filesize1 == 0:
                data1['inbox'].append({
                'username': name,
                'datetime': datetime,
                'message': msgs
                })
                json.dump(data1,f,indent=4)
                data1.clear()
                i+=1
    
            else:
                try:
                    mydata = json.load(f)
                    for t in mydata['inbox']:
                        if(t['datetime']==datetime):
                            bol=True
                            break
                        else:
                            bol=False
                except:
                    print("file is empty")
            if bol==False:
                    print("Unread message from:",name)
                    mydata['inbox'].append({
                    'username': name,
                    'datetime': datetime,
                    'message': msgs})
                    mydata.update(mydata)
                    f.seek(0)
                    json.dump(mydata,f,indent=4)
                    mydata.clear()
                    bol=True

                    
def followUser():
    global driver,follow_counter
    file=open("post.txt",'r')
    try:
        mydata = json.load(file)
        print("file is loaded")
        for t in mydata['post']:
            if(t['status']=="good post"):
                print("goodpost found")
                shortcode=t['shortcode']
                driver.get("https://www.instagram.com/p/"+shortcode+"/")
                sleep(random.randint(5,20))
                likepost()
                sleep(random.randint(1,2))
                del t
                try:
                
                    driver.find_element_by_xpath("//div[2]/div/div/a").click()
                    sleep(random.randint(2,10))
                except:
                    print("not working")
                    pass
                try:
                    sleep(random.randint(2,10))
                    driver.find_element_by_xpath("//button[contains(.,'Follow')]").click()#followuser
                    sleep(random.randint(2,10))
                    follow_counter+=1
                except:
                    print("already following")
                sleep(random.randint(2,10))

                followfollowersfollower()
                likefolloweduserfirstpic()
            else:
                continue
    except:
        pass
            
def followfollowersfollower():
    global driver,follow_counter
    try:
        driver.find_element_by_xpath("//li[3]/a").click() #followingclicked
        sleep(random.randint(2,10))
        try:
            driver.find_element_by_css_selector("li:nth-child(1).sqdOP").click()
            sleep(random.randint(3,150))
            follow_counter+=1
        except:
            print("already followed")
        try:
            driver.find_element_by_css_selector("li:nth-child(2).sqdOP").click()
            sleep(random.randint(3,150))
            follow_counter+=1
        except:
            print("already following")
        try:
            driver.find_element_by_css_selector("li:nth-child(3).sqdOP").click()
            sleep(random.randint(3,150))
            follow_counter+=1
        except:
            print("already following")
        try:
            driver.find_element_by_css_selector("li:nth-child(4).sqdOP").click()
            sleep(random.randint(3,150))
            follow_counter+=1
        except:
            print("already following")
        try:
            driver.find_element_by_css_selector("li:nth-child(5).sqdOP").click()
            sleep(random.randint(3,150))
            follow_counter+=1
        except:
            print("already following")
    except:
        print("unable to open following")

def likefolloweduserfirstpic():
    global driver
    try:
        html_to_parse=str(driver.page_source)
        html=bs(html_to_parse,'lxml')
        div=html.findAll("div", {"class":"v1Nh3 kIKUG _bz0w" })
        n=random.randint(3,6)
        for i in range(n):
            username=div[i]
            usrname=re.findall('<[a][^>]*>', str(username))
            char=(str(usrname[0]).replace('<a href="', ''))
            foo = char[:-2]
            print(foo)
            driver.get("https://www.instagram.com/"+foo)
            sleep(random.randint(3,20))
            likepost()#liked first post
    except:
        print("unable to open first post")
        
def searchposts(tag):
    
    global driver,request
    bol=True
    filesize1 = os.path.getsize("post.txt")
    data={}
    mydata1={}
    mydata1['post'] = []
    word=str(tag.rstrip())
    driver.get("https://www.instagram.com/explore/tags/"+word+"/?__a=1")
    html_to_parse=str(driver.page_source)
    data=bs(html_to_parse,'lxml').text
    res = json.loads(data)
    length=len(res['graphql']['hashtag']['edge_hashtag_to_media']['edges'])
    
    for i in range(length):
        
        f= open('post.txt','r+')
        try:
            timestamp=res['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['taken_at_timestamp']
            shortcode=res['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['shortcode']
            media_id=res['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['id']
            post_text=res['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['edge_media_to_caption']['edges'][0]['node']['text']
            timestamp_date = datetime.fromtimestamp(timestamp).date()
            returns_of_data=search_filter(shortcode,media_id,timestamp_date,post_text)
        except:
            pass

        if filesize1 == 0:
                mydata1['post'].append({
                'shortcode': returns_of_data[0],
                'media_id': returns_of_data[1],
                'status': returns_of_data[2],
                'datetime': returns_of_data[3]})
                json.dump(mydata1,f,indent=4)
                mydata1.clear()
                i+=1
                continue
        else:
            try:
                mydata = json.load(f)
                for t in mydata['post']:
                    if(t['media_id']==media_id):
                        bol=True
                        break
                    else:
                        bol=False
                        
            except:
                print("file is empty")
                    
        if bol==False:
            mydata['post'].append({
            'shortcode': returns_of_data[0],
            'media_id': returns_of_data[1],
            'status': returns_of_data[2],
            'datetime': returns_of_data[3]})
            mydata.update(mydata)
            f.seek(0)
            json.dump(mydata,f,indent=4)
            mydata.clear()
            bol=True
      
def search_filter(short_code, media_id, timestamp_date, post_text):
    # blacklists
    post_text_lowered = post_text.lower()
    post_text_cleaned = post_text_lowered.encode('ascii', 'ignore').decode('ascii')

    # detect language of post text
    try:
        post_text_lang = detect(post_text)
    except:
        post_text_lang = ''
        
    # find all hashtags in post text
    post_tags = list(set(re.findall(r'#([^\s#]+)', post_text_lowered)))

    # filter by language, timestamp, hashtags and post text catchwords
    if post_text_lang not in ('de', 'en'):
        output = [short_code, media_id, 'wrong language', str(datetime.now())]
    elif (date.today()-timestamp_date).days > 3:
        output = [short_code, media_id, 'too old', str(datetime.now())]
    elif any(t in post_tags for t in hashtag_blacklist):
        output = [short_code, media_id, 'hashtag blacklisted', str(datetime.now())]
    elif any(p in post_text_cleaned for p in post_blacklist):
        output = [short_code, media_id, 'post text blacklisted', str(datetime.now())]
    else:
        output = [short_code, media_id, 'good post', str(datetime.now())]

    return output

def hashtag():
    file= open("hashtags.txt",'r')
    tags=file.readlines()
    for i in tags:
        searchposts(i)
       
def main():
    global nooflinks,browser,commenttxt,Username,Password
    
    try:
        filesize = os.path.getsize("Login.txt")
        if filesize == 0:
            Username=input("Username: ")
            Password=input("Password: ")
            loginwrite(Username,Password)
        else:
            loginread()
    except:
        print("Cannot find the log file")
    sleep(2)
    try:
        login()
        followUser()
        sleep(random.randint(3,150))
        while True: 
            notifications()
            sleep(random.randint(3,150))
            directmessages()
            sleep(random.randint(5600,9000))
            now = datetime.now()
            current_time = now.strftime("%H")
            if (current_time>=15):
                    hashtag()
                    followUser()
            if(current_time==24 or current_time==1):
                sleep(28800)       
    except:
        pass
        
                 
if __name__ == "__main__":
    main()

