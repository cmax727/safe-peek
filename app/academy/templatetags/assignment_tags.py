from django import template

register = template.Library()


@register.filter
def is_member_of(user, assignment):
    try:
        return assignment.assignmentmembership_set.get(user=user)
    except:
        False
