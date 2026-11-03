from django.contrib import admin
from .models import ContactMessage, Project


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'order', 'created_at')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'short_description', 'technologies')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order', 'is_featured', 'category')
