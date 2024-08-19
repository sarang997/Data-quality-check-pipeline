from flask import Flask, request, jsonify
from pipeline_executor import PipelineExecutor
from exceptions import *
from models import PipelineConfig
from pydantic import ValidationError

app = Flask(__name__)

@app.route('/run_pipeline', methods=['POST'])
def run_pipeline():

    try:
        config_data = request.json
        config = PipelineConfig(**config_data)
        pipeline = PipelineExecutor(config.dict())
        results = pipeline.execute()
        return jsonify(results)
    
    except ValidationError as e:
        return jsonify({'error': 'Validation Error', 'details': e.errors()}), 400
    
    except NoFileFoundError as e:
        print("inside file not found error handling in route...")
        return jsonify({'error': e.message}), e.status_code
    
    except Exception as e:
        print("inside main exception...",e)
        return jsonify({'error': 'An unexpected error occurred-'}), 500

if __name__ == '__main__':
    app.run(debug=True)
