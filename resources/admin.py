from django.contrib import admin
from .models import ResourceCategory, MemberResource


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MemberResource)
class MemberResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'resource_type', 'is_premium', 'is_featured', 'view_count', 'created_at')
    list_filter = ('category', 'resource_type', 'is_premium', 'is_featured', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('view_count', 'download_count', 'created_at', 'updated_at')
