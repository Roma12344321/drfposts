from .models import Post, Favorite
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PostSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(read_only=True, source='user')
    class Meta:
        model = Post
        fields = ('id','title','content','user_details')

class PostSerializerForUser(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','title','content')


class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'post', 'added_date']

class PostUserSerializer(serializers.ModelSerializer):
    post_details = serializers.SerializerMethodField(read_only=True)

    def get_post_details(self, user):
        posts = Post.objects.filter(user=user)
        post_serializer = PostSerializerForUser(posts, many=True)
        return post_serializer.data

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'post_details')