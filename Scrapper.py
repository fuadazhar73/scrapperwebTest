from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4 as bs
import csv

#example code for scrapping Handphone from tokopedia

csv_header = ['Product_Name','Price','Description','Image_link','Rating','Name_of_store',]

class tokped_scraper():
    def __init__(self, keyword, PATH, filtered_words=[]):
        self.PATH = PATH # Path to chromedriver.exe
        self.driver = webdriver.Chrome(PATH)
        self.keyword = keyword
        self.pagesource = ""
        self.filtered_words = filtered_words
    
    def search(self):
        self.driver.get("https://www.tokopedia.com/search?&q=handphone&size=100".format(self.keyword))
        self.pagesource = self.driver.page_source

    def scrape(self):
        soup = bs.BeautifulSoup(self.pagesource, "html.parser")

        for i in soup.find_all("div", class_="css-wlcnlb"):
            product_name = i.find_all("div", class_="css-18c4yhp")[0].get_text()
            price = i.find_all("div", class_="css-rhd610")[0].get_text().replace('Rp', '').replace('.', '')
			image_link=i.find_all("div", class_="css-1dpp4z9")[0].get_attr('src')
			description_total_sales = i.find_all("div", class_="css-j3abbo")[0].get_text()
			rating = i.find_all("div", class_="css-etd83i")[0].get_text()
			name_of_store = i.find_all("div", class_="css-4pwgpi")[0].get_text()
            
            # Filtering out the words from list filtered_words
            for i in self.filtered_words:
                if i in product_name:
                    print("{} is in \"{}\"".format(i,product_name))
                    continue

            with open("data.csv","a") as data_file:
                writer = csv.DictWriter(data_file, fieldnames=csv_header)
                writer.writerow({
                    'Product Name': product_name,
                    'Price': price,
					'Image URL' : image_link,
					'Description' : description_total_sales,
					'Rating' : rating,
					'Name of Stroe' : name_of_store
                    })

# Contoh / Example
cari_switch = tokped_scraper(
    "rtx 3090", 
    "C:\\Program Files (x86)\\chromedriver.exe",
    ['2060','2070','GTX','2080'])
cari_switch.search()
cari_switch.scrape()