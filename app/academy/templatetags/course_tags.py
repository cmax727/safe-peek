from django import template

register = template.Library()


@register.filter
def is_member_of(user, course):
    try:
        return user.coursemembership_set.get(user=user).status == 1
    except:
        False


@register.filter
def membership_status(user, course):
    try:
        return user.coursemembership_set.get(user=user).status

    except:
        return 0


@register.filter
def is_manager_of(user, course):
    return user == course.professor


@register.filter
def is_enrolled_in(user, course):
    professor = user == course.professor
    active_students = user.coursemembership_set.filter(course=course, status=1).exists()
    return professor or active_students
