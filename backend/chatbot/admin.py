from django.contrib import admin
from .models import Hotel, Flight, Activity, Match, Package, Conversation

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'price_per_night', 'is_ai_suggested', 'created_at')
    list_filter = ('rating', 'is_ai_suggested')
    search_fields = ('name', 'location')

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('departure_city', 'arrival_city', 'airline', 'departure_time', 'price', 'is_ai_suggested')
    list_filter = ('airline', 'is_ai_suggested')
    search_fields = ('departure_city', 'arrival_city', 'airline')

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'duration', 'price', 'is_ai_suggested')
    list_filter = ('is_ai_suggested',)
    search_fields = ('name', 'location')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'date', 'venue', 'ticket_price')
    list_filter = ('date',)
    search_fields = ('home_team', 'away_team', 'venue')

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_price', 'discount_percentage', 'final_price', 'status', 'is_ai_suggested')
    list_filter = ('status', 'is_ai_suggested')
    search_fields = ('name',)
    filter_horizontal = ('activities',)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user_message', 'bot_message')
    list_filter = ('created_at',)
    search_fields = ('user_message', 'bot_message') 