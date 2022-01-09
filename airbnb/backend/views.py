from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json

from .models import Book,GeneralByCity
from .generalByCity import draw,calAvgScore,topAvgScoreByNeighborhood
from .per_price_response import build_per_price_response
from .popular_description_response import build_popular_description_response
from .predict_price_response import test_model
from .investor import build_ratio


# Create your views here.


@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book = Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def show_books(request):
    response = {}
    try:
        books = Book.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", books))
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def display_city(request):
    response = {}
    try:
        city = request.GET.get('city')
        room_type_x, room_type_y,tenancy_term_x,tenancy_term_y,Average_price = draw(city)
        response['city'] = city
        response['room_type_x'] = room_type_x
        response['room_type_y'] = room_type_y
        response['tenancy_term_x'] = tenancy_term_x
        response['tenancy_term_y'] = tenancy_term_y
        response['Average_price'] = Average_price
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def avg_score(request):
    response = {}
    try:
        city = request.GET.get('city')
        score, neighborhood = calAvgScore(city)
        response['city'] = city
        response['score'] = score
        response['neighborhood'] = neighborhood
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def top_score_neighborhood(request):
    response = {}
    try:
        city = request.GET.get('city')
        neighborhood = request.GET.get('neighborhood')
        id, score = topAvgScoreByNeighborhood(city,neighborhood)
        response['city'] = city
        response['neighborhood'] = neighborhood
        response['id'] = id
        response['score'] = score
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def per_price(request):
    response = {}
    try:
        city = request.GET.get('city')
        #country = request.GET.get('country')
        response['city'] = city
        #response['country'] = country
        avg_per_price_x, avg_per_price_y, median_per_price_x, median_per_price_y = build_per_price_response(city)
        response['avg_per_price_x'] = avg_per_price_x
        response['avg_per_price_y'] = avg_per_price_y
        response['median_per_price_x'] = median_per_price_x
        response['median_per_price_y'] = median_per_price_y
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def popular_description(request):
    response = {}
    try:
        city = request.GET.get('city')
        #country = request.GET.get('country')
        response['city'] = city
        #response['country'] = country
        key_word_x, key_word_y = build_popular_description_response(city)
        response['key_word_x'] = key_word_x
        response['key_word_y'] = key_word_y
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# test case: 2, 'Little Portugal', 1, 'Private room', 12.0
@require_http_methods(["GET"])
def predict_price(request):
    response = {}
    try:
        accommodates = int(request.GET.get('accommodates'))
        neighbourhood_cleansed = request.GET.get('neighbourhood_cleansed')
        bedrooms = int(request.GET.get('bedrooms'))
        room_type = request.GET.get('room_type')
        price = test_model(accommodates, neighbourhood_cleansed, bedrooms, room_type)
        response['price'] = price
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


#city,neighbourhood_cleansed,purchase_amount,loan_ratio,loan_monthly_payment_amount,water_electricity_fees,property_tax
#predict_ratio
@require_http_methods(["GET"])
def predict_ratio(request):
    response = {}
    try:
        city = request.GET.get('city')
        neighbourhood_cleansed = request.GET.get('neighbourhood_cleansed')
        purchase_amount = int(request.GET.get('purchase_amount'))
        loan_ratio = int(request.GET.get('loan_ratio'))
        loan_monthly_payment_amount = int(request.GET.get('loan_monthly_payment_amount'))
        water_electricity_fees = int(request.GET.get('water_electricity_fees'))
        property_tax = int(request.GET.get('property_tax'))
        ratio = build_ratio(city,neighbourhood_cleansed,purchase_amount,loan_ratio,loan_monthly_payment_amount,water_electricity_fees,property_tax)
        response['ratio'] = ratio
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)



