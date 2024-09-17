from django.contrib import admin
from .models import User, Post, Comment, Follower

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')

class PostAdmin(admin.ModelAdmin):
    list_display = ('creater', 'content_text', 'date_created')
    search_fields = ('content_text', 'creater__username')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'commenter', 'comment_content', 'comment_time')
    search_fields = ('comment_content', 'commenter__username')

class FollowerAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('followers',)

# Register the models and custom admin classes
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follower, FollowerAdmin)
