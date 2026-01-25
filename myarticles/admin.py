from django.contrib import admin
from django.utils.html import format_html, mark_safe 
from .models import Products, Category, Promotions
from import_export.admin import ImportExportModelAdmin
from adminsortable2.admin import SortableAdminMixin

class ProductsAdmin(SortableAdminMixin,ImportExportModelAdmin):
    
    list_display = ('display_image', 'name', 'price', 'stock', 'is_kilo', 'stock_status')
    list_editable = ('price', 'stock', 'is_kilo')
    list_display_links = ('name',)
    change_list_template = 'admin/mix_final.html'
    search_fields = ('name', 'details') 
    list_filter = ('category',)

    class Media:
        js = ('JavaScript/admin_automatizado.js',)

    def display_image(self, obj):
        """Displays a thumbnail of the product image in the admin panel."""
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: contain; border-radius: 5px; border: 1px solid #ddd;" />', obj.image.url)
        return "No Image"
    
    display_image.short_description = "Image"

    def stock_status(self, obj):
        """Displays a colored label indicating stock levels."""
        if obj.stock == 0:
            return mark_safe('<span style="color: red; font-weight: bold;">OUT OF STOCK ❌</span>')
        elif obj.stock < 5:
            return format_html('<span style="color: orange; font-weight: bold;">LOW ({}) ⚠️</span>', obj.stock)
        
        return format_html('<span style="color: green; font-weight: bold;">OK ({}) ✅</span>', obj.stock)
    
    stock_status.short_description = "Status"

class CategoryAdmin(SortableAdminMixin,admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_display_links = ('name',)
    

admin.site.register(Products, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Promotions)