from rest_framework.routers import DefaultRouter

from .views import (
    CreatorViewSet,
    MovieViewSet,
    GenreViewSet
    )

router = DefaultRouter()
router.register('creator', CreatorViewSet)
router.register('movie', MovieViewSet)
router.register('genre', GenreViewSet)

urlpatterns = [

]

urlpatterns += router.urls