from django.contrib import admin
from .models import Issues, Projects


class IssuesAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'referent')


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)


admin.site.register(Issues, IssuesAdmin)
admin.site.register(Projects, ProjectsAdmin)
