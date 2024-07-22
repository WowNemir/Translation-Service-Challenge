# Translation Service Challenge

## Description

The **Translation Service Challenge** is a project designed to provide a translation service with support for word definitions, translations, and example usage. The service uses FastAPI for the backend, MongoDB for data storage, and a Node.js subprocess script for fetching additional data from third-party APIs.

## Running the Application

### Using Docker Compose

1. **Clone the repository**:
   ```bash
   git clone https://github.com/WowNemir/Translation-Service-Challenge
   cd Translation-Service-Challenge
   ```

2. **Build and start the application**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - The FastAPI application will be available at `http://localhost:8000`.
   - SwaggerUI `http://localhost:8000/docs`

### API Endpoints

- **GET /word/{word}**: Retrieve details about a specific word, including translations and definitions.
- **GET /words/**: List words with optional filtering and pagination.
- **DELETE /word/{word_id}**: Delete a specific word by ID.

## Known Issues and Suggested Enhancements

### 1. Security and Reliability Issues

*The current setup relies on a Node.js subprocess script to interact with third-party APIs for translations and word definitions, given the lack of a Google API for definitions and examples. This method presents several concerns:*
- **Security**: Executing subprocesses can pose security risks, particularly if the inputs are not thoroughly validated.
- **Reliability**: Relying on external APIs introduces potential risks if those APIs undergo changes or become unavailable.

**Suggested Enhancements**:
- **Alternative Data Sources**: Explore and assess other APIs or services for obtaining translation and definition data, with a focus on their security and reliability.
- **API Integration**: Where feasible, integrate directly with more dependable and secure APIs to minimize reliance on subprocesses.

### 2. Database Design

The current database design uses a single collection for storing words, translations, and definitions. This can lead to inefficient queries and complex data management.

**Possible Improvements**:
- **Separate Collections**: Introduce separate collections for "Translations" and "Definitions" to simplify data management and improve query performance. This would involve restructuring the database and updating the application code to handle the new schema.
