# Flask User Management System

This Flask application demonstrates a simple user management system with registration, login, file upload, and dynamic content display based on user interactions. It's designed to showcase Flask's capabilities for web development beginners.

## Features

- **User Registration**: Enables new users to sign up by providing their username, first name, last name, email, and password, along with the ability to upload a text file.
- **Login System**: Allows users to log in to the application using their registered credentials.
- **File Upload**: During registration, users can upload a text file (`Limerick.txt`), which the application stores.
- **Word Count Display**: For the uploaded file, the application calculates and displays the word count on the user's success page.
- **Downloadable Content**: Users can download the previously uploaded file from their success page.
- **Dynamic Success Page**: Displays user-specific information, including the word count of the uploaded file, upon successful login or registration.

## Installation

To get this application up and running on your local machine, follow these steps:

### Prerequisites

Ensure you have Python and pip installed on your system. Flask is required to run this application, which can be installed via pip.

### Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/ameya1252/FlaskApp.git
cd FlaskApp
