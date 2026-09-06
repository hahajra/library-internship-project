\# Week 3 Authentication Concepts



\## Authentication



Authentication is the process of verifying who a user is.



In the Library project, a basic authentication foundation was created using user registration and login endpoints.



The current Week 3 implementation checks the username and password stored in the database.



\## Authorization



Authorization determines what an authenticated user is allowed to access or perform.



For example, a future version of the Library application could allow administrators to add or delete books while normal users could only view books.



\## JWT



JWT stands for JSON Web Token.



A JWT can be generated after a successful login and sent with later API requests to identify the logged-in user.



JWT authentication was studied during Week 3 but full JWT implementation was not required for the current foundation.



\## Password Security



Passwords should not be stored as plain text in a real application.



Production applications should hash passwords using a secure password hashing algorithm before storing them in the database.



The current login implementation is only a basic learning foundation for the internship task.



\## Current Project Authentication Flow



1\. User sends registration details.

2\. The API checks whether the username already exists.

3\. The user is stored in the SQL Server database.

4\. The user sends username and password to the login endpoint.

5\. The API checks the supplied credentials.

6\. Valid credentials return a successful login response.

7\. Invalid credentials return an unauthorized response.



\## Future Improvements



Possible future improvements include:



\- Password hashing

\- JWT token generation

\- Role-based authorization

\- Protected API endpoints

\- Token expiration

\- Refresh tokens

