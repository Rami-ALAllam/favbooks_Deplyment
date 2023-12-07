

from django.urls import path
from . import views

urlpatterns = [
    path('', views.form),
    path('register', views.register),
    path('login', views.login),
    path('main', views.main),
    path('logout', views.logout),
    path('create_book', views.book_create),
    path('book/<int:id>', views.show_book),
    path('book/update', views.update_book),
    path('book/<int:id>/destroy', views.destroy),
    path('book/<int:id>/favorite', views.favorite),
    path('book/<int:id>/unfavorite', views.unfavorite),
    path('book/myfav', views.myfav),
]