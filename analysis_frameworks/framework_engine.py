"""
Adaptive Legal Framework Engine for Indian Legal Documents
Intelligent framework selection based on document type and content
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from .constitutional_articles import CONSTITUTIONAL_ARTICLES, LANDMARK_CASES, DPDPA_PROVISIONS

logger = logging.getLogger(__name__)

class AdaptiveLegalFrameworkEngine:
    """Intelligent legal framework selection and application engine"""
    
    def __init__(self):
        self.constitutional_articles = CONSTITUTIONAL_ARTICLES
        self.landmark_cases = LANDMARK_CASES
        self.dpdpa_provisions = DPDPA_PROVISIONS
        self.framework_registry = self._initialize_framework_registry()
        self.application_rules = self._initialize_application_rules()
    
    def _initialize_framework_registry(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive legal framework registry"""
        return {
            "constitutional_analysis": {
                "description": "Constitutional law analysis using Articles 1-395",
                "applicable_documents": [
                    "government_notification", "constitutional_document", "supreme_court_judgment",
                    "constitutional_amendment", "recruitment_rules", "office_memorandum"
                ],
                "key_articles": [1, 12, 14, 19, 21, 32, 356, 368],
                "analysis_methods": [
                    "fundamental_rights_assessment", 
                    "directive_principles_evaluation",
                    "basic_structure_analysis",
                    "constitutional_validity_check"
                ],
                "priority": 1
            },
            "privacy_rights_analysis": {
                "description": "Article 21 privacy rights and Puttaswamy judgment framework",
                "applicable_documents": [
                    "privacy_policy", "dpdpa_compliance_document", "data_processing_agreement",
                    "employment_contract", "service_agreement"
                ],
                "key_articles": [21],
                "key_cases": ["puttaswamy", "maneka_gandhi"],
                "privacy_dimensions": [
                    "informational_privacy", "bodily_privacy", 
                    "communications_privacy", "territorial_privacy"
                ],
                "analysis_methods": [
                    "privacy_impact_assessment",
                    "constitutional_privacy_compliance",
                    "puttaswamy_framework_application"
                ],
                "priority": 2
            },
            "dpdpa_compliance": {
                "description": "Digital Personal Data Protection Act 2023 compliance analysis",
                "applicable_documents": [
                    "privacy_policy", "dpdpa_compliance_document", "data_processing_agreement"
                ],
                "key_provisions": ["section_3", "section_5", "section_8"],
                "constitutional_basis": ["article_21", "article_14"],
                "compliance_areas": [
                    "lawful_basis_assessment",
                    "consent_mechanism_evaluation",
                    "data_fiduciary_obligations",
                    "data_principal_rights"
                ],
                "analysis_methods": [
                    "dpdpa_compliance_scoring",
                    "constitutional_alignment_check",
                    "cross_border_compliance"
                ],
                "priority": 2
            },
            "contract_law_analysis": {
                "description": "Indian Contract Act 1872 and commercial law analysis",
                "applicable_documents": [
                    "service_agreement", "employment_contract", "non_disclosure_agreement",
                    "partnership_agreement", "loan_agreement", "lease_agreement"
                ],
                "key_statutes": ["indian_contract_act_1872"],
                "constitutional_basis": ["article_19", "article_21"],
                "contract_elements": [
                    "offer_acceptance", "consideration", "capacity", "legality",
                    "consent", "performance", "breach_remedies"
                ],
                "analysis_methods": [
                    "contract_validity_assessment",
                    "enforceability_analysis",
                    "constitutional_compliance_check"
                ],
                "priority": 3
            },
            "administrative_law": {
                "description": "Administrative law and government action analysis",
                "applicable_documents": [
                    "government_notification", "office_memorandum", "recruitment_rules",
                    "policy_document", "compliance_manual"
                ],
                "key_articles": [14, 19, 21, 309, 356],
                "administrative_principles": [
                    "natural_justice", "procedural_fairness", "reasonableness",
                    "proportionality", "legitimate_expectation"
                ],
                "analysis_methods": [
                    "administrative_validity_check",
                    "procedural_compliance_assessment",
                    "constitutional_authority_verification"
                ],
                "priority": 2
            },
            "general_legal_analysis": {
                "description": "General legal document analysis framework",
                "applicable_documents": ["general_legal_document", "unknown"],
                "analysis_methods": [
                    "legal_structure_analysis",
                    "compliance_overview",
                    "risk_identification"
                ],
                "priority": 4
            }
        }
    
    def _initialize_application_rules(self) -> Dict[str, Any]:
        """Initialize framework application rules and priorities"""
        return {
            "primary_selection_criteria": [
                "document_type_match",
                "content_relevance",
                "constitutional_significance",
                "legal_complexity"
            ],
            "combination_rules": {
                "government_documents": ["constitutional_analysis", "administrative_law"],
                "privacy_documents": ["privacy_rights_analysis", "dpdpa_compliance", "constitutional_analysis"],
                "commercial_contracts": ["contract_law_analysis", "constitutional_analysis"],
                "employment_matters": ["labor_law_analysis", "contract_law_analysis", "constitutional_analysis"],
                "judicial_documents": ["case_law_analysis", "constitutional_analysis"]
            },
            "minimum_frameworks": 1,
            "maximum_frameworks": 4,
            "confidence_threshold": 0.3
        }
    
    def select_frameworks(self, document_type: str, confidence: float, 
                         content_indicators: Dict[str, Any] = None) -> Dict[str, Any]:
        """Intelligently select appropriate legal frameworks"""
        
        selected_frameworks = []
        framework_reasons = {}
        content_indicators = content_indicators or {}
        
        # Primary framework selection based on document type
        primary_frameworks = self._get_primary_frameworks(document_type, confidence)
        selected_frameworks.extend(primary_frameworks)
        
        # Content-based framework selection
        content_frameworks = self._get_content_based_frameworks(content_indicators)
        for framework in content_frameworks:
            if framework not in selected_frameworks:
                selected_frameworks.append(framework)
        
        # Constitutional analysis is default for high-confidence legal documents
        if confidence >= 0.5 and "constitutional_analysis" not in selected_frameworks:
            selected_frameworks.append("constitutional_analysis")
        
        # Apply combination rules
        combined_frameworks = self._apply_combination_rules(document_type, selected_frameworks)
        
        # Priority sorting and limiting
        final_frameworks = self._prioritize_and_limit_frameworks(combined_frameworks)
        
        # Generate selection reasoning
        for framework in final_frameworks:
            framework_reasons[framework] = self._generate_selection_reason(
                framework, document_type, confidence, content_indicators
            )
        
        return {
            "selected_frameworks": final_frameworks,
            "framework_count": len(final_frameworks),
            "selection_confidence": confidence,
            "selection_reasons": framework_reasons,
            "document_type": document_type,
            "selection_timestamp": datetime.now().isoformat()
        }
    
    def _get_primary_frameworks(self, document_type: str, confidence: float) -> List[str]:
        """Get primary frameworks based on document type"""
        primary = []
        
        for framework_name, framework_config in self.framework_registry.items():
            if document_type in framework_config.get("applicable_documents", []):
                primary.append(framework_name)
        
        return primary
    
    def _get_content_based_frameworks(self, content_indicators: Dict[str, Any]) -> List[str]:
        """Select frameworks based on content analysis"""
        frameworks = []
        
        # Constitutional content
        if content_indicators.get("constitutional_relevance", False):
            frameworks.append("constitutional_analysis")
        
        # Privacy content
        if (content_indicators.get("dpdpa_relevance", False) or 
            content_indicators.get("privacy_terms", [])):
            frameworks.extend(["privacy_rights_analysis", "dpdpa_compliance"])
        
        # Government content
        if content_indicators.get("government_terms", []):
            frameworks.append("administrative_law")
        
        return frameworks
    
    def _apply_combination_rules(self, document_type: str, frameworks: List[str]) -> List[str]:
        """Apply framework combination rules"""
        combined = list(frameworks)  # Start with existing frameworks
        
        # Document type specific combinations
        doc_category = self._categorize_document_type(document_type)
        combination_rule = self.application_rules["combination_rules"].get(doc_category, [])
        
        for framework in combination_rule:
            if framework not in combined:
                combined.append(framework)
        
        return combined
    
    def _categorize_document_type(self, document_type: str) -> str:
        """Categorize document type for combination rules"""
        if document_type in ["government_notification", "office_memorandum", "recruitment_rules"]:
            return "government_documents"
        elif document_type in ["privacy_policy", "dpdpa_compliance_document"]:
            return "privacy_documents"
        elif document_type in ["service_agreement", "employment_contract"]:
            return "commercial_contracts"
        elif document_type in ["employment_contract"]:
            return "employment_matters"
        elif document_type in ["supreme_court_judgment", "high_court_judgment"]:
            return "judicial_documents"
        else:
            return "general_documents"
    
    def _prioritize_and_limit_frameworks(self, frameworks: List[str]) -> List[str]:
        """Sort frameworks by priority and apply limits"""
        # Sort by priority
        framework_priorities = []
        for framework in frameworks:
            priority = self.framework_registry.get(framework, {}).get("priority", 5)
            framework_priorities.append((framework, priority))
        
        # Sort by priority (lower number = higher priority)
        framework_priorities.sort(key=lambda x: x[1])
        
        # Extract frameworks and apply limits
        sorted_frameworks = [f[0] for f in framework_priorities]
        
        min_frameworks = self.application_rules["minimum_frameworks"]
        max_frameworks = self.application_rules["maximum_frameworks"]
        
        # Ensure minimum
        if len(sorted_frameworks) < min_frameworks:
            if "general_legal_analysis" not in sorted_frameworks:
                sorted_frameworks.append("general_legal_analysis")
        
        # Apply maximum
        return sorted_frameworks[:max_frameworks]
    
    def _generate_selection_reason(self, framework: str, document_type: str, 
                                 confidence: float, content_indicators: Dict[str, Any]) -> str:
        """Generate human-readable reason for framework selection"""
        
        framework_config = self.framework_registry.get(framework, {})
        
        reasons = []
        
        # Document type match
        if document_type in framework_config.get("applicable_documents", []):
            reasons.append(f"Document type '{document_type}' matches framework scope")
        
        # Content relevance
        if framework == "constitutional_analysis" and content_indicators.get("constitutional_relevance"):
            reasons.append("Constitutional content detected")
        elif framework == "privacy_rights_analysis" and content_indicators.get("privacy_terms"):
            reasons.append("Privacy-related content identified")
        elif framework == "dpdpa_compliance" and content_indicators.get("dpdpa_relevance"):
            reasons.append("DPDPA compliance requirements identified")
        
        # Confidence-based selection
        if confidence >= 0.7:
            reasons.append("High classification confidence supports framework application")
        
        # Default reason
        if not reasons:
            reasons.append("Selected based on document analysis and legal framework requirements")
        
        return "; ".join(reasons)
    
    def get_framework_details(self, framework_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific framework"""
        framework = self.framework_registry.get(framework_name, {})
        
        if not framework:
            return {"error": f"Framework '{framework_name}' not found"}
        
        # Enrich with constitutional data
        details = framework.copy()
        
        # Add constitutional articles details
        if "key_articles" in framework:
            details["constitutional_articles_details"] = {}
            for article_num in framework["key_articles"]:
                article_key = f"article_{article_num}"
                if article_key in self.constitutional_articles:
                    details["constitutional_articles_details"][article_num] = {
                        "title": self.constitutional_articles[article_key].get("title", f"Article {article_num}"),
                        "part": self.constitutional_articles[article_key].get("part", "Unknown"),
                        "chapter": self.constitutional_articles[article_key].get("chapter", "Unknown")
                    }
        
        return details
