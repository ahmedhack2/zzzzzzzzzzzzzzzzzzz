from flask_restx import Resource , Namespace , reqparse
import requests
from bs4 import BeautifulSoup
import time
from chat import get_response
from datetime import datetime
from search_amazon_product import extract_product_name,newsearch_amazon
from products import products
now = datetime.now()




ns = Namespace("api")
# api = Api(app)
task_post_args = reqparse.RequestParser()
product_name = reqparse.RequestParser()
chat = reqparse.RequestParser()
task_post_args.add_argument("task", type=str, required=True)
product_name.add_argument("product", type=str, required=True)
chat.add_argument("chat-massage", type=str, required=True)

@ns.route("/hello")
class Hello(Resource):
    def get(self):
        return {"hello": "restx"}

    @ns.expect(task_post_args)
    def post(self):
        args = task_post_args.parse_args()
        return args


    
@ns.route("/Bot")
class Bot(Resource):
    def get(self):
        return {
            "bot":"robotocs"
        }
    @ns.expect(product_name)
    def post(self):
        args = product_name.parse_args()
        url = "https://www.amazon.com/s?k="+str(args['product'])
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }

        # Send a GET request to the provided URL with headers
        response = requests.get(url, headers=headers)
        
        # Retry logic for 503 error
        max_retries = 150
        retries = 0
        while response.status_code == 503 and retries < max_retries:
            print('503 error - Retrying...')
            time.sleep(2)  # Wait for 2 seconds before retrying
            response = requests.get(url, headers=headers)
            retries += 1
        
        # If still getting 503 error after retries, return None
        if response.status_code == 503:
            print('503 error - Max retries reached. Service unavailable.')
            return None
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all the product containers on the page
        product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        # Initialize a list to store the results
        results = []
        
        # Iterate over each product container
        for container in product_containers:
            # Extract the product title
            title_element = container.find('h2')
            title = title_element.text.strip()
            
            # Extract the product price
            price_element = container.find('span', {'class': 'a-offscreen'})
            price = price_element.text.strip() if price_element else 'Not available'
            
            # Extract the product rating
            rating_element = container.find('span', {'class': 'a-icon-alt'})
            rating = rating_element.text.strip() if rating_element else 'Not rated'
            
            # Extract the product link
            link_element = container.find('a', {'class': 'a-link-normal'})
            link = 'https://www.amazon.com' + link_element['href'] if link_element else 'Link not available'
            
            # Create a dictionary of product details
            product = {
                'title': title,
                'price': price,
                'rating': rating,
                'link': link
            }
            
            # Add the product details to the results list
            results.append(product)
        return results


@ns.route("/Chat")
class Chat(Resource):
    def get(self):
        return {
            "bot":"robotocs"
        }
    @ns.expect(chat)
    def post(self):
        args = chat.parse_args()
        sentence = str(args['chat-massage'])
        product_name = extract_product_name(sentence)
        #if user input any massage not contains a product
        resp = get_response(str(args['chat-massage']))
        print("sssssssssssssssssssssssssssssssssssssssssssssss")
        if resp == "Date and Time":
            formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
            print("Current date and time: "+formatted_datetime)
            resp = formatted_datetime
        # if user unput contains product
        #if user input contain products
        elif product_name != "there is no product." :
            lowercase_word_list = [word.lower() for word in products]
            # words_after_buy = user_input.split("buy ")[-1].split()
            if "buy" in sentence:
                words_after_keyword = sentence.split("buy ")[-1].split()
                matching_words_of_product = " ".join(words_after_keyword).lower()
            elif "search on" in sentence:
                words_after_keyword = sentence.split("search on ")[-1].split()
                matching_words_of_product = " ".join(words_after_keyword).lower()
            elif "search for" in sentence:
                words_after_keyword = sentence.split("search for ")[-1].split()
                matching_words_of_product = " ".join(words_after_keyword).lower()

            # matching_words_of_product = " ".join(words_after_buy).lower()
            print("word after buy: "+ matching_words_of_product)
            print(remove_articles(matching_words_of_product))
            product_to_search =""
            for product in lowercase_word_list:
                if product == remove_articles(matching_words_of_product):
                    # print("yes, product name : "+product)
                    product_to_search = product
            print("User input contains a product: "+product_to_search)
            print("ok, i will search on amazon about "+product_to_search +"...")
            result = newsearch_amazon("https://www.amazon.com/s?k="+product_to_search)
            resp = result
        return resp

        

def remove_articles(text):
    # Split the text into words
    words = text.split()
    # Remove articles from the list of words
    words_without_articles = [word for word in words if word.lower() not in ['a', 'an', 'the']]
    # Join the remaining words into a single string
    extracted_word = ' '.join(words_without_articles)
    return extracted_word