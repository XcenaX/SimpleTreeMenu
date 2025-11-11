from django.contrib import admin
from .models import Menu, MenuItem

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0
    fields = ('parent', 'title', 'named_url', 'url', 'order',)
    autocomplete_fields = ('parent',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'title',)
    search_fields = ('name', 'title',)
    inlines = [MenuItemInline]

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'order', 'named_url', 'url')
    list_filter = ('menu',)
    search_fields = ('title', 'named_url', 'url')
    autocomplete_fields = ('parent', 'menu')
