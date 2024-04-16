from rest_framework.viewsets import ModelViewSet, GenericViewSet   
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)   

from .models import (
    Creator,
    Movie,
    Genre     
)
from .permissions import (
    IsOwner
)

from .serializers import (
    CreatorCreateSerializer, 
    CreatorListSerializer, 
    CreatorRetrieveSerializer,
    
    MovieCreateSerializer, 
    MovieListSerializer, 
    MovieUpdateSerializer, 
    MovieRetrieveSerializer,

    GenreCreateSerializer,   
    GenreListSerializer,     
    GenreRetrieveSerializer  
)

class CreatorViewSet(ModelViewSet):      
    queryset = Creator.objects.all()
    serializer_class = CreatorCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreatorCreateSerializer
        elif self.action == 'list':
            return CreatorListSerializer
        elif self.action == 'retrieve':
            return CreatorRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'list': 
            self.permission_classes = [AllowAny]
        elif self.action == 'retrieve': 
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']: 
            self.permission_classes = [IsAdminUser]
        elif self.action == 'destroy': 
            self.permission_classes = [IsOwner]
        return super().get_permissions()
    

class MovieViewSet(ModelViewSet):      # CRUD - Create, Retrieve, Update, Delete, 
    queryset = Movie.objects.all()
    serializer_class = MovieCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return MovieCreateSerializer
        elif self.action == 'list':
            return MovieListSerializer
        elif self.action in ['update', 'partial_update']:
            return MovieUpdateSerializer
        elif self.action == 'retrieve':
            return MovieRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'list': 
            self.permission_classes = [AllowAny]
        elif self.action == 'retrieve': 
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']: 
            self.permission_classes = [IsAdminUser]
        elif self.action == 'destroy': 
            self.permission_classes = [IsOwner]
        return super().get_permissions()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        creator_id = request.query_params.get('creator_id')
        if creator_id:
            queryset = queryset.filter(creator_id=creator_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GenreViewSet(mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return GenreCreateSerializer
        elif self.action == 'list':
            return GenreListSerializer
        elif self.action == 'retrieve':
            return GenreRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'list': 
            self.permission_classes = [AllowAny]
        elif self.action == 'retrieve': 
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']: 
            self.permission_classes = [IsAdminUser]
        elif self.action == 'destroy': 
            self.permission_classes = [IsOwner]
        return super().get_permissions()