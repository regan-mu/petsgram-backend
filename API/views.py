from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from .models import User, Post, Comment, Like, Follow
from .serializers import UserSerializer, PostSerializer, UpdateUserSerializer, CommentSerializer, LikeSerializer, FollowSerializer, SimpleUserSerializer, UpdateAvatarSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.select_related().all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ListUsersAPIView(generics.ListAPIView):
    queryset = User.objects.select_related().all()
    serializer_class = SimpleUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get("username") if self.request.query_params.get("username") != None else ""
        return User.objects.filter(username__icontains=query)


class RetrieveUserAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


class UpdateUserAPIView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UpdateAvatarAPIView(generics.UpdateAPIView):
    serializer_class = UpdateAvatarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

class CreateListPostView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        owner = self.request.user
        posts = Post.objects.filter(owner=owner.id)
        return posts
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response({"detail": "Created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = Follow.objects.filter(following=user).values_list('followed', flat=True)
        if not following_users:
            return Post.objects.all()
        return Post.objects.filter(owner__in=following_users)
        

class DeleteUpdatePostView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.select_related().all()
  
    
# Comments

class CreateListCommentsAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        post = self.kwargs['pk']
        return Comment.objects.filter(post=post).all()
    
    def perform_create(self, serializer):
        post_id = self.kwargs["pk"]
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValidationError({"detail": "Post doesn't exist"})
        if serializer.is_valid():
            owner = self.request.user
            serializer.save(post=post, owner=owner)
            return Response({"detail": "Comment added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateLikeAPIView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    
    def perform_create(self, serializer):
        owner = self.request.user
        post_id = self.kwargs["pk"]
        
        if Like.objects.filter(owner=owner, post_id=post_id).exists():
            raise ValidationError({"detail": "You have already liked this post"})
        
        post = Post.objects.get(id=post_id)
        serializer.save(post=post, owner=owner)


class RemoveLike(generics.DestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        post_id = self.kwargs["pk"]
        queryset = Like.objects.filter(post_id=post_id, owner=user)
        return queryset
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)

        return obj
    

class FollowUser(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    queryset = Follow.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        followed_id = self.request.data["follow_id"]
        if Follow.objects.filter(following__id=user.id, followed__id=followed_id).exists():
            raise ValidationError({"detail": "Already follows this user"})
        
        followed = User.objects.get(id=followed_id)
        serializer.save(following=user, followed=followed)


class UnFollowUserAPIView(generics.DestroyAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        following = self.request.user
        followed_id = self.kwargs["pk"]

        return Follow.objects.filter(following_id=following.id, followed_id=followed_id)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)

        return obj

    # Test the unfollow logic
    # Than start the frontend
    

