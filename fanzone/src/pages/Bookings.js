import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import api from '../api';
import { toast } from 'react-toastify';

const Bookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const response = await api.get('/api/bookings/');
        console.log('Bookings response:', response.data);
        setBookings(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching bookings:', err);
        setError('Failed to fetch bookings. Please try again later.');
        setLoading(false);
      }
    };

    fetchBookings();
  }, []);

  const handleCancelBooking = async (bookingId) => {
    try {
      console.log('Attempting to cancel booking:', bookingId);
      
      // First, get the current booking to verify its status
      const bookingResponse = await api.get(`/api/bookings/${bookingId}/`);
      const booking = bookingResponse.data;
      
      if (booking.status !== 'pending') {
        toast.error('Only pending bookings can be cancelled.');
        return;
      }
      
      // Send the cancellation request
      const response = await api.patch(`/api/bookings/${bookingId}/`, {
        status: 'cancelled'
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      console.log('Cancellation response:', response);
      
      // Remove the booking from the local state
      setBookings(bookings.filter(booking => booking.id !== bookingId));
      
      toast.success('Booking cancelled and removed successfully!');
    } catch (error) {
      console.error('Error cancelling booking:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        config: error.config
      });
      
      let errorMessage = 'Failed to cancel booking. Please try again.';
      
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.response?.data?.non_field_errors) {
        errorMessage = error.response.data.non_field_errors[0];
      } else if (error.response?.status === 404) {
        errorMessage = 'Booking not found.';
      } else if (error.response?.status === 403) {
        errorMessage = 'You do not have permission to cancel this booking.';
      } else if (error.response?.status === 400) {
        errorMessage = error.response.data.detail || 'Invalid request. Please try again.';
      }
      
      toast.error(errorMessage);
    }
  };

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
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Your Bookings</h1>
          <p className="text-xl text-gray-600">Manage your hotel, flight, and activity bookings</p>
        </div>

        {bookings.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-xl text-gray-600">You don't have any bookings yet.</p>
          </div>
        ) : (
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {bookings.map((booking) => (
              <motion.div
                key={booking.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white rounded-lg shadow-lg overflow-hidden"
              >
                <div className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">Booking #{booking.id}</h3>
                      <p className="text-sm text-gray-500">
                        {new Date(booking.booking_date).toLocaleDateString()}
                      </p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      booking.status === 'confirmed' 
                        ? 'bg-green-100 text-green-800'
                        : booking.status === 'cancelled'
                        ? 'bg-red-100 text-red-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                    </span>
                  </div>

                  {booking.hotel && booking.hotel.length > 0 && (
                    <div className="mb-4">
                      <h4 className="font-medium text-gray-900 mb-2">Hotels</h4>
                      {booking.hotel.map(hotel => (
                        <div key={hotel.id} className="text-sm text-gray-600">
                          {hotel.name} - {hotel.city}
                        </div>
                      ))}
                    </div>
                  )}

                  {booking.flight && booking.flight.length > 0 && (
                    <div className="mb-4">
                      <h4 className="font-medium text-gray-900 mb-2">Flights</h4>
                      {booking.flight.map(flight => (
                        <div key={flight.id} className="text-sm text-gray-600">
                          {flight.airline} - {flight.flight_number}
                        </div>
                      ))}
                    </div>
                  )}

                  {booking.activity && booking.activity.length > 0 && (
                    <div className="mb-4">
                      <h4 className="font-medium text-gray-900 mb-2">Activities</h4>
                      {booking.activity.map(activity => (
                        <div key={activity.id} className="text-sm text-gray-600">
                          {activity.name} - {activity.city}
                        </div>
                      ))}
                    </div>
                  )}

                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <div className="flex justify-between items-center">
                      <div className="text-lg font-bold text-primary-600">
                        {booking.total_price} MAD
                      </div>
                      {booking.status === 'pending' && (
                        <button
                          onClick={() => handleCancelBooking(booking.id)}
                          className="px-4 py-2 text-sm font-medium text-red-600 hover:text-red-800"
                        >
                          Cancel Booking
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Bookings; 