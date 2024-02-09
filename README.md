
# Student Report API

## Project Overview

The Student Report API is a Flask application that provides endpoints for managing batches, students, subjects, and generating reports based on student performance.

## Features

- Create and manage batches with program details.
- Add and retrieve student information.
- Record subject details, including marks achieved and total marks.
- Generate batch reports indicating the pass/fail status of each student.
- Retrieve individual student scores for each subject.

## Setup and Installation
## Clone the repository:
git clone [https://github.com/purniiiima/student-report-api.git](https://github.com/purniiiima/StudentReport.git)

## Navigate to the project directory:
cd student-report-api

## Set up environment variables:
- Create a .env file in the root directory.
- Add the following environment variables:
- FLASK_APP=app.py
- FLASK_ENV=development
- MONGO_URI=<your_mongodb_uri>

## Run the application:
- flask run

## Usage

- Use endpoints such as /batches, /students, /subjects to manage data.
- Use /reports endpoint to generate batch reports.
- Refer to the API documentation for detailed usage instructions.

## Features

- Create and manage batches with program details.
- Add and retrieve student information.
- Record subject details, including marks achieved and total marks.
- Generate batch reports indicating the pass/fail status of each student.
- Retrieve individual student scores for each subject.



