from selenium import webdriver
#from urllib.request import urlopen as u_req
from bs4 import BeautifulSoup as soup
import time


driver = webdriver.Chrome("C:\chromedriver.exe")
url = "https://www.ebay.com/fdbk/feedback_profile/littlekitty0103?filter=feedback_page:All"
driver.get(url)
time.sleep(2)

#To Change item per page
item_per_page = driver.find_element_by_xpath('//*[@id="mainContent"]/section[1]/section[2]/section/div[5]/div[3]/div/button[4]')
item_per_page.click()
time.sleep(2)
#To find number of pages
number_of_pages = driver.find_element_by_xpath('//*[@id="mainContent"]/section[1]/section[2]/section/div[5]/div[1]/span').text
number_of_pages = int(number_of_pages.split()[-1])


f=open("products.csv","w")

def run(number_of_pages):
    print("Data collection started ......")

    for _ in range(1,number_of_pages):
        page_soup = soup(driver.page_source, 'html.parser')
        card_notice = page_soup.find("table",{"id":"feedback-cards"})
        card_elements = card_notice.find("tbody")
        card_elements = card_elements.findAll("tr")

        for element in card_elements:

            notice = element.find("div",{"class":"card__notice"})
            if notice:
                    print(notice.text)
            else:    
                feedback = "null"
                price = "null"
                seller = "null"
                product = "null"
                containers = element.find("div",{"class":"card__feedback-container"})
                sellers = element.find("div",{"class":"card__from"})
                prices = element.find("div",{"class":"card__price"})
        
                if containers:
                    spans = containers.findAll("span")
                
                    if len(spans)>2:
                        feedback = spans[0]["aria-label"]
                        product = spans[-2].text
                        color = containers.find("div",{"class":"card__item"})
                        product += color.a.text + ")"
                    elif len(spans) ==2:
                        feedback = spans[0]["aria-label"]
                        product = spans[-1].text 
                    else:
                        feedback = spans[0]["aria-label"]  
                if sellers:
                    if  sellers.a:
                       seller=sellers.a.get_text()
                 
                    elif prices:
                        price = prices.span.text  
                print(feedback)
   
                f.write(feedback.replace(",","|") +"," + price.replace(",","|") + "," +seller.replace(",","|") + ',' + product.replace(",","|") + "\n") 
        next_button = driver.find_element_by_class_name("pagination__next")
        next_button.click()
        time.sleep(3)  
    print("Data saved successfully")  
f.close()    
run(number_of_pages)

