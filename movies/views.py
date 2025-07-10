from django.shortcuts import get_object_or_404, render

from .models import Movie


def home(request):
    movies = Movie.objects.order_by("-release_date")[:9]
    context = {"movies": movies}
    return render(request, "movies/home.html", context)


def detail(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    return render(request, "movies/detail.html", context={"movie": movie})
