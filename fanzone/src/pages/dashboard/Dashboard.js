import React from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const navigation = [
  { name: 'Overview', href: '/dashboard' },
  { name: 'Bookings', href: '/dashboard/bookings' },
  { name: 'Profile', href: '/dashboard/profile' },
];

const classNames = (...classes) => {
  return classes.filter(Boolean).join(' ');
};

const Dashboard = () => {
  const location = useLocation();
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
          <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">
            Welcome back, {user?.name || 'User'}!
          </p>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
          <div className="py-6">
            <div className="lg:grid lg:grid-cols-12 lg:gap-8">
              {/* Sidebar */}
              <div className="hidden lg:block lg:col-span-3">
                <nav className="space-y-1">
                  {navigation.map((item) => {
                    const isActive = location.pathname === item.href;
                    return (
                      <Link
                        key={item.name}
                        to={item.href}
                        className={classNames(
                          isActive
                            ? 'bg-primary-50 text-primary-600'
                            : 'text-gray-900 hover:bg-gray-50',
                          'group flex items-center px-3 py-2 text-sm font-medium rounded-md'
                        )}
                      >
                        {item.name}
                      </Link>
                    );
                  })}
                </nav>
              </div>

              {/* Main content */}
              <div className="mt-8 lg:mt-0 lg:col-span-9">
                <div className="bg-white shadow rounded-lg">
                  <div className="p-6">
                    <Outlet />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 