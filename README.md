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

## Known Flaws and Possible Improvements

### 1. Security and Reliability Concerns

The current implementation uses a Node.js subprocess script to call third-party APIs for translation and word definitions. This approach has several issues:
- **Security**: Direct subprocess calls can introduce security vulnerabilities, especially if the input is not properly sanitized.
- **Reliability**: Dependency on third-party services may lead to issues if the external API changes or becomes unavailable.

**Possible Improvements**:
- **Data Gathering**: Consider using alternative APIs or services to fetch translation and definition data. Evaluate services for security and reliability.
- **Direct API Integration**: Integrate directly with more reliable and secure APIs if possible, reducing reliance on subprocess calls.

### 2. Database Design

The current database design uses a single collection for storing words, translations, and definitions. This can lead to inefficient queries and complex data management.

**Possible Improvements**:
- **Separate Collections**: Introduce separate collections for "Translations" and "Definitions" to simplify data management and improve query performance. This would involve restructuring the database and updating the application code to handle the new schema.
