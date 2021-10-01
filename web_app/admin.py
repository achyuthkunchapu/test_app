from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Work
# Register your models here.
@admin.register(Work)
class WorkAdmin(ImportExportModelAdmin):
      list_display = ("id","key","Issue_Type","Summary","Status","Application")
