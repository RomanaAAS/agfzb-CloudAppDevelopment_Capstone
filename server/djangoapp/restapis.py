import requests
import os
import json
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
# e.g., response = requests.post(url, params=kwargs, json=payload)


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
                #sentiment=analyze_review_sentiments(item['review'])
                )
                results.append(item)
    else:
        status_code = response.status_code
        return status_code
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(review):
    params = dict()
    params["text"] = review
    params["version"] = "2018-09-21"
    params["features"] = dict(sentiment=dict())
    params["return_analyzed_text"] = True
    params["language"] = "en"
    url = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/2f1b5cbf-df64-464b-a5c5-79795feb0cb3'

    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                            auth=HTTPBasicAuth('apikey', os.getenv('NLU_API_KEY', 'V4CVkzPbgD79C9VAWJKi17u3B2JRj8IioO-hvXKlxp7l')))
    return json.loads(response.text)['sentiment']['document']['label']