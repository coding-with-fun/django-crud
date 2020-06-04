from django.contrib import admin
from crudApp.models import UserProfileInfo, User, Project, ProjectType, ProjectTag

# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(Project)
admin.site.register(ProjectType)
admin.site.register(ProjectTag)
