import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { toast } from 'react-hot-toast';

const Booking = () => {
  const { type, id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [quantity, setQuantity] = useState(1);

  // Fetch item details
  const { data: item, isLoading } = useQuery({
    queryKey: [type, id],
    queryFn: async () => {
      const response = await axios.get(`/api/${type}/${id}/`);
      return response.data;
    },
  });

  // Create booking mutation
  const createBooking = useMutation({
    mutationFn: async (bookingData) => {
      const response = await axios.post('/api/bookings/', bookingData);
      return response.data;
    },
    onSuccess: () => {
      toast.success('Booking created successfully!');
      queryClient.invalidateQueries(['bookings']);
      navigate('/dashboard/bookings');
    },
    onError: (error) => {
      toast.error(error.response?.data?.message || 'Failed to create booking');
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    createBooking.mutate({
      item_type: type,
      item_id: id,
      quantity,
    });
  };

  if (isLoading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  if (!item) {
    return <div className="flex justify-center items-center h-screen">Item not found</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Book {type}</h1>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">{item.name || item.title}</h2>
        <p className="text-gray-600 mb-4">{item.description}</p>
        <p className="text-lg font-semibold mb-4">Price: ${item.price}</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6">
        <div className="mb-4">
          <label htmlFor="quantity" className="block text-sm font-medium text-gray-700 mb-2">
            Quantity
          </label>
          <input
            type="number"
            id="quantity"
            min="1"
            value={quantity}
            onChange={(e) => setQuantity(parseInt(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="mb-4">
          <p className="text-lg font-semibold">
            Total: ${(item.price * quantity).toFixed(2)}
          </p>
        </div>

        <button
          type="submit"
          disabled={createBooking.isLoading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {createBooking.isLoading ? 'Processing...' : 'Confirm Booking'}
        </button>
      </form>
    </div>
  );
};

export default Booking; 