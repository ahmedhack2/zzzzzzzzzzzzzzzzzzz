# from flask import Flask ,request,jsonify
# from products import products
# from chat import get_response
# from search_amazon_product import extract_product_name,newsearch_amazon
# app = Flask(__name__)
# from datetime import datetime
# import re
# now = datetime.now()


# @app.get("/")
# def index_get():
#     return '<h1>E-Commerce Chat Bot</h1>'


# @app.route('/api')
# def api():
#     # input you will find in the end of url
#     user_input = request.args.get('input')
#     product_name = extract_product_name(user_input)
#     #if user input contain products
#     if product_name != "there is no product." :
#         lowercase_word_list = [word.lower() for word in products]
#         # words_after_buy = user_input.split("buy ")[-1].split()
#         if "buy" in user_input:
#             words_after_keyword = user_input.split("buy ")[-1].split()
#             matching_words_of_product = " ".join(words_after_keyword).lower()
#         elif "search on" in user_input:
#             words_after_keyword = user_input.split("search on ")[-1].split()
#             matching_words_of_product = " ".join(words_after_keyword).lower()
#         elif "search for" in user_input:
#             words_after_keyword = user_input.split("search for ")[-1].split()
#             matching_words_of_product = " ".join(words_after_keyword).lower()

#         # matching_words_of_product = " ".join(words_after_buy).lower()
#         print("word after buy: "+ matching_words_of_product)
#         print(remove_articles(matching_words_of_product))
#         product_to_search =""
#         for product in lowercase_word_list:
#             if product == remove_articles(matching_words_of_product):
#                 # print("yes, product name : "+product)
#                 product_to_search = product
#         print("User input contains a product: "+product_to_search)
#         print("ok, i will search on amazon about "+product_to_search +"...")
#         result = newsearch_amazon("https://www.amazon.com/s?k="+product_to_search)
#         print(result)
#         # print("User input contains a product: "+product_name)
#         # print("ok, i will search on amazon about "+product_name +"...")
#         # result = newsearch_amazon("https://www.amazon.com/s?k="+product_name)
#         # print(result)
#         # response = get_response(user_input)
#         json = {
#             'input': user_input,
#             'response': result,
#             # 'accuracy': response.accuracy
#         }
#         return json
#     else:
#         response = get_response(user_input)
#         if response == "Date and Time":
#             formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
#             print("Current date and time: "+formatted_datetime)
#             json = {
#                 'input': user_input,
#                 'response': "Current date and time: "+formatted_datetime,
#                 # 'accuracy': response.accuracy
#             }
#             return json

#         json = {
#             'input': user_input,
#             'response': response,
#             # 'accuracy': response.accuracy
#         }
#         return json
    

# def remove_articles(text):
#     # Split the text into words
#     words = text.split()
#     # Remove articles from the list of words
#     words_without_articles = [word for word in words if word.lower() not in ['a', 'an', 'the']]
#     # Join the remaining words into a single string
#     extracted_word = ' '.join(words_without_articles)
#     return extracted_word

# if __name__ == "__main__":
#     app.run(debug=True)


# from flask import Flask
# from extensions import api , db
# from resources import ns

# def create_app():
#     app = Flask(__name__)

#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
#     api.init_app(app)
#     db.init_app(app)

#     api.add_namespace(ns)
#     return app

from flask import Flask
from extensions import api
from resources import ns

def create_app():
    app = Flask(__name__)

    api.init_app(app)

    api.add_namespace(ns)
    return app