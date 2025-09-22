# """
# Complete Enhanced Indian Legal Document Processor
# Ready for Integration with Indian Legal KAG System
# Updated with Advanced Document Classifier Integration
# """

# import logging
# import fitz  # PyMuPDF
# import re
# from io import BytesIO
# from typing import List, Dict, Any, Optional, Tuple
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from sentence_transformers import SentenceTransformer
# from analysis_frameworks.document_classifier import AdvancedDocumentClassifier
# import streamlit as st
# from datetime import datetime

# logger = logging.getLogger(__name__)

# class IndianLegalDocumentProcessor:
#     """Enhanced document processor specifically for Indian legal documents"""
    
#     def __init__(self):
#         self.embedding_model = self._load_embedding_model()
#         self.indian_legal_patterns = self._initialize_indian_legal_patterns()
#         # ✅ Advanced Document Classifier Integration
#         self.document_classifier = AdvancedDocumentClassifier()
        
#     @staticmethod
#     @st.cache_resource
#     def _load_embedding_model():
#         """Load sentence transformer model with caching"""
#         try:
#             return SentenceTransformer('all-MiniLM-L6-v2')
#         except Exception as e:
#             logger.error(f"Failed to load embedding model: {str(e)}")
#             return None
    
#     def _initialize_indian_legal_patterns(self) -> Dict[str, List[str]]:
#         """Initialize patterns for Indian legal document recognition"""
#         return {
#             "constitutional_references": [
#                 r"Article\s+(\d+)(?:\s*(?:\([a-z]\)|\([0-9]+\)))?",
#                 r"Constitution\s+of\s+India",
#                 r"Fundamental\s+Rights?",
#                 r"Directive\s+Principles?",
#                 r"Part\s+III|Part\s+IV",
#                 r"Schedule\s+[IVX]+",
#                 r"Preamble"
#             ],
#             "indian_cases": [
#                 r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+v\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
#                 r"AIR\s+\d{4}\s+SC\s+\d+",
#                 r"(\d{4})\s+\d+\s+SCC\s+\d+",
#                 r"Supreme\s+Court",
#                 r"High\s+Court",
#                 r"Puttaswamy",
#                 r"Kesavananda\s+Bharati",
#                 r"Maneka\s+Gandhi"
#             ],
#             "indian_statutes": [
#                 r"Indian\s+Penal\s+Code",
#                 r"Code\s+of\s+Criminal\s+Procedure",
#                 r"Indian\s+Evidence\s+Act",
#                 r"Companies\s+Act\s+\d{4}",
#                 r"Information\s+Technology\s+Act",
#                 r"DPDPA\s+2023",
#                 r"Digital\s+Personal\s+Data\s+Protection\s+Act",
#                 r"Indian\s+Contract\s+Act",
#                 r"Labour\s+Laws?"
#             ],
#             "privacy_terms": [
#                 r"personal\s+data",
#                 r"data\s+protection",
#                 r"privacy\s+policy",
#                 r"data\s+subject",
#                 r"data\s+fiduciary",
#                 r"consent",
#                 r"processing\s+of\s+data",
#                 r"right\s+to\s+privacy",
#                 r"informational\s+privacy",
#                 r"territorial\s+privacy"
#             ],
#             "government_terms": [
#                 r"Government\s+of\s+India",
#                 r"Ministry\s+of",
#                 r"Department\s+of",
#                 r"Notification",
#                 r"Office\s+Memorandum",
#                 r"Gazette\s+of\s+India",
#                 r"Central\s+Government",
#                 r"State\s+Government"
#             ],
#             "legal_concepts": [
#                 r"whereas",
#                 r"hereby",
#                 r"provided\s+that",
#                 r"notwithstanding",
#                 r"subject\s+to",
#                 r"in\s+exercise\s+of",
#                 r"powers\s+conferred",
#                 r"shall\s+be\s+deemed"
#             ]
#         }
    
#     def extract_text_from_pdf(self, pdf_file: BytesIO) -> Dict[str, Any]:
#         """Enhanced PDF text extraction with Indian legal context"""
#         try:
#             # Read PDF bytes
#             pdf_bytes = pdf_file.read()
#             doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            
#             extraction_result = {
#                 "full_text": "",
#                 "page_texts": [],
#                 "metadata": {
#                     "total_pages": len(doc),
#                     "extraction_timestamp": datetime.now().isoformat(),
#                     "document_type": "unknown",
#                     "language": "english",
#                     "legal_jurisdiction": "india"
#                 },
#                 "indian_legal_indicators": {},
#                 "document_classification": {}
#             }
            
#             # Extract text page by page
#             full_text_parts = []
#             for page_num in range(len(doc)):
#                 try:
#                     page = doc.load_page(page_num)
#                     page_text = page.get_text()
                    
#                     if page_text.strip():  # Only add non-empty pages
#                         full_text_parts.append(page_text)
#                         extraction_result["page_texts"].append({
#                             "page_number": page_num + 1,
#                             "text": page_text,
#                             "char_count": len(page_text),
#                             "word_count": len(page_text.split())
#                         })
                        
#                 except Exception as e:
#                     logger.warning(f"Error extracting page {page_num + 1}: {str(e)}")
#                     continue
            
#             extraction_result["full_text"] = "\n".join(full_text_parts)
            
#             # Analyze for Indian legal indicators
#             extraction_result["indian_legal_indicators"] = self._analyze_indian_legal_indicators(
#                 extraction_result["full_text"]
#             )
            
#             # ✅ USE ADVANCED CLASSIFIER - Updated Classification
#             extraction_result["document_classification"] = self._classify_document_with_advanced_classifier(
#                 extraction_result["full_text"]
#             )
            
#             extraction_result["metadata"]["document_type"] = extraction_result["document_classification"]["primary_type"]
            
#             logger.info(f"✅ Successfully extracted {len(full_text_parts)} pages from PDF")
#             doc.close()
#             return extraction_result
            
#         except Exception as e:
#             logger.error(f"❌ PDF extraction failed: {str(e)}")
#             return {
#                 "full_text": "",
#                 "page_texts": [],
#                 "metadata": {"error": str(e)},
#                 "indian_legal_indicators": {},
#                 "document_classification": {"primary_type": "unknown", "confidence": 0.0}
#             }
    
#     def _classify_document_with_advanced_classifier(self, text: str) -> Dict[str, Any]:
#         """Use Advanced Document Classifier for document classification"""
#         try:
#             # ✅ USE THE ADVANCED CLASSIFIER
#             doc_type, confidence, all_scores = self.document_classifier.classify_with_confidence(text)
            
#             # Get additional analysis
#             comprehensive_analysis = self.document_classifier.analyze_document_comprehensive(text)
            
#             return {
#                 "primary_type": doc_type,
#                 "confidence": confidence,
#                 "confidence_level": self.document_classifier.get_classification_confidence_level(confidence),
#                 "all_scores": all_scores,
#                 "alternative_classifications": comprehensive_analysis["alternative_classifications"],
#                 "indian_legal_context": comprehensive_analysis["indian_legal_context"],
#                 "document_characteristics": comprehensive_analysis["document_characteristics"],
#                 "classification_reasoning": comprehensive_analysis["classification_reasoning"],
#                 "recommendations": comprehensive_analysis["recommendations"],
#                 "classification_method": "advanced_ml",
#                 "classification_timestamp": datetime.now().isoformat()
#             }
            
#         except Exception as e:
#             logger.error(f"Advanced classification failed: {str(e)}")
#             # Fallback to basic classification
#             return {
#                 "primary_type": "unknown",
#                 "confidence": 0.0,
#                 "confidence_level": "very_low",
#                 "all_scores": {},
#                 "classification_method": "fallback",
#                 "error": str(e)
#             }
    
#     def _analyze_indian_legal_indicators(self, text: str) -> Dict[str, Any]:
#         """Comprehensive analysis of Indian legal system indicators"""
#         indicators = {
#             "constitutional_references": [],
#             "indian_cases": [],
#             "indian_statutes": [],
#             "privacy_terms": [],
#             "government_terms": [],
#             "legal_concepts": [],
#             "confidence_scores": {},
#             "article_mentions": [],
#             "dpdpa_relevance": False,
#             "constitutional_relevance": False
#         }
        
#         text_lower = text.lower()
        
#         # Analyze each pattern category
#         for category, patterns in self.indian_legal_patterns.items():
#             found_matches = []
            
#             for pattern in patterns:
#                 try:
#                     matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
#                     if matches:
#                         if isinstance(matches[0], tuple):
#                             # Handle tuple matches (like case names)
#                             found_matches.extend([" v ".join(match) for match in matches])
#                         else:
#                             found_matches.extend(matches)
#                 except Exception as e:
#                     logger.warning(f"Pattern matching error for {pattern}: {str(e)}")
#                     continue
            
#             # Remove duplicates and store
#             indicators[category] = list(set(found_matches))
            
#             # Calculate confidence score (normalized by text length)
#             text_words = len(text_lower.split())
#             indicators["confidence_scores"][category] = len(found_matches) / max(1, text_words / 100)
        
#         # Special analysis for constitutional articles
#         article_pattern = r"Article\s+(\d+)"
#         article_matches = re.findall(article_pattern, text, re.IGNORECASE)
#         indicators["article_mentions"] = [int(num) for num in set(article_matches) if num.isdigit()]
        
#         # Assess DPDPA relevance
#         indicators["dpdpa_relevance"] = (
#             indicators["confidence_scores"].get("privacy_terms", 0) > 0.1 or
#             any("dpdpa" in term.lower() for term in indicators.get("indian_statutes", []))
#         )
        
#         # Assess constitutional relevance
#         indicators["constitutional_relevance"] = (
#             indicators["confidence_scores"].get("constitutional_references", 0) > 0.1 or
#             len(indicators["article_mentions"]) > 0
#         )
        
#         return indicators
    
#     def chunk_text_indian_legal(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Dict[str, Any]]:
#         """Advanced text chunking with Indian legal context preservation"""
        
#         # Legal-aware separators
#         legal_separators = [
#             "\n\n\n",      # Major section breaks
#             "\n\n",        # Paragraph breaks
#             ".\n",         # Sentence with newline
#             ". ",          # Regular sentence end
#             ";\n",         # Legal clause separator
#             "; ",          # Clause separator
#             ":\n",         # Colon with newline
#             "\n",          # Line break
#             " "            # Word break
#         ]
        
#         try:
#             splitter = RecursiveCharacterTextSplitter(
#                 chunk_size=chunk_size,
#                 chunk_overlap=chunk_overlap,
#                 separators=legal_separators,
#                 length_function=len
#             )
            
#             text_chunks = splitter.split_text(text)
            
#         except Exception as e:
#             logger.error(f"Text splitting failed: {str(e)}")
#             # Fallback to simple splitting
#             words = text.split()
#             text_chunks = []
#             for i in range(0, len(words), chunk_size // 10):  # Rough word-based chunking
#                 chunk = " ".join(words[i:i + chunk_size // 10])
#                 text_chunks.append(chunk)
        
#         # Enhance chunks with legal context
#         enhanced_chunks = []
#         for i, chunk in enumerate(text_chunks):
#             try:
#                 chunk_indicators = self._analyze_indian_legal_indicators(chunk)
                
#                 enhanced_chunk = {
#                     "chunk_id": i,
#                     "text": chunk,
#                     "char_count": len(chunk),
#                     "word_count": len(chunk.split()),
#                     "indian_legal_indicators": chunk_indicators,
#                     "chunk_type": self._classify_chunk_type(chunk, chunk_indicators),
#                     "constitutional_relevance": self._assess_constitutional_relevance(chunk_indicators),
#                     "privacy_relevance": self._assess_privacy_relevance(chunk_indicators),
#                     "dpdpa_relevance": chunk_indicators.get("dpdpa_relevance", False),
#                     "legal_importance": self._assess_legal_importance(chunk, chunk_indicators)
#                 }
                
#                 enhanced_chunks.append(enhanced_chunk)
                
#             except Exception as e:
#                 logger.warning(f"Error processing chunk {i}: {str(e)}")
#                 # Add basic chunk without enhancement
#                 enhanced_chunks.append({
#                     "chunk_id": i,
#                     "text": chunk,
#                     "char_count": len(chunk),
#                     "word_count": len(chunk.split()),
#                     "chunk_type": "basic",
#                     "constitutional_relevance": 0.0,
#                     "privacy_relevance": 0.0,
#                     "legal_importance": 0.5
#                 })
        
#         logger.info(f"✅ Created {len(enhanced_chunks)} enhanced chunks")
#         return enhanced_chunks
    
#     def _classify_chunk_type(self, chunk: str, indicators: Dict[str, Any]) -> str:
#         """Classify the type of legal content in chunk"""
        
#         # Check confidence scores
#         const_score = indicators["confidence_scores"].get("constitutional_references", 0)
#         privacy_score = indicators["confidence_scores"].get("privacy_terms", 0)
#         case_score = indicators["confidence_scores"].get("indian_cases", 0)
#         statute_score = indicators["confidence_scores"].get("indian_statutes", 0)
#         gov_score = indicators["confidence_scores"].get("government_terms", 0)
        
#         # Classification logic
#         if const_score > 0.5:
#             return "constitutional_provision"
#         elif privacy_score > 0.3:
#             return "privacy_clause"
#         elif case_score > 0.2:
#             return "case_citation"
#         elif statute_score > 0.3:
#             return "statute_reference"
#         elif gov_score > 0.3:
#             return "government_provision"
#         elif any(word in chunk.lower() for word in ["shall", "hereby", "whereas", "provided"]):
#             return "legal_clause"
#         else:
#             return "general_content"
    
#     def _assess_constitutional_relevance(self, indicators: Dict[str, Any]) -> float:
#         """Assess constitutional relevance score (0-1)"""
#         const_score = indicators["confidence_scores"].get("constitutional_references", 0)
#         case_score = indicators["confidence_scores"].get("indian_cases", 0) * 0.3
#         article_bonus = 0.2 if indicators.get("article_mentions") else 0
        
#         return min(1.0, const_score + case_score + article_bonus)
    
#     def _assess_privacy_relevance(self, indicators: Dict[str, Any]) -> float:
#         """Assess privacy relevance score (0-1)"""
#         privacy_score = indicators["confidence_scores"].get("privacy_terms", 0)
#         dpdpa_bonus = 0.3 if indicators.get("dpdpa_relevance", False) else 0
        
#         return min(1.0, privacy_score + dpdpa_bonus)
    
#     def _assess_legal_importance(self, chunk: str, indicators: Dict[str, Any]) -> float:
#         """Assess overall legal importance of chunk (0-1)"""
#         # Base importance factors
#         const_relevance = self._assess_constitutional_relevance(indicators)
#         privacy_relevance = self._assess_privacy_relevance(indicators)
#         case_relevance = indicators["confidence_scores"].get("indian_cases", 0)
#         legal_language = indicators["confidence_scores"].get("legal_concepts", 0)
        
#         # Weighted combination
#         importance = (
#             const_relevance * 0.3 +
#             privacy_relevance * 0.2 +
#             case_relevance * 0.2 +
#             legal_language * 0.3
#         )
        
#         return min(1.0, max(0.1, importance))  # Ensure minimum importance
    
#     def create_embeddings(self, enhanced_chunks: List[Dict[str, Any]]) -> Optional[List[List[float]]]:
#         """Create embeddings for enhanced chunks with error handling"""
#         if not self.embedding_model:
#             logger.error("❌ Embedding model not available")
#             return None
        
#         try:
#             chunk_texts = [chunk["text"] for chunk in enhanced_chunks]
#             embeddings = self.embedding_model.encode(
#                 chunk_texts, 
#                 convert_to_numpy=True,
#                 show_progress_bar=False
#             )
            
#             logger.info(f"✅ Created embeddings for {len(enhanced_chunks)} chunks")
#             return embeddings.tolist()
            
#         except Exception as e:
#             logger.error(f"❌ Embedding creation failed: {str(e)}")
#             return None
    
#     def select_analysis_frameworks(self, doc_type: str, confidence: float) -> List[str]:
#         """Select appropriate analysis frameworks based on document classification"""
        
#         frameworks = []
        
#         # Government documents
#         if doc_type in ["government_notification", "office_memorandum", "recruitment_rules"]:
#             frameworks.extend(["constitutional_analysis", "administrative_law"])
        
#         # Privacy-related documents  
#         elif doc_type in ["privacy_policy", "dpdpa_compliance_document"]:
#             frameworks.extend(["privacy_rights_analysis", "dpdpa_compliance"])
        
#         # Constitutional documents
#         elif doc_type in ["constitutional_document", "supreme_court_judgment"]:
#             frameworks.extend(["constitutional_analysis", "case_law_analysis"])
        
#         # Contracts
#         elif doc_type in ["employment_contract", "service_agreement"]:
#             frameworks.extend(["contract_law_analysis", "labor_law"])
        
#         # Default for unknown/low confidence
#         if confidence < 0.5 or doc_type == "unknown":
#             frameworks.append("general_legal_analysis")
        
#         return frameworks
    
#     def process_document_complete(self, pdf_file: BytesIO) -> Dict[str, Any]:
#         """Complete document processing pipeline with advanced classification"""
#         logger.info("🚀 Starting comprehensive document processing...")
        
#         try:
#             # Step 1: Extract text and metadata
#             extraction_result = self.extract_text_from_pdf(pdf_file)
            
#             if not extraction_result["full_text"]:
#                 logger.error("❌ No text extracted from document")
#                 return {
#                     "success": False,
#                     "error": "No text could be extracted from the document",
#                     "metadata": extraction_result.get("metadata", {})
#                 }
            
#             # Step 2: Create enhanced chunks
#             enhanced_chunks = self.chunk_text_indian_legal(
#                 extraction_result["full_text"]
#             )
            
#             # Step 3: Generate embeddings
#             embeddings = self.create_embeddings(enhanced_chunks)
            
#             # Step 4: Select analysis frameworks based on classification
#             analysis_frameworks = self.select_analysis_frameworks(
#                 extraction_result["document_classification"]["primary_type"],
#                 extraction_result["document_classification"]["confidence"]
#             )
            
#             # Step 5: Compile complete analysis
#             complete_analysis = {
#                 "success": True,
#                 "metadata": extraction_result["metadata"],
#                 "document_classification": extraction_result["document_classification"],
#                 "indian_legal_indicators": extraction_result["indian_legal_indicators"],
#                 "enhanced_chunks": enhanced_chunks,
#                 "embeddings": embeddings,
#                 "analysis_frameworks": analysis_frameworks,
#                 "processing_stats": {
#                     "total_pages": len(extraction_result["page_texts"]),
#                     "total_chunks": len(enhanced_chunks),
#                     "has_embeddings": embeddings is not None,
#                     "processing_timestamp": datetime.now().isoformat(),
#                     "constitutional_articles_mentioned": extraction_result["indian_legal_indicators"].get("article_mentions", []),
#                     "dpdpa_relevant": extraction_result["indian_legal_indicators"].get("dpdpa_relevance", False),
#                     "constitutional_relevant": extraction_result["indian_legal_indicators"].get("constitutional_relevance", False),
#                     "selected_frameworks": analysis_frameworks
#                 }
#             }
            
#             logger.info("✅ Document processing completed successfully")
#             return complete_analysis
            
#         except Exception as e:
#             logger.error(f"❌ Document processing failed: {str(e)}")
#             return {
#                 "success": False,
#                 "error": str(e),
#                 "metadata": {"processing_failed": True}
#             }

# # Usage Example:
# # processor = IndianLegalDocumentProcessor()
# # with open("legal_document.pdf", "rb") as f:
# #     result = processor.process_document_complete(BytesIO(f.read()))
# #     print(f"Document type: {result['document_classification']['primary_type']}")
# #     print(f"Confidence: {result['document_classification']['confidence']:.1%}")
# #     print(f"Confidence Level: {result['document_classification']['confidence_level']}")
# #     print(f"Analysis Frameworks: {result['analysis_frameworks']}")
# #     print(f"Constitutional articles mentioned: {result['processing_stats']['constitutional_articles_mentioned']}")
"""
Complete Enhanced Indian Legal Document Processor
Ready for Integration with Indian Legal KAG System
Updated with Advanced Document Classifier Integration + OCR Fallback
"""

import logging
import fitz  # PyMuPDF
import re
import os
from io import BytesIO
from typing import List, Dict, Any, Optional, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from .document_classifier import AdvancedDocumentClassifier
import streamlit as st
from datetime import datetime

# OCR imports with error handling
try:
    import easyocr
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

logger = logging.getLogger(__name__)


class IndianLegalDocumentProcessor:
    """Enhanced document processor specifically for Indian legal documents with OCR fallback"""
    
    def __init__(self):
        self.embedding_model = self._load_embedding_model()
        self.indian_legal_patterns = self._initialize_indian_legal_patterns()
        # ✅ Advanced Document Classifier Integration
        self.document_classifier = AdvancedDocumentClassifier()
        # ✅ OCR Integration
        self.ocr_reader = self._initialize_ocr()
        
    def _initialize_ocr(self):
        """Initialize OCR reader with error handling"""
        if OCR_AVAILABLE:
            try:
                # Initialize for English and Hindi (common in Indian legal docs)
                ocr_reader = easyocr.Reader(['en', 'hi'])
                logger.info("✅ OCR reader initialized successfully")
                return ocr_reader
            except Exception as e:
                logger.warning(f"⚠️ OCR initialization failed: {e}")
                return None
        else:
            logger.warning("⚠️ EasyOCR not available. Install with: pip install easyocr")
            return None
        
    @staticmethod
    @st.cache_resource
    def _load_embedding_model():
        """Load sentence transformer model with caching"""
        try:
            return SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            logger.error(f"Failed to load embedding model: {str(e)}")
            return None
    
    def _initialize_indian_legal_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for Indian legal document recognition"""
        return {
            "constitutional_references": [
                r"Article\s+(\d+)(?:\s*(?:\([a-z]\)|\([0-9]+\)))?",
                r"Constitution\s+of\s+India",
                r"Fundamental\s+Rights?",
                r"Directive\s+Principles?",
                r"Part\s+III|Part\s+IV",
                r"Schedule\s+[IVX]+",
                r"Preamble"
            ],
            "indian_cases": [
                r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+v\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
                r"AIR\s+\d{4}\s+SC\s+\d+",
                r"(\d{4})\s+\d+\s+SCC\s+\d+",
                r"Supreme\s+Court",
                r"High\s+Court",
                r"Puttaswamy",
                r"Kesavananda\s+Bharati",
                r"Maneka\s+Gandhi"
            ],
            "indian_statutes": [
                r"Indian\s+Penal\s+Code",
                r"Code\s+of\s+Criminal\s+Procedure",
                r"Indian\s+Evidence\s+Act",
                r"Companies\s+Act\s+\d{4}",
                r"Information\s+Technology\s+Act",
                r"DPDPA\s+2023",
                r"Digital\s+Personal\s+Data\s+Protection\s+Act",
                r"Indian\s+Contract\s+Act",
                r"Labour\s+Laws?"
            ],
            "privacy_terms": [
                r"personal\s+data",
                r"data\s+protection",
                r"privacy\s+policy",
                r"data\s+subject",
                r"data\s+fiduciary",
                r"consent",
                r"processing\s+of\s+data",
                r"right\s+to\s+privacy",
                r"informational\s+privacy",
                r"territorial\s+privacy"
            ],
            "government_terms": [
                r"Government\s+of\s+India",
                r"Ministry\s+of",
                r"Department\s+of",
                r"Notification",
                r"Office\s+Memorandum",
                r"Gazette\s+of\s+India",
                r"Central\s+Government",
                r"State\s+Government"
            ],
            "legal_concepts": [
                r"whereas",
                r"hereby",
                r"provided\s+that",
                r"notwithstanding",
                r"subject\s+to",
                r"in\s+exercise\s+of",
                r"powers\s+conferred",
                r"shall\s+be\s+deemed"
            ]
        }
    
    def _validate_pdf(self, pdf_bytes: bytes) -> Tuple[bool, Dict[str, Any]]:
        """Validate PDF file before processing"""
        validation_info = {
            "is_valid": False,
            "file_size": len(pdf_bytes),
            "has_text": False,
            "is_encrypted": False,
            "needs_password": False,
            "page_count": 0,
            "validation_errors": []
        }
        
        try:
            # Check PDF header
            if not pdf_bytes.startswith(b'%PDF-'):
                validation_info["validation_errors"].append("Invalid PDF header")
                return False, validation_info
            
            # Try to open with PyMuPDF
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            
            validation_info["page_count"] = len(doc)
            validation_info["is_encrypted"] = doc.is_encrypted
            validation_info["needs_password"] = doc.needs_pass
            
            if validation_info["needs_password"]:
                validation_info["validation_errors"].append("PDF requires password")
                doc.close()
                return False, validation_info
            
            # Check if any page has text
            text_found = False
            for page_num in range(min(3, len(doc))):  # Check first 3 pages
                page = doc.load_page(page_num)
                if page.get_text().strip():
                    text_found = True
                    break
            
            validation_info["has_text"] = text_found
            validation_info["is_valid"] = True
            
            doc.close()
            logger.info(f"✅ PDF validation: {validation_info['page_count']} pages, text: {text_found}")
            
            return True, validation_info
            
        except Exception as e:
            validation_info["validation_errors"].append(f"PDF validation error: {str(e)}")
            logger.error(f"❌ PDF validation failed: {e}")
            return False, validation_info
    
    def _extract_text_with_ocr(self, pdf_bytes: bytes) -> str:
        """Extract text using OCR as fallback method"""
        if not self.ocr_reader:
            logger.error("❌ OCR reader not available")
            return ""
        
        try:
            logger.info("🔍 Starting OCR text extraction...")
            
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            extracted_text_parts = []
            
            for page_num in range(len(doc)):
                try:
                    page = doc.load_page(page_num)
                    # Higher resolution for better OCR
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img_data = pix.tobytes("png")
                    
                    # OCR the image
                    results = self.ocr_reader.readtext(img_data)
                    page_text = " ".join([result[1] for result in results if result[2] > 0.5])  # Confidence filter
                    
                    if page_text.strip():
                        extracted_text_parts.append(f"\n--- Page {page_num + 1} (OCR) ---\n{page_text}")
                        
                except Exception as e:
                    logger.warning(f"OCR failed for page {page_num + 1}: {e}")
                    continue
            
            doc.close()
            extracted_text = "\n".join(extracted_text_parts)
            
            logger.info(f"✅ OCR extracted {len(extracted_text)} characters from {len(extracted_text_parts)} pages")
            return extracted_text
            
        except Exception as e:
            logger.error(f"❌ OCR extraction failed: {e}")
            return ""
    
    def _extract_text_primary(self, pdf_bytes: bytes) -> str:
        """Primary text extraction method using PyMuPDF"""
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            full_text_parts = []
            
            for page_num in range(len(doc)):
                try:
                    page = doc.load_page(page_num)
                    page_text = page.get_text()
                    
                    if page_text.strip():
                        full_text_parts.append(page_text)
                        
                except Exception as e:
                    logger.warning(f"Error extracting page {page_num + 1}: {e}")
                    continue
            
            doc.close()
            extracted_text = "\n".join(full_text_parts)
            
            logger.info(f"✅ Primary extraction: {len(extracted_text)} characters from {len(full_text_parts)} pages")
            return extracted_text
            
        except Exception as e:
            logger.error(f"❌ Primary extraction failed: {e}")
            return ""
    
    def _extract_text_alternative(self, pdf_bytes: bytes) -> str:
        """Alternative extraction using different methods"""
        try:
            # Try with different text extraction parameters
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            full_text_parts = []
            
            for page_num in range(len(doc)):
                try:
                    page = doc.load_page(page_num)
                    
                    # Try multiple extraction methods
                    methods = [
                        lambda p: p.get_text("text"),
                        lambda p: p.get_text("dict"),
                        lambda p: p.get_text("rawdict")
                    ]
                    
                    page_text = ""
                    for method in methods:
                        try:
                            result = method(page)
                            if isinstance(result, str):
                                page_text = result
                            elif isinstance(result, dict):
                                # Extract text from dict structure
                                blocks = result.get("blocks", [])
                                text_parts = []
                                for block in blocks:
                                    if "lines" in block:
                                        for line in block["lines"]:
                                            if "spans" in line:
                                                for span in line["spans"]:
                                                    if "text" in span:
                                                        text_parts.append(span["text"])
                                page_text = " ".join(text_parts)
                            
                            if page_text.strip():
                                break
                                
                        except Exception as e:
                            logger.debug(f"Alternative method failed: {e}")
                            continue
                    
                    if page_text.strip():
                        full_text_parts.append(page_text)
                        
                except Exception as e:
                    logger.warning(f"Alternative extraction failed for page {page_num + 1}: {e}")
                    continue
            
            doc.close()
            extracted_text = "\n".join(full_text_parts)
            
            logger.info(f"✅ Alternative extraction: {len(extracted_text)} characters")
            return extracted_text
            
        except Exception as e:
            logger.error(f"❌ Alternative extraction failed: {e}")
            return ""

    def extract_text_from_pdf(self, pdf_file: BytesIO) -> Dict[str, Any]:
        """Enhanced PDF text extraction with multiple fallback methods"""
        try:
            # Read PDF bytes
            pdf_bytes = pdf_file.read()
            
            # Initialize result structure
            extraction_result = {
                "full_text": "",
                "page_texts": [],
                "metadata": {
                    "total_pages": 0,
                    "extraction_timestamp": datetime.now().isoformat(),
                    "document_type": "unknown",
                    "language": "english",
                    "legal_jurisdiction": "india",
                    "extraction_method": "unknown",
                    "extraction_success": False
                },
                "indian_legal_indicators": {},
                "document_classification": {}
            }
            
            # Step 1: Validate PDF
            is_valid, validation_info = self._validate_pdf(pdf_bytes)
            extraction_result["metadata"]["validation_info"] = validation_info
            
            if not is_valid:
                logger.error(f"❌ PDF validation failed: {validation_info['validation_errors']}")
                extraction_result["metadata"]["error"] = "PDF validation failed"
                return extraction_result
            
            # Step 2: Try multiple extraction methods in order
            extraction_methods = [
                ("primary_pymupdf", self._extract_text_primary),
                ("alternative_pymupdf", self._extract_text_alternative),
                ("ocr_fallback", self._extract_text_with_ocr)
            ]
            
            extracted_text = ""
            successful_method = "none"
            
            for method_name, method_func in extraction_methods:
                try:
                    logger.info(f"🔍 Trying {method_name} extraction...")
                    
                    if method_name == "ocr_fallback" and not self.ocr_reader:
                        logger.info("⚠️ Skipping OCR - not available")
                        continue
                    
                    extracted_text = method_func(pdf_bytes)
                    
                    if extracted_text and len(extracted_text.strip()) > 50:  # Minimum text threshold
                        successful_method = method_name
                        logger.info(f"✅ Successful extraction with {method_name}")
                        break
                    else:
                        logger.info(f"⚠️ {method_name} extracted insufficient text ({len(extracted_text)} chars)")
                        
                except Exception as e:
                    logger.warning(f"⚠️ {method_name} failed: {e}")
                    continue
            
            # Check if any method succeeded
            if not extracted_text or len(extracted_text.strip()) < 10:
                logger.error("❌ All extraction methods failed or returned insufficient text")
                extraction_result["metadata"]["error"] = "No text could be extracted using any method"
                return extraction_result
            
            # Step 3: Process successful extraction
            extraction_result["full_text"] = extracted_text
            extraction_result["metadata"]["extraction_method"] = successful_method
            extraction_result["metadata"]["extraction_success"] = True
            extraction_result["metadata"]["total_pages"] = validation_info["page_count"]
            
            # Create page texts (simplified for successful extraction)
            words = extracted_text.split()
            avg_words_per_page = max(1, len(words) // max(1, validation_info["page_count"]))
            
            for page_num in range(validation_info["page_count"]):
                start_idx = page_num * avg_words_per_page
                end_idx = min((page_num + 1) * avg_words_per_page, len(words))
                page_text = " ".join(words[start_idx:end_idx])
                
                extraction_result["page_texts"].append({
                    "page_number": page_num + 1,
                    "text": page_text,
                    "char_count": len(page_text),
                    "word_count": len(page_text.split()),
                    "extraction_method": successful_method
                })
            
            # Step 4: Analyze for Indian legal indicators
            extraction_result["indian_legal_indicators"] = self._analyze_indian_legal_indicators(
                extraction_result["full_text"]
            )
            
            # Step 5: Document classification
            extraction_result["document_classification"] = self._classify_document_with_advanced_classifier(
                extraction_result["full_text"]
            )
            
            extraction_result["metadata"]["document_type"] = extraction_result["document_classification"]["primary_type"]
            
            logger.info(f"✅ Successfully extracted {len(extracted_text)} characters using {successful_method}")
            return extraction_result
            
        except Exception as e:
            logger.error(f"❌ PDF extraction completely failed: {str(e)}")
            return {
                "full_text": "",
                "page_texts": [],
                "metadata": {
                    "error": str(e),
                    "extraction_success": False,
                    "extraction_timestamp": datetime.now().isoformat()
                },
                "indian_legal_indicators": {},
                "document_classification": {"primary_type": "unknown", "confidence": 0.0}
            }
    
    def _classify_document_with_advanced_classifier(self, text: str) -> Dict[str, Any]:
        """Use Advanced Document Classifier for document classification"""
        try:
            # ✅ USE THE ADVANCED CLASSIFIER
            doc_type, confidence, all_scores = self.document_classifier.classify_with_confidence(text)
            
            # Get additional analysis
            comprehensive_analysis = self.document_classifier.analyze_document_comprehensive(text)
            
            return {
                "primary_type": doc_type,
                "confidence": confidence,
                "confidence_level": self.document_classifier.get_classification_confidence_level(confidence),
                "all_scores": all_scores,
                "alternative_classifications": comprehensive_analysis["alternative_classifications"],
                "indian_legal_context": comprehensive_analysis["indian_legal_context"],
                "document_characteristics": comprehensive_analysis["document_characteristics"],
                "classification_reasoning": comprehensive_analysis["classification_reasoning"],
                "recommendations": comprehensive_analysis["recommendations"],
                "classification_method": "advanced_ml",
                "classification_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Advanced classification failed: {str(e)}")
            # Fallback to basic classification
            return {
                "primary_type": "unknown",
                "confidence": 0.0,
                "confidence_level": "very_low",
                "all_scores": {},
                "classification_method": "fallback",
                "error": str(e)
            }
    
    def _analyze_indian_legal_indicators(self, text: str) -> Dict[str, Any]:
        """Comprehensive analysis of Indian legal system indicators"""
        indicators = {
            "constitutional_references": [],
            "indian_cases": [],
            "indian_statutes": [],
            "privacy_terms": [],
            "government_terms": [],
            "legal_concepts": [],
            "confidence_scores": {},
            "article_mentions": [],
            "dpdpa_relevance": False,
            "constitutional_relevance": False
        }
        
        text_lower = text.lower()
        
        # Analyze each pattern category
        for category, patterns in self.indian_legal_patterns.items():
            found_matches = []
            
            for pattern in patterns:
                try:
                    matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
                    if matches:
                        if isinstance(matches[0], tuple):
                            # Handle tuple matches (like case names)
                            found_matches.extend([" v ".join(match) for match in matches])
                        else:
                            found_matches.extend(matches)
                except Exception as e:
                    logger.warning(f"Pattern matching error for {pattern}: {str(e)}")
                    continue
            
            # Remove duplicates and store
            indicators[category] = list(set(found_matches))
            
            # Calculate confidence score (normalized by text length)
            text_words = len(text_lower.split())
            indicators["confidence_scores"][category] = len(found_matches) / max(1, text_words / 100)
        
        # Special analysis for constitutional articles
        article_pattern = r"Article\s+(\d+)"
        article_matches = re.findall(article_pattern, text, re.IGNORECASE)
        indicators["article_mentions"] = [int(num) for num in set(article_matches) if num.isdigit()]
        
        # Assess DPDPA relevance
        indicators["dpdpa_relevance"] = (
            indicators["confidence_scores"].get("privacy_terms", 0) > 0.1 or
            any("dpdpa" in term.lower() for term in indicators.get("indian_statutes", []))
        )
        
        # Assess constitutional relevance
        indicators["constitutional_relevance"] = (
            indicators["confidence_scores"].get("constitutional_references", 0) > 0.1 or
            len(indicators["article_mentions"]) > 0
        )
        
        return indicators
    
    def chunk_text_indian_legal(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Dict[str, Any]]:
        """Advanced text chunking with Indian legal context preservation"""
        
        # Legal-aware separators
        legal_separators = [
            "\n\n\n",      # Major section breaks
            "\n\n",        # Paragraph breaks
            ".\n",         # Sentence with newline
            ". ",          # Regular sentence end
            ";\n",         # Legal clause separator
            "; ",          # Clause separator
            ":\n",         # Colon with newline
            "\n",          # Line break
            " "            # Word break
        ]
        
        try:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=legal_separators,
                length_function=len
            )
            
            text_chunks = splitter.split_text(text)
            
        except Exception as e:
            logger.error(f"Text splitting failed: {str(e)}")
            # Fallback to simple splitting
            words = text.split()
            text_chunks = []
            for i in range(0, len(words), chunk_size // 10):  # Rough word-based chunking
                chunk = " ".join(words[i:i + chunk_size // 10])
                text_chunks.append(chunk)
        
        # Enhance chunks with legal context
        enhanced_chunks = []
        for i, chunk in enumerate(text_chunks):
            try:
                chunk_indicators = self._analyze_indian_legal_indicators(chunk)
                
                enhanced_chunk = {
                    "chunk_id": i,
                    "text": chunk,
                    "char_count": len(chunk),
                    "word_count": len(chunk.split()),
                    "indian_legal_indicators": chunk_indicators,
                    "chunk_type": self._classify_chunk_type(chunk, chunk_indicators),
                    "constitutional_relevance": self._assess_constitutional_relevance(chunk_indicators),
                    "privacy_relevance": self._assess_privacy_relevance(chunk_indicators),
                    "dpdpa_relevance": chunk_indicators.get("dpdpa_relevance", False),
                    "legal_importance": self._assess_legal_importance(chunk, chunk_indicators)
                }
                
                enhanced_chunks.append(enhanced_chunk)
                
            except Exception as e:
                logger.warning(f"Error processing chunk {i}: {str(e)}")
                # Add basic chunk without enhancement
                enhanced_chunks.append({
                    "chunk_id": i,
                    "text": chunk,
                    "char_count": len(chunk),
                    "word_count": len(chunk.split()),
                    "chunk_type": "basic",
                    "constitutional_relevance": 0.0,
                    "privacy_relevance": 0.0,
                    "legal_importance": 0.5
                })
        
        logger.info(f"✅ Created {len(enhanced_chunks)} enhanced chunks")
        return enhanced_chunks
    
    def _classify_chunk_type(self, chunk: str, indicators: Dict[str, Any]) -> str:
        """Classify the type of legal content in chunk"""
        
        # Check confidence scores
        const_score = indicators["confidence_scores"].get("constitutional_references", 0)
        privacy_score = indicators["confidence_scores"].get("privacy_terms", 0)
        case_score = indicators["confidence_scores"].get("indian_cases", 0)
        statute_score = indicators["confidence_scores"].get("indian_statutes", 0)
        gov_score = indicators["confidence_scores"].get("government_terms", 0)
        
        # Classification logic
        if const_score > 0.5:
            return "constitutional_provision"
        elif privacy_score > 0.3:
            return "privacy_clause"
        elif case_score > 0.2:
            return "case_citation"
        elif statute_score > 0.3:
            return "statute_reference"
        elif gov_score > 0.3:
            return "government_provision"
        elif any(word in chunk.lower() for word in ["shall", "hereby", "whereas", "provided"]):
            return "legal_clause"
        else:
            return "general_content"
    
    def _assess_constitutional_relevance(self, indicators: Dict[str, Any]) -> float:
        """Assess constitutional relevance score (0-1)"""
        const_score = indicators["confidence_scores"].get("constitutional_references", 0)
        case_score = indicators["confidence_scores"].get("indian_cases", 0) * 0.3
        article_bonus = 0.2 if indicators.get("article_mentions") else 0
        
        return min(1.0, const_score + case_score + article_bonus)
    
    def _assess_privacy_relevance(self, indicators: Dict[str, Any]) -> float:
        """Assess privacy relevance score (0-1)"""
        privacy_score = indicators["confidence_scores"].get("privacy_terms", 0)
        dpdpa_bonus = 0.3 if indicators.get("dpdpa_relevance", False) else 0
        
        return min(1.0, privacy_score + dpdpa_bonus)
    
    def _assess_legal_importance(self, chunk: str, indicators: Dict[str, Any]) -> float:
        """Assess overall legal importance of chunk (0-1)"""
        # Base importance factors
        const_relevance = self._assess_constitutional_relevance(indicators)
        privacy_relevance = self._assess_privacy_relevance(indicators)
        case_relevance = indicators["confidence_scores"].get("indian_cases", 0)
        legal_language = indicators["confidence_scores"].get("legal_concepts", 0)
        
        # Weighted combination
        importance = (
            const_relevance * 0.3 +
            privacy_relevance * 0.2 +
            case_relevance * 0.2 +
            legal_language * 0.3
        )
        
        return min(1.0, max(0.1, importance))  # Ensure minimum importance
    
    def create_embeddings(self, enhanced_chunks: List[Dict[str, Any]]) -> Optional[List[List[float]]]:
        """Create embeddings for enhanced chunks with error handling"""
        if not self.embedding_model:
            logger.error("❌ Embedding model not available")
            return None
        
        try:
            chunk_texts = [chunk["text"] for chunk in enhanced_chunks]
            embeddings = self.embedding_model.encode(
                chunk_texts, 
                convert_to_numpy=True,
                show_progress_bar=False
            )
            
            logger.info(f"✅ Created embeddings for {len(enhanced_chunks)} chunks")
            return embeddings.tolist()
            
        except Exception as e:
            logger.error(f"❌ Embedding creation failed: {str(e)}")
            return None
    
    def select_analysis_frameworks(self, doc_type: str, confidence: float) -> List[str]:
        """Select appropriate analysis frameworks based on document classification"""
        
        frameworks = []
        
        # Government documents
        if doc_type in ["government_notification", "office_memorandum", "recruitment_rules"]:
            frameworks.extend(["constitutional_analysis", "administrative_law"])
        
        # Privacy-related documents  
        elif doc_type in ["privacy_policy", "dpdpa_compliance_document"]:
            frameworks.extend(["privacy_rights_analysis", "dpdpa_compliance"])
        
        # Constitutional documents
        elif doc_type in ["constitutional_document", "supreme_court_judgment"]:
            frameworks.extend(["constitutional_analysis", "case_law_analysis"])
        
        # Contracts
        elif doc_type in ["employment_contract", "service_agreement"]:
            frameworks.extend(["contract_law_analysis", "labor_law"])
        
        # Default for unknown/low confidence
        if confidence < 0.5 or doc_type == "unknown":
            frameworks.append("general_legal_analysis")
        
        return frameworks
    
    def process_document_complete(self, pdf_file: BytesIO) -> Dict[str, Any]:
        """Complete document processing pipeline with advanced classification"""
        logger.info("🚀 Starting comprehensive document processing...")
        
        try:
            # Step 1: Extract text and metadata with multiple fallback methods
            extraction_result = self.extract_text_from_pdf(pdf_file)
            
            if not extraction_result["metadata"]["extraction_success"]:
                logger.error("❌ No text extracted from document")
                return {
                    "success": False,
                    "error": extraction_result["metadata"].get("error", "Text extraction failed"),
                    "metadata": extraction_result["metadata"],
                    "extraction_details": {
                        "validation_info": extraction_result["metadata"].get("validation_info", {}),
                        "attempted_methods": ["primary_pymupdf", "alternative_pymupdf", "ocr_fallback"],
                        "ocr_available": OCR_AVAILABLE
                    }
                }
            
            # Step 2: Create enhanced chunks
            enhanced_chunks = self.chunk_text_indian_legal(
                extraction_result["full_text"]
            )
            
            # Step 3: Generate embeddings
            embeddings = self.create_embeddings(enhanced_chunks)
            
            # Step 4: Select analysis frameworks based on classification
            analysis_frameworks = self.select_analysis_frameworks(
                extraction_result["document_classification"]["primary_type"],
                extraction_result["document_classification"]["confidence"]
            )
            
            # Step 5: Compile complete analysis
            complete_analysis = {
                "success": True,
                "metadata": extraction_result["metadata"],
                "document_classification": extraction_result["document_classification"],
                "indian_legal_indicators": extraction_result["indian_legal_indicators"],
                "enhanced_chunks": enhanced_chunks,
                "embeddings": embeddings,
                "analysis_frameworks": analysis_frameworks,
                "processing_stats": {
                    "total_pages": len(extraction_result["page_texts"]),
                    "total_chunks": len(enhanced_chunks),
                    "has_embeddings": embeddings is not None,
                    "processing_timestamp": datetime.now().isoformat(),
                    "constitutional_articles_mentioned": extraction_result["indian_legal_indicators"].get("article_mentions", []),
                    "dpdpa_relevant": extraction_result["indian_legal_indicators"].get("dpdpa_relevance", False),
                    "constitutional_relevant": extraction_result["indian_legal_indicators"].get("constitutional_relevance", False),
                    "selected_frameworks": analysis_frameworks,
                    "extraction_method": extraction_result["metadata"]["extraction_method"],
                    "text_length": len(extraction_result["full_text"])
                }
            }
            
            logger.info("✅ Document processing completed successfully")
            return complete_analysis
            
        except Exception as e:
            logger.error(f"❌ Document processing failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "metadata": {"processing_failed": True},
                "ocr_available": OCR_AVAILABLE,
                "recommendations": [
                    "Check if document is password-protected",
                    "Verify PDF is not corrupted",
                    "Install OCR dependencies: pip install easyocr",
                    "Try with a different PDF file"
                ]
            }


# Installation requirements (add to your requirements.txt):
"""
easyocr>=1.7.0
Pillow>=9.0.0
PyMuPDF>=1.23.0
sentence-transformers>=2.0.0
langchain>=0.1.0
streamlit>=1.28.0
"""

# Usage Example:
if __name__ == "__main__":
    processor = IndianLegalDocumentProcessor()
    
    # Test with a sample PDF file
    try:
        with open("test_legal_document.pdf", "rb") as f:
            result = processor.process_document_complete(BytesIO(f.read()))
            
        if result["success"]:
            print(f"✅ Document processed successfully!")
            print(f"Document type: {result['document_classification']['primary_type']}")
            print(f"Confidence: {result['document_classification']['confidence']:.1%}")
            print(f"Extraction method: {result['processing_stats']['extraction_method']}")
            print(f"Text length: {result['processing_stats']['text_length']} characters")
            print(f"Analysis frameworks: {result['analysis_frameworks']}")
        else:
            print(f"❌ Processing failed: {result['error']}")
            if "recommendations" in result:
                print("Recommendations:")
                for rec in result["recommendations"]:
                    print(f"  • {rec}")
                    
    except FileNotFoundError:
        print("❌ Test file 'test_legal_document.pdf' not found")
    except Exception as e:
        print(f"❌ Test failed: {e}")
