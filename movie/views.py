from django.shortcuts import render
from django.http import HttpResponse
from . import scrapper
from .models import Movie, Movie_link


def index(request):
    return render(request, 'movie/search.html')


# search for a movieself.If movie already exists, then return all the related
# links from db otherwise scarp imdb.

def search_movie(request):
    movie_name = request.POST['query']
    if movie_name.strip() == "":
        error_message = "Oohoo! You forgot to enter movie...."
        return render(request, 'movie/search.html', {"error_message": error_message})
    movies = Movie_link.objects.filter(movie__icontains = movie_name)
    if len(movies) == 0:
        url = scrapper.create_url(movie_name)
        movie_dict = scrapper.extract_all_items(url)
        for key,value in movie_dict.items():
            movie_links = Movie_link(
                                movie = value,
                                movie_links = key
                            )
            movie_links.save()
        movies = Movie_link.objects.filter(movie__icontains = movie_name)
    context = {"movies": movies}
    return render(request, "movie/movie-list.html", context)


#if movie details already exists in db, then return movie object
# otherwise store details in db first

def movie_details(request, movie_url):
    movie_details_list = scrapper.get_movie_details(movie_url[29:])
    try:
        movie= Movie.objects.get(movie_name =  movie_details_list[0])
    except:
        movie = Movie(movie_name = movie_details_list[0] ,
                    movie_director = movie_details_list[1] ,
                    ratings = float(movie_details_list[2]) ,
                    certificate = movie_details_list[3] ,
                    duration = movie_details_list[4] ,
                    movie_image_url = movie_details_list[5] ,
                    movie_video_url = movie_details_list[6] ,
                    genre = movie_details_list[7] ,
                    release_date = movie_details_list[8] ,
                    movie_credit_summary = movie_details_list[9] )
        movie.save()
    context = {"movie": movie}
    return render(request, "movie/movie-details.html", context)
