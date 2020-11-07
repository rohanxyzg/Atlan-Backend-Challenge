# Introduction


**Task State Manager** is an implementation of an upload/download system in which the functionality of pausing/resuming/terminating the task at hand is possible.

## ❓ Problem Statement

- We want to offer an implementation through which the user can stop the long-running task at any given point in time, and can choose to resume or terminate it. This will ensure that the resources like compute/memory/storage/time are used efficiently at our end, and do not go into processing tasks that have already been stopped (and then to roll back the work done post the stop-action)

## 🚧 Technology Stack

-Django Rest Framework
-PostgreSQL
-Python version 3.8.2

## ⬇️ Installation and Run with docker

```
# clone the repository to your local machine

# navigate to the project's directory and install all the relevant dev-dependencies
$ cd Atlan-Challenge---Long-Running-Task-Manager 

# Run
$ docker-compose up -d --build

# Then Run
$ docker-compose exec web python ./runningTask/manage.py migrate

# Visit http://localhost:8000/ in your browser
```




# 💡 Approach

### Upload

- A dummy CSV file is read using pandas and added row by row to a table in database.
  #### Pause
  When paused an Interrupt Exception is raised which stops the upload.
  #### Resume
  When resumed, the csv files gets read from the checkpoint
  ### Terminate
  Basic sql drop table
  ### Progress
  Basic maths

### Download/Export

- A database table from the server can be exported as a CSV file.
  #### Pause
  hen paused an Interrupt Exception is raised which stops the upload.
  #### Resume
  When resumed, the database files gets read from the checkpoint
  ### Terminate
  remove exported csv file
  ### Progress
  basic maths



## 🔨 API Endpoints

| REQUEST METHODS |      ENDPOINTS      |                                       DESCRIPTION |
| :-------------- | :-----------------: | ------------------------------------------------: |
| POST            |    /upload/start    |                      Start uploading the CSV File |
| POST            |    /upload/pause    |                                  Pause the upload |
| POST            |   /upload/resume    |                                 Resume the upload |
| POST            |  /upload/terminate  |                              Terminate the upload |
| GET             |  /upload/progress   |               Get the percntage upload completion |
| POST            |   /download/start   | Start downloading/exporting from DB into CSV file |
| POST            |   /download/pause   |                                Pause the download |
| POST            |  /download/resume   |                               Resume the download |
| POST            | /download/terminate |                            Terminate the download |
| GET             | /download/progress  |             Get the percntage download completion |
