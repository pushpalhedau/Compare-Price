import requests
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url_input = request.form['user_input']
        final_input = url_input.replace(" ", "+").strip()
        url = "https://www.google.com/search?q="+final_input+"&sca_esv=569740195&rlz=1C1VDKB_enIN928IN928&tbm=shop"
#print(url)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, "lxml")

        product_name = soup.find_all("h3", class_ = "tAxDx")
        product_list = []
        for i in product_name:
            name = i.text
            product_list.append(name)
#print(product_list)

        product_price = soup.find_all("span", class_ = "a8Pemb OFFNJ")
        price_list = []
        for i in product_price:
            price = i.text
            price_list.append(price)
#print(price_list)

        product_source = soup.find_all("div", class_ = "aULzUe IuHnof")
        source_list = []
        for i in product_source:
            source = i.text
            source_list.append(source)
#print(source_list)

        link_list = [a['href'] for a in soup.find_all('a', class_='Lq5OHe eaGTj translate-content')]
        new_list = [item.replace("/url?url=", "").strip() for item in link_list]
        final_list = [60]
        final_list = ["https://www.google.com" + element if not element.startswith("https") else element for element in new_list]
#print(new_list)

        df = pd.DataFrame({"PRODUCT":product_list, "PRICE":price_list, "SOURCE":source_list, "LINK":final_list})
        #print(df)

        return render_template('ComparePrice.html', names=product_list, prices=price_list, sources=source_list, links=final_list)
    return render_template('ComparePrice.html')
    

if __name__ == '__main__':
    app.run(debug=True)