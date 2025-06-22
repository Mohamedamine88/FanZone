import React from 'react';
import { createBrowserRouter, RouterProvider, Outlet, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/auth/PrivateRoute';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import Home from './pages/Home';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import Dashboard from './pages/dashboard/Dashboard';
import Bookings from './pages/Bookings';
import Profile from './pages/dashboard/Profile';
import Matches from './pages/Matches';
import Flights from './pages/Flights';
import Hotels from './pages/Hotels';
import Activities from './pages/Activities';
import ErrorBoundary from './components/ErrorBoundary';
import Booking from './pages/Booking';
import Chatbot from './components/Chatbot';

const queryClient = new QueryClient();

// Layout component that includes Navbar and Footer
const Layout = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar />
      <main className="flex-grow">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};

// Create the router with future flags
const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <>
        <Navbar />
        <main className="min-h-screen bg-gray-50">
          <Outlet />
        </main>
        <Footer />
      </>
    ),
    errorElement: <ErrorBoundary />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: 'login',
        element: <Login />,
      },
      {
        path: 'register',
        element: <Register />,
      },
      {
        path: 'matches',
        element: <Matches />,
      },
      {
        path: 'flights',
        element: <Flights />,
      },
      {
        path: 'hotels',
        element: <Hotels />,
      },
      {
        path: 'activities',
        element: <Activities />,
      },
      {
        path: 'book/:type/:id',
        element: (
          <PrivateRoute>
            <Booking />
          </PrivateRoute>
        ),
      },
      {
        path: 'dashboard',
        element: (
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        ),
        children: [
          {
            index: true,
            element: <Navigate to="profile" replace />,
          },
          {
            path: 'profile',
            element: <Profile />,
          },
          {
            path: 'bookings',
            element: <Bookings />,
          },
        ],
      },
    ],
  },
], {
  future: {
    v7_startTransition: true,
    v7_relativeSplatPath: true,
    v7_normalizeFormMethod: true,
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <RouterProvider router={router} />
        <ToastContainer 
          position="top-right" 
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
        <Chatbot />
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
