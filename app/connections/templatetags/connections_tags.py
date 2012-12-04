from django import template
from friendship.models import Friend

register = template.Library()


@register.filter
def is_friend_with(request_user, other_user):
    if request_user != other_user:
        friends = Friend.objects.are_friends(request_user, other_user)
        sent_requests = request_user.friendship_requests_sent.filter(to_user=other_user)
        return friends or len(sent_requests) > 0
    return True
