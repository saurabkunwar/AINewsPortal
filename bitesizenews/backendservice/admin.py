from django.contrib import admin
from .models import Article
from import_export.admin import ExportActionMixin

# Register your models here.

class ArticleAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["title", "publisher", "published_date", "category"]
    search_fields = ["title", "publisher", "published_date", "category"]
    list_filter = ["publisher", "published_date", "category"]
    class Meta:
        model = Article

admin.site.register(Article, ArticleAdmin)