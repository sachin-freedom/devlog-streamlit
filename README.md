# DevLog - Developer Productivity & Daily Log Tool

DevLog is a tool designed to help developers track their daily tasks, mood, and blockers. It allows users to submit their daily logs, which can be viewed later, and sends reminders to developers and managers about daily log submission.

## Features
- **Developer Dashboard**: Submit daily logs with details about tasks, time spent, mood, and blockers.
- **Manager Dashboard**: Review logs submitted by developers and view productivity reports.
- **Email Notifications**: Automatic reminders sent to developers for log submission, and managers are notified when logs are submitted.
- **Export Logs**: Download reports as CSV files.
- **Authentication**: User registration and login using MongoDB and password hashing for secure access.

## Requirements

Make sure you have the following installed:

- Python 3.x
- MongoDB (locally or remotely hosted)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/devlog.git
   cd devlog```

2. Create a virtual environment:
  ```bash
       python -m venv venv
  ```

3. Activate the virtual environment:
    - On windows:
      
      ```bash
      .\venv\Scripts\activate
      ```
      
   - On Mac/Linux:
     
      ```bash
      source venv/bin/activate
     ```
      
4. Install dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```
   
6. Set up your `.env` file for environment variables:
   
   ```bash
   MONGO_URI=mongodb://your_mongo_uri_here```

6. Run the application:
```bash
   streamlit run app.py
```


## **Folder Structure**
- `app.py`: Main entry point for the Streamlit app.

- `dev_dashboard.py`: Developer dashboard logic.

- `manager_dashboard.py`: Manager dashboard logic.

- `db.py`: MongoDB connection setup.

- `utils.py`: Helper functions and utilities.

- `auth.py`: Authentication-related functions.

- `requirements.txt`: Python dependencies for the project.

- `.env`: Environment variables for sensitive information (e.g., MongoDB URI).

## **Usage**
1. **Sign Up:** Users can create an account by providing a username, email, password, and role (developer/manager).

2. **Login:** Registered users can log in using their username and password.

3. **Daily Log Submission:** Developers can submit their daily tasks, mood, time spent, and blockers.

4. **Manager Dashboard:** Managers can review logs submitted by developers and track overall productivity.

## **Contributing**
If you'd like to contribute to this project, feel free to fork the repository, make changes, and submit a pull request. Please ensure that your code follows the same conventions as the existing codebase.


