from django.contrib import admin
from .models import *


admin.site.register(Course)
admin.site.register(CourseMembership)
admin.site.register(University)
admin.site.register(UniversityMembership)
admin.site.register(Syllabus)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmit)
