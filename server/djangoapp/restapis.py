import requests
import os
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a `post_request` to make HTTP POST requests
# e.g., 

def post_request(url, json_payload, **kwargs):
    try:
        request = requests.post(url, json=json_payload, params=kwargs)
    except:
        print("Network exception occurred")

    status_code = request.status_code
    print(request.request.body)
    print("With status {} ".format(status_code))
    json_data = json.loads(request.text)

    return response

   

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_Id):
    results = []
    #Call get_request with a URL parameter
    json_result = get_request(url, dealership=dealer_Id)
    if json_result !=None:
    # Get the row list in JSON as dealers
        #review_list = json_result["docs"]
        review_item = json_result["docs"]
        for item in review_item:
            if len(item) != 0:
                item = DealerReview(
                id="",
                name=item['name'],
                dealership=item['dealership'],
                purchase=item['purchase'] ,
                purchase_date=item['purchase_date'] if item['purchase'] else "",
                review=item['review'],
                car_make=item['car_make'] if item['purchase'] else "None",
                car_model=item['car_model'] if item['purchase'] else "None",
                car_year=item['car_year'] if item['purchase'] else "-",
                sentiment=analyze_review_sentiments(item['review'])
                )
                results.append(item)
    else:
        status_code = response.status_code
        return status_code
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(review):
    authenticator = IAMAuthenticator('V4CVkzPbgD79C9VAWJKi17u3B2JRj8IioO-hvXKlxp7l')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07', 
        authenticator=authenticator
        )
    NLU_URL = natural_language_understanding.set_service_url('https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/2f1b5cbf-df64-464b-a5c5-79795feb0cb3')

    response = natural_language_understanding.analyze(text = review, 
    features=Features(sentiment=SentimentOptions(document = True))).get_result()

    #print(json.dumps(response['sentiment']['document']['label'], indent=2))

    return response['sentiment']['document']['label']