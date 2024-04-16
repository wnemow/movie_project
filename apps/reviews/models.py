from django.db import models
from django.contrib.auth import get_user_model
# from django.urls import reverse


from apps. movie. models import Movie


User = get_user_model ()


class MovieComment (models.Model):
    user = models. ForeignKey (
        to=User,
        on_delete=models. CASCADE,
        related_name='comments'
    )
    movie = models. ForeignKey(
        to=Movie,
        on_delete=models.CASCADE,
        related_name= 'movies_comments'
    )
    comment_text = models. TextField ()
    created_at = models. DateTimeField (auto_now_add=True)
    
    def __str__(self) :
        return f'Comment from {self.user.username} to {self.movie.title}'
    

class MovieRating (models.Model) :
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    RATING_CHOICES = (
        (ONE,'1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR,'4'),
        (FIVE, '5'),
        (SIX, '6'),
        (SEVEN, '7'),
        (EIGHT, '8'),
        (NINE, '9'),
        (TEN, '10'),
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE, 
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    movie = models. ForeignKey (
        to=Movie, 
        on_delete=models.CASCADE, 
        related_name= 'movies_ratings'
    )

    def _str_ (self) -> str:
        return f'{self.rating} points to {self.movie.title}'
    
    class Meta:
        unique_together = ['user', 'movie', 'rating']

    
class MovieLike(models.Model):
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE, 
        related_name= 'likes'
    )
    movie = models.ForeignKey(
    to=Movie, 
    on_delete=models.CASCADE, 
    related_name= 'movies_likes'
    )

    def _str__(self) :
        return f'Liked by {self.user. username}'
    

class SavedMovie(models.Model):
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
    )
    movies = models. ForeignKey (
    to=Movie, 
    on_delete=models. CASCADE,
    )