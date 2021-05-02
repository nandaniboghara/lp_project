from django.contrib import admin
from .models import Bank, Details

# Register Bank model
class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    # search_fields = ('name')
    list_per_page = 20

admin.site.register(Bank, BankAdmin)

class DetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'interest', 'fees')
    list_display_links = ('id', 'name')
    # search_fields = ('name')
    list_per_page = 20

admin.site.register(Details, DetailsAdmin)