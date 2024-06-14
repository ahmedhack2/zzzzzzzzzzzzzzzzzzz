import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from search_amazon_product import extract_product_name,newsearch_amazon
from products import products
from datetime import datetime

now = datetime.now()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data: #read mode
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval() #evaluation
print("Startssssssssssssssssssssssssssssssssssssssssssssss")
# print(model_state)
# print(input_size)
# print(hidden_size)
# print(output_size)
# print(all_words)
# print(tags)

bot_name = "Robotocs"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    
    return "I do not understand..."


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ") # iwant to buy iphone
        # lowercase_word_list = [word.lower() for word in products]
        # # words_in_text = [word for word in sentence.lower().split() if word in lowercase_word_list]
        # words_after_buy = sentence.split("buy ")[-1].split()
        # matching_words_of_product = " ".join(words_after_buy).lower()
        # print("word after buy: "+ matching_words_of_product)
        # for product in lowercase_word_list:
        #     if product == matching_words_of_product:
        #         print("yes")
        #         print(product)

        product_name = extract_product_name(sentence)
        if sentence == "quit":
            break
        #if user input contain products
        if product_name != "there is no product.":
            lowercase_products_list = [word.lower() for word in products]
            # words_after_buy = sentence.split("buy ")[-1].split()
            if "buy" in sentence:
                words_after_keyword = sentence.split("buy ")[-1].split()
                matching_words_of_product = " ".join(words_after_keyword).lower()
            elif "search on" in sentence:
                words_after_keyword = sentence.split("search on ")[-1].split()
                matching_words_of_product = " ".join(words_after_keyword).lower()


            # matching_words_of_product = " ".join(words_after_buy).lower()
            print("word after buy: "+ matching_words_of_product)
            product_to_search =""
            for product in lowercase_products_list:
                if product == matching_words_of_product:
                    # print("yes, product name : "+product)
                    product_to_search = product
            print("User input contains a product: "+product_to_search)
            print("ok, i will search on amazon about "+product_to_search +"...")
            result = newsearch_amazon("https://www.amazon.com/s?k="+product_to_search)
            print(result)
            continue
        #if user input any massage not contains a product
        resp = get_response(sentence)
        if resp == "Date and Time":
            formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
            print("Current date and time: "+formatted_datetime)
            continue
        print(resp)

