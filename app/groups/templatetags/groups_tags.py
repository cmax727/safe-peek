from django import template

register = template.Library()

@register.filter
def is_member_of(user, group):
    try:
        return group.groupmembership_set.get(user=user).status == 1
    except:
        False


@register.filter
def membership_status(user, group):
    try:
        return group.groupmembership_set.get(user=user).status

    except:
        return 0


@register.filter
def is_manager_of(user, group):
    return user == group.created_by
