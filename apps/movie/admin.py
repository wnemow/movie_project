from django.contrib import admin

from .models import (
    Creator,
    Movie,
    Genre
)

admin.site.register(Creator)
admin.site.register(Movie)
admin.site.register(Genre)