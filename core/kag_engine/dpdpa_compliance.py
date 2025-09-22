"""
DPDPA 2023 Compliance Engine with Constitutional Integration - Complete Updated Version
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from .knowledge_graph.neo4j_manager import ConstitutionalKnowledgeGraph
from .kag_engine.privacy_analyzer import Article21PrivacyAnalyzer

logger = logging.getLogger(__name__)

class DPDPAComplianceEngine:
    """DPDPA 2023 compliance assessment with constitutional foundation"""
    
    def __init__(self):
        try:
            self.kg = ConstitutionalKnowledgeGraph()
        except Exception as e:
            logger.warning(f"Knowledge graph not available: {str(e)}")
            self.kg = None
            
        try:
            self.privacy_analyzer = Article21PrivacyAnalyzer()
        except Exception as e:
            logger.warning(f"Privacy analyzer not available: {str(e)}")
            self.privacy_analyzer = None
            
        self.dpdpa_provisions = self._load_dpdpa_framework()
        self.compliance_matrix = self._initialize_compliance_matrix()
    
    def _load_dpdpa_framework(self) -> Dict[str, Dict[str, Any]]:
        """Load comprehensive DPDPA 2023 framework"""
        return {
            "chapter_1": {
                "title": "Preliminary",
                "sections": {
                    "section_1": {
                        "title": "Short title and commencement",
                        "constitutional_relevance": "low",
                        "privacy_impact": "none"
                    },
                    "section_2": {
                        "title": "Definitions",
                        "key_definitions": [
                            "Data Principal", "Data Fiduciary", "Personal Data",
                            "Processing", "Consent", "Digital Personal Data"
                        ],
                        "constitutional_relevance": "high",
                        "privacy_impact": "foundational"
                    }
                }
            },
            "chapter_2": {
                "title": "Obligations of Data Fiduciary",
                "sections": {
                    "section_5": {
                        "title": "Grounds for processing personal data",
                        "requirements": [
                            "Lawful processing", "Purpose specification", "Data minimization",
                            "Accuracy", "Storage limitation", "Integrity and confidentiality"
                        ],
                        "constitutional_basis": ["article_21", "article_14"],
                        "privacy_impact": "critical",
                        "compliance_indicators": [
                            "clear legal basis", "explicit purpose", "minimal data collection",
                            "data accuracy measures", "retention policies", "security measures"
                        ]
                    },
                    "section_8": {
                        "title": "Duties of Data Fiduciary",
                        "requirements": [
                            "Fair and reasonable processing", "Technical safeguards",
                            "Organizational measures", "Data breach notification",
                            "Data protection impact assessment"
                        ],
                        "constitutional_basis": ["article_21"],
                        "privacy_impact": "critical",
                        "compliance_indicators": [
                            "fairness assessment", "technical security", "organizational policies",
                            "breach response procedures", "impact assessment processes"
                        ]
                    }
                }
            },
            "chapter_3": {
                "title": "Rights and Duties of Data Principal",
                "sections": {
                    "section_11": {
                        "title": "Rights of Data Principal",
                        "rights": [
                            "Right to information", "Right to correction", "Right to erasure",
                            "Right to grievance redressal", "Right to nominate"
                        ],
                        "constitutional_basis": ["article_21", "article_19"],
                        "privacy_impact": "high"
                    }
                }
            }
        }
    
    def _initialize_compliance_matrix(self) -> Dict[str, Dict[str, Any]]:
        """Initialize compliance assessment matrix"""
        return {
            "consent_management": {
                "weight": 0.25,
                "constitutional_source": "article_21",
                "puttaswamy_principle": "Informational Self-Determination",
                "assessment_criteria": [
                    "explicit_consent", "informed_consent", "specific_consent",
                    "withdrawable_consent", "granular_consent"
                ]
            },
            "data_minimization": {
                "weight": 0.20,
                "constitutional_source": "article_21",
                "puttaswamy_principle": "Data Minimization",
                "assessment_criteria": [
                    "purpose_limitation", "collection_limitation", "use_limitation",
                    "retention_limitation", "disclosure_limitation"
                ]
            },
            "security_safeguards": {
                "weight": 0.20,
                "constitutional_source": "article_21",
                "puttaswamy_principle": "Security and Integrity",
                "assessment_criteria": [
                    "technical_measures", "organizational_measures", "access_controls",
                    "encryption", "breach_prevention"
                ]
            },
            "transparency": {
                "weight": 0.15,
                "constitutional_source": "article_21",
                "puttaswamy_principle": "Transparency and Accountability",
                "assessment_criteria": [
                    "privacy_notice", "processing_disclosure", "rights_information",
                    "contact_details", "complaint_mechanisms"
                ]
            },
            "data_subject_rights": {
                "weight": 0.20,
                "constitutional_source": "article_21",
                "puttaswamy_principle": "Individual Rights",
                "assessment_criteria": [
                    "access_rights", "correction_rights", "erasure_rights",
                    "portability_rights", "objection_rights"
                ]
            }
        }
    
    def assess_dpdpa_compliance(self, document_text: str, privacy_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
        """Comprehensive DPDPA compliance assessment"""
        
        logger.info("📋 Starting DPDPA 2023 compliance assessment...")
        
        try:
            # Use existing privacy analysis or generate new one
            if not privacy_analysis and self.privacy_analyzer:
                privacy_analysis = self.privacy_analyzer.analyze_privacy_implications(document_text)
            elif not privacy_analysis:
                privacy_analysis = {}
            
            # Step 1: Section-by-section compliance assessment
            section_compliance = self._assess_section_compliance(document_text, privacy_analysis)
            
            # Step 2: Apply compliance matrix
            matrix_assessment = self._apply_compliance_matrix(document_text, privacy_analysis)
            
            # Step 3: Constitutional alignment check
            constitutional_alignment = self._check_constitutional_alignment(
                section_compliance, matrix_assessment, privacy_analysis
            )
            
            # Step 4: Risk assessment
            compliance_risks = self._assess_compliance_risks(
                section_compliance, matrix_assessment, constitutional_alignment
            )
            
            # Step 5: Generate recommendations
            recommendations = self._generate_dpdpa_recommendations(
                section_compliance, matrix_assessment, compliance_risks
            )
            
            # Step 6: Calculate overall compliance score
            overall_score = self._calculate_dpdpa_compliance_score(
                section_compliance, matrix_assessment, constitutional_alignment
            )
            
            return {
                "dpdpa_compliance_summary": {
                    "overall_score": overall_score["overall_score"],
                    "compliance_status": self._determine_compliance_status(overall_score["overall_score"]),
                    "constitutional_alignment": constitutional_alignment["alignment_score"],
                    "critical_gaps": compliance_risks.get("critical_issues", [])
                },
                "section_compliance": section_compliance,
                "matrix_assessment": matrix_assessment,
                "constitutional_alignment": constitutional_alignment,
                "compliance_risks": compliance_risks,
                "recommendations": recommendations,
                "overall_score": overall_score,
                "assessment_timestamp": datetime.now().isoformat(),
                "privacy_analysis_integration": privacy_analysis.get("analysis_timestamp")
            }
            
        except Exception as e:
            logger.error(f"❌ DPDPA compliance assessment failed: {str(e)}")
            return self._generate_compliance_error_response(str(e))
    
    def _assess_section_compliance(self, document_text: str, privacy_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess compliance with specific DPDPA sections"""
        
        section_assessments = {}
        
        for chapter_id, chapter_data in self.dpdpa_provisions.items():
            chapter_title = chapter_data["title"]
            
            for section_id, section_data in chapter_data.get("sections", {}).items():
                section_title = section_data["title"]
                
                assessment = {
                    "section_id": section_id,
                    "title": section_title,
                    "compliance_score": 0.0,
                    "compliance_status": "not_assessed",
                    "findings": [],
                    "gaps": [],
                    "constitutional_basis": section_data.get("constitutional_basis", []),
                    "privacy_impact": section_data.get("privacy_impact", "unknown")
                }
                
                # Assess specific sections
                if section_id == "section_5":
                    assessment = self._assess_section_5_compliance(assessment, document_text, privacy_analysis)
                elif section_id == "section_8":
                    assessment = self._assess_section_8_compliance(assessment, document_text, privacy_analysis)
                elif section_id == "section_11":
                    assessment = self._assess_section_11_compliance(assessment, document_text, privacy_analysis)
                else:
                    # Generic assessment for other sections
                    assessment = self._assess_generic_section_compliance(assessment, document_text)
                
                section_assessments[section_id] = assessment
        
        return section_assessments
    
    def _assess_section_5_compliance(self, assessment: Dict, document_text: str, privacy_analysis: Dict) -> Dict:
        """Assess Section 5: Grounds for processing personal data"""
        
        section_5_requirements = [
            "lawful_processing", "purpose_specification", "data_minimization",
            "accuracy", "storage_limitation", "integrity_confidentiality"
        ]
        
        compliance_scores = {}
        findings = []
        gaps = []
        
        # Check lawful processing
        lawful_basis_score = self._check_lawful_processing_basis(document_text, privacy_analysis)
        compliance_scores["lawful_processing"] = lawful_basis_score
        
        if lawful_basis_score >= 0.7:
            findings.append("✅ Clear lawful basis for processing identified")
        else:
            gaps.append("❌ Lawful basis for processing not clearly established")
        
        # Check purpose specification
        purpose_score = self._check_purpose_specification(document_text, privacy_analysis)
        compliance_scores["purpose_specification"] = purpose_score
        
        if purpose_score >= 0.7:
            findings.append("✅ Processing purposes clearly specified")
        else:
            gaps.append("❌ Processing purposes not adequately specified")
        
        # Check data minimization
        minimization_score = self._check_data_minimization(document_text, privacy_analysis)
        compliance_scores["data_minimization"] = minimization_score
        
        if minimization_score >= 0.7:
            findings.append("✅ Data minimization principle addressed")
        else:
            gaps.append("❌ Data minimization not adequately implemented")
        
        # Check accuracy requirements
        accuracy_score = self._check_accuracy_requirements(document_text)
        compliance_scores["accuracy"] = accuracy_score
        
        # Check storage limitation
        storage_score = self._check_storage_limitation(document_text)
        compliance_scores["storage_limitation"] = storage_score
        
        # Check integrity and confidentiality
        integrity_score = self._check_integrity_confidentiality(document_text)
        compliance_scores["integrity_confidentiality"] = integrity_score
        
        # Calculate overall section score
        overall_score = sum(compliance_scores.values()) / len(compliance_scores)
        
        assessment.update({
            "compliance_score": round(overall_score, 2),
            "compliance_status": "compliant" if overall_score >= 0.7 else "non_compliant" if overall_score < 0.5 else "partially_compliant",
            "findings": findings,
            "gaps": gaps,
            "requirement_scores": compliance_scores
        })
        
        return assessment
    
    def _assess_section_8_compliance(self, assessment: Dict, document_text: str, privacy_analysis: Dict) -> Dict:
        """Assess Section 8: Duties of Data Fiduciary"""
        
        section_8_requirements = [
            "fair_reasonable_processing", "technical_safeguards", "organizational_measures",
            "breach_notification", "impact_assessment"
        ]
        
        compliance_scores = {}
        findings = []
        gaps = []
        
        # Check fair and reasonable processing
        fairness_score = self._check_fair_reasonable_processing(document_text, privacy_analysis)
        compliance_scores["fair_reasonable_processing"] = fairness_score
        
        # Check technical safeguards
        technical_score = self._check_technical_safeguards(document_text, privacy_analysis)
        compliance_scores["technical_safeguards"] = technical_score
        
        # Check organizational measures
        organizational_score = self._check_organizational_measures(document_text)
        compliance_scores["organizational_measures"] = organizational_score
        
        # Check breach notification
        breach_score = self._check_breach_notification_procedures(document_text)
        compliance_scores["breach_notification"] = breach_score
        
        # Check impact assessment
        impact_score = self._check_impact_assessment_procedures(document_text)
        compliance_scores["impact_assessment"] = impact_score
        
        # Generate findings and gaps based on scores
        for requirement, score in compliance_scores.items():
            if score >= 0.7:
                findings.append(f"✅ {requirement.replace('_', ' ').title()} adequately addressed")
            else:
                gaps.append(f"❌ {requirement.replace('_', ' ').title()} needs improvement")
        
        # Calculate overall section score
        overall_score = sum(compliance_scores.values()) / len(compliance_scores)
        
        assessment.update({
            "compliance_score": round(overall_score, 2),
            "compliance_status": "compliant" if overall_score >= 0.7 else "non_compliant" if overall_score < 0.5 else "partially_compliant",
            "findings": findings,
            "gaps": gaps,
            "requirement_scores": compliance_scores
        })
        
        return assessment

    def _assess_section_11_compliance(self, assessment: Dict, document_text: str, privacy_analysis: Dict) -> Dict:
        """Assess Section 11: Rights of Data Principal"""
        
        rights_requirements = [
            "right_to_information", "right_to_correction", "right_to_erasure",
            "right_to_grievance_redressal", "right_to_nominate"
        ]
        
        compliance_scores = {}
        findings = []
        gaps = []
        
        # Check each right
        for right in rights_requirements:
            score = self._check_data_principal_right(document_text, right)
            compliance_scores[right] = score
            
            if score >= 0.6:
                findings.append(f"✅ {right.replace('_', ' ').title()} addressed")
            else:
                gaps.append(f"❌ {right.replace('_', ' ').title()} needs implementation")
        
        # Calculate overall section score
        overall_score = sum(compliance_scores.values()) / len(compliance_scores)
        
        assessment.update({
            "compliance_score": round(overall_score, 2),
            "compliance_status": "compliant" if overall_score >= 0.7 else "non_compliant" if overall_score < 0.5 else "partially_compliant",
            "findings": findings,
            "gaps": gaps,
            "requirement_scores": compliance_scores
        })
        
        return assessment

    def _assess_generic_section_compliance(self, assessment: Dict, document_text: str) -> Dict:
        """Generic assessment for DPDPA sections"""
        
        # Basic compliance indicators
        compliance_keywords = [
            'data protection', 'personal data', 'consent', 'lawful basis',
            'data subject', 'data controller', 'processing', 'privacy policy'
        ]
        
        text_lower = document_text.lower()
        keyword_matches = sum(1 for keyword in compliance_keywords if keyword in text_lower)
        
        # Calculate basic compliance score
        if keyword_matches >= 5:
            score = 0.75
            status = "compliant"
            findings = [f"Found {keyword_matches} DPDPA-related terms"]
            gaps = []
        elif keyword_matches >= 2:
            score = 0.60
            status = "partially_compliant" 
            findings = [f"Found {keyword_matches} DPDPA-related terms"]
            gaps = ["Limited DPDPA compliance indicators"]
        else:
            score = 0.40
            status = "non_compliant"
            findings = []
            gaps = ["Minimal DPDPA compliance measures identified"]
        
        assessment.update({
            "compliance_score": score,
            "compliance_status": status,
            "findings": findings,
            "gaps": gaps
        })
        
        return assessment
    
    def _apply_compliance_matrix(self, document_text: str, privacy_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Apply compliance assessment matrix"""
        
        matrix_results = {}
        
        for category, criteria in self.compliance_matrix.items():
            category_assessment = {
                "category": category,
                "weight": criteria["weight"],
                "constitutional_source": criteria["constitutional_source"],
                "puttaswamy_principle": criteria["puttaswamy_principle"],
                "assessment_score": 0.0,
                "evidence": [],
                "gaps": [],
                "criteria_scores": {}
            }
            
            # Assess each criterion
            for criterion in criteria["assessment_criteria"]:
                score = self._assess_compliance_criterion(criterion, document_text, privacy_analysis)
                category_assessment["criteria_scores"][criterion] = score
                
                if score >= 0.7:
                    category_assessment["evidence"].append(f"✅ {criterion.replace('_', ' ').title()}")
                else:
                    category_assessment["gaps"].append(f"❌ {criterion.replace('_', ' ').title()}")
            
            # Calculate category score
            category_assessment["assessment_score"] = (
                sum(category_assessment["criteria_scores"].values()) / 
                len(category_assessment["criteria_scores"])
            )
            
            matrix_results[category] = category_assessment
        
        return matrix_results
    
    def _check_constitutional_alignment(self, section_compliance: Dict, matrix_assessment: Dict, privacy_analysis: Dict) -> Dict[str, Any]:
        """Check alignment with constitutional privacy framework"""
        
        # Get Article 21 compliance from privacy analysis
        article_21_compliance = privacy_analysis.get("constitutional_compliance", {})
        
        alignment_assessment = {
            "article_21_alignment": article_21_compliance.get("article_21_compliance", "unknown"),
            "puttaswamy_compliance": self._assess_puttaswamy_compliance(matrix_assessment),
            "constitutional_test_results": article_21_compliance.get("constitutional_test_results", {}),
            "alignment_score": 0.0,
            "alignment_issues": [],
            "constitutional_recommendations": []
        }
        
        # Calculate alignment score
        alignment_scores = []
        
        # Article 21 compliance score
        if article_21_compliance.get("compliance_score"):
            alignment_scores.append(article_21_compliance["compliance_score"])
        
        # DPDPA-Constitution integration score
        integration_score = self._assess_dpdpa_constitutional_integration(section_compliance)
        alignment_scores.append(integration_score)
        
        # Puttaswamy principles compliance
        puttaswamy_score = alignment_assessment["puttaswamy_compliance"]
        alignment_scores.append(puttaswamy_score)
        
        alignment_assessment["alignment_score"] = sum(alignment_scores) / len(alignment_scores) if alignment_scores else 0.0
        
        # Identify alignment issues
        if alignment_assessment["alignment_score"] < 0.7:
            alignment_assessment["alignment_issues"] = self._identify_constitutional_alignment_issues(
                section_compliance, matrix_assessment, privacy_analysis
            )
        
        # Generate constitutional recommendations
        alignment_assessment["constitutional_recommendations"] = self._generate_constitutional_recommendations(
            alignment_assessment["alignment_issues"], article_21_compliance
        )
        
        return alignment_assessment

    def _assess_compliance_risks(self, section_compliance: Dict, matrix_assessment: Dict, constitutional_alignment: Dict) -> Dict[str, Any]:
        """Assess comprehensive compliance risks"""
        
        risks = {
            "critical_issues": [],
            "high_risk_areas": [],
            "medium_risk_areas": [],
            "risk_score": 0.0,
            "mitigation_priority": []
        }
        
        # Assess section-level risks
        for section_id, section_data in section_compliance.items():
            score = section_data.get("compliance_score", 0)
            
            if score < 0.4:
                risks["critical_issues"].append(f"Critical non-compliance in {section_id}")
            elif score < 0.6:
                risks["high_risk_areas"].append(f"High risk in {section_id}")
            elif score < 0.8:
                risks["medium_risk_areas"].append(f"Medium risk in {section_id}")
        
        # Assess matrix-level risks
        for category, data in matrix_assessment.items():
            score = data.get("assessment_score", 0)
            
            if score < 0.5:
                risks["critical_issues"].append(f"Critical gap in {category}")
            elif score < 0.7:
                risks["high_risk_areas"].append(f"High risk in {category}")
        
        # Calculate overall risk score
        all_scores = []
        for section_data in section_compliance.values():
            all_scores.append(section_data.get("compliance_score", 0))
        
        for matrix_data in matrix_assessment.values():
            all_scores.append(matrix_data.get("assessment_score", 0))
        
        if all_scores:
            avg_score = sum(all_scores) / len(all_scores)
            risks["risk_score"] = round(1.0 - avg_score, 2)  # Higher score = higher risk
        
        return risks

    def _generate_dpdpa_recommendations(self, section_compliance: Dict, matrix_assessment: Dict, compliance_risks: Dict) -> List[str]:
        """Generate DPDPA compliance recommendations"""
        
        recommendations = []
        
        # Section-specific recommendations
        for section_id, section_data in section_compliance.items():
            if section_data.get("compliance_score", 0) < 0.7:
                section_title = section_data.get("title", section_id)
                recommendations.append(f"Improve compliance with {section_title}")
        
        # Matrix-specific recommendations
        for category, data in matrix_assessment.items():
            if data.get("assessment_score", 0) < 0.7:
                recommendations.append(f"Strengthen {category.replace('_', ' ')}")
        
        # Risk-based recommendations
        if compliance_risks.get("critical_issues"):
            recommendations.append("Address critical compliance gaps immediately")
        
        if compliance_risks.get("high_risk_areas"):
            recommendations.append("Develop mitigation strategies for high-risk areas")
        
        # General recommendations
        recommendations.extend([
            "Conduct regular DPDPA compliance audits",
            "Implement privacy-by-design principles",
            "Train staff on data protection requirements",
            "Establish clear data governance policies"
        ])
        
        return recommendations[:8]  # Return top 8 recommendations
    
    def _calculate_dpdpa_compliance_score(self, section_compliance: Dict, matrix_assessment: Dict, constitutional_alignment: Dict) -> Dict[str, Any]:
        """Calculate overall DPDPA compliance score"""
        
        # Section compliance scores (40% weight)
        section_scores = [assessment["compliance_score"] for assessment in section_compliance.values()]
        section_average = sum(section_scores) / len(section_scores) if section_scores else 0.0
        
        # Matrix assessment scores (40% weight)
        weighted_matrix_score = sum(
            assessment["assessment_score"] * assessment["weight"] 
            for assessment in matrix_assessment.values()
        )
        
        # Constitutional alignment (20% weight)
        constitutional_score = constitutional_alignment.get("alignment_score", 0.0)
        
        # Calculate weighted overall score
        overall_score = (
            section_average * 0.40 +
            weighted_matrix_score * 0.40 +
            constitutional_score * 0.20
        )
        
        return {
            "overall_score": round(overall_score * 100, 2),  # Convert to percentage
            "component_scores": {
                "section_compliance": round(section_average * 100, 2),
                "matrix_assessment": round(weighted_matrix_score * 100, 2),
                "constitutional_alignment": round(constitutional_score * 100, 2)
            },
            "score_interpretation": self._interpret_dpdpa_score(overall_score * 100),
            "compliance_grade": self._assign_compliance_grade(overall_score * 100),
            "calculation_timestamp": datetime.now().isoformat()
        }
    
    # Helper methods for specific assessments
    def _check_lawful_processing_basis(self, document_text: str, privacy_analysis: Dict) -> float:
        """Check for clear lawful basis for processing"""
        lawful_basis_keywords = ["consent", "contract", "legal obligation", "legitimate interest", "vital interest"]
        
        score = 0.0
        text_lower = document_text.lower()
        
        for keyword in lawful_basis_keywords:
            if keyword in text_lower:
                score += 0.2
        
        return min(score, 1.0)
    
    def _check_purpose_specification(self, document_text: str, privacy_analysis: Dict) -> float:
        """Check for clear purpose specification"""
        purpose_keywords = ["purpose", "objective", "reason", "use", "processing for"]
        
        score = 0.0
        text_lower = document_text.lower()
        
        for keyword in purpose_keywords:
            if keyword in text_lower:
                score += 0.25
        
        return min(score, 1.0)

    def _check_data_minimization(self, document_text: str, privacy_analysis: Dict) -> float:
        """Check for data minimization principles"""
        minimization_keywords = ["necessary", "minimal", "required", "essential", "limited", "specific purpose"]
        
        score = 0.0
        text_lower = document_text.lower()
        
        for keyword in minimization_keywords:
            if keyword in text_lower:
                score += 0.15
        
        return min(score, 1.0)

    def _check_accuracy_requirements(self, document_text: str) -> float:
        """Check for data accuracy requirements"""
        accuracy_keywords = ["accurate", "correct", "up-to-date", "verify", "validation"]
        
        score = 0.3  # Base score
        text_lower = document_text.lower()
        
        for keyword in accuracy_keywords:
            if keyword in text_lower:
                score += 0.15
        
        return min(score, 1.0)

    def _check_storage_limitation(self, document_text: str) -> float:
        """Check for storage limitation measures"""
        storage_keywords = ["retention", "storage period", "delete", "expire", "archive"]
        
        score = 0.2  # Base score
        text_lower = document_text.lower()
        
        for keyword in storage_keywords:
            if keyword in text_lower:
                score += 0.2
        
        return min(score, 1.0)

    def _check_integrity_confidentiality(self, document_text: str) -> float:
        """Check for integrity and confidentiality measures"""
        integrity_keywords = ["security", "confidentiality", "integrity", "encrypt", "secure", "protection"]
        
        score = 0.2  # Base score
        text_lower = document_text.lower()
        
        for keyword in integrity_keywords:
            if keyword in text_lower:
                score += 0.15
        
        return min(score, 1.0)

    def _check_fair_reasonable_processing(self, document_text: str, privacy_analysis: Dict) -> float:
        """Check for fair and reasonable processing"""
        fairness_keywords = ["fair", "reasonable", "transparent", "lawful", "proportionate"]
        
        score = 0.3  # Base score
        text_lower = document_text.lower()
        
        for keyword in fairness_keywords:
            if keyword in text_lower:
                score += 0.15
        
        return min(score, 1.0)

    def _check_technical_safeguards(self, document_text: str, privacy_analysis: Dict) -> float:
        """Check for technical safeguards"""
        technical_keywords = ["encryption", "firewall", "access control", "authentication", "technical measures"]
        
        score = 0.2  # Base score
        text_lower = document_text.lower()
        
        for keyword in technical_keywords:
            if keyword in text_lower:
                score += 0.2
        
        return min(score, 1.0)

    def _check_organizational_measures(self, document_text: str) -> float:
        """Check for organizational measures"""
        org_keywords = ["policy", "procedure", "training", "staff", "organizational measures"]
        
        score = 0.2  # Base score
        text_lower = document_text.lower()
        
        for keyword in org_keywords:
            if keyword in text_lower:
                score += 0.2
        
        return min(score, 1.0)

    def _check_breach_notification_procedures(self, document_text: str) -> float:
        """Check for breach notification procedures"""
        breach_keywords = ["breach", "notification", "incident", "report", "alert"]
        
        score = 0.1  # Base score
        text_lower = document_text.lower()
        
        for keyword in breach_keywords:
            if keyword in text_lower:
                score += 0.2
        
        return min(score, 1.0)

    def _check_impact_assessment_procedures(self, document_text: str) -> float:
        """Check for impact assessment procedures"""
        impact_keywords = ["impact assessment", "privacy impact", "DPIA", "assessment", "evaluation"]
        
        score = 0.1  # Base score
        text_lower = document_text.lower()
        
        for keyword in impact_keywords:
            if keyword in text_lower:
                score += 0.2
        
        return min(score, 1.0)

    def _check_data_principal_right(self, document_text: str, right_type: str) -> float:
        """Check for specific data principal rights"""
        rights_keywords = {
            "right_to_information": ["information", "notice", "inform", "disclosure"],
            "right_to_correction": ["correct", "rectify", "update", "modify"],
            "right_to_erasure": ["delete", "erase", "remove", "forget"],
            "right_to_grievance_redressal": ["complaint", "grievance", "redressal", "appeal"],
            "right_to_nominate": ["nominate", "nomination", "representative", "delegate"]
        }
        
        keywords = rights_keywords.get(right_type, [])
        score = 0.2  # Base score
        text_lower = document_text.lower()
        
        for keyword in keywords:
            if keyword in text_lower:
                score += 0.2
        
        return min(score, 1.0)
    
    def _assess_compliance_criterion(self, criterion: str, document_text: str, privacy_analysis: Dict) -> float:
        """Assess individual compliance criterion"""
        criterion_keywords = {
            "explicit_consent": ["explicit consent", "clear consent", "unambiguous consent"],
            "informed_consent": ["informed consent", "information provided", "notice given"],
            "specific_consent": ["specific consent", "purpose-specific", "granular consent"],
            "withdrawable_consent": ["withdraw consent", "revoke consent", "opt-out"],
            "granular_consent": ["granular consent", "specific purpose", "choice"],
            "purpose_limitation": ["purpose limitation", "specific purpose", "intended use"],
            "collection_limitation": ["collection limitation", "minimal collection", "necessary data"],
            "technical_measures": ["encryption", "security", "technical safeguards"],
            "organizational_measures": ["policies", "procedures", "training"],
            "access_rights": ["access", "right to access", "data subject access"],
            "correction_rights": ["correction", "rectification", "update"],
            "erasure_rights": ["deletion", "erasure", "right to be forgotten"],
            "privacy_notice": ["privacy notice", "privacy policy", "information notice"],
            "processing_disclosure": ["processing disclosure", "data use", "purpose disclosure"]
        }
        
        keywords = criterion_keywords.get(criterion, [criterion.replace("_", " ")])
        text_lower = document_text.lower()
        
        score = 0.0
        for keyword in keywords:
            if keyword in text_lower:
                score += (1.0 / len(keywords))
        
        return min(score, 1.0)

    def _assess_puttaswamy_compliance(self, matrix_assessment: Dict) -> float:
        """Assess compliance with Puttaswamy principles"""
        principle_scores = []
        
        for category, data in matrix_assessment.items():
            principle_scores.append(data.get("assessment_score", 0))
        
        return sum(principle_scores) / len(principle_scores) if principle_scores else 0.0

    def _assess_dpdpa_constitutional_integration(self, section_compliance: Dict) -> float:
        """Assess DPDPA-Constitution integration"""
        constitutional_sections = []
        
        for section_id, section_data in section_compliance.items():
            if section_data.get("constitutional_basis"):
                constitutional_sections.append(section_data.get("compliance_score", 0))
        
        return sum(constitutional_sections) / len(constitutional_sections) if constitutional_sections else 0.5

    def _identify_constitutional_alignment_issues(self, section_compliance: Dict, matrix_assessment: Dict, privacy_analysis: Dict) -> List[str]:
        """Identify constitutional alignment issues"""
        issues = []
        
        # Check for low scoring constitutional sections
        for section_id, section_data in section_compliance.items():
            if section_data.get("constitutional_basis") and section_data.get("compliance_score", 0) < 0.6:
                issues.append(f"Low compliance in constitutionally-based {section_id}")
        
        # Check privacy analysis issues
        privacy_compliance = privacy_analysis.get("constitutional_compliance", {})
        if privacy_compliance.get("article_21_compliance") in ["non_compliant", "partially_compliant"]:
            issues.append("Article 21 privacy rights not adequately addressed")
        
        return issues[:5]  # Return top 5 issues

    def _generate_constitutional_recommendations(self, alignment_issues: List[str], article_21_compliance: Dict) -> List[str]:
        """Generate constitutional recommendations"""
        recommendations = []
        
        if alignment_issues:
            recommendations.extend([
                "Strengthen constitutional basis for data processing provisions",
                "Ensure Article 21 privacy rights are adequately protected",
                "Align data protection measures with Puttaswamy judgment principles"
            ])
        
        # Add specific recommendations based on Article 21 compliance
        if article_21_compliance.get("compliance_score", 0) < 0.7:
            recommendations.extend([
                "Implement constitutional privacy safeguards",
                "Conduct constitutional compliance review"
            ])
        
        return recommendations[:5]  # Return top 5 recommendations

    def _determine_compliance_status(self, overall_score: float) -> str:
        """Determine compliance status from score"""
        if overall_score >= 80:
            return "fully_compliant"
        elif overall_score >= 60:
            return "substantially_compliant"
        elif overall_score >= 40:
            return "partially_compliant"
        else:
            return "non_compliant"

    def _interpret_dpdpa_score(self, score: float) -> str:
        """Interpret DPDPA compliance score"""
        if score >= 80:
            return "Excellent DPDPA compliance with strong constitutional alignment"
        elif score >= 60:
            return "Good compliance with some areas for improvement"
        elif score >= 40:
            return "Moderate compliance requiring significant improvements"
        else:
            return "Poor compliance with major gaps requiring immediate attention"

    def _assign_compliance_grade(self, score: float) -> str:
        """Assign compliance grade"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"

    def _generate_compliance_error_response(self, error_message: str) -> Dict[str, Any]:
        """Generate error response for failed compliance assessment"""
        return {
            "error": True,
            "error_message": error_message,
            "dpdpa_compliance_summary": {"overall_score": 0, "error": True},
            "assessment_timestamp": datetime.now().isoformat()
        }
