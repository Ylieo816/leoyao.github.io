# Patent Infringement Check Application

This application provides a tool for checking potential patent infringements by analyzing company products against specific patents.

## Project Structure

The project is divided into two main parts: backend and frontend.

### Backend - FastAPI (Python)

- `app/`
  - `main.py`: Entry point for the FastAPI application
  - `services/`
    - `infringement_check.py`: Core logic for infringement checking
    - `llm_service.py`: Integration with OpenAI's GPT 3.5 for analysis

- `Dockerfile`: Docker configuration for the backend

### Frontend - React 

- `src/`
  - `components/`
    - `InfringementCheck.js`: Main component for the infringement check interface
    - `InfringementCheck.css`: CSS Style for User Interface Settings
  - `App.js`: Root component
  - `index.js`: Entry point for React app

- `public/`
  - `index.html`: HTML template

- `package.json`: Node.js dependencies and scripts
- `Dockerfile`: Docker configuration for the frontend

### Data

- `data/`
  - `company_products.json`: Contains company and product information
  - `patents.json`: Contains patent information

## Setup and Running the Application

### Prerequisites

- Docker and Docker Compose
- Node.js and npm (for local development)

### Running with Docker in Local Env

1. docker-compose up --build
2. Access the application at `http://localhost:3000`
3. Test the Test Data
4. Finish via docker-compose down 

### (Bonus Points) Running on a web server
http://172.104.36.87:3000/


Copyright ©2024 All rights reserved | This Source Code is made with Leo Yao for Take-Home Assignment of Patlytics