from django.db import models
from django.core.validators import validate_email
from datetime import datetime, date
import bcrypt

# Create your models here.


class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data["first_name"]) < 3:
            errors["first_name"] = "Please enter more than 2 characters for First Name!"
        if len(post_data["last_name"]) < 3:
            errors["last_name"] = "Please enter more than 2 characters for Last Name!"
        try:
            validate_email(post_data["email"])
        except:
            errors["email"] = "Please enter a valid email!"
        if len(post_data["password"]) < 8:
            errors["password"] = "Please enter at least 8 characters for Password!"

        if post_data["password"] != post_data["pw_confirm"]:
            errors["pw_confirm"] = "Please ensure the password matched for confirmation"

        if len(post_data["student_id"]) < 1:
            errors["student_id"] = "Please enter your  Student ID number!"
        elif len(post_data["student_id"]) < 9:
            errors["student_id"] = "Please ensure Student ID number has 9 numbers!"
        elif len(post_data["student_id"]) > 10:
            errors["student_id"] = "Please ensure Student ID number has 9 numbers!"

        user_email = User.objects.filter(email=post_data['email'])
        if len(user_email) != 0:
            errors["email"] = "This email already registered!"

        # user_id = User.objects.filter(student_id=post_data['student_id'])
        # if len(str(user_id)) != 0:
        #     errors["student_id"] = "You already registered with this student ID number!"

        return errors

    def login_validation(self, post_data):
        user = User.objects.filter(email=post_data['login_email'])
        # user_id = User.objects.filter(student_id = post_data['login_id'])

        errors = {}
        if len(post_data["login_email"]) < 1:
            errors["login_email"] = "Please enter Your Email or Create new User!"
        elif not user:
            errors['email'] = "No user Found! Please Create New User"
        # if user:
        #     errors['user'] = "Welcome Back!"
        if user and not bcrypt.checkpw(post_data['login_password'].encode('utf8'), user[0].password.encode('utf8')):
            errors['password'] = "Invalid email or password!"

        return errors
    
    # def logout_validation(self,post_data):
    #     user = User.objects.get(id=post_data["logged_in"])
    #     errors = {}

    #     if not user:
    #         errors["logout"] =  "You didn't signin"
    #     return errors

    def message_validator(self, post_data):
        errors = {}
        
        if len(post_data["question_message"])<3:
            errors["question_message"] = "Please Specify!"


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    student_id = models.IntegerField()
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return (self.first_name+" "+self.last_name)


class BookManager(models.Manager):
    def book_validator(self, post_data):
        errors = {}
        if len(post_data['title']) < 0:
            errors["title"] = "Please enter The Book Title"
        if len(post_data["desc"]) < 0:
            errors["desc"] = "Please enter the Book Description"
        if len(post_data["release_date"]) < 1:
            errors["release_date"] = "Please provide the Release Date!"
        if str(date.today()) < str(post_data['release_date']):
            errors["release_date"] = "Please input a valid Date. Note: Release date can not be in the future."
        return errors


class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    release_date = models.DateField()
    users = models.ManyToManyField(User,related_name="books", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

    def __str__(self):
        return self.title

class  MessageManager(models.Manager):
    def message_validator(self,post_data):
        errors = {}

        if len(post_data["question_message"])<3:
            errors["question_message"] = "Please Specify!"
        
        return errors


class Message(models.Model):
    message = models.TextField()
    message_email= models.EmailField(max_length=255, null=True)
    message_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()
    
    def __str__(self):
        return (self.message_name + " with email " + self.message_email + " left a message: " +self.message)
