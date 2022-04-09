from django.contrib import admin
from .models import Issue, Project


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'referent')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)


admin.site.register(Issue, IssueAdmin)
admin.site.register(Project, ProjectAdmin)
