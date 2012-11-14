from django import template
from friendship.models import Friend

register = template.Library()

@register.filter
def is_friend_with(request_user, other_user):
    if request_user != other_user:
        return Friend.objects.are_friends(request_user, other_user)
    return True
