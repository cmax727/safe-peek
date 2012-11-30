from django import template

register = template.Library()


@register.filter
def already_submit(user, assignment):
    try:
        submit = assignment.assignmentsubmit_set.get(user=user)
        return submit
    except:
        False
