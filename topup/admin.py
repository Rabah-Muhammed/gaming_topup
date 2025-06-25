from django.contrib import admin
from .models import Game, TopUpProduct, TopUpOrder,UserProfile,PaymentTransaction

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
    
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'date_of_birth', 'preferred_game')
    search_fields = ('user__username', 'phone_number')
    list_filter = ('preferred_game',)
    
@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'topup_order', 'status', 'provider', 'created_at')
    search_fields = ('transaction_id', 'provider')
    list_filter = ('status', 'provider', 'created_at')