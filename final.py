from selenium import webdriver
import time
import pandas
driver = webdriver.Chrome("C:\chromedriver.exe")
driver.get("https://www.ebay.com/fdbk/feedback_profile/littlekitty0103?filter=feedback_page:All")
time.sleep(2)

#To Change item per page
item_per_page = driver.find_element_by_xpath('//*[@id="mainContent"]/section[1]/section[2]/section/div[5]/div[3]/div/button[4]')
item_per_page.click()

#To find number of pages
number_of_pages = driver.find_element_by_xpath('//*[@id="mainContent"]/section[1]/section[2]/section/div[5]/div[1]/span').text
number_of_pages = int(number_of_pages.split()[-1])
#print(number_of_pages)
#To store the data in csv file


f=open("products.csv","w")
def run(number_of_pages):
    feedback_list=[]
    product_list =[]
    seller_list = []
    price_list = []
    for _ in range(1,number_of_pages):
        #Data container list
        feedback_container = driver.find_elements_by_class_name("card__comment")
        product_container = driver.find_elements_by_class_name("card__item")
        seller_container = driver.find_elements_by_class_name("card__from")
        price_container = driver.find_elements_by_class_name("card__price")

        
        feed = driver.find_elements_by_class_name("card__feedback-container")

        #storing data into a list
        
        #feedback_list += [feedback.text for feedback in feedback_container]

        #product_list += [product.text for product in product_container]

        #seller_list += [seller.text for seller in seller_container]

        #price_list += [price.text for price in price_container]
    
        #next_button = driver.find_element_by_class_name("pagination__next")
        #next_button.click()
        time.sleep(3)            

    '''products = pandas.DataFrame(
    {"FEEDBACK":feedback_list,
     "PRICE":price_list,
     "SELLER NAME":seller_list,
     "PRODUCT NAME":product_list,
     })    
    products.to_csv("Reviews.csv") '''
    print("data collected Succesfully")
run(number_of_pages)
