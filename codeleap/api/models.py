from django.db import models


class Post(models.Model):
    username = models.CharField(max_length=150)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="post_images/", null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.username}"


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    content = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.username} on {self.post.title}"
