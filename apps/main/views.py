from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.


def main(request):
    if 'logged_in' in request.session:
        # messages.success(request,"Welcome to Tom's Library!"),
        return render(request, 'main/index.html',{
        "books": Book.objects.order_by('created_at').reverse(),
        "user": User.objects.get(id=request.session["logged_in"])
    })
    else:
        return render(request, 'main/index.html',{
            "books": Book.objects.order_by('created_at').reverse(),
        })

def index(request):
    if "logged_in" in request.session:
        messages.success(request,"You already signed in!")
        return redirect("/")

    return render(request, 'main/login.html')

def register(request):
    form = request.POST

    errors = User.objects.basic_validator(form)

    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/')

    User.objects.create(
        first_name=form["first_name"],
        last_name=form["last_name"],
        student_id=form["student_id"],
        email=form["email"],
        password=bcrypt.hashpw(form["password"].encode(), bcrypt.gensalt()),
    )
    user = User.objects.last()
    request.session["logged_in"] = user.id
    request.session["first_name"] = user.first_name
    request.session["last_name"] = user.last_name
    request.session["email"] = user.email
    request.session["student_id"] = user.student_id
    return redirect('/')


def login(request):
    form = request.POST

    try:
        user=User.objects.get(email=form["login_email"])
    except:
        messages.error(request,"Please enter a correct email!")
        return redirect("/login")
    if bcrypt.checkpw(form["login_password"].encode(), user.password.encode()) == False:
        messages.error(request,"Please enter a correct password!")
        return redirect("/login")

    errors = User.objects.login_validation(form)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
    
    user = User.objects.get(email=form['login_email'])
    request.session["logged_in"] = user.id
    request.session["email"] = user.email
    request.session["first_name"] = user.first_name
    request.session["last_name"] = user.last_name
    request.session["student_id"] = user.student_id
    return redirect('/login')

    # return redirect("/login")


def logout(request):
    # form = request.session
    # errors = User.objects.logout_validation(form)
    # user = User.objects.get(id=request.session["logged_in"])

    # if not user:
    #     messages.error(request,"your didn't signin")
    # else:
    # if len(errors) > 0:
    #     for key, val in errors.items():
    #         messages.error(request, val)

    request.session.clear()

    return redirect('/login')

def add_question(request):
    form = request.POST

    Message.objects.create(
        message= form['question_message'],
        user= request.session["logged_in"]
    )
    return redirect('/')

def add_book(request,book_id):
    return render(request,'main/product-single.html',{
        "books": Book.objects.all(),
        "user": User.objects.get(id=request.session["logged_in"]),
    })


def about(request):
    if "logged_in" not in request.session:
        return render(request, 'main/about.html')
    else:
        return render(request, 'main/about.html',{
            "user": User.objects.get(id=request.session["logged_in"]),
        })

def books(request):
    
    if "logged_in" in request.session:
    # this_book = Book.objects.get(id=request.session["logged_in"])
        return render(request, 'main/books.html',{
            "user": User.objects.get(id=request.session["logged_in"]),
            "books": Book.objects.all(),
            "recent_added_book": Book.objects.order_by('created_at').reverse()
        })
    
    else:
        return render(request, 'main/books.html',{
                "books": Book.objects.all(),
                "recent_added_book": Book.objects.order_by('created_at').reverse()
            })

def faq(request):
    if "logged_in" not in request.session:
        return render(request, 'main/faq.html')
    else:
        return render(request, 'main/faq.html',{
            "user": User.objects.get(id=request.session["logged_in"]),
        })

def privacy_policy(request):
    if "logged_in" not in request.session:
        return render(request, 'main/privacy_policy.html')
    else:
        return render(request, 'main/privacy-policy.html',{
            "user": User.objects.get(id=request.session["logged_in"]),
        })

def terms_conditions(request):
    if "logged_in" not in request.session:
        return render(request, 'main/terms-conditions.html')
    else:
        return render(request, 'main/terms-conditions.html',{
            "user": User.objects.get(id=request.session["logged_in"]),
        })

def products(request):
    if "logged_in" not in request.session:
        return render(request, 'main/products.html',{
            "books": Book.objects.all(),
            "recent_added_book": Book.objects.order_by('created_at').reverse(),
        })
    else:
        return render(request, 'main/products.html',{
            "user": User.objects.get(id=request.session["logged_in"]),
            "books": Book.objects.all(),
            "recent_added_book": Book.objects.order_by('created_at').reverse(),
        })


def book_detail(request,book_id):
    if 'logged_in' not in request.session:
        # messages.error(request, "You need to log in first!")
        # return redirect('/login')
        return render(request,'main/product-single.html',{
            "this_book": Book.objects.get(id=book_id)
        })
    else:
        this_book = Book.objects.get(id= book_id)
        this_user = User.objects.get(id= request.session["logged_in"])

        user_book= this_user.books.all

        return render(request, 'main/product-single.html',{
            "user": User.objects.get(id=request.session['logged_in']),
            "this_book": Book.objects.get(id=book_id),
            "books": Book.objects.all(),
            "user_book": user_book,
        })

def borrow(request,book_id):
    if 'logged_in' not in request.session:
        messages.error(request, "You need to log in first!")
        return redirect('/login')
    
    this_book = Book.objects.get(id= book_id)
    this_user = User.objects.get(id= request.session["logged_in"])

    if this_user in this_book.users.all():
        messages.error(request,"You already chose this book!")
        return redirect(f"/books/{book_id}")
    else:
        this_book.users.add(this_user)
        messages.success(request,"Success!")
        return redirect(f"/books/{book_id}")


    
# def choose_book(request,book_id):
#     form = request.POST

#     this_user = User.objects.get(id=request.session["logged_in"])
    
#     this_book = Book.objects.get(id=request.session["logged_in"])
def question(request):
    form = request.POST

    # # errors = Message.objects.message_validator(form)

    # if len(errors):
    #     for key, value in errors.items():
    #         messages.error(request, value)
    # else:
    Message.objects.create(message= form['question_message'],message_email= form['question_email'],message_name=form['question_name'])
    return redirect('/')



def profile(request):

    # book= Book.objects.all()
    this_person = User.objects.get(id=request.session["logged_in"])

    books_add = this_person.books.all()

    return render(request,"main/profile.html",{
        "user": User.objects.get(id=request.session["logged_in"]),
        "books": books_add.order_by('created_at'),
        "books_add": books_add,
    })

def delete_book(request,book_id):
    this_book = Book.objects.get(id=book_id)
    this_user = User.objects.get(id=request.session["logged_in"])

    this_user.books.remove(this_book)
    return redirect('/profile')
def delete_book1(request,book_id):
    this_book = Book.objects.get(id=book_id)
    this_user = User.objects.get(id=request.session["logged_in"])

    if this_book not in this_user.books.all():
        messages.error(request,"You didn't choose this book!")
    else:
        this_user.books.remove(this_book)
        
        messages.success(request,"Remove")
    return redirect(f'/books/{book_id}')

# def search(request):
#     if request.method == "GET":
#         query = request.GET.get('q')
#         submitbutton = request.GET.get('submit')

#         if query is not None:
#             lookup = Book(title= query)