# FilezUp

FilezUp is a web application built to streamline file management with secure authentication, upload, download, and deletion functionalities. Designed with a React frontend and a Django backend, FilezUp provides an intuitive user interface for seamless file handling and secure user data storage.

## Features

- **User Authentication**: Secure login and logout functionality with token-based authentication.
- **File Upload**: Multiple files can be uploaded at once, and files are stored with metadata for easy management.
- **File Download**: Download files directly from the server without renaming, ensuring original filenames are preserved.
- **File Deletion**: Easy deletion of files with instant UI updates reflecting file removal.
- **Responsive Design**: Optimized for desktop and mobile viewing, with dark mode support.
  
## Getting Started

### Prerequisites

- **Backend**:
  - Python 3.8+
  - Django 4.x
  - Django Rest Framework
  - SQLite

- **Frontend**:
  - Node.js 14+
  - React 18+
  - Redux Toolkit (for state management)

### Installation

#### Backend Setup

1. Clone the repository and navigate to the backend directory:
   ```bash
   git clone https://github.com/yourusername/filezup.git
   cd filezup/backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database and apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the Django server:
   ```bash
   python manage.py runserver
   ```

#### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React app:
   ```bash
   npm start
   ```

## API Documentation

The Django REST API provides endpoints for user authentication, file upload, file download, and file deletion. For more details, see the API documentation:

- `POST /api/login/` - User login
- `POST /api/register/` - User register
- `POST /api/logout/` - User logout
- `POST /api/file/upload/` - Upload files
- `GET /api/file/` - Fetch list of files
- `GET /api/file/download/<file_id>/` - Download a file
- `DELETE /api/file/delete/<file_id>/` - Delete a file

## Usage

1. **Login**: Start by logging in with your credentials.
2. **Upload Files**: Select multiple files for upload.
3. **Manage Files**: Download or delete files from the uploaded files list.
4. **Logout**: End your session securely.

## Technologies

- **Frontend**: React, Redux Toolkit, Axios, Bootstrap
- **Backend**: Django, Django REST Framework, SQLite

