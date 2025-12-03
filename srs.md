# Software Requirements Specification (SRS)
# E-Commerce Website

---

## 1. Introduction

### 1.1 Purpose
This document provides a detailed description of the requirements for the E-Commerce Website. It outlines the functional and non-functional requirements of the system, and it serves as a guide for the development and testing of the project. This project is developed as a graduation project for the ITI Institute, focusing on comprehensive automation testing.

### 1.2 Document Conventions
This document follows a standard SRS template. All requirements are uniquely identified and written in a clear and concise manner.

### 1.3 Intended Audience
This document is intended for project stakeholders, primarily the ITI Institute. The core team consists of a single individual acting as both developer and tester. This document aims to provide a common understanding of the system to be built and tested.

### 1.4 Project Scope
The project is to build a fully functional E-Commerce Website with features for user authentication, product management, shopping cart, checkout, order management, and more. The system will have a user-facing front-end and a back-end API for managing the data.

### 1.5 References
*   USER_STORY.md
*   API_USER_STORY.md
*   POSTMAN_DOCUMENTIONS.md
*   UI User Story.md
*   UI TestCases_v3.csv

---

## 2. Overall Description

### 2.1 Product Perspective
The E-Commerce Website is a new, self-contained product. It will provide a platform for users to browse and purchase products online.

### 2.2 Product Features
The major features of the system are:
*   User Authentication (Registration, Login, Logout)
*   Product Catalog (View, Search, Filter)
*   Shopping Cart Management
*   Order and Checkout System
*   User Profile Management
*   Wishlist
*   Product Reviews and Ratings
*   Admin Dashboard

### 2.3 User Classes and Characteristics
*   **Anonymous User:** Can browse products and view product details.
*   **Registered User:** Can perform all actions of an anonymous user, plus manage their profile, cart, orders, wishlist, and write reviews.
*   **Administrator:** Can perform all actions of a registered user, plus manage products, categories, orders, and users.

### 2.4 Operating Environment
The system will be a web-based application accessible through standard web browsers. It will run on a server with a Python backend and a database for data storage.

### 2.5 Design and Implementation Constraints
*   The back-end will be developed using Python and the Flask framework.
*   The front-end will use HTML, CSS, and JavaScript.
*   The data will be stored in JSON files.
*   The project is developed and tested by a single individual, serving dual roles as developer in the morning and tester in the night.

### 2.6 Assumptions and Dependencies
*   The system assumes that users have a stable internet connection.
*   The system depends on a third-party service for product images.

---

## 3. System Features

### 3.1. Authentication
*   **3.1.1. User Registration:** The system shall allow new users to register with a unique email and password.
*   **3.1.2. User Login:** The system shall allow registered users to log in with their email and password.
*   **3.1.3. User Logout:** The system shall allow logged-in users to log out.
*   **31.4. Admin Login:** The system shall provide a separate login for administrators.

### 3.2. Product Management
*   **3.2.1. View Products:** The system shall display a list of all available products.
*   **3.2.2. View Product Details:** The system shall display detailed information for each product.
*   **3.2.3. Search Products:** The system shall allow users to search for products by name and description.
*   **32.4. Filter Products:** The system shall allow users to filter products by category and price.
*   **3.2.5. Create Product (Admin):** The system shall allow administrators to add new products.
*   **3.2.6. Update Product (Admin):** The system shall allow administrators to update existing products.
*   **3.2.7. Delete Product (Admin):** The system shall allow administrators to delete products.

### 3.3. Shopping Cart
*   **3.3.1. Add to Cart:** The system shall allow users to add products to their shopping cart.
*   **3.3.2. View Cart:** The system shall allow users to view the contents of their shopping cart.
*   **3.3.3. Update Cart Quantity:** The system shall allow users to update the quantity of items in their cart.
*   **3.3.4. Remove from Cart:** The system shall allow users to remove items from their cart.
*   **3.3.5. Clear Cart:** The system shall allow users to clear their entire cart.

### 3.4. Checkout and Orders
*   **3.4.1. Proceed to Checkout:** The system shall allow users to proceed to checkout from their cart.
*   **3.4.2. Place Order:** The system shall allow users to place an order by providing a shipping address.
*   **3.4.3. View Orders:** The system shall allow users to view their order history.
*   **3.4.4. Filter Orders:** The system shall allow users to filter their orders by status.
*   **3.4.5. Cancel Order:** The system shall allow users to cancel their pending orders.

### 3.5. User Profile
*   **3.5.1. View Profile:** The system shall allow users to view their profile information.
*   **35.2. Update Profile:** The system shall allow users to update their profile information.
*   **3.5.3. Change Password:** The system shall allow users to change their password.
*   **3.5.4. Delete Account:** The system shall allow users to delete their account.

### 3.6. Wishlist
*   **3.6.1. Add to Wishlist:** The system shall allow users to add products to their wishlist.
*   **3.6.2. View Wishlist:** The system shall allow users to view their wishlist.
*   **3.6.3. Remove from Wishlist:** The system shall allow users to remove products from their wishlist.

### 3.7. Reviews
*   **3.7.1. View Reviews:** The system shall display reviews for products.
*   **3.7.2. Write Review:** The system shall allow logged-in users to write reviews for products.

### 3.8. Help and Contact
*   **3.8.1. Help Page:** The system shall provide a help page with FAQs.
*   **3.8.2. Contact Page:** The system shall provide a contact form for users to send messages to support.

### 3.9. Other Features
*   **3.9.1. Advanced Search:** The system shall provide an advanced search page with more filter options.
*   **3.9.2. Notifications:** The system shall display notifications to users.
*   **3.9.3. Admin Dashboard:** The system shall provide a dashboard for administrators to view store statistics.

---

## 4. External Interface Requirements

### 4.1. User Interfaces
The system will have a web-based user interface that is intuitive and easy to use. The UI will be responsive and accessible on different devices.

### 4.2. Hardware Interfaces
No special hardware is required. The system will be accessible through standard computers and mobile devices.

### 4.3. Software Interfaces
*   **Web Browser:** The system will be compatible with modern web browsers (Chrome, Firefox, Safari, Edge).
*   **API:** The front-end will communicate with the back-end through a RESTful API.

### 4.4. Communications Interfaces
The system will use the HTTP/S protocol for communication between the client and the server.

---

## 5. Non-functional Requirements

### 5.1. Performance Requirements
The system should be able to handle a reasonable number of concurrent users without a significant degradation in performance. Pages should load within 3 seconds.

### 5.2. Safety Requirements
N/A

### 5.3. Security Requirements
*   All passwords must be hashed and salted before being stored in the database.
*   The system must be protected against common web vulnerabilities, such as SQL injection and Cross-Site Scripting (XSS).
*   The API must be secured with tokens to prevent unauthorized access.

### 5.4. Software Quality Attributes
*   **Reliability:** The system should be available 24/7 with minimal downtime.
*   **Usability:** The system should be easy to learn and use.
*   **Maintainability:** The code should be well-structured and documented to facilitate future maintenance.
*   **Testability:** The system will be thoroughly tested using automated tools. UI automation will be performed using Java Selenium, while API testing will utilize Java Rest Assured and Postman.

---

## 6. Other Requirements
This section can be used for any other requirements not covered in the previous sections.