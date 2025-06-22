from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Flight, Hotel, MatchTicket, Activity, Booking, Package

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'phone_number', 'address')
        read_only_fields = ('id',)

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class MatchTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchTicket
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    flight = FlightSerializer(read_only=True, many=True)
    hotel = HotelSerializer(read_only=True, many=True)
    match_ticket = MatchTicketSerializer(read_only=True, many=True)
    activity = ActivitySerializer(read_only=True, many=True)
    flight_ids = serializers.PrimaryKeyRelatedField(
        queryset=Flight.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    hotel_ids = serializers.PrimaryKeyRelatedField(
        queryset=Hotel.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    match_ticket_ids = serializers.PrimaryKeyRelatedField(
        queryset=MatchTicket.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    activity_ids = serializers.PrimaryKeyRelatedField(
        queryset=Activity.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    status = serializers.ChoiceField(choices=Booking.STATUS_CHOICES, required=False)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'flight', 'hotel', 'match_ticket', 'activity', 
                 'flight_ids', 'hotel_ids', 'match_ticket_ids', 'activity_ids',
                 'status', 'total_price', 'booking_date', 'updated_at']
        read_only_fields = ['id', 'user', 'booking_date', 'updated_at']

    def validate(self, data):
        # If this is a status update
        if len(data) == 1 and 'status' in data:
            instance = getattr(self, 'instance', None)
            if instance and instance.status != 'pending' and data['status'] == 'cancelled':
                raise serializers.ValidationError("Only pending bookings can be cancelled.")
            return data

        # For new bookings
        if not any([
            data.get('flight_ids'),
            data.get('hotel_ids'),
            data.get('match_ticket_ids'),
            data.get('activity_ids')
        ]):
            raise serializers.ValidationError("At least one booking type (flight, hotel, match ticket, or activity) is required.")

        # Calculate total price
        calculated_price = 0
        if data.get('flight_ids'):
            calculated_price += sum(flight.price for flight in data['flight_ids'])
        if data.get('hotel_ids'):
            calculated_price += sum(hotel.price_per_night for hotel in data['hotel_ids'])
        if data.get('match_ticket_ids'):
            calculated_price += sum(ticket.price for ticket in data['match_ticket_ids'])
        if data.get('activity_ids'):
            calculated_price += sum(activity.price for activity in data['activity_ids'])

        if 'total_price' in data and calculated_price != data['total_price']:
            raise serializers.ValidationError(f"Total price ({data['total_price']}) does not match the sum of items ({calculated_price})")

        return data

    def create(self, validated_data):
        # Extract the IDs for each related field
        flight_ids = validated_data.pop('flight_ids', [])
        hotel_ids = validated_data.pop('hotel_ids', [])
        match_ticket_ids = validated_data.pop('match_ticket_ids', [])
        activity_ids = validated_data.pop('activity_ids', [])

        # Create the booking
        booking = Booking.objects.create(
            user=self.context['request'].user,
            total_price=validated_data['total_price'],
            status='pending'
        )

        # Add the related objects
        booking.flight.set(flight_ids)
        booking.hotel.set(hotel_ids)
        booking.match_ticket.set(match_ticket_ids)
        booking.activity.set(activity_ids)

        return booking

class PackageSerializer(serializers.ModelSerializer):
    flights = FlightSerializer(many=True, read_only=True)
    hotels = HotelSerializer(many=True, read_only=True)
    match_tickets = MatchTicketSerializer(many=True, read_only=True)
    activities = ActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'phone_number', 'address')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'phone_number': {'required': False},
            'address': {'required': False}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords don't match."})
        return data

    def create(self, validated_data):
        # Remove confirm_password from the data
        validated_data.pop('confirm_password', None)
        
        # Create user with default role
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='user',  # Set default role
            phone_number=validated_data.get('phone_number', ''),
            address=validated_data.get('address', '')
        )
        return user 