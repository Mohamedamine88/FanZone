# FanZone - CAN 2025 & World Cup 2030 travel platform

FanZone is a comprehensive travel booking platform specifically designed for CAN 2025 and World Cup 2030 in Morocco. The platform allows users to book flights, hotels, match tickets, and local activities, with the ability to create complete travel packages.

## Features

### Core Functionality
- **Flight Booking**: Search and book flights to Morocco
- **Hotel Reservations**: Find and reserve accommodations
- **Match Tickets**: Purchase tickets for CAN 2025 and World Cup 2030 matches
- **Local Activities**: Discover and book local tours and activities
- **Package Deals**: Create custom travel packages combining all services
- **User Authentication**: Secure JWT-based authentication system
- **Admin Panel**: Comprehensive admin interface for managing all resources

### Advanced Features
- **AI Chatbot**: Intelligent customer support powered by OpenAI
- **Real-time Updates**: Live booking status and availability
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Modern UI/UX**: Beautiful interface with Framer Motion animations
- **Form Validation**: Robust form handling with Formik and Yup

## Architecture

This is a full-stack application with the following architecture:

```
FanZone/
├── backend/          # Django REST API
│   ├── chatbot/      # AI Chatbot functionality
│   ├── activities/   # Local activities management
│   ├── core/         # Core Django settings
│   └── fanzone_backend/  # Main Django app
├── fanzone/          # React Frontend
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── context/      # React context providers
│   │   └── assets/       # Static assets
│   └── public/       # Public assets
└── PFA/              # Additional Django configuration
```

## Getting Started

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**
- **Git**

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Unix/MacOS
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the `backend/` directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   OPENAI_API_KEY=your-openai-api-key
   ```

5. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

The backend API will be available at `http://localhost:8000/`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd fanzone
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```

The frontend application will be available at `http://localhost:3000/`

## API Documentation

### Authentication Endpoints
- `POST /api/users/register/` - Register a new user
- `POST /api/token/` - Get JWT authentication token
- `POST /api/token/refresh/` - Refresh JWT token

### Resource Endpoints
- **Users**: `/api/users/`
- **Flights**: `/api/flights/`
- **Hotels**: `/api/hotels/`
- **Match Tickets**: `/api/match-tickets/`
- **Activities**: `/api/activities/`
- **Bookings**: `/api/bookings/`
- **Packages**: `/api/packages/`

### Chatbot Endpoints
- `POST /api/chatbot/` - Send message to AI chatbot

## Technologies Used

### Backend
- **Django 5.2** - Web framework
- **Django REST Framework** - API framework
- **Django CORS Headers** - Cross-origin resource sharing
- **Django REST Framework Simple JWT** - JWT authentication
- **OpenAI** - AI chatbot functionality
- **Channels & Daphne** - WebSocket support
- **SQLite** - Database (development)

### Frontend
- **React 18.2.0** - UI library
- **React Router DOM** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **React Query (TanStack Query)** - Data fetching
- **Formik & Yup** - Form handling and validation
- **Axios** - HTTP client
- **React Hot Toast** - Toast notifications
- **Headless UI** - Accessible UI components
- **Heroicons** - Icon library

## UI/UX Features

- **Responsive Design**: Mobile-first approach
- **Smooth Animations**: Framer Motion powered transitions
- **Loading States**: Skeleton loaders and spinners
- **Error Handling**: User-friendly error messages
- **Form Validation**: Real-time validation feedback
- **Toast Notifications**: Success/error feedback

## Development

### Running Tests
```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd fanzone
npm test
```

### Building for Production
```bash
# Frontend build
cd fanzone
npm run build
```

### Code Style
- **Backend**: Follow PEP 8 Python style guide
- **Frontend**: ESLint configuration included
- **Git**: Conventional commit messages

## Project Structure

```
├── backend/
│   ├── chatbot/          # AI chatbot functionality
│   ├── activities/       # Local activities app
│   ├── core/            # Core Django settings
│   ├── fanzone_backend/ # Main Django app
│   ├── manage.py        # Django management script
│   ├── settings.py      # Django settings
│   └── requirements.txt # Python dependencies
├── fanzone/
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── pages/       # Page components
│   │   ├── context/     # React context
│   │   ├── assets/      # Static assets
│   │   └── App.js       # Main app component
│   ├── public/          # Public assets
│   ├── package.json     # Node.js dependencies
│   └── tailwind.config.js # Tailwind configuration
├── PFA/                 # Additional configuration
├── requirements.txt     # Root Python dependencies
└── README.md           # This file
```

## Team

This project was developed as part of the PFA (Projet de fin d'année) for our 4IIR course.

## Future Enhancements

- [ ] Payment gateway integration
- [ ] Real-time notifications
- [ ] Multi-language support
- [ ] Advanced search filters
- [ ] User reviews and ratings
- [ ] Social media integration
- [ ] Mobile app development
- [ ] Analytics dashboard
