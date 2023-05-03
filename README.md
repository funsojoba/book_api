# Book API with User Authentication and CRUD Operations

This project is a Flask app that provides an API for books, with user authentication and CRUD operations for books by user. The API is built using Python Flask framework and uses MongoDB as the database for storing books and user authentication data. RabbitMQ is used for message queueing.

### Features
* User authentication and authorization using JWT (JSON Web Token)
* CRUD operations for books by user
* Message queueing using RabbitMQ for notifications and background processing

### Requirements

* Python 3.x
* Docker
* Docker Compose

### Setup

1. Clone the repository
`git clone https://github.com/funsojoba/book_api.git`

2. Navigate to the project directory:
`cd book_api`

3. Build and run the application:
`docker compose up --build`

4. Access the API at `http://localhost:6000`

### Endpoints

The following endpoints are available in the API:
Authentication

    POST /api/auth/signup/ - Register a new user
    POST /api/auth/login - Authenticate a user and return a JWT token

### Books

    GET /api/books - Get a list of all books
    POST /api/books - Create a new book
    GET /api/books/<book_id> - Get a book by ID
    PUT /api/books/<book_id> - Update a book by ID
    DELETE /api/books/<book_id> - Delete a book by ID


### Environment Variables

A list of environment variables can be found in the `.env.example`



### Postman collection

Here's the link to the [Postman Collextion](https://documenter.getpostman.com/view/9644998/2s93eU2Zrd)
