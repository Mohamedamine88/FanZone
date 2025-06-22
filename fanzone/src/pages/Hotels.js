import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import api from '../api';
import { toast } from 'react-toastify';

const cities = ['All', 'Rabat', 'Casablanca', 'Marrakech', 'Tangier', 'Fez', 'El Jadida', 'Agadir'];
const priceRanges = [
  { label: 'All Prices', value: 'all' },
  { label: 'Under 2000 MAD', value: 'budget' },
  { label: '2000-3000 MAD', value: 'mid' },
  { label: 'Over 3000 MAD', value: 'luxury' }
];

const Hotels = () => {
  const navigate = useNavigate();
  const [hotels, setHotels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCity, setSelectedCity] = useState('All');
  const [selectedPriceRange, setSelectedPriceRange] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedAmenities, setSelectedAmenities] = useState([]);
  const [bookingLoading, setBookingLoading] = useState({});

  useEffect(() => {
    const fetchHotels = async () => {
      try {
        console.log('Fetching hotels from:', `${api.defaults.baseURL}/api/hotels/`);
        const response = await api.get('/api/hotels/');
        console.log('Hotels response:', response.data);
        setHotels(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching hotels:', {
          message: err.message,
          response: err.response?.data,
          status: err.response?.status,
          headers: err.response?.headers
        });
        setError(`Failed to fetch hotels: ${err.message}. Please try again later.`);
        setLoading(false);
      }
    };

    fetchHotels();
  }, []);

  const allAmenities = [...new Set(hotels.flatMap(hotel => hotel.amenities || []))];

  const filteredHotels = hotels.filter(hotel => {
    const matchesCity = selectedCity === 'All' || hotel.city === selectedCity;
    const matchesSearch = hotel.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         hotel.city.toLowerCase().includes(searchTerm.toLowerCase());
    const price = parseFloat(hotel.price_per_night);
    const matchesPrice = selectedPriceRange === 'all' ||
                        (selectedPriceRange === 'budget' && price < 2000) ||
                        (selectedPriceRange === 'mid' && price >= 2000 && price <= 3000) ||
                        (selectedPriceRange === 'luxury' && price > 3000);
    const matchesAmenities = selectedAmenities.length === 0 ||
                            selectedAmenities.every(amenity => hotel.amenities?.includes(amenity));
    return matchesCity && matchesSearch && matchesPrice && matchesAmenities;
  });

  const toggleAmenity = (amenity) => {
    setSelectedAmenities(prev =>
      prev.includes(amenity)
        ? prev.filter(a => a !== amenity)
        : [...prev, amenity]
    );
  };

  const handleBook = async (hotelId) => {
    try {
      setBookingLoading(prev => ({ ...prev, [hotelId]: true }));
      
      const hotel = hotels.find(h => h.id === hotelId);
      if (!hotel) {
        console.error('Hotel not found:', hotelId);
        toast.error('Hotel not found. Please try again.');
        return;
      }
      console.log('Found hotel:', hotel);
      
      const bookingData = {
        hotel_ids: [hotelId],
        total_price: parseFloat(hotel.price_per_night)
      };
      
      console.log('Preparing to send booking data:', bookingData);
      
      const response = await api.post('/api/bookings/', bookingData);
      console.log('Received booking response:', response);
      
      if (response.data) {
        console.log('Booking successful, response data:', response.data);
        toast.success('Hotel booked successfully!');
        // Add a small delay before navigation to ensure the toast is visible
        setTimeout(() => {
          navigate('/dashboard/bookings');
        }, 1000);
      } else {
        console.warn('Booking response missing data:', response);
        toast.warning('Booking created but no confirmation received.');
        navigate('/dashboard/bookings');
      }
    } catch (error) {
      console.error('Error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        headers: error.response?.headers,
        config: error.config
      });
      
      let errorMessage = 'Failed to book hotel. Please try again.';
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      toast.error(errorMessage);
    } finally {
      console.log('Cleaning up booking process');
      setBookingLoading(prev => ({ ...prev, [hotelId]: false }));
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
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero Section */}
      <div className="relative h-[500px] overflow-hidden">
        <div className="absolute inset-0">
          <img
            src="https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80"
            alt="Luxury hotel"
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
              Luxury Hotels in Morocco
            </motion.h1>
            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="text-xl md:text-2xl text-gray-200 mb-8"
            >
              Experience world-class hospitality during CAN 2025 and World Cup 2030
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
            >
              <Link
                to="/register"
                className="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-full text-white bg-primary-600 hover:bg-primary-700 transition-all duration-300 shadow-lg hover:shadow-xl"
              >
                Book Your Stay
              </Link>
            </motion.div>
          </div>
        </motion.div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-12">
          <div className="space-y-8">
            <div className="flex flex-wrap gap-4 justify-center">
              {cities.map((city) => (
                <motion.button
                  key={city}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setSelectedCity(city)}
                  className={`px-6 py-3 rounded-full text-sm font-medium transition-all duration-300 ${
                    selectedCity === city
                      ? 'bg-primary-600 text-white shadow-lg'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {city}
                </motion.button>
              ))}
            </div>
            <div className="flex flex-wrap gap-4 justify-center">
              {priceRanges.map((range) => (
                <motion.button
                  key={range.value}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setSelectedPriceRange(range.value)}
                  className={`px-6 py-3 rounded-full text-sm font-medium transition-all duration-300 ${
                    selectedPriceRange === range.value
                      ? 'bg-green-600 text-white shadow-lg'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {range.label}
                </motion.button>
              ))}
            </div>
            <div className="flex flex-wrap gap-3 justify-center">
              {allAmenities.map((amenity) => (
                <motion.button
                  key={amenity}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => toggleAmenity(amenity)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 ${
                    selectedAmenities.includes(amenity)
                      ? 'bg-blue-600 text-white shadow-lg'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {amenity}
                </motion.button>
              ))}
            </div>
            <div className="max-w-md mx-auto">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search hotels..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full px-6 py-4 rounded-full border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent shadow-sm pl-12"
                />
                <svg
                  className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <AnimatePresence mode="wait">
          <motion.div 
            key={selectedCity + selectedPriceRange + searchTerm + selectedAmenities.join(',')}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="grid gap-8 md:grid-cols-2 lg:grid-cols-3"
          >
            {filteredHotels.map((hotel, index) => (
              <motion.div
                key={hotel.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                whileHover={{ scale: 1.02 }}
                className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300"
              >
                <div className="relative h-64">
                  <img
                    src={hotel.image_url || "https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80"}
                    alt={hotel.name}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent" />
                  <div className="absolute bottom-6 left-6 right-6">
                    <div className="flex justify-between items-center mb-4">
                      <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-white/90 text-gray-900">
                        {hotel.city}
                      </span>
                      <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-green-100 text-green-800">
                        {hotel.status}
                      </span>
                    </div>
                    <h3 className="text-2xl font-bold text-white mb-2">{hotel.name}</h3>
                    <div className="flex items-center text-white">
                      <svg className="h-5 w-5 text-yellow-400 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.363 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.363-1.118l-2.8-2.034c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                      <span className="ml-1">{hotel.rating}</span>
                    </div>
                  </div>
                </div>
                <div className="p-6">
                  <div className="mb-6">
                    <div className="flex flex-wrap gap-2">
                      {(hotel.amenities || []).map((amenity, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
                        >
                          {amenity}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <div className="text-2xl font-bold text-primary-600">{hotel.price_per_night} MAD</div>
                    <button
                      onClick={() => handleBook(hotel.id)}
                      disabled={bookingLoading[hotel.id]}
                      className="inline-flex items-center px-6 py-3 border border-transparent text-sm font-medium rounded-full text-white bg-primary-600 hover:bg-primary-700 transition-all duration-300 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {bookingLoading[hotel.id] ? 'Booking...' : 'Book Now'}
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </AnimatePresence>

        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-16 text-center"
        >
          <p className="text-xl text-gray-600 mb-6">
            Want to book a hotel? Register now to get started!
          </p>
          <Link
            to="/register"
            className="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-full text-white bg-primary-600 hover:bg-primary-700 transition-all duration-300 shadow-lg hover:shadow-xl"
          >
            Create an Account
          </Link>
        </motion.div>
      </div>
    </div>
  );
};

export default Hotels; 