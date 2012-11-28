from django import template

register = template.Library()


@register.filter
def is_school_admins_for(user, university):
    return user.academy_roles.filter(university=university, role=3).exists()


@register.filter
def is_professor_for(user, university):
    return user.academy_roles.filter(university=university, role=2).exists()


@register.filter
def is_student_of(user, university):
    return user.academy_roles.filter(university=university, role=1).exists()
