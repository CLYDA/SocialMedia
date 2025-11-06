from rest_framework import serializers
from social.models import Post , User
 

class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username', 'email']  


class PostSerializer(serializers.ModelSerializer):
    users = PostUserSerializer(source='author', read_only=True)
    class Meta: 
        model = Post
        fields = ['id', 'users', 'description', 'likes', 'created']