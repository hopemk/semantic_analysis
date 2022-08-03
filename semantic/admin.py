from django.contrib import admin
from .models import Classification
# Register your models here.

class Classifications(admin.ModelAdmin):
    list_display = ['date_created','text', 'num_rows', 'classification']


admin.site.register(Classification, Classifications)

