"""
Basic functionality tests for Indian Legal KAG System
"""
import pytest
import os
from unittest.mock import Mock, patch
from .processors.document_processor import IndianLegalDocumentProcessor
from .messaging.smtp_manager import SMTPEmailManager
from .indian_legal_utils import validate_environment_variables

def test_document_processor_initialization():
    """Test document processor can be initialized"""
    processor = IndianLegalDocumentProcessor()
    assert processor is not None

def test_smtp_manager_initialization():
    """Test SMTP manager can be initialized"""
    manager = SMTPEmailManager()
    assert manager is not None
    assert manager.smtp_providers is not None

def test_environment_validation():
    """Test environment variable validation"""
    # Mock environment variables
    with patch.dict(os.environ, {
        'NEO4J_URI': 'bolt://localhost:7687',
        'NEO4J_USER': 'neo4j',
        'NEO4J_PASSWORD': 'password',
        'GROQ_API_KEY': 'test_key'
    }):
        results = validate_environment_variables()
        assert results['neo4j'] == True
        assert results['groq'] == True

def test_smtp_provider_config():
    """Test SMTP provider configuration"""
    manager = SMTPEmailManager()
    
    gmail_config = manager.get_provider_config('gmail')
    assert gmail_config is not None
    assert gmail_config['server'] == 'smtp.gmail.com'
    assert gmail_config['port'] == 587

if __name__ == "__main__":
    pytest.main([__file__])
