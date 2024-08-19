#Used for validating the config before running the pipeline
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class TaskParams(BaseModel):    
    class Config:
        extra = 'allow'  # Allows additional fields with any key-value pairs

class Task(BaseModel):
    name: str
    params: TaskParams

class OutputConfig(BaseModel):
    log_file: str
    report_file: str

class PipelineConfig(BaseModel):
    pipeline_name: str
    input_file: str
    tasks: List[Task]
    output: OutputConfig
