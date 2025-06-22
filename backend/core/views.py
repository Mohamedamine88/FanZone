from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Flight, Hotel, MatchTicket, Activity, Booking, Package, MatchType, ActivityType
from .serializers import (
    UserSerializer, FlightSerializer, HotelSerializer,
    MatchTicketSerializer, ActivitySerializer, BookingSerializer,
    PackageSerializer, UserRegistrationSerializer
)
from .chatbot import Chatbot
from django import forms
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone_number', 'address')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.address = self.cleaned_data['address']
        if commit:
            user.save()
        return user

# Initialize chatbot
chatbot = Chatbot()

# Template-based views
def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def flights(request):
    flights = Flight.objects.all()
    return render(request, 'flights.html', {'flights': flights})

@login_required
def hotels(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels.html', {'hotels': hotels})

@login_required
def match_tickets(request):
    match_type = request.GET.get('match_type')
    tickets = MatchTicket.objects.all()
    
    if match_type:
        tickets = tickets.filter(match_type=match_type)
    
    context = {
        'tickets': tickets,
        'match_types': MatchType.choices,
        'selected_type': match_type
    }
    return render(request, 'match_tickets.html', context)

@login_required
def activities(request):
    activity_type = request.GET.get('activity_type')
    activities = Activity.objects.all()
    
    if activity_type:
        activities = activities.filter(activity_type=activity_type)
    
    context = {
        'activities': activities,
        'activity_types': ActivityType.choices,  # This line passes all activity types
        'selected_type': activity_type
    }
    return render(request, 'activities.html', context)

@login_required
def packages(request):
    packages = Package.objects.all()
    return render(request, 'packages.html', {'packages': packages})

@login_required
def bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings.html', {'bookings': bookings})

@login_required
def profile(request):
    return render(request, 'profile.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

class MatchTicketViewSet(viewsets.ModelViewSet):
    queryset = MatchTicket.objects.all()
    serializer_class = MatchTicketSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data.get('status') == 'cancelled':
            # Delete the booking instead of updating its status
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().partial_update(request, *args, **kwargs)

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def book(self, request, pk=None):
        package = self.get_object()
        booking = Booking.objects.create(
            user=request.user,
            total_price=package.price * (1 - package.discount/100)
        )
        booking.flight.set(package.flights.all())
        booking.hotel.set(package.hotels.all())
        booking.match_ticket.set(package.match_tickets.all())
        booking.activity.set(package.activities.all())
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def chat_message(request):
    """
    Handle chat messages from users
    """
    message = request.data.get('message')
    if not message:
        return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    response = chatbot.process_message(message, request.user)
    return Response({'response': response})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def chat_history(request):
    """
    Get chat history for the current user
    """
    history = chatbot.get_conversation_history()
    return Response({'history': history})
