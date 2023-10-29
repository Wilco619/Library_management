from django.urls import path 
from . import views, forms
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view

urlpatterns = [
    path(" /", forms.loginForm, name ="login-form"),
    path("home/", views.home, name ="home"),
    path("books/",views.books, name="books"),
    path("book-details/<bpk>",views.book_details, name="book-details"),
    path("members/",views.members, name="members"),
    path("mdetails/<int:pk>/",views.mdetails, name="mdetails"),

    path("member/",views.MemberView.as_view(),name="member"),
    path("book/",views.BookView.as_view(),name="book"),
    path('search/', views.search_feature, name='search-view'),

    path('book-search/', views.search_book, name='search-book'),
    path('popup/<popk>/', views.pop, name='popup'),



    path("update-member/<upk>/",views.update_member, name="update-member"),
    path("delete-member/<dpk>/",views.delete_member, name="delete-member"),

    path("member-csv",views.member_csv, name="member-csv"),
    path("book-csv",views.book_csv, name="book-csv"),

    


    #user authentication
    path("",forms.loginForm,name="login"),
    path("logoutForm/",forms.logoutForm,name="logoutForm"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)