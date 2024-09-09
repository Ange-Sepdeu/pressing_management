PressPro Application
Overview
PressPro is a comprehensive web application designed for managing pressing services, including marketing and promotions. The platform allows admins and managers to efficiently handle user profiles, manage marketing campaigns, and promote services through various social media platforms.

Features
1. User Management
Admin: Can manage users, roles, and permissions.
Pressing Manager: Manages pressing profiles and oversees promotions.
Deliver: Manages deliveries and tracks statuses.
Client: Interacts with the platform to book services and view updates.
2. Pressing Profile Management
Create and Edit Pressing Profiles: Manage business information, services, and media (photos/videos).
Approval Workflow: Profiles must be approved before they go live.
3. Marketing and Promotions
Marketing Dashboard: Admins can select pressing profiles and manage promotional content.
Social Media Integration: Promote pressing services on Facebook, Instagram, TikTok, and YouTube.
Media Upload: Upload videos and photos for marketing purposes.
4. Real-Time Chat
Chat Messaging: Real-time communication between users.
Installation
Prerequisites
Python 3.x
Django 4.x
Django REST Framework
PostgreSQL (or another database supported by Django)
Setup
Clone the Repository

bash
Copy code
git clone https://github.com/your-repo/presspro.git
cd presspro
Create and Activate a Virtual Environment

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Configure Database

Update settings.py with your database configuration.

Run Migrations

bash
Copy code
python manage.py migrate
Create a Superuser

bash
Copy code
python manage.py createsuperuser
Run the Development Server

bash
Copy code
python manage.py runserver
Access the Application

Open your browser and go to http://127.0.0.1:8000/.

URL Patterns
/marketing-promotions/: Dashboard for managing marketing and promotions.
Actors and Their Functions
1. Admin
Functions:

Manage Users: Create, update, and delete user accounts. Assign roles.
Pressing Management: Oversee all pressing profiles, approve or reject profiles.
Marketing & Promotions: Manage marketing campaigns and promotions.
Settings: Configure system settings and integrations.
2. Pressing Manager
Functions:

Pressing Profile Management: Create, update, and delete pressing profiles.
Marketing: Upload promotional content (photos/videos) and manage social media marketing.
3. Deliver
Functions:

Delivery Management: Track and manage delivery statuses.
4. Client
Functions:

Book Services: Request and manage pressing services.
View Updates: Check the status of their bookings and any promotions.
Models
CustomUser
Manages user roles and profile pictures.
Contact
Stores contact information for inquiries and service rates.
PressingProfile
Contains details about pressing services, including media and business information.
Photo
Stores photos related to pressing profiles.
Video
Stores video files for promotional content.
Receipt
Manages receipts for transactions.
ChatMessage
Facilitates real-time messaging between users.
Contributing
Contributions are welcome! Please follow the standard Git workflow:

Fork the repository.
Create a feature branch.
Make your changes and commit them.
Push your branch and create a pull request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

