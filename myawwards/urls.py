from django.conf.urls import url
from . import views

urlpatterns=[
    url('^$',views.index,name = 'index'),
    url(r'^register/', views.registerPage, name="register"),
    url(r'^login/', views.loginPage, name="login"),
    url(r'^logout/', views.logoutUser, name="logout")

]