"""
Advanced Legal Document Summarization with Multiple Formats
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

class LegalDocumentSummarizer:
    """Advanced legal document summarization with multiple output formats"""
    
    def __init__(self):
        self.groq_llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=2048
        )
        self.summarization_prompts = self._create_summarization_prompts()
    
    def _create_summarization_prompts(self) -> Dict[str, PromptTemplate]:
        """Create different summarization prompts for various formats"""
        
        executive_summary_template = """You are an expert legal analyst. Create a concise executive summary of the following legal document.

Document Text: {document_text}

Create an executive summary that includes:
1. Document Type and Purpose
2. Key Parties (if applicable)
3. Main Legal Issues
4. Critical Terms and Conditions
5. Risk Assessment
6. Recommendations

Executive Summary:"""

        detailed_analysis_template = """You are a senior legal counsel. Provide a detailed analysis of the following legal document.

Document Text: {document_text}

Provide a comprehensive analysis including:
1. Document Classification
2. Legal Framework and Applicable Laws
3. Constitutional Implications (if any)
4. Privacy and Data Protection Aspects
5. Compliance Requirements
6. Potential Legal Risks
7. Recommendations for Action

Detailed Analysis:"""

        constitutional_summary_template = """You are an expert in Indian Constitutional Law. Analyze the following document for constitutional implications.

Document Text: {document_text}

Focus on:
1. Constitutional Articles Referenced or Implicated
2. Fundamental Rights Considerations (Articles 12-35)
3. Privacy Rights under Article 21
4. DPDPA 2023 Compliance Implications
5. Constitutional Validity Assessment
6. Recommendations for Constitutional Compliance

Constitutional Analysis:"""

        privacy_summary_template = """You are a privacy law expert specializing in Indian data protection. Analyze this document for privacy implications.

Document Text: {document_text}

Analyze for:
1. Personal Data Collection and Processing
2. Article 21 Privacy Rights Implications
3. DPDPA 2023 Compliance Requirements
4. Data Subject Rights
5. Privacy Risk Assessment
6. Recommendations for Privacy Compliance

Privacy Analysis:"""

        return {
            "executive": PromptTemplate(template=executive_summary_template, input_variables=["document_text"]),
            "detailed": PromptTemplate(template=detailed_analysis_template, input_variables=["document_text"]),
            "constitutional": PromptTemplate(template=constitutional_summary_template, input_variables=["document_text"]),
            "privacy": PromptTemplate(template=privacy_summary_template, input_variables=["document_text"])
        }
    
    def summarize_document(self, document_text: str, summary_type: str = "executive", 
                          chunk_size: int = 4000) -> Dict[str, Any]:
        """Summarize document with specified format"""
        
        try:
            # Handle long documents by chunking
            if len(document_text) > chunk_size:
                return self._summarize_long_document(document_text, summary_type, chunk_size)
            else:
                return self._summarize_chunk(document_text, summary_type)
                
        except Exception as e:
            logger.error(f"Summarization error: {str(e)}")
            return {
                "summary": "Error generating summary. Please try again.",
                "summary_type": summary_type,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _summarize_chunk(self, text: str, summary_type: str) -> Dict[str, Any]:
        """Summarize a single chunk of text"""
        
        prompt = self.summarization_prompts.get(summary_type, self.summarization_prompts["executive"])
        formatted_prompt = prompt.format(document_text=text)
        
        response = self.groq_llm.invoke(formatted_prompt)
        
        return {
            "summary": response.content,
            "summary_type": summary_type,
            "word_count": len(response.content.split()),
            "timestamp": datetime.now().isoformat(),
            "source_length": len(text)
        }
    
    def _summarize_long_document(self, document_text: str, summary_type: str, chunk_size: int) -> Dict[str, Any]:
        """Summarize long documents by chunking and combining"""
        
        # Split document into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " "]
        )
        
        chunks = text_splitter.split_text(document_text)
        chunk_summaries = []
        
        # Summarize each chunk
        for i, chunk in enumerate(chunks):
            chunk_summary = self._summarize_chunk(chunk, summary_type)
            chunk_summaries.append({
                "chunk_id": i + 1,
                "summary": chunk_summary["summary"]
            })
        
        # Combine chunk summaries
        combined_text = "\n\n".join([cs["summary"] for cs in chunk_summaries])
        
        # Create final summary
        final_summary_prompt = f"""
        Combine the following section summaries into a coherent {summary_type} summary:
        
        {combined_text}
        
        Create a unified, well-structured summary that maintains all key information:
        """
        
        final_response = self.groq_llm.invoke(final_summary_prompt)
        
        return {
            "summary": final_response.content,
            "summary_type": summary_type,
            "chunks_processed": len(chunks),
            "chunk_summaries": chunk_summaries,
            "word_count": len(final_response.content.split()),
            "timestamp": datetime.now().isoformat(),
            "source_length": len(document_text)
        }
    
    def generate_all_summaries(self, document_text: str) -> Dict[str, Any]:
        """Generate all types of summaries for a document"""
        
        all_summaries = {}
        summary_types = ["executive", "detailed", "constitutional", "privacy"]
        
        for summary_type in summary_types:
            try:
                summary_result = self.summarize_document(document_text, summary_type)
                all_summaries[summary_type] = summary_result
            except Exception as e:
                logger.error(f"Error generating {summary_type} summary: {str(e)}")
                all_summaries[summary_type] = {
                    "summary": f"Error generating {summary_type} summary",
                    "error": str(e)
                }
        
        return {
            "summaries": all_summaries,
            "generation_timestamp": datetime.now().isoformat(),
            "document_length": len(document_text)
        }
