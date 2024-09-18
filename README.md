# Library Management and Recommendation System
A Django-based RESTful API project to manage books and authors, including features such as user authentication, book search, and an optimized recommendation system for large datasets.

### Features
1. #### Books API:
* `GET /api/books/`: Retrieve a list of all books.
* `GET /api/books/:id`: Retrieve a specific book by ID.
* `POST /api/books/`: Create a new book (JWT protected).
* `PUT /api/books/:id`: Update an existing book (JWT protected).
* `DELETE /api/books/:id`: Delete a book (JWT protected).

2. #### Authors API:
* `GET /api/authors/`: Retrieve a list of all authors.
* `GET /api/authors/:id`: Retrieve a specific author by ID.
* `POST /api/authors/`: Create a new author (JWT protected).
* `PUT /api/authors/:id`: Update an existing author (JWT protected).
* `DELETE /api/authors/:id`: Delete an author (JWT protected).

3. #### Authentication:
* JWT-based user authentication.
* `POST /api/register/`: Register a new user.
* `POST /api/login/`: Login with a registered user.

4. #### Search Functionality:
* Search books by title or author name using GET /api/books?search=query.

5. #### Recommendation System:
* A content-based and collaborative filtering recommendation system to suggest books based on user preferences.
* Content-based recommendations using metadata similarity (TF-IDF on title, author, and genre).
* Collaborative filtering using a matrix factorization approach for personalized recommendations based on similar users.
* Combines both methods to recommend the top 5 books for the user.

6. #### Favorites:
* Users can add/remove books from their favorites list.
* Recommendation system suggests new books based on the user's favorite list.
* The system recommends titles similar to those in the user's favorites, with a maximum of 20 favorite titles.
