import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import api from '../api';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

const Flights = () => {
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [bookingLoading, setBookingLoading] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFlights = async () => {
      try {
        console.log('Fetching flights from:', `${api.defaults.baseURL}/api/flights/`);
        const response = await api.get('/api/flights/');
        console.log('Flights response:', response.data);
        setFlights(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching flights:', {
          message: err.message,
          response: err.response?.data,
          status: err.response?.status,
          headers: err.response?.headers
        });
        setError(`Failed to fetch flights: ${err.message}. Please try again later.`);
        setLoading(false);
      }
    };

    fetchFlights();
  }, []);

  const handleBook = async (flightId) => {
    try {
      setBookingLoading(prev => ({ ...prev, [flightId]: true }));
      
      const flight = flights.find(f => f.id === flightId);
      console.log('Booking flight:', flight);
      
      const bookingData = {
        flight_ids: [flightId],
        total_price: parseFloat(flight.price)
      };
      
      console.log('Sending booking data:', bookingData);
      
      const response = await api.post('/api/bookings/', bookingData);
      console.log('Booking response:', response.data);
      
      toast.success('Flight booked successfully!');
      
      // Add a small delay before navigation to show the success message
      setTimeout(() => {
        navigate('/dashboard/bookings');
      }, 1500);
    } catch (error) {
      console.error('Error booking flight:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status
      });
      
      let errorMessage = 'Failed to book flight. Please try again.';
      
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.response?.status === 401) {
        errorMessage = 'Please log in to book a flight.';
      }
      
      toast.error(errorMessage);
    } finally {
      setBookingLoading(prev => ({ ...prev, [flightId]: false }));
    }
  };

  const filteredFlights = flights.filter(flight => {
    return flight.departure_city.toLowerCase().includes(searchTerm.toLowerCase()) ||
           flight.arrival_city.toLowerCase().includes(searchTerm.toLowerCase());
  });

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-red-600 text-xl">{error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero Section */}
      <div className="relative h-[500px] overflow-hidden">
        <div className="absolute inset-0">
          <img
            src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2074&q=80"
            alt="Airplane in sky"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-black/70" />
        </div>
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center"
        >
          <div className="text-center text-white max-w-3xl mx-auto">
            <motion.h1 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-5xl md:text-6xl font-bold mb-6 leading-tight"
            >
              Flight Bookings
            </motion.h1>
            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="text-xl md:text-2xl text-gray-200 mb-8"
            >
              Find the perfect flight for your journey
            </motion.p>
          </div>
        </motion.div>
      </div>

      {/* Search Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <div className="grid grid-cols-1 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Search Flights</label>
              <input
                type="text"
                placeholder="Search by departure or arrival city..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
        </div>

        {/* Flights Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <AnimatePresence>
            {filteredFlights.map((flight) => (
              <motion.div
                key={flight.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
                className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300"
              >
                <div className="relative h-48">
                  <img
                    src={flight.image_url || "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2074&q=80"}
                    alt={`${flight.airline} flight`}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {flight.flight_number}
                  </h3>
                  <div className="flex items-center text-gray-600 mb-4">
                    <span className="mr-2">{flight.departure_city}</span>
                    <svg
                      className="w-4 h-4 mx-2"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M17 8l4 4m0 0l-4 4m4-4H3"
                      />
                    </svg>
                    <span>{flight.arrival_city}</span>
                  </div>
                  <div className="text-gray-600 mb-4">
                    <p>Departure: {new Date(flight.departure_time).toLocaleString()}</p>
                    <p>Arrival: {new Date(flight.arrival_time).toLocaleString()}</p>
                  </div>
                  <div className="flex justify-between items-center">
                    <div className="text-primary-600 font-semibold">
                      {flight.price} MAD
                    </div>
                    <div className="text-sm text-gray-600">
                      Available Seats: {flight.available_seats}
                    </div>
                  </div>
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <div className="flex justify-between items-center">
                      <button
                        onClick={() => handleBook(flight.id)}
                        disabled={bookingLoading[flight.id]}
                        className={`px-4 py-2 rounded-md text-sm font-medium text-white ${
                          bookingLoading[flight.id]
                            ? 'bg-gray-400 cursor-not-allowed'
                            : 'bg-primary-600 hover:bg-primary-700'
                        }`}
                      >
                        {bookingLoading[flight.id] ? 'Booking...' : 'Book Now'}
                      </button>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

export default Flights; 