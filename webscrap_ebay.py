from urllib.request import urlopen as u_req
from bs4 import BeautifulSoup as soup

ebay_url = "https://www.ebay.com/fdbk/feedback_profile/littlekitty0103?filter=feedback_page:All"

f = open("products.csv","w",encoding = 'utf-8')
f.write("FEEDBACK,SELLER NAME,PRODUCT NAME,PRODUCT PRICE\n") 

u_client = u_req(ebay_url)
page_html = u_client.read()
u_client.close()
page_soup = soup(page_html,"html.parser")

pages = page_soup.find("div",{"class":"footer"})

total_pages = pages.span.text.split()
page_end = int(total_pages[-1])

def next_url(page_number):
    next_url = "https://www.ebay.com/fdbk/feedback_profile/littlekitty0103?filter=feedback_page:All,period:All&page_id=" + str(page_number) +"&limit=25"
    u_client = u_req(next_url)
    page_html = u_client.read()
    u_client.close()
    return page_html
    
def find_all_data(page_html):
    page_soup = soup(page_html,"html.parser")
    containers = page_soup.findAll("div",{"class":"card__feedback-container"})
    sellers = page_soup.find_all("div",{"class":"card__from"})
    prices = page_soup.findAll("div",{"class":"card__price"})
    card_items = page_soup.findAll("div",{"class":"card__item"})
    sell_iter = 0
    for contain in containers:
        feedback = contain.find("span").text
        if sellers[sell_iter].span["aria-label"] == "Feedback left by buyer.":
            seller = "null"

            if len(prices)!=0:
                price = prices[0].span.text
                prices = prices[1:]
            else:
                price = "null"
            
            if len(card_items)!=0:
                product =  card_items[0].span.text
                card_items = card_items[1:]
            else:
                product = "null"
        
        else:
            seller = sellers[sell_iter].a.text
            price = "null"
            product = "null"
        sell_iter += 1   

        f.write(feedback.replace(",","|") + "," + seller + "," + product.replace(",","|") + "," + price + '\n')

def main():
    
    for page_number in range(page_end):
        page_html = next_url(page_number)
        find_all_data(page_html)
        
main()
f.close()








