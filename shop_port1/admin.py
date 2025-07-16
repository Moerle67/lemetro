from django.contrib import admin
from .models import Product, Category, ProductGroup, ArticleGroup, Article, Deliver, CartItem, Order
from django.utils.html import format_html

# ✅ Warenzugang entfernt, da es jetzt Product heißt
# admin.site.register(Product)
admin.site.register(ArticleGroup)
admin.site.register(Article)
admin.site.register(Deliver)
# admin.site.register(CartItem)
admin.site.register(Order)


#@admin.register(Article)
#class FrageBlock(admin.ModelAdmin):  # ✅
#list_display = ['designation', 'price', 'deliver', 'image_preview']
#    list_filter = ['articlegroup', 'deliver']#
#
#    def image_preview(self, obj):
#        if obj.image:
#            return format_html('<img src="{}" style="height: 50px;"/>', obj.image.url)
#        return "-"
#    image_preview.short_description = "Bild"

#@admin.register(Category)
#class CategoryAdmin(admin.ModelAdmin):
#    list_display = ('name', 'slug', 'image_tag')  # `image_tag` statt `image` verwenden
#    prepopulated_fields = {'slug': ('name',)}
#
#   def image_tag(self, obj):
#       if obj.image:
#            return format_html('<img src="{}" style="width: 50px; height: auto;" />'.format(obj.image.url))
#        return "(Kein Bild)"

#    image_tag.allow_tags = True
#    image_tag.short_description = "Vorschau"

@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ("number", "name")

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_filter = ['user',]