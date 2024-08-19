# Data quality check framework

## Introduction

The framework allows users to configure and trigger data processing pipelines through API calls, enabling reusable code and better data quality. It includes a library of atomic data cleaning tasks that can be executed in a user-defined order to generate detailed reports.

## Features

- **Configurable Pipeline**: Users trigger data pipeline through API call.
- **Atomic Tasks**: A library of atomic data quality check tasks, including missing values assessment and duplicate rows identification.
- **Custom Task Order**: The pipeline executes tasks in the order provided by the user and generates a corresponding report.
- **Task Library Management**: Easily add or update tasks in the library.
- **Quality report and log**: The output produced is a quality report of the dataset and the logging of details of atomic tasks that were performed during pipeline execution.

## Usage Guide

### Install the following
1. Clone this repo somewhere and cd into "Data-quality-check-pipeline" folder.
2. **Python 3.x**: Make sure Python 3.x is installed on your system.
3. **Required Libraries**: Install the necessary Python libraries using the following command:
  ```bash 
  pip install -r requirements.txt
  ```
4. **Start flask**- Start the flask server using the following command-
 
 ```bash
  python app.py
``` 
5. **Make the request**- Make the request using the curl given in the sample http request curl in the end of this file.
6. **HTTP request** -

### Endpoint

**POST** `/run_pipeline`

This endpoint is used to trigger the data processing pipeline.

### Request Curl
```bash
curl --location 'http://localhost:5000/run_pipeline' \
--header 'Content-Type: application/json' \
--data '{
    "pipeline_name": "assignment_task_pipeline",
    "input_file": "./input/Assignment Task _ Dataset - Sheet1.csv",
    "tasks": [
          {
      "name": "check_missing_values",
      "params": {
          "columns": ["Name", "Age"],
          "thresholds": {
          "name": 10.0,
          "Age": 1.0
        }
      }
    },
           {
        "name": "check_duplicate_rows",
        "params": {
          "check_type": "row",
          "columns": ["ID"]
        }
      },
      {
        "name": "check_inconsistent_dates",
        "params": {
          "columns": ["Last_Login", "Join_Date"],
          "date_format": "%Y-%m-%d"

        }
      }
      
    ],
    "output": {
      "log_file": "./output/assignment_quality_report.txt",
      "report_file": "./output/assignment_quality_report.json"
    }
  }'
```



## Config structure 

```json
{
    "pipeline_name": "assignment_task_pipeline",
    "input_file": "input.csv",
    "tasks": [
      {
        "name": "check_missing_values",
        "params": {
          "columns": ["ID", "Name"],
          "thresholds": {
            "Title": 1,
            "Brand": 1.0
          }
        }
      },
      {
        "name": "check_duplicate_rows",
        "params": {
          "check_type": "row",
          "columns": ["Brand"]
        }
      }
    ],
    "output": {
      "log_file": "./output/assignment_quality_report.txt",
      "report_file": "./output/assignment_quality_report.json"
    }
  }
```
### Details of config
 #### **pipeline_name** - Name of the pipeline.
 #### **input_file** - Input csv file path.
 #### **tasks** - Array containing task objects.(executed in the order specified)
 Each task object will have name and params keys. There could be any n number of params in a task. 
 #### **output** - Contains report_file which is the quality report and the log_file which is the path of output log file.

### Using Existing Atomic Tasks-
There are 4 existing atomic tasks in the framework. Below I have described how to add them to the tasks array in config. 
- **check_missing_values**-
  ```json
      {
        "name": "check_missing_values",
        "params": {
            "columns": ["Name", "Age"],
            "thresholds": {
            "name": 10.0,
            "Age": 1.0
          }
        }
      }

       ```
 
 - **check_duplicate_rows**- In this if you set check type to 'row' the function will check for row duplicates. If its set to col and columns are specifieid in "columns" parameter it will look for duplicates in ****
  

  ```json
        {
        "name": "check_duplicate_rows",
        "params": {
          "check_type": "col",
          "columns": ["Name"]
           }
        }
  ```
- **check_inconsistent_dates**-
  ```json
        {
        "name": "check_inconsistent_dates",
        "params": {
          "columns": ["Last_Login", "Join_Date"],
          "date_format": "%Y-%m-%d"

          }
        }
  ```
checks if the date formating is inconsistent.  
### Adding Atomic Tasks-
A task method can be added to DataQualityTasks class in [task_library.py](task_library.py)  file. The method takes any number of params and returns the dictionary containing quality metrics. You dont need to pass data to this function since its already defined in the constructor of the class and is part of the object attribute.
## Framework Overview

The framework is built using Object Oriented approach, making it easy to maintain and etxtend.
The following files are present in the framework:

- [app.py](app.py)                                    # Flask server file for running the API
-  [exceptions.py](exceptions.py)                     # Custom exceptions for pipeline errors
- [pipeline_executor.py](pipeline_executor.py)        # PipelineExecutor class for managing and executing the pipeline
- [task_library.py](task_library.py)                  # DataQualityTasks class for defining data quality tasks
- [utils.py](utils.py)                                # Utility functions like logging
- - [models.py](models.py)                            # Contains data models for validating the input config before the pipeline runs (makes sure the proper input config is provided) 

- [input directory](input)                            # Directory containing input datasets
- [output directory](output)                          # Directory where output logs and reports are stored.
  
 Below is the description of each file in the framework:

### 1. API Server (`app.py`)

- The API server is built using Flask. It exposes endpoints that allow users to configure and trigger the data processing pipeline. The server listens for POST requests, which contain the pipeline configuration, including the tasks to be executed and their order.

### 2. `PipelineExecutor` Class (`pipeline_executor.py`)

- **Purpose**: The `PipelineExecutor` class is responsible for executing the data pipeline.
- **Key Method**: 
  - `execute`: This method loads the dataset, picks tasks from the configuration in the order defined by the user, and executes each task. The results of these tasks are stored for further analysis. Once all tasks are processed, the `generate_quality_report` method is called to produce the final data quality report.

### 3. `DataQualityTasks` Class (`task_library.py`)

- **Purpose**: The `DataQualityTasks` class is designed to encapsulate various data cleaning tasks. It allows for easy addition of new tasks.
- **Task Methods**:
  - Each task method can take a set of parameters defined in the configuration, process them, and return a dictionary containing key-value pairs that represent quality metrics. This design allows the framework to be flexible and easily extendable.

### 4. `Utils` Class (`utils.py`)

- **Purpose**: The `Utils` class contains utility functions that support the operation of the pipeline.
- **Key Functions**:
  - Logger setup and custom logging functions are included in this class, making it easy to implement consistent logging throughout the framework. Additional utility functions can be added here as needed.

### 5. `PipelineError` Class (`exceptions.py`)

- **Purpose**: `PipelineError` is the base class for handling exceptions within the pipeline. This class provides a structured approach to error handling, ensuring that issues are managed gracefully.
- **Derived Classes**:
  - Example: 
    - `NoFileFoundError(PipelineError)`: Raised when the input file is not found. This class sets the `status_code` to `404`, which corresponds to the HTTP status code for "Not Found."
  - Additional exception classes can be created by inheriting from `PipelineError`, allowing the framework to handle a variety of errors specific to data processing tasks.

### 6. Task Library (`task_library.py`)

- The task library contains all the atomic tasks that can be used within the pipeline. New tasks can be added by simply creating a new method within the `DataQualityTasks` class.



    
