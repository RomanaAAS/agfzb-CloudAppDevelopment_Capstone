from re import A
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from urllib3 import HTTPResponse
from .models import CarMake, CarModel, CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import http.client

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context) 
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')
# ...

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration_bootstrap.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://90152bc2.eu-gb.apigw.appdomain.cloud/api/dealerships"

        # Get dealers from the URL
        #dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        context['dealerships']=get_dealers_from_cf(url)
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        url = "https://90152bc2.eu-gb.apigw.appdomain.cloud/api/reviews"
        context['dealer_reviews'] = get_dealer_reviews_from_cf(url, dealer_id)

        url2 = "https://90152bc2.eu-gb.apigw.appdomain.cloud/api/dealerships"
        context['dealerships'] = get_dealers_from_cf(url2)
        #context['full_name'] = current_dealer.full_name
        context['dealer'] = dealer_id
        #print(context)

        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "GET":
        context = {}
        url = "https://90152bc2.eu-gb.apigw.appdomain.cloud/api/dealership_id?id={dealer_id}"
        context['dealerships'] = get_dealers_from_cf(url)
        context['dealer'] = dealer_id
        context['cars'] = CarModel.objects.filter(dealership=dealer_id)
        print(context['cars'])

        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST" and request.user.is_authenticated:
        url_post = "https://90152bc2.eu-gb.apigw.appdomain.cloud/api/submit_review"
        context={}
        review_payload = dict()
        #review_payload["time"] = datetime.utcnow().isoformat()
        review_payload["dealership"] = dealer_id
        review_payload["name"] = request.POST.get('name', "")
        review_payload["review"] = request.POST.get('review', "")
        review_payload["purchased"] = request.POST.get('purchased', False)
        #print(review_payload)

        if review_payload['purchased']:
            car = CarModel.objects.filter(model_id=int(request.POST.get('car')))[0]
            review_payload['purchase']= "true"
            review_payload["purchase_date"] = request.POST.get('purchasedate')
            review_payload["car_model"] = car.name_model
            review_payload["car_year"] = car.year.strftime("%Y")
            review_payload["car_make"] = car.name_make.name_make
        else: 
            review_payload['purchase']= 'false'
            review_payload["purchase_date"] = ''
            review_payload["car_model"] = ''
            review_payload["car_year"] = ''
            review_payload["car_make"] = ''

        json_payload = json.dumps(review_payload)
        response = post_request(url_post,json_payload)
        print(json_payload)
        messages.success(request, 'Thank you for your review')
        #return HttpResponse(response)
        #return render(request, "index.html", context)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    elif request.user.is_authenticated != True:
        context={}
        context['error_message'] = "Please sign up first to leave a review!"
        return render(request, 'djangoapp/user_registration_bootstrap.html', context)   