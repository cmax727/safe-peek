from django import template

register = template.Library()


@register.filter
def is_member_of(user, course):
    try:
        return course.coursemembership_set.get(user=user).status == 1
    except:
        False


@register.filter
def membership_status(user, course):
    try:
        return course.coursemembership_set.get(user=user).status

    except:
        return 0


@register.filter
def is_manager_of(user, course):
    return user == course.professor
