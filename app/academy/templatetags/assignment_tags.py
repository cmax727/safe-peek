from django import template

register = template.Library()


@register.filter
def already_submit(user, assignment=None):
    try:
        submit = assignment.assignmentsubmit_set.get(user=user)
        return submit
    except:
        return False
