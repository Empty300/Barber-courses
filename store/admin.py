from django.contrib import admin

from store.models import Lessons


@admin.register(Lessons)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'access_level')
    fields = ('id', 'name', 'access_level', 'description', 'video_file')
    readonly_fields = ('id',)
