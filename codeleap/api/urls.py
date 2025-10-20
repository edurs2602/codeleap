from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentCreateView

router = DefaultRouter()
router.register(r"careers", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "careers/<int:post_id>/comments/",
        CommentCreateView.as_view(),
        name="post-comments-create",
    ),
]
