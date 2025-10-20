from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @swagger_auto_schema(
        operation_description="List posts or filter by username",
        manual_parameters=[
            openapi.Parameter(
                "username",
                openapi.IN_QUERY,
                description="Filter posts by username",
                type=openapi.TYPE_STRING,
            )
        ],
        responses={200: PostSerializer(many=True)},
    )
    def list(self, request):
        username = request.query_params.get("username")
        queryset = Post.objects.all().order_by("-created_datetime")
        if username:
            queryset = queryset.filter(username=username)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new post",
        request_body=PostSerializer,
        responses={201: PostSerializer, 400: "Bad Request"},
    )
    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a post (partial update)",
        request_body=PostSerializer,
        responses={200: PostSerializer, 400: "Bad Request"},
    )
    def partial_update(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a post", responses={204: "No Content"}
    )
    def destroy(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Like a post", responses={200: "Post liked"}
    )
    @action(detail=True, methods=["post"], url_path="like")
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        post.likes += 1
        post.save()
        return Response({"status": "liked", "likes": post.likes})

    @swagger_auto_schema(
        operation_description="Unlike a post", responses={200: "Post unliked"}
    )
    @action(detail=True, methods=["post"], url_path="unlike")
    def unlike(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        post.likes = max(post.likes - 1, 0)
        post.save()
        return Response({"status": "unliked", "likes": post.likes})


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer

    @swagger_auto_schema(
        operation_description="Add a comment to a post",
        request_body=CommentSerializer,
        responses={201: CommentSerializer, 400: "Bad Request"},
    )
    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        serializer.save(post=post)
