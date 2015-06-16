from django import template
from app.models import Subscription

register = template.Library()

__author__ = 'marvin'


def check_subscribe(context, master_user):
    request = context['request']
    follower = Subscription.objects.filter(follower=request.user).first()
    return {
        "is_subscribe": follower and follower.is_master(master_user),
        "master": master_user,
    }

register.inclusion_tag('app/subscription.html', takes_context=True)(check_subscribe)
