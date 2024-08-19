import logging
import os

class Utils:
    def __init__(self, log_file):
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        # Reset the logging configuration
        logging.shutdown()
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        print("Setting up logging", self.log_file)
        # Create the log file if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w'):
                pass  # Create the file and close it immediately
        
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def log_task(self, task_name):
        logging.info(f"End of task- '{task_name}'")
        
    def log_message(self, message):
        print("inside log task")
        logging.info(message)


# Example usage:
# utils = Utils("path_to_log_file.log")
# utils.log_task("check_missing_values", {"status": "success"})

