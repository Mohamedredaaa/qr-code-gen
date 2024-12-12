# QR Code Generator Project

## Overview
This project is a simple QR code generator web application that allows users to create QR codes for any text or URL. The application is containerized with Docker, deployed with a Procfile, and has a user-friendly interface for ease of use.

---

## Features
- Generate QR codes for text or URLs.
- Downloadable QR code images.
- Responsive and modern UI.
- Deployable via Docker.

---

## Project Structure
```
qr-code-gen
├── static/           # Static files (CSS, JS, images, etc.)
├── templates/        # HTML templates for the application
├── venv/             # Virtual environment for dependencies
├── Dockerfile        # Dockerfile for containerization
├── Procfile          # For deployment configuration
├── app.py            # Main application script
├── requirements.txt  # Python dependencies
```

---

## Setup Instructions

### Prerequisites
- Python 3.x
- Docker (optional for containerized deployment)

### Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Mohamedredaaa/qr-code-gen.git
   cd qr-code-gen
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open the application in your browser at `http://127.0.0.1:5000`.

### Docker Setup
1. Build the Docker image:
   ```bash
   docker build -t qr-code-gen .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 qr-code-gen
   ```

3. Access the application at `http://localhost:5000`.

---

## Deployment
This application is configured for deployment using a `Procfile`. Ensure you have a platform like Heroku to deploy the application seamlessly.

---

## Future Enhancements
- Add QR code customization options (colors, sizes).
- Provide analytics for generated QR codes.
- Support batch QR code generation.

---

## Contributing
Feel free to fork the repository, make changes, and submit a pull request. Contributions are always welcome!

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

