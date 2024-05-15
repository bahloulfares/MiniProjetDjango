from django.contrib import admin
from .models import Post, Housing, ClubEvent, SocialEvent, Stage ,Like,Transportation,Comment,Notification

admin.site.register(Post)
admin.site.register(Stage)
admin.site.register(Housing)
admin.site.register(Transportation)
admin.site.register(ClubEvent)
admin.site.register(SocialEvent)
admin.site.register(Like)
admin.site.register(Comment)
# admin.site.register(Reaction)
admin.site.register(Notification)
