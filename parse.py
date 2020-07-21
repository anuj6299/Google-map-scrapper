from selenium import webdriver
from urllib.parse import urlencode
import webbrowser
import sqlite3

options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(options=options)

conn = sqlite3.connect('gmap.sqlite')

cur = conn.cursor()

cur.executescript('''
    DROP TABLE IF EXISTS gdata;

    CREATE TABLE gdata(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Name TEXT,
    Rating TEXT,
    Detail TEXT,
    Location TEXT,
    Closing_time TEXT,
    Phone TEXT
    )
    ''')

#url = "https://www.google.com/maps/place/Papa+John's+Pizza/@12.3216081,75.5001326,8z/data=!3m1!4b1!4m5!3m4!1s0x89c2580eaa74451b:0x15d743e4f841e5ed!8m2!3d40.7936551!4d-74.0124687"

#url = "https://www.google.com/maps/place/Lucky+Dhaba/@30.653792,76.8165233,17z/data=!3m1!4b1!4m5!3m4!1s0x390feb3e3de1a031:0x862036ab85567f75!8m2!3d30.653792!4d76.818712"

#gmapsurl = "https://www.google.com/maps/search/?api=1&"
#url = "https://www.google.com/maps/place/Mall+Of+Mysore/@12.2975437,76.6622001,17z/data=!3m1!4b1!4m5!3m4!1s0x3baf7018a81e0e5d:0x5b736aafd8221b5d!8m2!3d12.2975437!4d76.6643888"
place = input("Enter the place : ")

if len(place) == 0:
	place = 'pune'

search = input("What are u looking for? ")

if len(search) == 0:
	search = 'medicals'

mydict = {"query": search, "place":place}

gmapsurl = f"https://www.google.com/maps/search/{search}+near+{place}/"
print(gmapsurl)

url = gmapsurl + urlencode(mydict)


browser.get(url)
#name_element = browser.find_elements_by_class_name("section-result-text-content")

#print('New elemets:',name_element)
no = 1
while True:
    titles = browser.find_elements_by_class_name("section-result-title")
    ratings = browser.find_elements_by_class_name("section-result-rating")
    details = browser.find_elements_by_class_name("section-result-details")
    locations = browser.find_elements_by_class_name("section-result-location")
    openings = browser.find_elements_by_class_name("section-result-opening-hours")
    phone_nos = browser.find_elements_by_class_name("section-result-phone-number")

    #print(type(phone_nos))

    # print('\nphones:',phone_nos)
    # print('\nTitles:',titles)
    # print('\nRatings',ratings)
    # print('\nlocations:',locations)
    # print('\nopenings:', openings)
    # print('\ndetails:', details)
    for title,rating,detail,location,opening,phone in zip(titles,ratings,details,locations,openings,phone_nos):
        print('\nNo :',no)
        print('Tiltle :',title.text)
        print('Rating :',rating.text)
        print('Detail :',detail.text)
        print('Location :',location.text)
        print('Opens at :',opening.text)
        print('Phone no: ',phone.text)
        no += 1
        cur.execute('''INSERT INTO gdata (Name, Rating, Detail, Location, Closing_time, Phone)
            VALUES (?,?,?,?,?,?)''',(title.text,rating.text,detail.text,location.text,opening.text,phone.text,))

    try:
        browser.find_element_by_id("n7lv7yjyC35__section-pagination-button-next").click()
    except:
        conn.commit()
        print("program completed")



# for i1,v in enumerate(name_element):
#     #print(v.text)
#     #print(type(v.text))
#     print()
    
#     l = (v.text).split('\n')
#     print('No:',i1+1)

#     for i,line in enumerate(l):
#         if i == 0:
#             print('Name :',line)
#         if i == 1:
#             print('Rating :',line[0:3])
#         if i == 2:
#             print('Address :',line)
#         if i == 3:
#             print('Phone no :',line[-14:-1].strip())

    
#     #if i1 == 10:
#     	#break

conn.commit()
print("program completed")
#https://www.google.com/maps/place/Sanmati+Medicals/@16.6954157,74.2363717,15z/data=!4m8!1m2!2m1!1smedicals+near+kolhapur!3m4!1s0x3bc1003e081fcf57:0xeb80c5fd882fcf8b!8m2!3d16.6943972!4d74.2422259
'''
name_element = browser.find_elements_by_class_name("section-result-title")
for i in name_element:
    print(i.text)

address_element = browser.find_elements_by_class_name("section-result-details-container")
for i in address_element:
    print(i.text)






name_element = browser.find_elements_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/h1/span[1]')[0]
name = name_element.text
print(name)
# review titles / username / Person who reviews

address_element = browser.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[12]/button/div/div[2]/div[1]')
address = address_element.text //*[@id="pane"]/div/div[1]/div/div/div[8]/button/div/div[2]/div[1]
print(address)

status_element = browser.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[13]/div[1]/div/div[1]/span[1]/span[1]')
status = status_element.text
print(status)

phone_element = browser.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[15]/button/div/div[2]/div[1]')
phone = phone_element.text
print(phone)

stars_element = browser.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[31]/div/div[2]/button')
stars = stars_element.text
print(stars)

review_titles = browser.find_elements_by_class_name("section-review-title")

print([a.text for a in review_titles])

# review text / what did they think

review_text = browser.find_elements_by_class_name("section-review-review-content")

print([a.text for a in review_text])

# get the number of stars

stars = browser.find_elements_by_class_name("section-review-stars")

first_review_stars = stars[0]

active_stars = first_review_stars.find_elements_by_class_name("section-review-star-active")

print(f"the stars the first review got was {len(active_stars)}")'''