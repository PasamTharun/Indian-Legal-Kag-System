"""
Indian Legal System Utilities and Constants
Enhanced utility functions for Constitutional Law, Privacy Rights, and DPDPA Compliance
"""
import logging
import re
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
import streamlit as st
from dotenv import load_dotenv
import os
import json
import hashlib
from pathlib import Path

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Updated constants for Indian Legal KAG System
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
LLM_MODEL_NAME = "llama-3.3-70b-versatile"  # Groq model
CHUNK_SIZE = 1200  # Increased for legal documents
CHUNK_OVERLAP = 300  # Increased overlap for legal context
TOP_K = 5  # Increased for better constitutional reasoning

# Indian Legal System Constants
CONSTITUTIONAL_PARTS = {
    "part_1": {"title": "The Union and its Territory", "articles": "1-4"},
    "part_2": {"title": "Citizenship", "articles": "5-11"},
    "part_3": {"title": "Fundamental Rights", "articles": "12-35"},
    "part_4": {"title": "Directive Principles of State Policy", "articles": "36-51"},
    "part_4a": {"title": "Fundamental Duties", "articles": "51A"},
    "part_5": {"title": "The Union", "articles": "52-151"},
    "part_6": {"title": "The States", "articles": "152-237"},
    "part_7": {"title": "The States in the B part of the First Schedule (Repealed)", "articles": "238"},
    "part_8": {"title": "The Union Territories", "articles": "239-242"},
    "part_9": {"title": "The Panchayats", "articles": "243-243O"},
    "part_9a": {"title": "The Municipalities", "articles": "243P-243ZG"},
    "part_9b": {"title": "The Co-operative Societies", "articles": "243ZH-243ZT"},
    "part_10": {"title": "The Scheduled and Tribal Areas", "articles": "244"},
    "part_11": {"title": "Relations between the Union and the States", "articles": "245-263"},
    "part_12": {"title": "Finance, Property, Contracts and Suits", "articles": "264-300A"},
    "part_13": {"title": "Trade, Commerce and Intercourse within the territory of India", "articles": "301-307"},
    "part_14": {"title": "Services Under the Union and the States", "articles": "308-323"},
    "part_14a": {"title": "Tribunals", "articles": "323A-323B"},
    "part_15": {"title": "Elections", "articles": "324-329A"},
    "part_16": {"title": "Special Provisions Relating to certain Classes", "articles": "330-342"},
    "part_17": {"title": "Official Language", "articles": "343-351"},
    "part_18": {"title": "Emergency Provisions", "articles": "352-360"},
    "part_19": {"title": "Miscellaneous", "articles": "361-367"},
    "part_20": {"title": "Amendment of the Constitution", "articles": "368"},
    "part_21": {"title": "Temporary, Transitional and Special Provisions", "articles": "369-392"}
}

# Supreme Court Citation Patterns
SC_CITATION_PATTERNS = [
    r"AIR\s+(\d{4})\s+SC\s+(\d+)",
    r"(\d{4})\s+(\d+)\s+SCC\s+(\d+)",
    r"(\d{4})\s+(\d+)\s+SCR\s+(\d+)",
    r"\[(\d{4})\]\s+(\d+)\s+SCC\s+(\d+)",
    r"(\d{4})\s+SCALE\s+(\d+)",
    r"JT\s+(\d{4})\s+(\d+)\s+SC\s+(\d+)"
]

# High Court Citation Patterns
HC_CITATION_PATTERNS = [
    r"AIR\s+(\d{4})\s+([A-Za-z\s&]+)\s+(\d+)",
    r"(\d{4})\s+(\d+)\s+([A-Za-z\s&]+)HC\s+(\d+)",
    r"ILR\s+(\d{4})\s+([A-Za-z\s&]+)\s+(\d+)"
]

# DPDPA 2023 Section References
DPDPA_SECTIONS = {
    "chapter_1": {
        "title": "Preliminary",
        "sections": ["1", "2"]
    },
    "chapter_2": {
        "title": "Obligations of Data Fiduciary",
        "sections": ["3", "4", "5", "6", "7", "8", "9", "10"]
    },
    "chapter_3": {
        "title": "Rights and Duties of Data Principal",
        "sections": ["11", "12", "13", "14", "15", "16"]
    },
    "chapter_4": {
        "title": "Data Protection Board of India",
        "sections": ["17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33"]
    },
    "chapter_5": {
        "title": "Transfer of Personal Data Outside India",
        "sections": ["34", "35"]
    },
    "chapter_6": {
        "title": "Exemptions",
        "sections": ["36", "37", "38", "39", "40"]
    },
    "chapter_7": {
        "title": "Miscellaneous",
        "sections": ["41", "42", "43", "44", "45"]
    }
}

# Privacy Framework Constants
PRIVACY_FRAMEWORK = {
    "constitutional_source": "Article 21",
    "landmark_case": "Justice K.S. Puttaswamy (Retd.) v. Union of India",
    "citation": "(2017) 10 SCC 1",
    "bench_size": 9,
    "privacy_dimensions": [
        "informational_privacy",
        "bodily_privacy", 
        "communications_privacy",
        "territorial_privacy"
    ],
    "constitutional_tests": [
        "legitimate_state_aim",
        "necessity",
        "proportionality"
    ]
}

# Indian Legal Terminology
INDIAN_LEGAL_TERMS = {
    "constitutional_terms": [
        "fundamental rights", "directive principles", "fundamental duties",
        "basic structure", "constitutional morality", "living constitution",
        "constitutional interpretation", "judicial review", "separation of powers"
    ],
    "privacy_terms": [
        "informational privacy", "bodily privacy", "territorial privacy",
        "communications privacy", "data protection", "personal data",
        "data fiduciary", "data principal", "processing", "consent"
    ],
    "legal_procedure_terms": [
        "writ petition", "public interest litigation", "suo moto",
        "judicial precedent", "ratio decidendi", "obiter dicta",
        "ultra vires", "intra vires", "natural justice", "due process"
    ]
}

def initialize_indian_legal_session_state():
    """Initialize session state for Indian Legal KAG System"""
    
    session_defaults = {
        # Basic session data
        'chat_history': [],
        'document_processed': False,
        'text_chunks': [],
        'embeddings': None,
        'full_text': "",
        
        # KAG-specific data
        'constitutional_analysis': {},
        'privacy_analysis': {},
        'dpdpa_analysis': {},
        'knowledge_graph_stats': {},
        'constitutional_pathways': [],
        
        # Indian legal document data
        'indian_legal_indicators': {},
        'document_classification': "",
        'constitutional_articles_identified': [],
        'supreme_court_cases_referenced': [],
        'high_court_cases_referenced': [],
        'dpdpa_sections_identified': [],
        
        # Analysis results
        'compliance_score': {
            'overall_score': 0,
            'component_scores': {},
            'calculation_timestamp': None
        },
        
        # Report and messaging
        'comprehensive_report': None,
        'email_sent': False,
        'last_email_timestamp': None,
        'report_generation_history': [],
        
        # Neo4j and KAG status
        'neo4j_connected': False,
        'kg_initialized': False,
        'kag_engines_loaded': False,
        'graph_stats': {},
        
        # SMTP configuration status
        'smtp_configured': False,
        'smtp_test_result': None,
        'email_history': [],
        
        # Performance monitoring
        'analysis_performance': {
            'document_processing_time': 0,
            'constitutional_analysis_time': 0,
            'privacy_analysis_time': 0,
            'dpdpa_analysis_time': 0,
            'total_analysis_time': 0
        },
        
        # Error tracking
        'error_log': [],
        'warning_log': []
    }
    
    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def validate_environment_variables() -> Dict[str, bool]:
    """Validate required environment variables for Indian Legal KAG System"""
    
    required_vars = {
        'neo4j': ['NEO4J_URI', 'NEO4J_USER', 'NEO4J_PASSWORD'],
        'groq': ['GROQ_API_KEY'],
        'smtp': ['SMTP_SERVER', 'SENDER_EMAIL', 'SENDER_PASSWORD']
    }
    
    validation_results = {}
    
    for category, vars_list in required_vars.items():
        validation_results[category] = all(os.getenv(var) for var in vars_list)
    
    return validation_results

def get_indian_legal_constants() -> Dict[str, Any]:
    """Get Indian legal system constants"""
    
    return {
        "constitutional_parts": CONSTITUTIONAL_PARTS,
        "privacy_framework": PRIVACY_FRAMEWORK,
        "dpdpa_framework": {
            "act_name": "Digital Personal Data Protection Act 2023",
            "sections": DPDPA_SECTIONS,
            "constitutional_basis": "Article 21",
            "implementation_date": "2023",
            "key_principles": [
                "lawful_processing", "purpose_limitation", "data_minimization",
                "accuracy", "storage_limitation", "integrity_confidentiality"
            ]
        },
        "supreme_court_patterns": SC_CITATION_PATTERNS,
        "high_court_patterns": HC_CITATION_PATTERNS,
        "legal_terms": INDIAN_LEGAL_TERMS
    }

@st.cache_data
def load_indian_legal_stopwords() -> List[str]:
    """Load Indian legal document stopwords"""
    
    legal_stopwords = [
        # Legal procedural terms
        "whereas", "hereby", "herein", "hereof", "hereto", "heretofore",
        "thereafter", "thereby", "therein", "thereof", "thereto", "therefore",
        "notwithstanding", "provided", "however", "nevertheless", "furthermore",
        "moreover", "accordingly", "consequently", "pursuant", "subject",
        
        # Constitutional references
        "article", "section", "clause", "sub-clause", "paragraph", "proviso",
        "constitution", "amendment", "schedule", "part", "chapter",
        
        # Legal conjunctions and connectors
        "wheresoever", "whensoever", "howsoever", "whatsoever", "whosoever",
        "aforesaid", "aforementioned", "abovementioned", "hereinafter",
        "hereinbefore", "hereunder", "hereunto", "herewith",
        
        # Court and legal procedure
        "petitioner", "respondent", "appellant", "defendant", "plaintiff",
        "learned", "counsel", "court", "judge", "justice", "bench",
        
        # Indian legal specific
        "honble", "lordship", "ladyship", "shri", "smt", "kumari"
    ]
    
    return legal_stopwords

def format_constitutional_article_reference(article_number: int) -> str:
    """Format constitutional article reference with proper styling"""
    
    if 1 <= article_number <= 4:
        part = "I (The Union and its Territory)"
    elif 5 <= article_number <= 11:
        part = "II (Citizenship)"
    elif 12 <= article_number <= 35:
        part = "III (Fundamental Rights)"
    elif 36 <= article_number <= 51:
        part = "IV (Directive Principles)"
    elif article_number == 51:  # 51A
        part = "IVA (Fundamental Duties)"
    elif 52 <= article_number <= 151:
        part = "V (The Union)"
    elif 152 <= article_number <= 237:
        part = "VI (The States)"
    elif 239 <= article_number <= 242:
        part = "VIII (Union Territories)"
    elif 245 <= article_number <= 263:
        part = "XI (Relations between Union and States)"
    elif 324 <= article_number <= 329:
        part = "XV (Elections)"
    elif 352 <= article_number <= 360:
        part = "XVIII (Emergency Provisions)"
    elif article_number == 368:
        part = "XX (Amendment of Constitution)"
    else:
        part = "Constitutional Provision"
    
    return f"Article {article_number} - Part {part}"

def parse_legal_citation(citation: str) -> Dict[str, Any]:
    """Parse legal citation and extract components"""
    
    citation_info = {
        "original": citation,
        "type": "unknown",
        "year": None,
        "court": None,
        "volume": None,
        "page": None,
        "journal": None,
        "is_valid": False
    }
    
    # Supreme Court patterns
    for pattern in SC_CITATION_PATTERNS:
        match = re.search(pattern, citation)
        if match:
            citation_info.update({
                "type": "supreme_court",
                "year": int(match.group(1)),
                "court": "Supreme Court of India",
                "is_valid": True
            })
            
            if "SCC" in citation:
                citation_info.update({
                    "journal": "Supreme Court Cases",
                    "volume": int(match.group(2)) if len(match.groups()) > 1 else None,
                    "page": int(match.group(3)) if len(match.groups()) > 2 else None
                })
            elif "AIR" in citation:
                citation_info.update({
                    "journal": "All India Reporter",
                    "page": int(match.group(2)) if len(match.groups()) > 1 else None
                })
            break
    
    # High Court patterns
    if not citation_info["is_valid"]:
        for pattern in HC_CITATION_PATTERNS:
            match = re.search(pattern, citation)
            if match:
                citation_info.update({
                    "type": "high_court",
                    "year": int(match.group(1)),
                    "is_valid": True
                })
                
                if len(match.groups()) > 2:
                    citation_info["court"] = f"{match.group(2).strip()} High Court"
                break
    
    return citation_info

def extract_constitutional_articles(text: str) -> List[Dict[str, Any]]:
    """Extract constitutional article references from text"""
    
    article_patterns = [
        r"Article\s+(\d+)(?:\s*\([a-zA-Z0-9]+\))?",
        r"Art\.?\s+(\d+)(?:\s*\([a-zA-Z0-9]+\))?",
        r"Articles?\s+(\d+)\s*(?:to|and|\&)\s*(\d+)",
        r"Art\.?\s+(\d+)\s*(?:to|and|\&)\s*(\d+)"
    ]
    
    found_articles = []
    
    for pattern in article_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        
        for match in matches:
            if len(match.groups()) == 2 and match.group(2):  # Range of articles
                start_article = int(match.group(1))
                end_article = int(match.group(2))
                
                for article_num in range(start_article, end_article + 1):
                    found_articles.append({
                        "article_number": article_num,
                        "reference_text": match.group(0),
                        "position": match.span(),
                        "formatted_reference": format_constitutional_article_reference(article_num),
                        "is_range": True,
                        "range_start": start_article,
                        "range_end": end_article
                    })
            else:  # Single article
                article_num = int(match.group(1))
                found_articles.append({
                    "article_number": article_num,
                    "reference_text": match.group(0),
                    "position": match.span(),
                    "formatted_reference": format_constitutional_article_reference(article_num),
                    "is_range": False
                })
    
    # Remove duplicates and sort
    unique_articles = {}
    for article in found_articles:
        key = article["article_number"]
        if key not in unique_articles:
            unique_articles[key] = article
    
    return sorted(unique_articles.values(), key=lambda x: x["article_number"])

def extract_case_references(text: str) -> List[Dict[str, Any]]:
    """Extract legal case references from text"""
    
    case_patterns = [
        r"([A-Z][a-zA-Z\s\.&,]+)\s+v\.?\s+([A-Z][a-zA-Z\s\.&,]+)(?:\s+(?:\((\d{4})\)\s+)?(?:(\d+)\s+)?([A-Z]+)\s+(\d+))?",
        r"([A-Z][a-zA-Z\s\.&,]+)\s+vs\.?\s+([A-Z][a-zA-Z\s\.&,]+)(?:\s+(?:\((\d{4})\)\s+)?(?:(\d+)\s+)?([A-Z]+)\s+(\d+))?"
    ]
    
    found_cases = []
    
    for pattern in case_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        
        for match in matches:
            case_info = {
                "petitioner": match.group(1).strip(),
                "respondent": match.group(2).strip(),
                "full_citation": match.group(0),
                "position": match.span()
            }
            
            # Extract citation details if available
            if len(match.groups()) > 2:
                case_info.update({
                    "year": match.group(3) if match.group(3) else None,
                    "volume": match.group(4) if match.group(4) else None,
                    "journal": match.group(5) if match.group(5) else None,
                    "page": match.group(6) if match.group(6) else None
                })
            
            # Parse full citation
            citation_details = parse_legal_citation(case_info["full_citation"])
            case_info["citation_details"] = citation_details
            
            found_cases.append(case_info)
    
    return found_cases

def calculate_constitutional_hierarchy_score(articles: List[int]) -> Dict[str, Any]:
    """Calculate constitutional hierarchy score based on articles involved"""
    
    hierarchy_weights = {
        "fundamental_rights": 1.0,  # Articles 12-35
        "directive_principles": 0.7,  # Articles 36-51
        "fundamental_duties": 0.8,  # Article 51A
        "union_structure": 0.6,  # Articles 52-151
        "state_structure": 0.6,  # Articles 152-237
        "federal_relations": 0.8,  # Articles 245-263
        "emergency_provisions": 0.9,  # Articles 352-360
        "amendment_power": 0.95  # Article 368
    }
    
    category_scores = {
        "fundamental_rights": 0,
        "directive_principles": 0,
        "fundamental_duties": 0,
        "union_structure": 0,
        "state_structure": 0,
        "federal_relations": 0,
        "emergency_provisions": 0,
        "amendment_power": 0
    }
    
    for article in articles:
        if 12 <= article <= 35:
            category_scores["fundamental_rights"] += hierarchy_weights["fundamental_rights"]
        elif 36 <= article <= 51:
            category_scores["directive_principles"] += hierarchy_weights["directive_principles"]
        elif article == 51:  # 51A
            category_scores["fundamental_duties"] += hierarchy_weights["fundamental_duties"]
        elif 52 <= article <= 151:
            category_scores["union_structure"] += hierarchy_weights["union_structure"]
        elif 152 <= article <= 237:
            category_scores["state_structure"] += hierarchy_weights["state_structure"]
        elif 245 <= article <= 263:
            category_scores["federal_relations"] += hierarchy_weights["federal_relations"]
        elif 352 <= article <= 360:
            category_scores["emergency_provisions"] += hierarchy_weights["emergency_provisions"]
        elif article == 368:
            category_scores["amendment_power"] += hierarchy_weights["amendment_power"]
    
    total_score = sum(category_scores.values())
    normalized_scores = {k: (v / total_score if total_score > 0 else 0) for k, v in category_scores.items()}
    
    return {
        "category_scores": category_scores,
        "normalized_scores": normalized_scores,
        "total_score": total_score,
        "hierarchy_assessment": "high" if total_score >= 3.0 else "medium" if total_score >= 1.5 else "low"
    }

def generate_document_hash(text: str) -> str:
    """Generate unique hash for document content"""
    
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]

def log_kag_operation(operation: str, details: Dict[str, Any] = None, level: str = "info"):
    """Enhanced logging for KAG system operations"""
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "operation": operation,
        "system": "Indian Legal KAG",
        "level": level,
        "details": details or {},
        "session_id": st.session_state.get("session_id", "unknown")
    }
    
    # Log to appropriate level
    if level == "error":
        logger.error(f"KAG Operation Error: {operation} - {log_entry}")
    elif level == "warning":
        logger.warning(f"KAG Operation Warning: {operation} - {log_entry}")
    else:
        logger.info(f"KAG Operation: {operation} - {log_entry}")
    
    # Store in session state for monitoring
    if 'kag_operations_log' not in st.session_state:
        st.session_state.kag_operations_log = []
    
    st.session_state.kag_operations_log.append(log_entry)
    
    # Store errors and warnings separately
    if level == "error":
        if 'error_log' not in st.session_state:
            st.session_state.error_log = []
        st.session_state.error_log.append(log_entry)
    elif level == "warning":
        if 'warning_log' not in st.session_state:
            st.session_state.warning_log = []
        st.session_state.warning_log.append(log_entry)
    
    # Keep only last 50 operations
    if len(st.session_state.kag_operations_log) > 50:
        st.session_state.kag_operations_log = st.session_state.kag_operations_log[-50:]

def measure_performance(operation_name: str):
    """Decorator to measure performance of operations"""
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            
            try:
                result = func(*args, **kwargs)
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                log_kag_operation(
                    f"performance_measurement_{operation_name}",
                    {
                        "duration_seconds": duration,
                        "start_time": start_time.isoformat(),
                        "end_time": end_time.isoformat(),
                        "operation": operation_name,
                        "status": "success"
                    }
                )
                
                # Store performance data
                if 'analysis_performance' in st.session_state:
                    st.session_state.analysis_performance[f"{operation_name}_time"] = duration
                
                return result
                
            except Exception as e:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                log_kag_operation(
                    f"performance_measurement_{operation_name}",
                    {
                        "duration_seconds": duration,
                        "start_time": start_time.isoformat(),
                        "end_time": end_time.isoformat(),
                        "operation": operation_name,
                        "status": "error",
                        "error": str(e)
                    },
                    level="error"
                )
                
                raise e
        
        return wrapper
    return decorator

def clean_legal_text(text: str) -> str:
    """Clean and normalize legal text for analysis"""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove page numbers and footer text
    text = re.sub(r'Page\s+\d+\s+of\s+\d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
    
    # Normalize legal citations
    text = re.sub(r'v\.\s+', 'v. ', text)
    text = re.sub(r'vs\.\s+', 'v. ', text)
    
    # Normalize article references
    text = re.sub(r'Art\.\s*', 'Article ', text)
    text = re.sub(r'Sec\.\s*', 'Section ', text)
    
    # Clean up punctuation
    text = re.sub(r'\s+([.,;:])', r'\1', text)
    text = re.sub(r'([.,;:])\s+', r'\1 ', text)
    
    return text.strip()

def validate_legal_document_structure(text: str) -> Dict[str, Any]:
    """Validate structure of legal document"""
    
    validation_results = {
        "is_valid_legal_document": False,
        "document_type": "unknown",
        "validation_score": 0.0,
        "structural_elements": {
            "has_title": False,
            "has_parties": False,
            "has_legal_citations": False,
            "has_constitutional_references": False,
            "has_conclusion": False
        },
        "recommendations": []
    }
    
    # Check for title/heading
    if re.search(r'^[A-Z\s]{10,}$', text[:200], re.MULTILINE):
        validation_results["structural_elements"]["has_title"] = True
        validation_results["validation_score"] += 0.2
    
    # Check for parties (case law pattern)
    if re.search(r'[A-Z][a-zA-Z\s]+\s+v\.?\s+[A-Z][a-zA-Z\s]+', text):
        validation_results["structural_elements"]["has_parties"] = True
        validation_results["validation_score"] += 0.2
        validation_results["document_type"] = "case_law"
    
    # Check for legal citations
    citations = extract_case_references(text)
    if citations:
        validation_results["structural_elements"]["has_legal_citations"] = True
        validation_results["validation_score"] += 0.2
    
    # Check for constitutional references
    articles = extract_constitutional_articles(text)
    if articles:
        validation_results["structural_elements"]["has_constitutional_references"] = True
        validation_results["validation_score"] += 0.2
    
    # Check for conclusion/decision
    conclusion_patterns = [
        r'held\s*:',
        r'conclusion\s*:',
        r'decision\s*:',
        r'order\s*:',
        r'judgment\s*:',
        r'disposed\s+of',
        r'prayer\s+granted'
    ]
    
    for pattern in conclusion_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            validation_results["structural_elements"]["has_conclusion"] = True
            validation_results["validation_score"] += 0.2
            break
    
    # Determine if valid legal document
    validation_results["is_valid_legal_document"] = validation_results["validation_score"] >= 0.6
    
    # Generate recommendations
    if not validation_results["structural_elements"]["has_legal_citations"]:
        validation_results["recommendations"].append("Document may benefit from legal precedent citations")
    
    if not validation_results["structural_elements"]["has_constitutional_references"]:
        validation_results["recommendations"].append("Consider adding constitutional framework references")
    
    return validation_results

def create_analysis_summary(
    constitutional_analysis: Dict[str, Any],
    privacy_analysis: Dict[str, Any],
    dpdpa_analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """Create comprehensive analysis summary"""
    
    summary = {
        "analysis_timestamp": datetime.now().isoformat(),
        "overall_assessment": "unknown",
        "key_findings": [],
        "critical_issues": [],
        "recommendations": [],
        "compliance_overview": {
            "constitutional_compliance": "unknown",
            "privacy_compliance": "unknown",
            "dpdpa_compliance": "unknown"
        },
        "scores": {
            "constitutional_score": 0,
            "privacy_score": 0,
            "dpdpa_score": 0,
            "overall_score": 0
        }
    }
    
    # Extract scores
    if constitutional_analysis:
        const_score = constitutional_analysis.get("compliance_score", {}).get("overall_score", 0)
        summary["scores"]["constitutional_score"] = const_score
        summary["compliance_overview"]["constitutional_compliance"] = (
            "compliant" if const_score >= 80 else
            "partially_compliant" if const_score >= 60 else
            "non_compliant"
        )
    
    if privacy_analysis:
        privacy_score = privacy_analysis.get("privacy_risk_score", {}).get("overall_score", 0)
        summary["scores"]["privacy_score"] = privacy_score
        summary["compliance_overview"]["privacy_compliance"] = (
            privacy_analysis.get("article_21_compliance", "unknown")
        )
    
    if dpdpa_analysis:
        dpdpa_score = dpdpa_analysis.get("dpdpa_compliance_summary", {}).get("overall_score", 0)
        summary["scores"]["dpdpa_score"] = dpdpa_score
        summary["compliance_overview"]["dpdpa_compliance"] = (
            dpdpa_analysis.get("dpdpa_compliance_summary", {}).get("compliance_status", "unknown")
        )
    
    # Calculate overall score
    scores = [v for v in summary["scores"].values() if v > 0]
    summary["scores"]["overall_score"] = sum(scores) / len(scores) if scores else 0
    
    # Determine overall assessment
    overall_score = summary["scores"]["overall_score"]
    if overall_score >= 80:
        summary["overall_assessment"] = "excellent"
    elif overall_score >= 70:
        summary["overall_assessment"] = "good"
    elif overall_score >= 60:
        summary["overall_assessment"] = "satisfactory"
    elif overall_score >= 50:
        summary["overall_assessment"] = "needs_improvement"
    else:
        summary["overall_assessment"] = "poor"
    
    # Generate key findings
    if constitutional_analysis.get("constitutional_articles"):
        article_count = len(constitutional_analysis["constitutional_articles"])
        summary["key_findings"].append(f"Analysis identified {article_count} relevant constitutional articles")
    
    if privacy_analysis.get("privacy_categorization", {}).get("overall_privacy_impact"):
        impact = privacy_analysis["privacy_categorization"]["overall_privacy_impact"]
        summary["key_findings"].append(f"Privacy impact assessment: {impact}")
    
    if dpdpa_analysis.get("section_compliance"):
        compliant_sections = len([
            s for s in dpdpa_analysis["section_compliance"].values()
            if s.get("compliance_status") == "compliant"
        ])
        total_sections = len(dpdpa_analysis["section_compliance"])
        summary["key_findings"].append(f"DPDPA compliance: {compliant_sections}/{total_sections} sections compliant")
    
    return summary

class IndianLegalConfigManager:
    """Enhanced configuration manager for Indian Legal KAG System"""
    
    def __init__(self):
        self.config = self._load_config()
        self.validation_cache = {}
        self.last_validation = None
    
    def _load_config(self) -> Dict[str, Any]:
        """Load comprehensive system configuration"""
        
        return {
            "system": {
                "name": "Indian Legal KAG System",
                "version": "1.0.0",
                "jurisdiction": "India",
                "constitution": "Constitution of India",
                "primary_language": "English",
                "supported_languages": ["English", "Hindi"],
                "legal_framework": "Indian Legal System",
                "data_protection_act": "DPDPA 2023"
            },
            "neo4j": {
                "uri": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
                "user": os.getenv("NEO4J_USER", "neo4j"),
                "password": os.getenv("NEO4J_PASSWORD", ""),
                "database": os.getenv("NEO4J_DATABASE", "neo4j"),
                "connection_timeout": int(os.getenv("NEO4J_CONNECTION_TIMEOUT", "30")),
                "max_connection_lifetime": int(os.getenv("NEO4J_MAX_CONNECTION_LIFETIME", "1800")),
                "max_connection_pool_size": int(os.getenv("NEO4J_MAX_CONNECTION_POOL_SIZE", "50"))
            },
            "groq": {
                "api_key": os.getenv("GROQ_API_KEY", ""),
                "model": os.getenv("GROQ_MODEL", "llama3-70b-8192"),
                "temperature": float(os.getenv("GROQ_TEMPERATURE", "0.1")),
                "max_tokens": int(os.getenv("GROQ_MAX_TOKENS", "4000")),
                "request_timeout": int(os.getenv("GROQ_REQUEST_TIMEOUT", "60")),
                "max_retries": int(os.getenv("GROQ_MAX_RETRIES", "3"))
            },
            "smtp": {
                "server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
                "port": int(os.getenv("SMTP_PORT", "587")),
                "sender_email": os.getenv("SENDER_EMAIL", ""),
                "sender_password": os.getenv("SENDER_PASSWORD", ""),
                "sender_name": os.getenv("SENDER_NAME", "Indian Legal KAG System"),
                "use_tls": os.getenv("USE_TLS", "true").lower() == "true",
                "connection_timeout": int(os.getenv("SMTP_CONNECTION_TIMEOUT", "30"))
            },
            "analysis": {
                "chunk_size": int(os.getenv("CHUNK_SIZE", "1200")),
                "chunk_overlap": int(os.getenv("CHUNK_OVERLAP", "300")),
                "top_k": int(os.getenv("TOP_K", "5")),
                "embedding_model": os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"),
                "max_document_size_mb": int(os.getenv("MAX_DOCUMENT_SIZE_MB", "50")),
                "enable_caching": os.getenv("ENABLE_CACHING", "true").lower() == "true"
            },
            "performance": {
                "max_analysis_time_seconds": int(os.getenv("MAX_ANALYSIS_TIME_SECONDS", "300")),
                "enable_performance_monitoring": os.getenv("ENABLE_PERFORMANCE_MONITORING", "true").lower() == "true",
                "log_level": os.getenv("LOG_LEVEL", "INFO"),
                "enable_debug": os.getenv("ENABLE_DEBUG", "false").lower() == "true"
            },
            "security": {
                "enable_session_encryption": os.getenv("ENABLE_SESSION_ENCRYPTION", "true").lower() == "true",
                "session_timeout_minutes": int(os.getenv("SESSION_TIMEOUT_MINUTES", "60")),
                "max_failed_attempts": int(os.getenv("MAX_FAILED_ATTEMPTS", "3")),
                "enable_audit_log": os.getenv("ENABLE_AUDIT_LOG", "true").lower() == "true"
            }
        }
    
    def get_config(self, section: str = None) -> Any:
        """Get configuration section or entire config"""
        
        if section:
            return self.config.get(section, {})
        
        return self.config
    
    def validate_config(self, force_refresh: bool = False) -> Dict[str, bool]:
        """Enhanced configuration validation with caching"""
        
        # Use cache if available and not forced refresh
        if (not force_refresh and 
            self.last_validation and 
            self.validation_cache and
            (datetime.now() - self.last_validation).total_seconds() < 300):  # 5 minutes cache
            return self.validation_cache
        
        validation_results = {
            "neo4j": bool(
                self.config["neo4j"]["uri"] and 
                self.config["neo4j"]["user"] and 
                self.config["neo4j"]["password"]
            ),
            "groq": bool(self.config["groq"]["api_key"]),
            "smtp": bool(
                self.config["smtp"]["server"] and 
                self.config["smtp"]["sender_email"] and 
                self.config["smtp"]["sender_password"]
            ),
            "analysis": bool(
                self.config["analysis"]["chunk_size"] > 0 and
                self.config["analysis"]["chunk_overlap"] >= 0 and
                self.config["analysis"]["top_k"] > 0
            ),
            "performance": bool(
                self.config["performance"]["max_analysis_time_seconds"] > 0
            ),
            "security": bool(
                self.config["security"]["session_timeout_minutes"] > 0 and
                self.config["security"]["max_failed_attempts"] > 0
            )
        }
        
        validation_results["overall"] = all(validation_results.values())
        
        # Cache results
        self.validation_cache = validation_results
        self.last_validation = datetime.now()
        
        return validation_results
    
    def get_performance_config(self) -> Dict[str, Any]:
        """Get performance-specific configuration"""
        
        return {
            "max_analysis_time": self.config["performance"]["max_analysis_time_seconds"],
            "enable_monitoring": self.config["performance"]["enable_performance_monitoring"],
            "log_level": self.config["performance"]["log_level"],
            "enable_debug": self.config["performance"]["enable_debug"],
            "enable_caching": self.config["analysis"]["enable_caching"]
        }
    
    def get_security_config(self) -> Dict[str, Any]:
        """Get security-specific configuration"""
        
        return {
            "session_encryption": self.config["security"]["enable_session_encryption"],
            "session_timeout": self.config["security"]["session_timeout_minutes"],
            "max_failed_attempts": self.config["security"]["max_failed_attempts"],
            "audit_log": self.config["security"]["enable_audit_log"]
        }

class IndianLegalPerformanceMonitor:
    """Performance monitoring for Indian Legal KAG System"""
    
    def __init__(self):
        self.start_times = {}
        self.performance_data = []
    
    def start_operation(self, operation_name: str):
        """Start monitoring an operation"""
        self.start_times[operation_name] = datetime.now()
    
    def end_operation(self, operation_name: str, additional_data: Dict[str, Any] = None):
        """End monitoring an operation"""
        
        if operation_name not in self.start_times:
            return None
        
        end_time = datetime.now()
        start_time = self.start_times[operation_name]
        duration = (end_time - start_time).total_seconds()
        
        performance_record = {
            "operation": operation_name,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
            "additional_data": additional_data or {}
        }
        
        self.performance_data.append(performance_record)
        
        # Store in session state
        if 'performance_data' not in st.session_state:
            st.session_state.performance_data = []
        
        st.session_state.performance_data.append(performance_record)
        
        # Clean up
        del self.start_times[operation_name]
        
        return performance_record
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        
        if not self.performance_data:
            return {"message": "No performance data available"}
        
        operations = {}
        for record in self.performance_data:
            op_name = record["operation"]
            if op_name not in operations:
                operations[op_name] = {
                    "count": 0,
                    "total_duration": 0,
                    "durations": []
                }
            
            operations[op_name]["count"] += 1
            operations[op_name]["total_duration"] += record["duration_seconds"]
            operations[op_name]["durations"].append(record["duration_seconds"])
        
        # Calculate statistics
        summary = {}
        for op_name, data in operations.items():
            durations = data["durations"]
            summary[op_name] = {
                "count": data["count"],
                "total_duration": data["total_duration"],
                "average_duration": data["total_duration"] / data["count"],
                "min_duration": min(durations),
                "max_duration": max(durations),
                "median_duration": sorted(durations)[len(durations)//2]
            }
        
        return summary

# Global instances
@st.cache_resource
def get_config_manager():
    """Get cached configuration manager instance"""
    return IndianLegalConfigManager()

@st.cache_resource
def get_performance_monitor():
    """Get cached performance monitor instance"""
    return IndianLegalPerformanceMonitor()

# Utility functions for session management
def reset_session_state():
    """Reset session state to initial values"""
    
    for key in list(st.session_state.keys()):
        if key.startswith(('constitutional_', 'privacy_', 'dpdpa_', 'document_', 'analysis_', 'compliance_')):
            del st.session_state[key]
    
    initialize_indian_legal_session_state()
    log_kag_operation("session_reset", {"timestamp": datetime.now().isoformat()})

def export_session_data() -> Dict[str, Any]:
    """Export session data for backup or analysis"""
    
    exportable_keys = [
        'constitutional_analysis', 'privacy_analysis', 'dpdpa_analysis',
        'compliance_score', 'document_classification', 'analysis_performance',
        'kag_operations_log', 'error_log', 'warning_log'
    ]
    
    export_data = {
        "export_timestamp": datetime.now().isoformat(),
        "system_version": "1.0.0",
        "session_data": {}
    }
    
    for key in exportable_keys:
        if key in st.session_state:
            export_data["session_data"][key] = st.session_state[key]
    
    return export_data

def import_session_data(data: Dict[str, Any]) -> bool:
    """Import session data from backup"""
    
    try:
        if "session_data" in data:
            for key, value in data["session_data"].items():
                st.session_state[key] = value
        
        log_kag_operation("session_import", {
            "import_timestamp": datetime.now().isoformat(),
            "original_export_timestamp": data.get("export_timestamp", "unknown")
        })
        
        return True
        
    except Exception as e:
        log_kag_operation("session_import_error", {"error": str(e)}, level="error")
        return False

# Version and system information
SYSTEM_INFO = {
    "name": "Indian Legal KAG System",
    "version": "1.0.0",
    "build_date": "2025-01-13",
    "jurisdiction": "India",
    "legal_framework": "Indian Constitution & DPDPA 2023",
    "supported_document_types": [
        "Legal contracts", "Privacy policies", "Constitutional documents",
        "Court judgments", "Legal opinions", "Compliance documents"
    ],
    "key_features": [
        "Constitutional reasoning pathways",
        "Article 21 privacy analysis",
        "DPDPA 2023 compliance assessment", 
        "Knowledge graph integration",
        "AI-powered legal analysis",
        "Comprehensive report generation"
    ]
}

def get_system_info() -> Dict[str, Any]:
    """Get system information"""
    return SYSTEM_INFO.copy()

# Export all utility functions and classes
__all__ = [
    'initialize_indian_legal_session_state',
    'validate_environment_variables', 
    'get_indian_legal_constants',
    'load_indian_legal_stopwords',
    'format_constitutional_article_reference',
    'parse_legal_citation',
    'extract_constitutional_articles',
    'extract_case_references',
    'calculate_constitutional_hierarchy_score',
    'generate_document_hash',
    'log_kag_operation',
    'measure_performance',
    'clean_legal_text',
    'validate_legal_document_structure',
    'create_analysis_summary',
    'IndianLegalConfigManager',
    'IndianLegalPerformanceMonitor',
    'get_config_manager',
    'get_performance_monitor',
    'reset_session_state',
    'export_session_data',
    'import_session_data',
    'get_system_info',
    'CONSTITUTIONAL_PARTS',
    'SC_CITATION_PATTERNS',
    'HC_CITATION_PATTERNS',
    'DPDPA_SECTIONS',
    'PRIVACY_FRAMEWORK',
    'INDIAN_LEGAL_TERMS',
    'SYSTEM_INFO'
]
