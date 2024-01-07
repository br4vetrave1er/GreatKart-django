# Great-Kart

## E-commerce Website

e-commerce website project aimed at showcasing web development Skills. The project focused on creating an intuitive online shopping platform for users.
problems solved in this project
* back-end infrastructure to manage product listings and order processing.
* Implemented secure payment processing using the Stripe API
* Integrated a user-friendly product catalog with search and filter functionalities.
* Established a scalable and maintainable database structure for efficient data management.
* a secure user authentication system to manage customer accounts.
* real-time order tracking feature, providing customers with updates on their purchases.

### more about Application

I spearheaded the end-to-end development of a feature-rich eCommerce web application, harnessing the capabilities of the Django web framework, HTML, and CSS, with seamless payment processing integrated through the Stripe API. Django's Model-View-Controller (MVC) architecture facilitated a scalable and maintainable codebase for the backend. The application incorporated the Stripe API to handle secure and efficient payment processing, supporting major credit cards and online payment methods. Utilizing Django's form handling capabilities, I seamlessly integrated the necessary forms for collecting and validating payment details.

The frontend, crafted using HTML and CSS, was not only visually appealing but also designed for optimal user experience during the checkout process. Responsive design principles were employed to ensure a consistent and user-friendly interface across various devices. AJAX was leveraged to create a smooth and dynamic user experience, especially during payment confirmation and order tracking.

To enhance security, the application implemented tokenization of payment data through Stripe, ensuring that sensitive information was never stored on our servers. Customized Django signals were implemented to handle successful and failed payment transactions, providing users with clear feedback. Additionally, Django's built-in security features were complemented by Stripe's advanced fraud detection tools, creating a robust and secure payment environment.

### Images



### Tech-Stack
<img src="https://brandslogos.com/wp-content/uploads/images/large/django-logo.png" width="40" height="40"> <img src="https://brandslogos.com/wp-content/uploads/thumbs/python-logo-vector.svg" width="40" height="40"> <img src="https://brandslogos.com/wp-content/uploads/thumbs/postgresql-inc-logo-vector.svg" width="40" height="40">
<img src="https://brandslogos.com/wp-content/uploads/thumbs/html5-logo-vector.svg" width="40" height="40">
<img src="https://brandslogos.com/wp-content/uploads/thumbs/css3-logo-vector.svg" width="40" height="40">
<img src="https://brandslogos.com/wp-content/uploads/thumbs/javascript-logo-vector.svg" width="40" height="40">
<img src="https://brandslogos.com/wp-content/uploads/thumbs/stripe-logo-vector-2.svg" width="40" height="40">



### Installation
1. Clone the GitHub repository
    ```
    !git clone https://github.com/br4vetrave1er/GreatKart-django.git
    ```
2. create a virtual environment
    ```
    python -m venv [environment name] 
   ```
3. install necessary libraries using requirement.txt
    ```
    pip install -r requirements.txt
   ```
4. If you want to use this project in development server then
    ```
    python manage.py runserver
   ```
5. For using email based services provide following details in .env file or directly in projects settings file
    ```
     EMAIL_BACKEND = config('EMAIL_BACKEND')
     EMAIL_HOST = config('EMAIL_HOST')
     EMAIL_PORT = config('EMAIL_PORT', cast=int)
     EMAIL_HOST_USER = config('EMAIL_HOST_USER')
     EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
     EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
   ```
6. For using postgresql database instead of default provide following info in settings file within project
    ```
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.environ['RDS_DB_NAME'],
    'USER': os.environ['RDS_USERNAME'],
    'PASSWORD': os.environ['RDS_PASSWORD'],
    'HOST': os.environ['RDS_HOSTNAME'],
    'PORT': os.environ['RDS_PORT'],
    ```
7. For using the Admin page do check settings as custom urls and django-honeypot library is used.

### Improvements to be done
* Addition of more products and categories
* Elastic search based search system
* recommendation system based on user purchases
* inclusion of more dynamic UI
* Addition of UPI payment system
