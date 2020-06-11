#PASSING THE REQUIRED MODULES OF PYTHON TO OPEN A LINK REQUEST AND TO WEB SCRAPE
from urllib.request import urlopen as openReq

from bs4 import BeautifulSoup as bs

#OPENING A .CSV FILE WITH THE NAME ITEMS.CSV
filename = "items.csv"
f = open(filename,"w",encoding = 'utf-8')

f.write("FEEDBACK,SELLER NAME,PRODUCT NAME,PRODUCT PRICE\n")

#OPEN THE URL AND PARSE IT INTO HTML FORMAT
def client(url):
    
    Client = openReq(url)

    feedback_page = Client.read()

    Client.close()

    #RETURNING THE PARSE CODE IN HTML
    return bs(feedback_page,"html.parser")

#GETTING THE PAGES FROM PAGINATION
def pages():
    task_url = "https://www.ebay.com/fdbk/feedback_profile/littlekitty0103?filter=feedback_page:All,period:All&page_id=1&limit=25"

    feedback_bs = client(task_url)

    pages = feedback_bs.find("div",{"class":"footer"})

    total_pages = pages.span.text.split()

    return total_pages


def scrape(page):
    #OPENING THE URL LINK FROM WHERE WE STORED IT AND MAKING IT READABLE 
    #AFTER THAT TERMINATING THE LINK
    task_url = "https://www.ebay.com/fdbk/feedback_profile/littlekitty0103?filter=feedback_page:All,period:All&page_id=" + str(page) +"&limit=25"

    feedback_bs = client(task_url)

    #STORING EACH WHOLE FEEDBACK IN CONTAINERS
    containers = feedback_bs.findAll("div",{"class":"card__feedback-container"})

    #STORING ALL THE TAGS RELATED TO SELLER NAMES IN SELLER_NAMES AS AN ARRAY
    seller_names = feedback_bs.findAll("div",{"class":"card__from"})

    #STORING ALL THE TAGS RELATED TO PRICES OF THE PRODUCT IN PRODUCT_PRICES AS AN ARRAY
    product_prices = feedback_bs.findAll("div",{"class":"card__price"})

    #STORING ALL THE TAGS RELATED TO PRODUCT NAMES IN PRODUCT_NAMES AS AN ARRAY
    product_names = feedback_bs.findAll("div",{"class":"card__item"})

    # pages = feedback_bs.findAll("div",{"class":"footer"})

    index = 0
    for item in containers:
        feedback = item.find("span").text

        if seller_names[index].span["aria-label"] == "Feedback left by buyer.":
            seller_name = "null"

            if product_prices != []:
                product_price = product_prices[0].span.text
                product_prices = product_prices[1:]
            else:
                product_price = "null"
            
            if product_names != []:
                product_name = product_names[0].span.text
                product_names = product_names[1:]
            else:
                product_name = "null"
        
        else:
            seller_name = seller_names[index].a.text
            product_price = "null"
            product_name = "null"
        index+=1
        f.write(feedback.replace(",","-") + "," + seller_name + "," + product_name.replace(",","-") + "," + product_price + '\n')

#DRIVER FUNCTION
def main():
    #CALLING THE FUNCTION PAGES TO GET TOTAL NUMBER OF PAGES
    pages_list = pages()

    total_pages = int(pages_list[-1])

    #SCRAPES EACH PAGE ONE BY ONE
    for page in range(1,total_pages+1):
        scrape(page)
main()

f.close()