# Translation Service Challenge

This project demonstrates a translation service using FastAPI, MongoDB, and Docker Compose, with a Node.js script for calling third-party APIs.

## Running the Application

### Using Docker Compose

1. **Clone the repository:**
    ```bash
    git clone https://github.com/WowNemir/Translation-Service-Challenge.git
    cd Translation-Service-Challenge
    ```

2. **Build and run the Docker containers:**
    ```bash
    docker-compose up --build
    ```

3. **Access the application**:
   - The FastAPI application will be available at `http://localhost:8000`.
   - SwaggerUI `http://localhost:8000/docs`
   - MongoDB will be accessible on port `27017`.

## Known Issues and Suggested Enhancements

### 1. Node.js Script Call Workaround

**The current implementation uses a Node.js subprocess script to interact with third-party APIs for translations and definitions due to the lack of a suitable API for definitions and examples. This approach has several critical drawbacks:**

- **Security Risks**: Executing subprocesses can introduce security vulnerabilities, especially if input validation is not thorough.
- **Productivity Bottleneck**: This workaround can be a productivity bottleneck, as it creates a dependency on external APIs, which can become unreliable if these services change or become unavailable.
- **Performance Impact**: Subprocess calls can slow down the service and consume significant memory. Additionally, generating many subprocesses can lead to resource exhaustion, making this approach unsuitable for production environments.

**Suggested Enhancements**:
- **Explore Alternative Data Sources**: Evaluate other APIs or services for translation and definition data, focusing on their security and reliability to minimize risks.
- **Make the Definitions, Examples, and Synonyms Optional Features**: Use the Google API to only translate the words and use this advanced API call to enrich the data.

### 2. Database Design

The current database design uses a single collection for storing words, translations, and definitions. This can lead to inefficient queries and complex data management.

**Possible Improvements**:
- **Separate Collections**: Introduce separate collections for "Translations" and "Definitions" to simplify data management and improve query performance. This would involve restructuring the database and updating the application code to handle the new schema.

### 3. Project Structure

The current project structure places all files in the root directory, which can make the project harder to navigate and maintain.

**Suggested Enhancements**:
- **Organize the Project Structure**: Create a more organized structure by grouping related files into directories such as `app`, `routes`, `db`, `models`, and `scripts`. Update the imports and Docker configurations accordingly.
