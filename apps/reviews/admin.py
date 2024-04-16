from django.contrib import admin
from .models import (
    MovieComment,
    MovieRating,
    MovieLike,
)


admin.site.register([MovieComment, MovieRating, MovieLike])