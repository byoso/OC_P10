from django.contrib import admin
from .models import Issue, Project, Contributor


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assignee')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project',)

admin.site.register(Issue, IssueAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
