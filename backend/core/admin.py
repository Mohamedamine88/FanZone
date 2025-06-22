from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Flight, Hotel, MatchTicket, Activity, Booking, Package

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'phone_number', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'departure_city', 'arrival_city', 'departure_time', 'price', 'available_seats', 'image_url')
    list_editable = ('departure_city', 'arrival_city', 'departure_time', 'price', 'available_seats', 'image_url')
    list_filter = ('departure_city', 'arrival_city')
    search_fields = ('flight_number', 'departure_city', 'arrival_city')

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'price_per_night', 'available_rooms', 'rating', 'image_url', 'get_description')
    list_editable = ('city', 'price_per_night', 'available_rooms', 'rating', 'image_url')
    list_filter = ('city', 'rating')
    search_fields = ('name', 'city', 'address')
    fields = ('name', 'city', 'address', 'description', 'price_per_night', 'available_rooms', 'rating', 'image_url')

    def get_description(self, obj):
        return obj.description[:100] + '...' if len(obj.description) > 100 else obj.description
    get_description.short_description = 'Description'

@admin.register(MatchTicket)
class MatchTicketAdmin(admin.ModelAdmin):
    list_display = ('match_name', 'stadium', 'match_date', 'price', 'available_tickets', 'image_url', 'match_type')
    list_editable = ('stadium', 'match_date', 'price', 'available_tickets', 'image_url', 'match_type')
    list_filter = ('stadium', 'match_type')
    search_fields = ('match_name', 'stadium')

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'match_type':
            kwargs['choices'] = [
                ('CAN', 'CAN 2025'),
                ('WORLD_CUP', 'World Cup 2030')
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'price', 'available_spots', 'activity_date', 'image_url', 'activity_type', 'get_description')
    list_editable = ('city', 'price', 'available_spots', 'activity_date', 'image_url', 'activity_type')
    list_filter = ('city', 'activity_type')
    search_fields = ('name', 'city', 'description')

    def get_description(self, obj):
        return obj.description[:100] + '...' if len(obj.description) > 100 else obj.description
    get_description.short_description = 'Description'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'total_price', 'booking_date')
    list_filter = ('status', 'booking_date')
    search_fields = ('user__username', 'user__email')

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount')
    filter_horizontal = ('flights', 'hotels', 'match_tickets', 'activities')
    search_fields = ('name', 'description')
