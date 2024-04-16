from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    SavedMovieViewSet,
    MovieCommentView,
    RatingView,
    LikeView,
)


router = DefaultRouter()


router.register('saved-movie',SavedMovieViewSet, 'saved movie' )
router.register('movie-comment', MovieCommentView, 'comment')
router.register( 'movie-rating', RatingView, 'rating')
router.register( 'movie-like', LikeView, 'like')


urlpatterns = [

]
urlpatterns += router.urls