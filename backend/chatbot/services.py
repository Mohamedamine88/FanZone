import json
import os
import logging
from datetime import datetime, timedelta
from django.db.models import Q
from dotenv import load_dotenv
from django.conf import settings
from django.utils import timezone
import requests

from .models import Hotel, Flight, Activity, Match, Package, Conversation
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

logger = logging.getLogger(__name__)

class ChatbotService:
    def __init__(self):
        try:
            # List available models that support content generation
            models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            logger.info(f"Available models: {[m.name for m in models]}")

            # Choose a valid supported model
            supported_model = 'models/gemini-1.5-flash'
            if supported_model not in [m.name for m in models]:
                supported_model = models[0].name  # fallback if not available

            self.model = genai.GenerativeModel(supported_model)

            # Set generation configuration
            self.chat_config = genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.8,
                top_k=40,
                max_output_tokens=2048,
            )
            self.chat = None
            # Start the chat session
            self.chat = self.model.start_chat(history=[])

            # Define system prompt
            self.system_prompt = """You are a helpful travel package assistant specializing in sports tourism. 
            You help users find and book:
            1. Sports event tickets
            2. Flights to event locations
            3. Hotel accommodations
            4. Local activities and tours
            5. Complete travel packages
            
            Please provide specific, relevant information and always maintain a professional, friendly tone.
            If you don't have specific information about prices or availability, 
            suggest that the user contact customer service for the most up-to-date details."""

            # Send system prompt
            self.chat.send_message(self.system_prompt, generation_config=self.chat_config)

            # Initialize conversation context
            self.last_location = None

            # Initialize API credentials
            self.hotels_api_key = os.getenv('HOTELS_API_KEY')
            self.hotels_api_url = "https://hotels4.p.rapidapi.com/properties/v2/list"

        except Exception as e:
            logger.error(f"Error initializing ChatbotService: {str(e)}", exc_info=True)
            raise

    def search_database(self, query, category):
        """Search the database for relevant items based on the query and category"""
        try:
            if category == 'hotel':
                return Hotel.objects.filter(
                    Q(name__icontains=query) | 
                    Q(location__icontains=query)
                )[:5]
            elif category == 'flight':
                return Flight.objects.filter(
                    Q(departure_city__icontains=query) | 
                    Q(arrival_city__icontains=query)
                )[:5]
            elif category == 'activity':
                return Activity.objects.filter(
                    Q(name__icontains=query) | 
                    Q(location__icontains=query)
                )[:5]
            elif category == 'match':
                return Match.objects.filter(
                    Q(home_team__icontains=query) | 
                    Q(away_team__icontains=query) |
                    Q(venue__icontains=query)
                )[:5]
            return None
        except Exception as e:
            logger.error(f"Error searching database: {str(e)}", exc_info=True)
            return None

    def suggest_package(self, location, date_range=None):
        """Suggest a package based on location and optional date range"""
        try:
            # Find relevant items
            hotels = Hotel.objects.filter(location__icontains=location)[:3]
            flights = Flight.objects.filter(
                Q(departure_city__icontains=location) | 
                Q(arrival_city__icontains=location)
            )[:3]
            activities = Activity.objects.filter(location__icontains=location)[:3]
            matches = Match.objects.filter(venue__icontains=location)[:3]

            if not any([hotels, flights, activities, matches]):
                return None

            # Calculate total price and discount
            total_price = sum([
                sum(h.price_per_night for h in hotels),
                sum(f.price for f in flights),
                sum(a.price for a in activities),
                sum(m.ticket_price for m in matches)
            ])
            discount = 0.15  # 15% discount for packages
            final_price = total_price * (1 - discount)

            # Create package name
            package_name = f"Sports Tourism Package - {location}"

            # Create the package
            package = Package.objects.create(
                name=package_name,
                hotel=hotels.first() if hotels else None,
                flight=flights.first() if flights else None,
                match=matches.first() if matches else None,
                total_price=total_price,
                discount_percentage=discount * 100,
                final_price=final_price,
                is_ai_suggested=True,
                status="suggested"
            )

            # Add activities
            if activities:
                package.activities.set(activities)

            return package
        except Exception as e:
            logger.error(f"Error suggesting package: {str(e)}", exc_info=True)
            return None

    def search_external_hotels(self, location):
        """Search for hotels from an external API"""
        try:
            if not self.hotels_api_key:
                logger.error("Hotels API key not configured")
                return []

            # Prepare the API request
            headers = {
                "X-RapidAPI-Key": self.hotels_api_key,
                "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
            }

            # First, search for the destination ID
            search_url = "https://hotels4.p.rapidapi.com/locations/v3/search"
            search_params = {
                "q": location,
                "locale": "en_US",
                "langid": "1033",
                "siteid": "300000001"
            }

            search_response = requests.get(search_url, headers=headers, params=search_params)
            search_data = search_response.json()

            if not search_data.get('sr'):
                logger.error(f"No destination found for location: {location}")
                return []

            # Get the first destination ID
            destination_id = search_data['sr'][0]['gaiaId']

            # Now search for hotels in that destination
            payload = {
                "currency": "USD",
                "eapid": 1,
                "locale": "en_US",
                "siteId": 300000001,
                "destination": {"id": destination_id},
                "checkInDate": {
                    "day": 10,
                    "month": 10,
                    "year": 2024
                },
                "checkOutDate": {
                    "day": 15,
                    "month": 10,
                    "year": 2024
                },
                "rooms": [{"adults": 2}],
                "resultsStartingIndex": 0,
                "resultsSize": 3,
                "sort": "PRICE_LOW_TO_HIGH"
            }

            response = requests.post(self.hotels_api_url, headers=headers, json=payload)
            data = response.json()

            if not data.get('data', {}).get('propertySearch', {}).get('properties'):
                logger.error(f"No hotels found for location: {location}")
                return []

            # Transform the API response into our hotel format
            hotels = []
            for property in data['data']['propertySearch']['properties']:
                hotel = {
                    "name": property['name'],
                    "location": location,
                    "rating": float(property.get('reviews', {}).get('score', 0)) / 2,  # Convert to 5-star scale
                    "price_per_night": float(property.get('price', {}).get('lead', {}).get('amount', 0)),
                    "description": property.get('summary', {}).get('location', ''),
                    "image_url": property.get('propertyGallery', {}).get('images', [{}])[0].get('image', {}).get('url', '')
                }
                hotels.append(hotel)

            return hotels

        except Exception as e:
            logger.error(f"Error searching external hotels: {str(e)}", exc_info=True)
            return []

    def process_message(self, user_message):
        try:
            logger.info(f"Processing message: {user_message}")

            # Store user message
            conversation = Conversation.objects.create(
                user_message=user_message,
                created_at=timezone.now()
            )

            # First check for "search for other options" or similar phrases
            if any(phrase in user_message.lower() for phrase in ['search for other options', 'more options', 'other options', 'show more']):
                if self.last_location:
                    # Search for more hotels in the last mentioned location
                    external_hotels = self.search_external_hotels(self.last_location)
                    
                    if external_hotels:
                        response = f"Here are some additional hotels in {self.last_location}:\n\n"
                        for hotel in external_hotels:
                            response += f"- {hotel['name']}\n  Location: {hotel['location']}\n  Rating: {hotel['rating']}/5\n  Price per night: ${hotel['price_per_night']}\n\n"
                        
                        # Add the hotels to the database
                        for hotel_data in external_hotels:
                            self.create_or_update_hotel(hotel_data)
                        
                        response += "Would you like to know more about any of these hotels, or should I search for other options?"
                    else:
                        response = f"I couldn't find any more hotels in {self.last_location}. Would you like to try a different location?"
                else:
                    # If no location was previously mentioned, extract location from current message
                    location = self.extract_location(user_message)
                    if location:
                        self.last_location = location
                        external_hotels = self.search_external_hotels(location)
                        
                        if external_hotels:
                            response = f"Here are some hotels in {location}:\n\n"
                            for hotel in external_hotels:
                                response += f"- {hotel['name']}\n  Location: {hotel['location']}\n  Rating: {hotel['rating']}/5\n  Price per night: ${hotel['price_per_night']}\n\n"
                            
                            # Add the hotels to the database
                            for hotel_data in external_hotels:
                                self.create_or_update_hotel(hotel_data)
                            
                            response += "Would you like to know more about any of these hotels, or should I search for other options?"
                        else:
                            response = f"I couldn't find any hotels in {location}. Would you like to try a different location?"
                    else:
                        response = "Could you please specify which location you're interested in? I can then show you more hotel options in that area."

            # Then check for specific queries about hotels
            elif any(word in user_message.lower() for word in ['hotel', 'accommodation', 'stay']):
                # Search for hotels in database
                location = self.extract_location(user_message)
                if location:
                    # Store the location for future reference
                    self.last_location = location
                    
                    # Check both Hotel models
                    from core.models import Hotel as CoreHotel
                    from chatbot.models import Hotel as ChatbotHotel
                    
                    # Search in both models
                    core_hotels = CoreHotel.objects.filter(city__icontains=location)
                    chatbot_hotels = ChatbotHotel.objects.filter(location__icontains=location)
                    
                    if core_hotels.exists() or chatbot_hotels.exists():
                        response = f"I found these hotels in {location} from our database:\n\n"
                        
                        # Add hotels from core model
                        for hotel in core_hotels:
                            response += f"- {hotel.name}\n  Location: {hotel.city}\n  Rating: {hotel.rating}/5\n  Price per night: ${hotel.price_per_night}\n\n"
                        
                        # Add hotels from chatbot model
                        for hotel in chatbot_hotels:
                            response += f"- {hotel.name}\n  Location: {hotel.location}\n  Rating: {hotel.rating}/5\n  Price per night: ${hotel.price_per_night}\n\n"
                        
                        response += "Would you like to know more about any of these hotels, or should I search for other options?"
                    else:
                        # If no hotels found in database, use external API to suggest hotels
                        external_hotels = self.search_external_hotels(location)
                        
                        if external_hotels:
                            response = f"I found these hotels in {location}:\n\n"
                            for hotel in external_hotels:
                                response += f"- {hotel['name']}\n  Location: {hotel['location']}\n  Rating: {hotel['rating']}/5\n  Price per night: ${hotel['price_per_night']}\n\n"
                            
                            # Add the hotels to the database
                            for hotel_data in external_hotels:
                                self.create_or_update_hotel(hotel_data)
                            
                            response += "Would you like to know more about any of these hotels, or should I search for other options?"
                        else:
                            response = f"I couldn't find any hotels in {location}. Would you like to try a different location?"
                else:
                    response = "Could you please specify which location you're interested in?"

            # Then check for package queries
            elif any(word in user_message.lower() for word in ['package', 'deal', 'offer']):
                # Suggest a package
                location = self.extract_location(user_message)
                if location:
                    # Store the location for future reference
                    self.last_location = location
                    
                    # First check if we have enough items in the database
                    from core.models import Hotel as CoreHotel
                    from chatbot.models import Hotel as ChatbotHotel
                    
                    hotels = list(CoreHotel.objects.filter(city__icontains=location)) + \
                            list(ChatbotHotel.objects.filter(location__icontains=location))
                    
                    flights = Flight.objects.filter(
                        Q(departure_city__icontains=location) | 
                        Q(arrival_city__icontains=location)
                    )
                    activities = Activity.objects.filter(location__icontains=location)
                    matches = Match.objects.filter(venue__icontains=location)

                    if hotels and (flights.exists() or activities.exists() or matches.exists()):
                        package = self.suggest_package(location)
                        if package:
                            response = f"I've created a special package for {location}:\n\n"
                            response += f"Package: {package.name}\n"
                            if package.hotel:
                                response += f"Hotel: {package.hotel.name}\n"
                            if package.flight:
                                response += f"Flight: {package.flight.flight_number}\n"
                            if package.match:
                                response += f"Match: {package.match.home_team} vs {package.match.away_team}\n"
                            response += f"Activities: {', '.join(a.name for a in package.activities.all())}\n"
                            response += f"Original Price: ${package.total_price}\n"
                            response += f"Discount: {package.discount_percentage}%\n"
                            response += f"Final Price: ${package.final_price}\n\n"
                            response += "Would you like to book this package or would you like me to suggest alternatives?"
                    else:
                        response = f"I don't have enough options in our database to create a complete package for {location}. "
                        if hotels:
                            response += f"I have {len(hotels)} hotels available. "
                        if flights.exists():
                            response += f"I have {flights.count()} flights available. "
                        if activities.exists():
                            response += f"I have {activities.count()} activities available. "
                        if matches.exists():
                            response += f"I have {matches.count()} matches available. "
                        response += "\nWould you like me to search for additional options to complete the package?"
                else:
                    response = "Could you please specify which location you're interested in for the package?"

            # Finally, use Gemini for general queries
            else:
                # Use Gemini for general queries
                response = self.chat.send_message(
                    user_message,
                    generation_config=self.chat_config
                ).text

            # Store bot response
            conversation.bot_message = response
            conversation.save()

            return response

        except Exception as e:
            logger.error(f"Error in process_message: {str(e)}", exc_info=True)
            return "I apologize, but I encountered an error. Please try again or contact customer service for assistance."

    def extract_location(self, message):
        """Extract location from user message using Gemini"""
        try:
            prompt = f"Extract the location from this message, return only the location name: {message}"
            response = self.chat.send_message(prompt, generation_config=self.chat_config).text
            return response.strip()
        except Exception as e:
            logger.error(f"Error extracting location: {str(e)}", exc_info=True)
            return None

    def create_or_update_hotel(self, hotel_data):
        """Create or update a hotel in both core and chatbot databases"""
        try:
            from core.models import Hotel as CoreHotel
            from chatbot.models import Hotel as ChatbotHotel

            # Create or update in chatbot database
            chatbot_hotel, chatbot_created = ChatbotHotel.objects.get_or_create(
                name=hotel_data["name"],
                defaults={
                    "location": hotel_data["location"],
                    "rating": hotel_data["rating"],
                    "price_per_night": hotel_data["price_per_night"],
                    "description": hotel_data.get("description", ""),
                    "is_ai_suggested": True
                }
            )

            # Create or update in core database
            core_hotel, core_created = CoreHotel.objects.get_or_create(
                name=hotel_data["name"],
                defaults={
                    "city": hotel_data["location"],  # Use location as city
                    "address": hotel_data.get("description", ""),  # Use description as address
                    "description": hotel_data.get("description", ""),
                    "price_per_night": hotel_data["price_per_night"],
                    "available_rooms": 10,  # Default value
                    "rating": hotel_data["rating"],
                    "image_url": hotel_data.get("image_url", "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80")
                }
            )

            return core_hotel  # Return the core hotel for frontend display
        except Exception as e:
            logger.error(f"Error creating/updating hotel: {str(e)}", exc_info=True)
            return None

    def create_or_update_flight(self, flight_data):
        """Create or update a flight in the database"""
        try:
            flight, created = Flight.objects.get_or_create(
                flight_number=flight_data["flight_number"],
                defaults={
                    "departure_city": flight_data["departure_city"],
                    "arrival_city": flight_data["arrival_city"],
                    "departure_time": flight_data["departure_time"],
                    "arrival_time": flight_data["arrival_time"],
                    "price": flight_data["price"],
                    "available_seats": flight_data.get("available_seats", 100),
                    "is_ai_suggested": True
                }
            )
            return flight
        except Exception as e:
            logger.error(f"Error creating/updating flight: {str(e)}", exc_info=True)
            return None

    def create_or_update_activity(self, activity_data):
        """Create or update an activity in the database"""
        try:
            activity, created = Activity.objects.get_or_create(
                name=activity_data["name"],
                defaults={
                    "location": activity_data["location"],
                    "description": activity_data.get("description", ""),
                    "price": activity_data["price"],
                    "is_ai_suggested": True
                }
            )
            return activity
        except Exception as e:
            logger.error(f"Error creating/updating activity: {str(e)}", exc_info=True)
            return None

    def create_or_update_package(self, package_data):
        # Create or get related objects
        hotel = self.create_or_update_hotel(package_data["hotel"])
        flight = self.create_or_update_flight(package_data["flight"])
        activities = [
            self.create_or_update_activity(activity_data)
            for activity_data in package_data["activities"]
        ]

        # Create the package
        package = Package.objects.create(
            name=package_data["name"],
            hotel=hotel,
            flight=flight,
            match=package_data["match"],
            total_price=package_data["total_price"],
            discount_percentage=package_data["discount_percentage"],
            final_price=package_data["final_price"],
            is_ai_suggested=True,
            status="suggested"
        )

        # Add activities to package
        package.activities.set(activities)

        return package
