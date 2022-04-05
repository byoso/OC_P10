from django.contrib import admin
from .models import Ticket, Project


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'referent')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Project, ProjectAdmin)
