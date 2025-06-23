from django.contrib import admin
from .models import Game, TopUpProduct, TopUpOrder

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'game_id', 'is_active')
    search_fields = ('name', 'game_id')

@admin.register(TopUpProduct)
class TopUpProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'game', 'price', 'in_game_currency')
    search_fields = ('name', 'game__name')
    list_filter = ('game',)

@admin.register(TopUpOrder)
class TopUpOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_email', 'product', 'status', 'created_at')
    search_fields = ('user_email', 'product__name')
    list_filter = ('status', 'created_at')