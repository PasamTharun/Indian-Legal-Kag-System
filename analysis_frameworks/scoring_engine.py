"""
Universal Legal Scoring Engine for Indian Legal Documents
Multi-dimensional compliance scoring and risk assessment
"""

import logging
import math
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class UniversalLegalScoringEngine:
    """Comprehensive legal compliance scoring and risk assessment engine"""
    
    def __init__(self):
        self.scoring_criteria = self._initialize_scoring_criteria()
        self.risk_thresholds = self._initialize_risk_thresholds()
    
    def _initialize_scoring_criteria(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive scoring criteria for different aspects"""
        return {
            "constitutional_compliance": {
                "weight": 0.4,
                "max_score": 100,
                "criteria": {
                    "fundamental_rights_adherence": {
                        "weight": 0.3,
                        "articles": [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35],
                        "scoring_method": "rights_protection_analysis"
                    },
                    "constitutional_validity": {
                        "weight": 0.3,
                        "articles": [1, 309, 356, 368],
                        "scoring_method": "validity_framework_analysis"
                    },
                    "procedural_compliance": {
                        "weight": 0.4,
                        "scoring_method": "due_process_evaluation"
                    }
                }
            },
            "privacy_compliance": {
                "weight": 0.3,
                "max_score": 100,
                "criteria": {
                    "article_21_compliance": {
                        "weight": 0.4,
                        "privacy_dimensions": [
                            "informational_privacy",
                            "bodily_privacy", 
                            "communications_privacy",
                            "territorial_privacy"
                        ],
                        "scoring_method": "puttaswamy_framework_assessment"
                    },
                    "consent_mechanism": {
                        "weight": 0.3,
                        "scoring_method": "consent_validity_analysis"
                    },
                    "transparency": {
                        "weight": 0.3,
                        "scoring_method": "disclosure_adequacy_assessment"
                    }
                }
            },
            "dpdpa_compliance": {
                "weight": 0.3,
                "max_score": 100,
                "criteria": {
                    "lawful_basis": {
                        "weight": 0.35,
                        "scoring_method": "lawful_processing_assessment"
                    },
                    "data_fiduciary_obligations": {
                        "weight": 0.35,
                        "scoring_method": "fiduciary_compliance_analysis"
                    },
                    "data_principal_rights": {
                        "weight": 0.3,
                        "scoring_method": "principal_rights_protection"
                    }
                }
            }
        }
    
    def _initialize_risk_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Initialize risk assessment thresholds"""
        return {
            "constitutional_risk": {
                "very_low": 90,
                "low": 75,
                "medium": 60,
                "high": 40,
                "very_high": 0
            },
            "privacy_risk": {
                "very_low": 85,
                "low": 70,
                "medium": 55,
                "high": 35,
                "very_high": 0
            },
            "compliance_risk": {
                "very_low": 88,
                "low": 73,
                "medium": 58,
                "high": 38,
                "very_high": 0
            },
            "overall_risk": {
                "very_low": 87,
                "low": 72,
                "medium": 57,
                "high": 37,
                "very_high": 0
            }
        }
    
    def calculate_comprehensive_score(self, document_analysis: Dict[str, Any], 
                                    frameworks_applied: List[str]) -> Dict[str, Any]:
        """Calculate comprehensive compliance score across all dimensions"""
        
        scoring_results = {
            "overall_score": 0.0,
            "category_scores": {},
            "risk_assessment": {},
            "compliance_level": "unknown",
            "critical_issues": [],
            "recommendations": [],
            "scoring_breakdown": {},
            "confidence_level": 0.0,
            "scoring_timestamp": datetime.now().isoformat()
        }
        
        total_weighted_score = 0.0
        total_weight = 0.0
        
        # Score each applicable category based on frameworks
        for framework in frameworks_applied:
            category_score = self._score_framework_category(framework, document_analysis)
            if category_score is not None:
                category_name = self._map_framework_to_category(framework)
                scoring_results["category_scores"][category_name] = category_score
                
                # Get category weight
                category_weight = self._get_category_weight(category_name)
                total_weighted_score += category_score["score"] * category_weight
                total_weight += category_weight
                
                # Collect critical issues
                scoring_results["critical_issues"].extend(category_score.get("issues", []))
                scoring_results["recommendations"].extend(category_score.get("recommendations", []))
        
        # Calculate overall score
        if total_weight > 0:
            scoring_results["overall_score"] = total_weighted_score / total_weight
        else:
            scoring_results["overall_score"] = 0.0
        
        # Determine compliance level
        scoring_results["compliance_level"] = self._determine_compliance_level(
            scoring_results["overall_score"]
        )
        
        # Risk assessment
        scoring_results["risk_assessment"] = self._assess_comprehensive_risk(
            scoring_results["category_scores"],
            scoring_results["overall_score"]
        )
        
        # Calculate confidence level
        scoring_results["confidence_level"] = self._calculate_scoring_confidence(
            document_analysis,
            frameworks_applied,
            scoring_results["category_scores"]
        )
        
        return scoring_results
    
    def _score_framework_category(self, framework: str, document_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Score a specific framework category"""
        
        category_name = self._map_framework_to_category(framework)
        if category_name not in self.scoring_criteria:
            return None
        
        category_config = self.scoring_criteria[category_name]
        category_score = 0.0
        category_issues = []
        category_recommendations = []
        criterion_scores = {}
        
        # Score each criterion within the category
        for criterion_name, criterion_config in category_config["criteria"].items():
            criterion_score = self._score_criterion(
                criterion_name,
                criterion_config,
                document_analysis,
                framework
            )
            
            criterion_scores[criterion_name] = criterion_score
            category_score += criterion_score["score"] * criterion_config["weight"]
            category_issues.extend(criterion_score.get("issues", []))
            category_recommendations.extend(criterion_score.get("recommendations", []))
        
        return {
            "score": min(100, max(0, category_score)),
            "criterion_scores": criterion_scores,
            "issues": category_issues,
            "recommendations": category_recommendations,
            "category": category_name,
            "framework": framework
        }
    
    def _score_criterion(self, criterion_name: str, criterion_config: Dict[str, Any],
                        document_analysis: Dict[str, Any], framework: str) -> Dict[str, Any]:
        """Score an individual criterion"""
        
        scoring_method = criterion_config.get("scoring_method", "default")
        base_score = 65.0  # Default score
        issues = []
        recommendations = []
        
        try:
            if scoring_method == "rights_protection_analysis":
                score_result = self._score_fundamental_rights_protection(
                    criterion_config, document_analysis
                )
            elif scoring_method == "puttaswamy_framework_assessment":
                score_result = self._score_privacy_rights_compliance(
                    criterion_config, document_analysis
                )
            elif scoring_method == "lawful_processing_assessment":
                score_result = self._score_dpdpa_lawful_basis(
                    criterion_config, document_analysis
                )
            else:
                score_result = self._default_scoring_method(
                    criterion_config, document_analysis
                )
            
            base_score = score_result.get("score", base_score)
            issues = score_result.get("issues", [])
            recommendations = score_result.get("recommendations", [])
            
        except Exception as e:
            logger.error(f"Error scoring criterion {criterion_name}: {str(e)}")
            issues.append(f"Scoring error for {criterion_name}: {str(e)}")
        
        return {
            "score": base_score,
            "issues": issues,
            "recommendations": recommendations,
            "criterion": criterion_name,
            "method": scoring_method
        }
    
    def _score_fundamental_rights_protection(self, config: Dict[str, Any], 
                                           analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Score fundamental rights protection"""
        score = 70.0
        issues = []
        recommendations = []
        
        # Check constitutional compliance
        constitutional_indicators = analysis.get("indian_legal_indicators", {})
        constitutional_relevance = constitutional_indicators.get("constitutional_relevance", False)
        
        if constitutional_relevance:
            score += 15
        else:
            score -= 10
            issues.append("Constitutional relevance not clearly established")
        
        # Check for article mentions
        article_mentions = constitutional_indicators.get("article_mentions", [])
        if article_mentions:
            score += len(article_mentions) * 3
        else:
            issues.append("No constitutional articles specifically referenced")
            recommendations.append("Reference relevant constitutional provisions")
        
        return {
            "score": min(100, max(0, score)),
            "issues": issues,
            "recommendations": recommendations
        }
    
    def _score_privacy_rights_compliance(self, config: Dict[str, Any], 
                                       analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Score privacy rights compliance using Puttaswamy framework"""
        score = 60.0
        issues = []
        recommendations = []
        
        # Check privacy relevance
        privacy_indicators = analysis.get("indian_legal_indicators", {})
        privacy_terms = privacy_indicators.get("privacy_terms", [])
        
        if privacy_terms:
            score += len(privacy_terms) * 8
        else:
            score -= 15
            issues.append("Privacy protection measures not adequately addressed")
            recommendations.append("Implement comprehensive privacy protection measures")
        
        # Check for DPDPA compliance
        dpdpa_relevance = privacy_indicators.get("dpdpa_relevance", False)
        if dpdpa_relevance:
            score += 15
        else:
            issues.append("DPDPA compliance requirements not addressed")
            recommendations.append("Implement DPDPA 2023 compliance measures")
        
        return {
            "score": min(100, max(0, score)),
            "issues": issues,
            "recommendations": recommendations
        }
    
    def _score_dpdpa_lawful_basis(self, config: Dict[str, Any], 
                                 analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Score DPDPA lawful basis compliance"""
        score = 65.0
        issues = []
        recommendations = []
        
        # Check for consent mechanisms
        text_chunks = analysis.get("enhanced_chunks", [])
        consent_mentions = 0
        lawful_basis_mentions = 0
        
        for chunk in text_chunks:
            chunk_text = chunk.get("text", "").lower()
            if "consent" in chunk_text:
                consent_mentions += 1
            if any(term in chunk_text for term in ["lawful basis", "legitimate interest"]):
                lawful_basis_mentions += 1
        
        if consent_mentions > 0:
            score += 15
        else:
            issues.append("No clear consent mechanism identified")
            recommendations.append("Implement clear consent collection procedures")
        
        if lawful_basis_mentions > 0:
            score += 10
        else:
            issues.append("Lawful basis for processing not clearly established")
            recommendations.append("Establish and document lawful basis for data processing")
        
        return {
            "score": min(100, max(0, score)),
            "issues": issues,
            "recommendations": recommendations
        }
    
    def _default_scoring_method(self, config: Dict[str, Any], 
                              analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Default scoring method for unspecified criteria"""
        return {
            "score": 65.0,
            "issues": [],
            "recommendations": ["Manual review recommended for detailed assessment"]
        }
    
    def _map_framework_to_category(self, framework: str) -> str:
        """Map framework name to scoring category"""
        mapping = {
            "constitutional_analysis": "constitutional_compliance",
            "privacy_rights_analysis": "privacy_compliance",
            "dpdpa_compliance": "dpdpa_compliance",
            "administrative_law": "constitutional_compliance",
            "general_legal_analysis": "constitutional_compliance"
        }
        return mapping.get(framework, "constitutional_compliance")
    
    def _get_category_weight(self, category: str) -> float:
        """Get weight for scoring category"""
        return self.scoring_criteria.get(category, {}).get("weight", 0.33)
    
    def _determine_compliance_level(self, overall_score: float) -> str:
        """Determine compliance level based on overall score"""
        if overall_score >= 90:
            return "excellent"
        elif overall_score >= 80:
            return "good"
        elif overall_score >= 70:
            return "satisfactory"
        elif overall_score >= 60:
            return "needs_improvement"
        else:
            return "poor"
    
    def _assess_comprehensive_risk(self, category_scores: Dict[str, Any], 
                                 overall_score: float) -> Dict[str, Any]:
        """Assess comprehensive risk across all categories"""
        risk_assessment = {
            "overall_risk_level": self._get_risk_level("overall_risk", overall_score),
            "category_risks": {},
            "critical_risks": [],
            "risk_factors": []
        }
        
        for category, score_data in category_scores.items():
            score = score_data.get("score", 0)
            risk_level = self._get_risk_level(f"{category.split('_')[0]}_risk", score)
            risk_assessment["category_risks"][category] = {
                "risk_level": risk_level,
                "score": score,
                "issues": score_data.get("issues", [])
            }
            
            # Identify critical risks
            if risk_level in ["high", "very_high"]:
                risk_assessment["critical_risks"].append({
                    "category": category,
                    "risk_level": risk_level,
                    "score": score
                })
        
        return risk_assessment
    
    def _get_risk_level(self, risk_type: str, score: float) -> str:
        """Get risk level based on score and risk type"""
        thresholds = self.risk_thresholds.get(risk_type, self.risk_thresholds["overall_risk"])
        
        for level, threshold in thresholds.items():
            if score >= threshold:
                return level
        
        return "very_high"
    
    def _calculate_scoring_confidence(self, document_analysis: Dict[str, Any], 
                                    frameworks_applied: List[str], 
                                    category_scores: Dict[str, Any]) -> float:
        """Calculate confidence level in scoring results"""
        confidence_factors = []
        
        # Document classification confidence
        classification = document_analysis.get("document_classification", {})
        classification_confidence = classification.get("confidence", 0.5)
        confidence_factors.append(classification_confidence)
        
        # Framework coverage
        framework_coverage = len(frameworks_applied) / 3  # Assuming 3 max frameworks
        confidence_factors.append(min(1.0, framework_coverage))
        
        # Content richness
        content_indicators = document_analysis.get("indian_legal_indicators", {})
        content_richness = len([v for v in content_indicators.values() if v]) / 8  # Normalize
        confidence_factors.append(min(1.0, content_richness))
        
        return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.6
