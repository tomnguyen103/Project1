from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main),
    url(r'^register$', views.register),
    url(r'^login$', views.index),
    url(r'^process_login$', views.login),

    url(r'^logout$', views.logout),
    url(r'^faq$', views.faq),
    url(r'^privacy_policy$', views.privacy_policy),
    url(r'^terms_conditions$', views.terms_conditions),
    url(r'^products$', views.products),
    url(r'^about$', views.about),
    url(r'^profile$', views.profile),
    url(r'^books/delete/(?P<book_id>\d+)$', views.delete_book),
    url(r'^books/delete1/(?P<book_id>\d+)$', views.delete_book1),

    url(r'^books$', views.books),
    url(r'^books/(?P<book_id>\d+)$', views.book_detail),
    url(r'^borrow/(?P<book_id>\d+)$', views. borrow),
    url(r'^question$', views.question), 
]
