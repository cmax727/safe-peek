from django import template

register = template.Library()


@register.filter
def already_submit(user, assignment):
    try:
        return assignment.assignmentsubmit_set.get(user=user)
    except:
        False
