# Backend Assignment

## Introduction

I have created a back end application based on the requirements mentioned and this file will give you a brief about how the project should be set up and run. The codebase has comments throughout to help you understand what each method does or a snippet of code does.

### Features
- Endpoints as per requirement
- Input validation
- Complete working backend

### Technologies Used
- Python 3
- Flask
- MongoDB
- Python helper libraries

## Setup

Follow the instructions below to get the project up and running on your local machine.

### Prerequisites

Make sure you have the following installed:
- Python3
- MongoDB
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/project-name.git
   ```
2. Open the directory in any code editor
3. Create and activate a virtual environment
    ```bash
    python3 -m venv venv
    venv\Scripts\activate
    ```
4. Install all the packages required that are mentioned in requirements.txt
    ```bash
    pip install -r requirements.txt
    ```
5. After installing all the packages, run the app.py
    ```bash
    python app.py
    ```
6. Your project should be running now, I have already created a postman collection with all endpoints to test out the application

### Usage
1. All the endpoints mentioned in the requirements have been created
2. Start the project by running `python app.py`
2. Import Assignment.postman_collection.json into your postman workspace
3. Create an environment variable named URL in postman with the localhost ip where the project is running, Ex.,
    ```
    http://127.0.0.1:5000
    ```
4. Endpoints have been created as per the requirement
5. First create a user as well as admin using UserRegister and AdminRegister requests in postman
6. After creating am user and admin, you need to log in using UserLogin to use user endpoints and AdminLogin to use admin endpoints
7. Ensure when using `UploadAssignment` enter the user access_token that is created after logging in using `UserLogin`, in the authorization tab and use Auth Type as Bearer Token
8. Same goes for `GetAssignemnts, AcceptAssignemnt and RejectAssignment` enter the access_token created after logging into an admin using `AdminLogin` into the authorization tab, this helps to authenticate if the right admin is trying to access the objects
9. Examples of every model is given in the ModelExample.txt file

## Conclusion
Overall, all the requirements have been fulfilled and the application is working as inteded along with input validations and proper error messages.
