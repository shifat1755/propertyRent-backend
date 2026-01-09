# **Under Construction..**

This is the backend for a property rental platform. The backend is built with **FastAPI** and its ecosystem (**Pydantic, SQLAlchemy, Alembic**), integrates **Elasticsearch** for full-text search functionality, uses **PostgreSQL** for data storage, and **Redis** for caching and token management.

### Ongoing:

- **Backend work is currently paused to focus on the client side.**

---

## **Completed Features**

### **Authentication**

- User registration and login with JWT-based authentication.
- Password hashing using **bcrypt** for secure storage.

### **Property Management**

- CRUD operations for property listings.
- Property data stored in **PostgreSQL**.

### **Full-Text Search**

- Full-text search for properties using **Elasticsearch**.
- Search across fields like `title` and `description` with support for:
  - Fuzzy matching (handles typos).
  - Highlighting matched terms in the search results.

### **Caching**

- **Redis** is used for:
  - Caching frequently accessed data.
  - Managing refresh tokens for authentication.

### **Error Handling**

- Custom error classes for consistent error responses.

### **Data Ingestion**

- **Logstash** is used to ingest property data into Elasticsearch.

---

### **Modular Architecture**

- Clean and modular code structure:
  - **Domain Layer**: Defines entities and business rules.
  - **Application Layer**: Contains use cases for core business logic.
  - **Infrastructure Layer**: Handles data access, security, and external integrations.
  - **Presentation Layer**: Defines API routes and request/response schemas.

## **How to Run the App Locally**

### **Prerequisites**

1. Install **Docker** and **Docker Compose** on your system.

---

### **Steps to Run**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/shifat1755/propertyRent-backend.git
   cd propertyRent-backend
   ```
2. **Start the Application Use Docker Compose to build and start all the service**

   ```bash
   docker-compose up --build
   ```

Open your browser and navigate to http://127.0.0.1:8000/docs to explore the API documentation.
