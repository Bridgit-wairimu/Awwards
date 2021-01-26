from django.conf.urls import url
from . import views
from .views import PostListView,PostDetailView,PostCreateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    url('^$',PostListView.as_view(),name = 'index'),
    url(r'^register/', views.registerPage, name="register"),
    url(r'^login/', views.loginPage, name="login"),
    url(r'^logout/', views.logoutUser, name="logout"),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    url(r'^post/new/', PostCreateView.as_view(), name='post-create'),
    url(r'^search/', views.search_project, name='search'),
    url(r'^projects/<post>',views.projects, name='projects'),
  ]


if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

    