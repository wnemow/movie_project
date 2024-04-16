from rest_framework import serializers


from .models import (
    Creator,
    Movie,
    Genre
    )


class CreatorCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Creator
        exclude = ('slug',)

    def validate(self, attrs):
        author = attrs.get('name')
        if Creator.objects.filter(name=author).exists():
            raise serializers.ValidationError(
                'This creator already exists'
            )
        user = self.context['request'].user                   
        attrs['user'] = user
        return attrs
    

class CreatorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator 
        fields = ['first_name', 'last_name', 'slug', 'user']  


class CreatorRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Creator
        fields = '__all__'

    def validate(self, attrs):                               
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class MovieCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username') # 4
    
    class Meta:
        model = Movie
        exclude = ('slug',)

    def validate(self, attrs: dict):
        movie = attrs.get('title')
        if Movie.objects.filter(title=Movie).exists():
            raise serializers.ValidationError(
                'This movie already exists'
            )
        user = self.context['request'].user                 # 4
        attrs['user'] = user
        return attrs
    

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie 
        fields = ['title', 'creator', 'slug', 'user']       # 5


class MovieUpdateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 6

    class Meta:
        model = Movie                                       # 6
        fields = ['title', 'creator', 'desc', 'image', 'year_publ', 'pages', 'slug', 'status', 'movie', 'genre', 'user']
    
    def validate(self, attrs):                                 # 6
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class MovieRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')   # 7

    class Meta:
        model = Movie
        fields = '__all__'

    def validate(self, attrs):                                 # 7
        user = self.context['request'].user
        attrs['user'] = user
        return attrs
    

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)

    #     rep['comments'] = CommentSerializer(
    #     instance.movies_comments.all(), many=True
    #     ).data

    #     rating = instance.movies_ratings.aggregate(Avg('rating'))['rating__avg']   
    #     if rating:
    #         rep['rating'] = round(rating, 1) 
    #     else:
    #         rep['rating'] = 0.0
        
    #     rep['likes'] = instance.movies_likes.all().count()
    #     rep['liked_by'] = LikeSerializer(
    #         instance.movies
    # _likes.all().only('user'), many=True).data 

    #     return rep


class GenreCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')   

    class Meta:
        model = Genre
        fields = ['genre', 'user']                             

    def validate(self, attrs):
        genre = attrs.get('genre')
        if Genre.objects.filter(genre=genre).exists():
            raise serializers.ValidationError(
                'Such genre already exists'
            )
        user = self.context['request'].user                    
        attrs['user'] = user
        return attrs


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
class GenreRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')    
    Movies = MovieListSerializer(read_only=True, many=True)

    class Meta: 
        model = Genre  
        fields = ['user', 'genre', 'movies']                     

    def to_representation(self, instance: Genre):
        movies = instance.movie_genre.all()
        rep = super().to_representation(instance)
        rep['movies'] = MovieListSerializer(
            instance=movies, many=True).data
        return rep
    
    def validate(self, attrs):                                   
        user = self.context['request'].user
        attrs['user'] = user
        return attrs