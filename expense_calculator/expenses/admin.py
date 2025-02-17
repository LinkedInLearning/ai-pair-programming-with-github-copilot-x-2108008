from django.contrib import admin

from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'timestamp', 'category')
    list_filter = ('timestamp',)
    search_fields = ('name', 'category__name')
