from django.conf.urls import url
from . import views

app_name ='movie'

urlpatterns = [
    url(r'^$', views.index , name='index'),
    url(r'^search/$', views.search_movie , name='search_movie' ),
    url(r'^search/(?P<movie_url>.*)/$' , views.movie_details, name='movie_details'),
]
