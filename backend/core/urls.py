from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, FlightViewSet, HotelViewSet,
    MatchTicketViewSet, ActivityViewSet,
    BookingViewSet, PackageViewSet,
    chat_message, chat_history,
    home, login_view, logout_view, register_view,
    flights, hotels, match_tickets,
    activities, packages, bookings,
    profile
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'flights', FlightViewSet)
router.register(r'hotels', HotelViewSet)
router.register(r'match-tickets', MatchTicketViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'packages', PackageViewSet)

urlpatterns = [
    # Template-based views
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('flights/', flights, name='flights'),
    path('hotels/', hotels, name='hotels'),
    path('match-tickets/', match_tickets, name='match_tickets'),
    path('activities/', activities, name='activities'),
    path('packages/', packages, name='packages'),
    path('bookings/', bookings, name='bookings'),
    path('profile/', profile, name='profile'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/chat/message/', chat_message, name='chat_message'),
    path('api/chat/history/', chat_history, name='chat_history'),
] 