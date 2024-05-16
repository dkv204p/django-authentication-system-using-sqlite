# Django Authentication System Using SQLite

![Django Logo](https://www.djangoproject.com/s/img/logos/django-logo-negative.png)

## Overview

This Django project implements a robust authentication system using SQLite as the database backend. With the growing importance of secure user authentication in web applications, this project provides a solid foundation for implementing user registration, login, logout, and password management functionalities.

## Key Features

- **User Registration:** Users can sign up for new accounts by providing a unique username, a valid email address, and a secure password.
- **User Authentication:** Registered users can securely log in to their accounts using their username/email and password combination.
- **Session Management:** Upon successful authentication, the system establishes a session for each user, allowing them to navigate authenticated areas of the application without needing to re-enter their credentials for each request.
- **Password Management:** Users can reset their password if forgotten and change their password for enhanced account security.

## Technologies Used

- **Django:** The web framework provides a secure and scalable architecture for building web applications, including robust user authentication features.
- **SQLite:** A lightweight and self-contained relational database management system, perfect for development and small-scale production environments.
- **HTML/CSS/JavaScript:** Frontend technologies used for designing user interfaces and enhancing user experience.

## Getting Started

1. Clone this repository to your local machine.
2. Install Django and other dependencies using `pip install -r requirements.txt`.
3. Run migrations to create the SQLite database schema: `python manage.py migrate`.
4. Start the development server: `python manage.py runserver`.
5. Access the application in your web browser at `http://localhost:8000` or `http://127.0.0.1:8000`.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests. Suggestions for further enhancements are appreciated.

## License

This project is licensed under the [MIT License](LICENSE).

## Additional Information

- **Edits are Welcomed**: This project is open to edits and improvements. If you have any ideas or enhancements to propose, please feel free to contribute.
