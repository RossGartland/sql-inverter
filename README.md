# SQL INSERT/DELETE Inversion Web App

This application is a web-based tool for converting SQL `INSERT` statements into equivalent `DELETE` statements. Built with Python and Flask, it allows users to input SQL scripts and receive transformed queries that replace `INSERT` operations with their corresponding `DELETE` versions while preserving formatting and comments.

## Features
- Parses and modifies SQL scripts using `sqlparse`
- Replaces `INSERT` statements with `DELETE` statements
- Maintains comment integrity by adjusting `INSERT` references
- Supports batch processing of SQL scripts

## Technologies Used
- **Backend:** Python, Flask
- **Containerization:** Docker
- **Cloud Deployment:** AWS EC2
- **CI/CD:** GitHub Actions

## Setup Instructions

### Prerequisites
- Python 3.x
- Docker installed
- AWS EC2 instance set up with proper access

### Local Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/sql-insert-delete-processor.git
   cd sql-insert-delete-processor
   ```
2. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the Flask app:
   ```sh
   flask run
   ```
   The app will be available at `http://127.0.0.1:5000/`.

### Docker Setup
1. Build and run the Docker container:
   ```sh
   docker build -t sql-processor .
   docker run -p 5000:5000 sql-processor
   ```

### Deployment on AWS EC2
1. SSH into your EC2 instance:
   ```sh
   ssh ec2-user@your-ec2-ip
   ```
2. Clone the repository and navigate to the project directory.
3. Build and run the Docker container on the instance:
   ```sh
   docker build -t sql-processor .
   docker run -d -p 80:5000 sql-processor
   ```
4. Access the web app via `http://your-ec2-public-ip/`.

### CI/CD with GitHub Actions
- The repository includes a GitHub Actions workflow for automated testing and deployment.
- On every push to `main`, the workflow:
  1. Runs unit tests
  2. Builds a Docker image
  3. Deploys the updated container to AWS EC2

## Usage
- Paste an SQL script into the web interface.
- Click "Process" to receive the transformed SQL script.
- Download or copy the result for further use.

## Contributing
Pull requests are welcome! Please open an issue first for discussion before making changes.

## License
This project is licensed under the MIT License.

