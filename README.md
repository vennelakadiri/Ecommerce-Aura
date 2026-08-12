# Aura - Dynamic Ecommerce Application

A comprehensive ecommerce platform built with Django, featuring customer, admin, and delivery boy interfaces.

## Features

### Customer Side
- **Product Catalog**: Browse products with advanced filtering and search
- **Product Details**: Detailed product pages with image galleries, reviews, and specifications
- **Shopping Cart**: Add/remove items, update quantities
- **Wishlist**: Save favorite products for later
- **User Profile**: Manage account settings and order history
- **Payment Processing**: Secure checkout with multiple payment options
- **Responsive Design**: Mobile-friendly interface

### Admin Side
- **Dashboard Analytics**: Comprehensive business insights
- **Product Management**: Add, edit, and manage inventory
- **Order Management**: Process and track customer orders
- **Staff Management**: Manage admin roles and permissions
- **Delivery Boy Management**: Assign and monitor delivery personnel
- **Payment & Settlements**: Financial transaction management
- **Notifications**: Send alerts to customers and staff
- **Reports**: Generate detailed business reports
- **Advertisement Management**: Create and manage promotional campaigns

### Delivery Boy Side
- **Order Dashboard**: View assigned orders and delivery schedules
- **Order Details**: Complete order information and customer details
- **Map Navigation**: Integrated maps for delivery routes
- **Status Updates**: Real-time order status updates
- **Earnings Tracking**: Monitor delivery earnings and commissions
- **Profile Management**: Update personal and vehicle information

## Tech Stack

- **Backend**: Django 4.2.7, Python
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **API**: Django REST Framework
- **Authentication**: Custom user model with role-based access

## Installation

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Miniproject
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create sample data**
   ```bash
   python manage.py create_sample_data
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main URL: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Demo Credentials

### Customer Login
- **Email/Phone**: customer@aura.com
- **Password**: customer123

### Admin Login
- **Email/Phone**: admin@aura.com
- **Password**: admin123

### Delivery Boy Login
- **Email/Phone**: delivery@aura.com
- **Password**: delivery123

## Project Structure

```
Miniproject/
    aura/                  # Django project settings
    accounts/              # User management and authentication
    store/                 # Product catalog and inventory
    orders/                # Order processing and management
    delivery/              # Delivery boy functionality
    templates/             # HTML templates
    media/                 # Media files (images)
    static/                # Static files (CSS, JS)
    manage.py              # Django management script
    requirements.txt       # Python dependencies
```

## Key Features Implementation

### Authentication System
- Custom user model with role-based access control
- Three user types: Customer, Admin, Delivery Boy
- Secure login/logout functionality
- Profile management for each user type

### Product Management
- Dynamic product catalog with categories and brands
- Product images with gallery functionality
- Inventory tracking and stock management
- Product reviews and ratings system
- Advanced search and filtering

### Order Processing
- Complete order lifecycle management
- Shopping cart functionality
- Multiple payment options
- Order status tracking
- Delivery assignment system

### Responsive Design
- Mobile-first approach
- Bootstrap-like grid system
- Touch-friendly interfaces
- Optimized for all screen sizes

## API Endpoints

### Products API
- `GET /api/products/` - List all products
- `GET /api/products/<slug>/` - Get product details
- `GET /api/categories/` - List categories

### Authentication API
- `POST /accounts/login/` - User login
- `POST /accounts/logout/` - User logout

## Database Models

### User Management
- **User**: Extended user model with roles
- **CustomerProfile**: Customer-specific data
- **AdminProfile**: Admin-specific data
- **DeliveryBoyProfile**: Delivery boy data

### Ecommerce
- **Category/SubCategory**: Product categorization
- **Brand**: Product brands
- **Product**: Product information
- **ProductImage**: Product images
- **Order**: Order management
- **OrderItem**: Order line items
- **Payment**: Payment processing

## Development Notes

### Customization
- The UI design follows the exact color scheme and layout provided
- All pages are fully responsive
- Images use placeholder URLs that can be replaced with actual media
- The project is production-ready with proper error handling

### Security
- CSRF protection enabled
- Secure password hashing
- Role-based access control
- Input validation and sanitization

### Performance
- Optimized database queries
- Efficient image handling
- Minimal external dependencies
- Fast page load times

## Deployment

### Production Setup
1. Set `DEBUG = False` in settings.py
2. Configure production database (PostgreSQL recommended)
3. Set up static files serving
4. Configure media files storage
5. Set up environment variables for sensitive data
6. Configure domain and SSL

### Environment Variables
Create a `.env` file with:
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=your-database-url
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For any issues or questions, please contact the development team.

## License

This project is licensed under the MIT License.
