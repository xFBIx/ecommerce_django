# Sweet Pants

Website Link : www.detrace.systems/ecommerce/

# E-commerce App

A comprehensive online marketplace built with Django, designed for vendors to sell books and customers to make purchases. This project evolves through various stages to enhance functionality and user experience.

## Overview

This repository hosts an e-commerce application with the following capabilities:

- **Authentication and User Management:**

  - Utilizes Django's authentication system to manage vendors and customers separately.
  - Librarians can register and manage their book listings.
  - Users can register, view orders, and manage their profiles.

- **Core Functionality:**

  - Database models structured for efficient management of users, books, orders, and reviews.
  - Supports vendor actions such as adding and deleting books, and viewing orders related to their books.
  - Users can add funds to their accounts and place orders based on available funds and book availability.
  - Implements a home page listing all available items with top-selling items prioritized.

- **Additional Features:**

  - Integration of OAuth for Google sign-in using Django Allauth.
  - Email notifications to vendors upon customer purchases, facilitated through Mailjet API.
  - Migration from SQLite to PostgreSQL for robust database management.
  - Librarian ability to generate CSV/Excel reports of their sales history.
  - Enhanced ordering capability allowing customers to order multiple types of items simultaneously with a shopping cart model.
  - Wishlist functionality for customers to save desired items for future purchase.

- **Deployment:**
  - Deployed on DigitalOcean using Docker, Nginx, and Gunicorn for bookion readiness.
  - Provides a scalable and secure environment for hosting the application.

## Setup

To set up the project:

1. Clone the repository.
2. Create a `keyconfig.py` file in the directory where `settings.py` exists with the following format:

   ```python
   # Django settings
   SECRET_KEY = 'your_secret_key_here'
   DEBUG = True  # Set to False in bookion

   # Google Allauth
   CLIENT_ID = 'your_google_client_id'
   CLIENT_SECRET = 'your_google_client_secret'

   # Mailjet
   MJ_APIKEY_PUBLIC = 'your_mailjet_public_key'
   MJ_APIKEY_PRIVATE = 'your_mailjet_private_key'
   ```

3. Configure Django settings as per your environment (development or bookion).
4. Set up Django admin groups 'User' and 'Librarian' for user permissions.

## Usage

Navigate to the IP address of your DigitalOcean droplet to access the live application.

---
