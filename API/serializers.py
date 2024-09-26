from rest_framework import serializers
from .models import User, Post, Comment, Like, Follow
from django.template.defaultfilters import timesince_filter


class SimpleUserSerializer(serializers.ModelSerializer):
    """Simple User serializer to be used in the Post serializer to return the post owners"""
    class Meta:
        model = User
        fields = ["id", "username", "email", "bio", "avatar", "gender"]


class CommentSerializer(serializers.ModelSerializer):
    owner = SimpleUserSerializer(read_only=True)
    age = serializers.SerializerMethodField(method_name="get_comment_age")
    class Meta:
        model = Comment
        fields = ("id", "message", "created_at", "owner", "age")

    def get_comment_age(self, comment: Comment):
        """Time Since the post was created"""
        timeIsince = timesince_filter(comment.created_at)
        left = timeIsince.split(",")[0]
        number = left.split()[0]
        time = left.split()[1][0]
        return f"{number}{time}"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "created_at", "owner")
        extra_kwargs = {"owner": {"read_only": True}}


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    age = serializers.SerializerMethodField(method_name="get_post_age")
    owner = SimpleUserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ["id", "message", "created_at", "image", "comments", "likes", "age", "owner"]

    def get_post_age(self, post: Post):
        """Time Since the post was created"""
        timeIsince = timesince_filter(post.created_at)
        left = timeIsince.split(",")[0]
        number = left.split()[0]
        time = left.split()[1][0]
        return f"{number}{time}"


class FollowSerializer(serializers.ModelSerializer):
    followers = SimpleUserSerializer(read_only=True)
    following = SimpleUserSerializer(read_only=True)
    class Meta:
        model = Follow
        fields =("id", "created_at", "followers", "following")
    


class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    followings = FollowSerializer(many=True, read_only=True)
    followers = FollowSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "bio", "avatar", "gender", "posts", "followings", "followers"]
        extra_kwargs = {
            "password": {"write_only": True},
            "followings": {"read_only": True},
            "followers": {"read_only": True},
            "bio": {"required": False},
            "avatar": {"required": False}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model=User
        fields = ("username", "email", "bio", "avatar", "gender")
    
    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.exclude(id=user.id).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use"})
        return value
    
    def validate_username(self, value):
        user =self.context["request"].user
        if User.objects.exclude(id=user.id).filter(username=value).exists():
            raise serializers.ValidationError({"username": "Username is taken"})
        return value
        
    def update(self, instance, validated_data):
        instance.bio = validated_data["bio"]
        instance.username = validated_data["username"]
        instance.email = validated_data["email"]
        instance.gender = validated_data["gender"]

        instance.save()
        return instance


class UpdateAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["avatar"]