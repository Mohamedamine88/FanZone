from .models import Package, Flight, Hotel, MatchTicket, Activity

class Chatbot:
    def __init__(self):
        self.conversation_history = []

    def process_message(self, message, user=None):
        message = message.lower()
        
        # Add message to conversation history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Basic intent recognition
        if any(word in message for word in ['hello', 'hi', 'hey']):
            response = "Hello! I'm your FanZone assistant. How can I help you today? I can help you find packages for matches, flights, hotels, or activities."
        
        elif any(word in message for word in ['package', 'deal', 'offer']):
            packages = Package.objects.all()[:5]
            if packages:
                response = "Here are some popular packages:\n\n"
                for package in packages:
                    response += f"- {package.name}: {package.description}\n  Price: ${package.price}\n\n"
            else:
                response = "I don't have any packages available at the moment. Would you like me to help you create a custom itinerary?"
        
        elif any(word in message for word in ['flight', 'fly', 'plane']):
            flights = Flight.objects.all()[:5]
            if flights:
                response = "Here are some available flights:\n\n"
                for flight in flights:
                    response += f"- Flight {flight.flight_number}: {flight.departure_city} to {flight.arrival_city}\n  Price: ${flight.price}\n\n"
            else:
                response = "I don't have any flights available at the moment. Please check back later or let me help you with something else."
        
        elif any(word in message for word in ['hotel', 'stay', 'accommodation']):
            hotels = Hotel.objects.all()[:5]
            if hotels:
                response = "Here are some recommended hotels:\n\n"
                for hotel in hotels:
                    response += f"- {hotel.name} in {hotel.city}\n  Price per night: ${hotel.price_per_night}\n  Rating: {hotel.rating}/5\n\n"
            else:
                response = "I don't have any hotels available at the moment. Please check back later or let me help you with something else."
        
        elif any(word in message for word in ['match', 'game', 'ticket']):
            matches = MatchTicket.objects.all()[:5]
            if matches:
                response = "Here are some upcoming matches:\n\n"
                for match in matches:
                    response += f"- {match.match_name}\n  Stadium: {match.stadium}\n  Price: ${match.price}\n\n"
            else:
                response = "I don't have any match tickets available at the moment. Please check back later or let me help you with something else."
        
        elif any(word in message for word in ['activity', 'tour', 'visit']):
            activities = Activity.objects.all()[:5]
            if activities:
                response = "Here are some popular activities:\n\n"
                for activity in activities:
                    response += f"- {activity.name} in {activity.city}\n  Price: ${activity.price}\n\n"
            else:
                response = "I don't have any activities available at the moment. Please check back later or let me help you with something else."
        
        elif any(word in message for word in ['help', 'support']):
            response = """I can help you with:
1. Finding match tickets
2. Booking flights
3. Finding hotels
4. Discovering local activities
5. Finding package deals
6. Creating custom itineraries

Just let me know what you're interested in!"""
        
        else:
            response = "I'm not sure I understand. Would you like help with booking match tickets, flights, hotels, or activities? Or would you like to see our package deals?"
        
        # Add response to conversation history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response

    def get_conversation_history(self):
        return self.conversation_history 