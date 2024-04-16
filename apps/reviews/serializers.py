from rest_framework import serializers 
from django.contrib.auth import get_user_model

from .models import (
    MovieComment,
    MovieRating,
    MovieLike,
    SavedMovie,
)


User = get_user_model() 


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(), 
        source='user.username'
    )
    
    class Meta: 
        model = MovieComment 
        exclude = ['id']

        
class LikeSerializer(serializers.ModelSerializer): 
    user = serializers.ReadOnlyField(source='user.username') 
    
    class Meta: 
        model = MovieLike 
        fields = '__all__'
 
    def create(self, validated_data): 
        user = self.context.get('request').user 
        movie = self.context.get('movie') 
        like = MovieLike.objects.filter(user=user, movie=movie).first() 
        if like: 
            raise serializers.ValidationError('already liked') 
        return super().create(validated_data) 
    
    def unlike(self): 
        user = self.context.get('request').user 
        movie = self.context.get('movie') 
        like = MovieLike.objects.filter(user=user, movie=movie).first()
        if like: 
            like.delete() 
        else: 
            raise serializers.ValidationError('not liked yet')
        

class RatingSerializer(serializers.ModelSerializer): 
    user = serializers.ReadOnlyField(source='user.username') 

    class Meta: 
        model = MovieRating 
        fields = ('rating', 'user', 'movie') 

    def validate(self, attrs): 
        user = self.context.get('request').user 
        attrs ['user'] = user 
        rating = attrs.get('rating') 
        if rating not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
            raise serializers.ValidationError('Incorrect value. The rating should be between 1 and 10.') 
        # if rating: 
        #   raise serializers.ValidationError('already exists') 
        return attrs 
    
    def update(self, instance, validated_data): 
        instance.rating = validated_data.get('rating') 
        instance.save() 
        return super().update(instance, validated_data)
    

class SavedMovieSerializer(serializers.ModelSerializer): 
    user = serializers.ReadOnlyField(source='user.username') 
    
    class Meta: 
        model = SavedMovie 
        fields = 'all' 
        
    def create(self, validated_data): 
        user = self.context.get('request').user 
        request = self.context.get('request').data 
        movie = request.get('movie') 
        favorite = SavedMovie.objects.filter(user=user, movie=movie).first() 
        if not favorite: 
            return super().create(validated_data) 
        raise serializers. ValidationError('This movie has been saved') 
    
    def del_favorite(self, validated_data): 
        user = self.context.get('request').user 
        request = self.context.get('request').data 
        movie = request.get('movie').slug 
        favorite = SavedMovie.objects.filter(user=user, movie=movie).first() 
        if favorite: 
            favorite.delete() 
        else: 
            raise serializers. ValidationError('This movie has not been saved')