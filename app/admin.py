from django.contrib import admin
from app.models import BlogRecord, Subscription


class BlogRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created')
    list_filter = ('user',)

admin.site.register(BlogRecord, BlogRecordAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('follower',)
    list_filter = ('follower',)

admin.site.register(Subscription, SubscriptionAdmin)
