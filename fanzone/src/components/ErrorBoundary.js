import React from 'react';
import { useRouteError } from 'react-router-dom';

const ErrorBoundary = () => {
  const error = useRouteError();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Oops!</h1>
        <p className="text-gray-600 mb-4">
          {error?.statusText || error?.message || 'Something went wrong'}
        </p>
        <p className="text-sm text-gray-500 mb-8">
          {error?.status ? `Error ${error.status}` : ''}
        </p>
        <button
          onClick={() => window.location.href = '/'}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
        >
          Go Home
        </button>
      </div>
    </div>
  );
};

export default ErrorBoundary; 