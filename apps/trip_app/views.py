from django.shortcuts import render, redirect, HttpResponse
from .models import *
import json
import bcrypt

import time

def index(request):
    print('ehllo')
    return redirect('/login_register')

def login_register(request):
    
    return render(request, 'login_register.html')

def create_user(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            print(errors)
            context = {"errors": errors, "redirect": False}
            return HttpResponse(json.dumps(context), content_type = 'application/json')
        else:
            User.objects.create_user(request.POST)
            context = { "redirect" : True }
            return HttpResponse(json.dumps(context), content_type = 'application/json')

def login(request):
    if request.method == 'POST':
        validate_user = User.objects.validate_user(request.POST)
        context = {}
        if validate_user != False:
            request.session['id'] = validate_user.id
            request.session['login'] = True
            request.session['user_name'] = f'{validate_user.first_name} {validate_user.last_name}'
            context['url'] = '/trips'
        else:
            context['error'] = True
        return HttpResponse(json.dumps(context), content_type = 'application/json')
    else:
        return HttpResponse('Access Denied')


def view_trips(request):
    if request.session['login'] == True:
        trips = Trip.objects.get_trips(request.session['id'])
        current_user = User.objects.get(id = request.session['id'])
        other_trips = Trip.objects.all()

        selected_other_trips = []

        for trip in other_trips:
            if trip.created_by != current_user and trip not in trips:
                trip.start_date = trip.start_date.strftime('%m-%m-%Y')
                trip.end_date = trip.end_date.strftime('%m-%d-%Y')
                selected_other_trips.append(trip)

        for trip in trips:
            trip.start_date = trip.start_date.strftime('%m-%m-%Y')
            trip.end_date = trip.end_date.strftime('%m-%d-%Y')

        context = {
            "id": request.session['id'],
            "user_name": request.session['user_name'], 
            "trips": trips,
            "other_trips": selected_other_trips,
            "user": current_user
        }


        return render(request, 'trips.html', context)
    else:
        return HttpResponse('**Access Denied**')

def view_trip_form(request):
    if request.session['login'] == True:
        date = datetime.now().strftime('%Y-%m-%d')
        context = { "user_name" : request.session['user_name'] , "date": date}
        return render(request, 'trip_form.html', context)
    else:
        return HttpResponse('**Access Denied**')


def create_trip(request):
    if request.session['login'] == True:
        if request.method == 'POST':
            errors = Trip.objects.validator(request.POST)
            if len(errors) > 0:
                context = {"errors": errors, "redirect": False}
                return HttpResponse(json.dumps(context), content_type = 'application/json')
            else:
                error = Trip.objects.create_trip(request.POST, request.session['id'])
                print(error)
                print('*' * 10)
                context = { "redirect" : True }
                return HttpResponse(json.dumps(context), content_type = 'application/json')
    else:
        return HttpResponse('Acces Denied')
        
def show_trip(request, trip_id):
    if request.session['login'] == True:
        trip = Trip.objects.get_single_trip(trip_id)
        creator = trip.created_by
        trip.start_date = trip.start_date.strftime('%Y-%m-%d')
        trip.end_date = trip.end_date.strftime('%Y-%m-%d')
        all_users = trip.users_who_joined.all()

        users = []
        for user in all_users:
            if user != creator:
                users.append(user)
        
        context = { 'trip' : trip, "users": users,"user_name": request.session['user_name']}
        return render(request, 'show_trip.html', context)
    else:
        return HttpResponse('Acces Denied')


def edit_trip(request, trip_id):
    if request.session['login'] == True:
        trip = Trip.objects.get_single_trip(trip_id)
        trip.start_date = trip.start_date.strftime('%Y-%m-%d')
        trip.end_date = trip.end_date.strftime('%Y-%m-%d')
        context = { 'trip' : trip, "user_name": request.session['user_name']}
        return render(request, 'edit_trip.html', context)
    else:
        return HttpResponse('**Access Denied**')


def update_trip(request, trip_id):
    if request.session['login'] == True:
        if request.method == 'POST':
            errors = Trip.objects.validator(request.POST)
            if len(errors) > 0:
                context = {"errors": errors, "redirect": False}
                return HttpResponse(json.dumps(context), content_type = 'application/json')
            else:
                Trip.objects.update_trip(trip_id, request.POST)
                context = { "redirect" : True }
                return HttpResponse(json.dumps(context), content_type = 'application/json')
    else:
        return HttpResponse('Acces Denied')

def delete_trip(request, trip_id):
    if request.session['login'] == True:
        Trip.objects.delete_trip(trip_id)
        return redirect('/trips')
    else:
        return HttpResponse('Acces Denied')


def log_off(request):
    if request.session['login'] == True:
        request.session['login'] = False
        return redirect('/')
    else:
        return HttpResponse('**Access Denied**')

def join_trip(request, trip_id):
    if request.session['login'] == True:
        user_id = request.session['id']
        Trip.objects.join_trip(user_id, trip_id)
        return redirect('/trips')
    else:
        return HttpResponse('**Access Denied**')

def cancel_trip(request, trip_id):
    if request.session['login'] == True:
        user_id = request.session['id']
        Trip.objects.cancel_trip(user_id, trip_id)
        return redirect('/trips')
    else:
        return HttpResponse('**Access Denied**')


