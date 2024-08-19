import pandas as pd
import numpy as np
from task_library import DataQualityTasks
from utils import Utils
import json
from exceptions import *

class PipelineExecutor:
    def __init__(self, config):
        self.config = config
        self.data = None
        self.results = {}
        self.logger = Utils(config['output']['log_file'])  # Instantiate the Utils class
    
    
    def load_data(self):
        file_path = self.config.get('input_file', 'data.csv')
        try:
            self.data = pd.read_csv(file_path)
            self.logger.log_message(f"Loaded data from {file_path} with {len(self.data)} rows and {len(self.data.columns)} columns.\n")
        except FileNotFoundError as e:
            print("test...")
            error_msg = f"File not found: {file_path}. Exception: {e}"
            self.logger.log_message(error_msg)
            raise NoFileFoundError(error_msg)
        except pd.errors.EmptyDataError as e:
            error_msg = f"No data: {file_path} is empty. Exception: {e}"
            self.logger.log_message(error_msg)
            raise
        except pd.errors.ParserError as e:
            error_msg = f"Error parsing data: {file_path}. Exception: {e}"
            self.logger.log_message(error_msg)
            raise
        except Exception as e:
            error_msg = f"An unexpected error occurred while loading data: {e}"
            self.logger.log_message(error_msg)
            raise

    def execute(self):
        try:
            self.logger.log_message("==========================")
            
            self.logger.log_message("Pipeline execution started.")
            self.load_data()
            tasks = DataQualityTasks(self.data, logger=self.logger)  # Pass the logger here
            for task in self.config['tasks']:
                task_name = task['name']
                self.logger.log_message(f"Starting Atomic task- {task_name}")
                task_params = task['params']
                if hasattr(tasks, task_name):
                    try:
                        task_function = getattr(tasks, task_name)
                        result = task_function(**task_params)
                        self.results[task_name] = result
                        self.logger.log_message(f"Atomic task result- {result}.\n")
                        
                        # self.logger.log_task(task_name)
                        self.logger.log_message("End of atomic task.\n")
                        
                    except Exception as e:
                        error_msg = f"Error executing task {task_name}: {e}"
                        self.logger.log_message(error_msg)
                        raise
                else:
                    warning_msg = f"Task {task_name} is not defined."
                    self.logger.log_message(warning_msg)
            self.generate_quality_report()
            self.logger.log_message("==========================\n")
            # self.logger.log_message("\n")
            return {"status":"successful", "code": 200}
            
        except Exception as e:
            self.logger.log_message(f"Pipeline execution failed: {e}")
            raise


    def generate_quality_report(self):
        try:
            report = {
                'pipeline_name': self.config['pipeline_name'],
                'input_file': self.config.get('input_file', 'data.csv'),
                'results': self.json_serialize(self.results)
            }
            
            output_file = self.config['output']['report_file']
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"Report generated and saved to {output_file}")
            self.logger.log_message(f"Report generated and saved to {output_file}")
        except IOError as e:
            error_msg = f"Failed to write report to {output_file}: {e}"
            self.logger.log_message(error_msg)
            raise
        except Exception as e:
            error_msg = f"An unexpected error occurred while generating the report: {e}"
            self.logger.log_message(error_msg)
            raise

    def json_serialize(self, obj):
        if isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {self.json_serialize(key): self.json_serialize(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.json_serialize(item) for item in obj]
        else:
            return obj
        
# RUN THIS FILE TO RUN THE JSON CONFIG MANUALLY WITHOUT API(USED FOR DEBUGGING)

if __name__ == "__main__":
    def load_config(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)

    config_file = "laptop_data_config.json"
    config = load_config(config_file)
    pipeline = PipelineExecutor(config)
    pipeline.execute()