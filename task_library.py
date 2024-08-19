from datetime import datetime
import logging

class DataQualityTasks:
    def __init__(self, data, logger=None):
        self.data = data #pandas DataFrame 
        self.logger = logger or logging.getLogger(__name__)
        
    def check_missing_values(self, columns, thresholds):
        # self.logger.log_message(f"Checking for missing values. Columns: {columns}")
        results = {}
        for col in columns:
            try:
                missing_count = int(self.data[col].isnull().sum())
                missing_percentage = float((missing_count / len(self.data)) * 100)
                threshold = thresholds.get(col, 0)
                if threshold < 0:
                    self.logger.log_message(f"threshhold must be >=0.")
                    continue
                else:
                    results[col] = {
                        'missing_count': missing_count,
                        'missing_percentage': missing_percentage,
                        'exceeds_threshold': bool(missing_percentage > threshold)
                    }

                self.logger.log_message(f"Column {col}: {missing_count} missing values ({missing_percentage:.2f}%)")
            except KeyError:
                self.logger.log_message(f"Column '{col}' not found in dataframe. Skipping.")
            except Exception as e:
                self.logger.log_message(f"Error processing column '{col}': {str(e)}")
                results[col] = {'error': str(e)}

        return results
    def check_duplicate_rows(self, check_type, columns=None):
        result = {
            "check_type": check_type,
            "columns": columns if columns else list(self.data.columns),
            "total_duplicates": 0,
            "duplicate_indices": []  # Initialize a list to hold duplicate row indices
        }

        if check_type == "row":
            duplicates = self.data.duplicated(keep=False)  # Keep all duplicates
            result["total_duplicates"] = duplicates.sum()
            result["duplicate_indices"] = self.data.index[duplicates].tolist()

        elif check_type == "individual":
            result["column_duplicates"] = {}
            for col in result["columns"]:
                duplicates = self.data[col].duplicated(keep=False)
                result["column_duplicates"][col] = {
                    "count": duplicates.sum(),
                    "indices": self.data.index[duplicates].tolist()
                }
            result["total_duplicates"] = sum(value["count"] for value in result["column_duplicates"].values())
            # Aggregate all duplicate indices from individual columns
            all_duplicate_indices = set()
            for indices in result["column_duplicates"].values():
                all_duplicate_indices.update(indices["indices"])
            result["duplicate_indices"] = list(all_duplicate_indices)

        elif check_type == "combined":
            if not columns:
                raise ValueError("Columns must be specified for combined check type")
            duplicates = self.data.duplicated(subset=columns, keep=False)
            result["total_duplicates"] = duplicates.sum()
            result["duplicate_indices"] = self.data.index[duplicates].tolist()

        else:
            raise ValueError("Invalid check_type. Must be 'row', 'individual', or 'combined'")

        return result

    def check_missing_values(self, columns, thresholds):
        # self.logger.log_message(f"Checking for missing values. Columns: {columns}")
        results = {}
        for col in columns:
            try:
                missing_count = int(self.data[col].isnull().sum())
                missing_percentage = float((missing_count / len(self.data)) * 100)
                threshold = thresholds.get(col, 0)
                if threshold < 0:
                    self.logger.log_message(f"threshhold must be >=0.")
                    continue
                else:
                    results[col] = {
                        'missing_count': missing_count,
                        'missing_percentage': missing_percentage,
                        'exceeds_threshold': bool(missing_percentage > threshold)
                    }

                self.logger.log_message(f"Column {col}: {missing_count} missing values ({missing_percentage:.2f}%)")
            except KeyError:
                self.logger.log_message(f"Column '{col}' not found in dataframe. Skipping.")
            except Exception as e:
                self.logger.log_message(f"Error processing column '{col}': {str(e)}")
                results[col] = {'error': str(e)}

        return results
    
    def check_inconsistent_dates(self, columns, date_format):
        self.logger.log_message(f"Checking for inconsistent dates in columns: {columns}")
        
        if isinstance(columns, str):
            columns = [columns]  # Convert single column to list
        
        results = {}

        for column in columns:
            column_result = {
                'inconsistent_count': 0,
                'inconsistent_percentage': 0,
                'inconsistent_indices': []
            }

            try:
                if column not in self.data.columns:
                    raise KeyError(f"Column '{column}' not found in dataframe.")

                def is_valid_date(date_string):
                    try:
                        datetime.strptime(str(date_string), date_format)
                        return True
                    except ValueError:
                        return False

                mask = self.data[column].astype(str).apply(is_valid_date)
                inconsistent_dates = ~mask

                column_result['inconsistent_count'] = int(inconsistent_dates.sum())
                column_result['inconsistent_percentage'] = float((column_result['inconsistent_count'] / len(self.data)) * 100)
                column_result['inconsistent_indices'] = inconsistent_dates[inconsistent_dates].index.tolist()

                self.logger.log_message(f"Column {column}: Found {column_result['inconsistent_count']} inconsistent dates "
                                        f"({column_result['inconsistent_percentage']:.2f}%)")

            except Exception as e:
                self.logger.log_message(f"Error in check_inconsistent_dates for column '{column}': {str(e)}")
                column_result['error'] = str(e)

            results[column] = column_result

        return results
    
    #ADD ATOMIC FUNCTIONS HERE AS CLASS METHODS