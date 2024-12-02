from dataclasses import dataclass, field
from typing import Dict, Optional, List
from enum import Enum
import json

class PromptCategory(str, Enum):
    """Categories for different types of prompts"""
    EXTRACTION = 'extraction'
    SUMMARIZATION = 'summarization'
    ANALYSIS = 'analysis'
    TRANSFORMATION = 'transformation'
    CLASSIFICATION = 'classification'
    OTHER = 'other'

class PromptStatus(str, Enum):
    """Status indicators for prompts"""
    DRAFT = 'draft'
    ACTIVE = 'active'
    ARCHIVED = 'archived'
    TESTING = 'testing'

@dataclass
class PromptMetadata:
    """Metadata for tracking prompt information"""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    created_by: Optional[str] = None
    last_edited_by: Optional[str] = None
    version: int = 1
    is_favorite: bool = False

@dataclass
class PromptData:
    """Main class for storing and validating prompt information"""
    name: str  # Unique identifier for the prompt
    display_name: str  # Human-readable name
    category: PromptCategory  # Type of prompt
    main_prompt: str  # The primary prompt text
    description: Optional[str] = None  # Description of what the prompt does
    system_prompt: Optional[str] = None  # System-level instructions
    output_format: Optional[Dict] = None  # Expected output structure
    input_schema: Optional[Dict] = None  # Expected input structure
    guidelines: Optional[List[str]] = None  # Usage guidelines
    example_input: Optional[str] = None  # Example input for testing
    example_output: Optional[str] = None  # Expected output for example
    notes: Optional[str] = None  # Additional notes
    tags: List[str] = field(default_factory=list)  # Searchable tags
    status: PromptStatus = PromptStatus.DRAFT  # Current status
    ui_section_order: Optional[Dict] = None  # Order of sections in UI
    metadata: PromptMetadata = field(default_factory=PromptMetadata)

    def __post_init__(self):
        """Validate and process data after initialization"""
        # Convert string category to enum if needed
        if isinstance(self.category, str):
            self.category = PromptCategory(self.category.lower())
        
        # Convert string status to enum if needed
        if isinstance(self.status, str):
            self.status = PromptStatus(self.status.lower())
        
        # Ensure tags are unique and lowercase
        if self.tags:
            self.tags = list(set(tag.lower() for tag in self.tags))
        
        # Initialize metadata if not provided
        if not isinstance(self.metadata, PromptMetadata):
            self.metadata = PromptMetadata(**self.metadata if isinstance(self.metadata, dict) else {})

    def to_dict(self) -> Dict:
        """Convert the prompt data to a dictionary format"""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "category": self.category.value,
            "main_prompt": self.main_prompt,
            "description": self.description,
            "system_prompt": self.system_prompt,
            "output_format": self.output_format,
            "input_schema": self.input_schema,
            "guidelines": self.guidelines,
            "example_input": self.example_input,
            "example_output": self.example_output,
            "notes": self.notes,
            "tags": self.tags,
            "status": self.status.value,
            "ui_section_order": self.ui_section_order,
            "metadata": {
                "created_at": self.metadata.created_at,
                "updated_at": self.metadata.updated_at,
                "created_by": self.metadata.created_by,
                "last_edited_by": self.metadata.last_edited_by,
                "version": self.metadata.version,
                "is_favorite": self.metadata.is_favorite
            }
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'PromptData':
        """Create a PromptData instance from a dictionary"""
        # Extract metadata if present
        metadata = data.pop('metadata', {})
        if metadata:
            metadata = PromptMetadata(**metadata)
        
        # Create instance with remaining data
        return cls(**data, metadata=metadata)

    def validate(self) -> bool:
        """Validate the prompt data structure and content"""
        try:
            # Check required fields
            if not self.name or not self.display_name or not self.main_prompt:
                return False
            
            # Validate output format if provided
            if self.output_format:
                # Attempt to parse as JSON if string
                if isinstance(self.output_format, str):
                    json.loads(self.output_format)
            
            # Validate input schema if provided
            if self.input_schema:
                if isinstance(self.input_schema, str):
                    json.loads(self.input_schema)
            
            return True
        except Exception:
            return False

# Example usage for creating a prompt:
def create_example_prompt() -> PromptData:
    """Create an example prompt to demonstrate usage"""
    return PromptData(
        name="earnings_metrics_extraction",
        display_name="Earnings Call Metrics Extractor",
        category=PromptCategory.EXTRACTION,
        description="Extracts financial metrics with YoY and QoQ comparisons",
        main_prompt="Extract all financial metrics...",
        system_prompt="You are a precise financial metrics extractor...",
        output_format={
            "metrics": {
                "type": "object",
                "properties": {}
            }
        },
        guidelines=["Extract only explicit metrics", "Maintain source references"],
        tags=["earnings", "metrics", "financial"],
        status=PromptStatus.ACTIVE
    )