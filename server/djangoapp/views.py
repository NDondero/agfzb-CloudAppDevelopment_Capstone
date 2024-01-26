from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime

from .models import CarModel
from .restapis import (
    get_dealers_from_cf,
    get_dealer_by_id_from_cf,
    get_dealer_reviews_from_cf,
    post_request,
)
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import random

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, "djangoapp/about.html")


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, "djangoapp/contact.html")


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context["message"] = "Invalid username or password."
            return render(request, "djangoapp/user_login.html", context)
    else:
        return render(request, "djangoapp/user_login.html", context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/registration.html", context)
    elif request.method == "POST":
        # Check if user exists
        username = request.POST["username"]
        password = request.POST["psw"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context["message"] = "User already exists."
            return render(request, "djangoapp/registration.html", context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        state = request.GET.get("state", None)
        url = "https://ndondero-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        # kwargs = {'state': state}
        dealerships = get_dealers_from_cf(url, state=state)
        context["dealerships"] = dealerships
        return render(request, "djangoapp/index.html", context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        dealer_url = f"https://ndondero-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get?id={dealer_id}"
        dealership = get_dealer_by_id_from_cf(dealer_url, dealer_id)
        context["dealership"] = dealership
        url = f"https://ndondero-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews?id={dealer_id}"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context["reviews"] = reviews
        return render(request, "djangoapp/dealer_details.html", context)


# Create a `add_review` view to submit a review
@login_required
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        dealer_url = f"https://ndondero-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get?id={dealer_id}"
        dealership = get_dealer_by_id_from_cf(dealer_url, dealer_id)
        context["dealership"] = dealership
        if dealership is not None:
            car_models = CarModel.objects.all()
            context["car_models"] = car_models
        return render(request, "djangoapp/add_review.html", context)
    elif request.method == "POST":
        car_model_id = request.POST["car_model_id"]
        car_model = CarModel.objects.get(pk=car_model_id)
        purchase_date = datetime.utcnow().strftime("%m/%d/%Y")
        car_year = car_model.year.strftime("%Y")
        purchase_value = request.POST.get("purchase", False)
        purchase = purchase_value == "on"
        json_payload = {
            "purchase_date": purchase_date,
            "name": request.POST["name"],
            "dealership": dealer_id,
            "review": request.POST["review"],
            "purchase": purchase_value,
            "car_make": car_model.make.name,
            "car_model": car_model.name,
            "car_year": car_year,
            "id": random.randint(1, 9999),
        }
        
        url = "https://ndondero-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
        response = post_request(url, json_payload, dealer_id=dealer_id)
        print(response)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
