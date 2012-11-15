from django import template

register = template.Library()

@register.filter
def is_member_of(user, group):
    return user in group.members.all()

@register.filter
def is_manager_of(user, group):
    return user == group.created_by