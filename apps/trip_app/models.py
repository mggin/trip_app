from django.db import models
import re
import bcrypt

from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, data):
        errors = []
        if len(data['first_name']) < 1:
            errors.append('f_name_err')
        if len(data['last_name']) < 1:
            errors.append('l_name_err')
        if not EMAIL_REGEX.match(data['email']) or len(data['email']) < 1:
            errors.append('invalid_email_err')
        if len(data['password']) < 8:
            errors.append('password_length_err')
        return errors

    def create_user(self, data):
        hashed_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name = data['first_name'], last_name = data['last_name'], email = data['email'], password = hashed_password)
        return user

    def validate_user(self, data):   
        users = User.objects.filter(email = data['email'])
        context = {}
        if len(users) < 1:
            return False
        else:
            current_user = users[0]
            if  bcrypt.checkpw(data['password'].encode(), current_user.password.encode()):
                print('password match')
                return current_user
            else:
                return False
        
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()



class TripManager(models.Manager):

    def validator(self, data):
        errors = []
        if len(data['destination']) < 3:
            errors.append('dest_err')
        if len(data['plan']) < 3:
            errors.append('plan_err')
        if len(data['start_date']) == 0:
            errors.append('start_err')
        if len(data['end_date']) == 0:
            errors.append('end_err')
        return errors
    
    def get_trips(self, user_id):
        user = User.objects.get(id = user_id)
        trips = list(reversed(user.joined_trips.all()))
        return trips
    
    def create_trip(self, data, user_id):
        user = User.objects.get(id = user_id)
        print('#' * 100)

        trip = Trip.objects.create(destination = data['destination'], start_date = data['start_date'], end_date = data['end_date'], plan = data['plan'], created_by = user)
        trip.users_who_joined.add(user)
        return trip

    def get_single_trip(self, trip_id):
        trip = Trip.objects.get(id = trip_id)
        return trip

    def update_trip(self, trip_id, data):
        trip = self.get_single_trip(trip_id)
        trip.destination = data['destination']
        trip.start_date = data['start_date']
        trip.end_date = data['end_date']
        trip.plan = data['destination']
        trip.save()
        return trip

    def delete_trip(self, trip_id):
        trip = self.get_single_trip(trip_id)
        trip.delete()

    def join_trip(self, user_id, trip_id):
        trip = Trip.objects.get(id = trip_id)
        user = User.objects.get(id = user_id)

        trip.users_who_joined.add(user)


    def cancel_trip(self, user_id, trip_id):
        trip = Trip.objects.get(id = trip_id)
        user = User.objects.get(id = user_id)

        trip.users_who_joined.remove(user)
        

class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.TextField()
    created_by = models.ForeignKey(User, related_name="trips", )
    users_who_joined = models.ManyToManyField(User, related_name = "joined_trips")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()
    



