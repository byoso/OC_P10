from django.contrib import admin
from .models import Issue, Project, Contributor, Comment


class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'project', 'assignee')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'author', 'issue')


admin.site.register(Issue, IssueAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Comment, CommentAdmin)
