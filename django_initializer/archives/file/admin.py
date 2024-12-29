from django.contrib import admin

from file.models import File


# Register your models here.
class FileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in File._meta.fields]

admin.site.register(File, FileAdmin)