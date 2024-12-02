import secrets
from flask import Blueprint, Flask, render_template, request, jsonify
from datetime import datetime
import time
import json
from typing import Optional
import traceback
from astrocub.core.prompt_manager import prompt_manager
from .models import PromptData, PromptCategory, PromptStatus, PromptMetadata

bp = Blueprint('genetl', __name__, 
               url_prefix='/genetl',  # All routes will be prefixed with /genetl
               template_folder='templates')  # Look for templates in blueprint's folder


def generate_process_id():
    """Generate a unique process ID using timestamp and random string"""
    return f"prompt_{int(time.time())}_{secrets.token_hex(4)}"

class ProcessStatus:
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"

class PipelineStage:
    UPLOAD = "upload"
    PROCESSING = "processing"
    ANALYSIS = "analysis"

def log_pipeline_event(process_id: str, stage: str, status: str, 
                      metadata: Optional[dict] = None, error_message: Optional[str] = None,
                      processing_time: Optional[float] = None):
    """Log pipeline events to track processing status"""
    event = {
        "process_id": process_id,
        "stage": stage,
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": metadata or {},
        "processing_time": processing_time
    }
    if error_message:
        event["error_message"] = error_message
    
    # In practice, you'd save this to a database
    print(f"Pipeline Event: {json.dumps(event, indent=2)}")

@bp.route('/')
def index():
    """Render the main prompt testing interface"""
    # Get list of available prompts from manager
    prompts = prompt_manager.list_prompts()
    return render_template('prompt_testing.html', prompts=prompts)

@bp.route('/api/prompt', methods=['POST'])
def save_prompt():
    """API endpoint to save or update a prompt"""
    try:
        data = request.json
        # Convert incoming JSON to PromptData object
        prompt_data = PromptData.from_dict(data)
        
        # Validate the prompt data
        if not prompt_data.validate():
            return jsonify({"error": "Invalid prompt data"}), 400
            
        user_id = "test_user"  # In practice, get this from your auth system
        
        # Update metadata
        prompt_data.metadata.last_edited_by = user_id
        prompt_data.metadata.updated_at = datetime.utcnow().isoformat()
        
        if not prompt_data.metadata.created_at:
            prompt_data.metadata.created_at = datetime.utcnow().isoformat()
            prompt_data.metadata.created_by = user_id
        
        # Save to database using prompt manager
        result = prompt_manager.save_prompt(prompt_data, user_id)
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@bp.route('/api/prompt/<name>', methods=['GET'])
def get_prompt(name):
    """API endpoint to get a specific prompt"""
    try:
        version = request.args.get('version', type=int)
        prompt_dict = prompt_manager.get_prompt(name, version=version)
        
        if prompt_dict:
            # Convert dictionary to PromptData object
            prompt = PromptData.from_dict(prompt_dict)
            return jsonify(prompt.to_dict())
            
        return jsonify({"error": "Prompt not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/api/prompts', methods=['GET'])
def list_prompts():
    """API endpoint to list all prompts"""
    try:
        category = request.args.get('category')
        if category:
            category = PromptCategory(category)
            
        status = request.args.get('status')
        if status:
            status = PromptStatus(status)
            
        search = request.args.get('search')
        
        prompt_dicts = prompt_manager.list_prompts(
            category=category,
            status=status,
            search_term=search
        )
        
        # Convert all prompts to PromptData objects
        prompts = [PromptData.from_dict(p).to_dict() for p in prompt_dicts]
        return jsonify({"prompts": prompts})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# @bp.route('/api/test-prompt', methods=['POST'])
# def test_prompt():
#     """API endpoint to test a prompt with sample input"""
#     process_id = generate_process_id()
#     start_time = time.time()
    
#     try:
#         data = request.json
#         prompt_name = data.get('prompt_name')
#         test_input = data.get('test_input')
        
#         log_pipeline_event(
#             process_id=process_id,
#             stage=PipelineStage.PROCESSING,
#             status=ProcessStatus.STARTED,
#             metadata={'prompt_name': prompt_name}
#         )
        
#         # Get the prompt
#         prompt = prompt_manager.get_prompt(prompt_name)
#         if not prompt:
#             raise ValueError(f"Prompt {prompt_name} not found")
            
#         # Create analyzer instance
#         analyzer = EarningsCallAnalyzer(prompt_manager)
        
#         # Process based on prompt category
#         if prompt['category'] == PromptCategory.EXTRACTION:
#             result = await analyzer.analyze_metrics(test_input)
#         elif prompt['category'] == PromptCategory.SUMMARIZATION:
#             result = await analyzer.generate_summary(test_input)
#         else:
#             raise ValueError(f"Unsupported prompt category: {prompt['category']}")
            
#         processing_time = time.time() - start_time
        
#         log_pipeline_event(
#             process_id=process_id,
#             stage=PipelineStage.PROCESSING,
#             status=ProcessStatus.COMPLETED,
#             processing_time=processing_time,
#             metadata={'prompt_name': prompt_name}
#         )
        
#         return jsonify({
#             'result': result,
#             'process_id': process_id,
#             'processing_time': processing_time
#         })
        
#     except Exception as e:
#         processing_time = time.time() - start_time
#         log_pipeline_event(
#             process_id=process_id,
#             stage=PipelineStage.PROCESSING,
#             status=ProcessStatus.FAILED,
#             error_message=str(e),
#             processing_time=processing_time
#         )
#         return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    bp.run(debug=True)