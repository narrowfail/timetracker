from django.contrib.admin import ModelAdmin, site

from .forms import RowModelForm
from .models import ProjectModel, RowModel


class ProjectModelAdmin(ModelAdmin):
    search_fields = ('id', 'name')
    list_display = ('id', 'name', 'description')
    list_display_links = ('id',)


site.register(ProjectModel, ProjectModelAdmin)


class RowModelAdmin(ModelAdmin):
    form = RowModelForm
    search_fields = ('id', 'week', 'project__name')
    list_display = ('id', 'week', 'project')
    list_display_links = ('id',)
    readonly_fields = ('total_duration',)


site.register(RowModel, RowModelAdmin)
