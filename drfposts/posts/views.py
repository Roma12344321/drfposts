from django.contrib.auth.models import User
from django.forms import model_to_dict
from rest_framework import generics, status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Favorite
from .serializers import PostSerializer, PostUserSerializer


class PostAPIView(APIView):
    def get(self, request):
        posts = Post.objects.select_related('user').all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        title = request.data['title']
        content = request.data['content']
        username = request.data['username']
        user = User.objects.get(username=username)
        Post.objects.create(title=title, content=content, user_id=user.id)
        return Response({"success": "success"})


class UserAPIView(APIView):
    def get(self, request):
        name = str(request.GET.get("name", ""))
        user = User.objects.get(username=name)
        return Response(model_to_dict(user))

    def post(self, request):
        if request.data['username'] != "" and request.data['email'] != "" and request.data['password'] != "":
            user_new = User(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password']
            )
            user_new.set_unusable_password()
            user_new.password = request.data['password']
            user_new.save()
            return Response({"success": "success"})


class UsersPostAPIView(APIView):
    def get(self, request):
        name = request.GET.get("name", "")
        users = User.objects.filter(username=name).prefetch_related('user')
        serializer = PostUserSerializer(users, many=True)
        return Response(serializer.data)


def index(request):
    return render(request, "index.html")


class DeletePostAPIView(APIView):
    def post(self, request):
        id = int(request.data['id'])
        post = Post.objects.get(id=id)
        post.delete()
        return Response({"success": "success"})

class GetFavouritePostAPIView(APIView):
    def get(self, request):
        name = request.GET.get("name", "")
        users = User.objects.get(username=name)
        favourites = Favorite.objects.filter(user=users)
        posts = [fav.post for fav in favourites]
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
