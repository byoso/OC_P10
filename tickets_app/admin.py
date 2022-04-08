from django.contrib import admin
from .models import Ticket, Projects


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'referent')


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Projects, ProjectsAdmin)
