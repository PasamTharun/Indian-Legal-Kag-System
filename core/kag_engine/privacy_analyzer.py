"""

Article 21 Privacy Rights Specialized Analyzer - Complete Updated Version

Enhanced with comprehensive privacy analysis framework

"""

import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from .knowledge_graph.neo4j_manager import ConstitutionalKnowledgeGraph

logger = logging.getLogger(__name__)

class Article21PrivacyAnalyzer:
    """Specialized analyzer for Article 21 privacy rights implications"""

    def __init__(self):
        try:
            self.kg = ConstitutionalKnowledgeGraph()
        except Exception as e:
            logger.warning(f"Knowledge graph not available: {str(e)}")
            self.kg = None
            
        self.privacy_keywords = self._initialize_privacy_keywords()
        self.privacy_categories = self._initialize_privacy_categories()
        self.puttaswamy_principles = self._initialize_puttaswamy_principles()

    def _initialize_privacy_keywords(self) -> Dict[str, List[str]]:
        """Initialize privacy-related keywords for detection"""
        return {
            "personal_data": [
                "personal information", "personal data", "individual data",
                "private information", "confidential data", "sensitive data",
                "biometric data", "genetic data", "health data", "financial data",
                "behavioral data", "location data", "communication data"
            ],
            "data_processing": [
                "data collection", "data processing", "data storage", "data sharing",
                "data transfer", "data analysis", "data mining", "profiling",
                "automated decision making", "algorithmic processing",
                "data aggregation", "data linking", "data matching"
            ],
            "consent_related": [
                "consent", "authorization", "permission", "approval",
                "opt-in", "opt-out", "withdraw consent", "explicit consent",
                "informed consent", "free consent", "specific consent",
                "granular consent", "consent management"
            ],
            "surveillance": [
                "surveillance", "monitoring", "tracking", "observation",
                "recording", "interception", "eavesdropping", "wiretapping",
                "location tracking", "behavioral monitoring", "cctv",
                "facial recognition", "biometric surveillance"
            ],
            "data_rights": [
                "right to access", "right to rectification", "right to erasure",
                "right to portability", "right to be forgotten", "data subject rights",
                "right to object", "right to restrict processing",
                "right to information", "right to correction"
            ]
        }

    def _initialize_privacy_categories(self) -> Dict[str, Dict[str, Any]]:
        """Initialize privacy categories as per Puttaswamy judgment"""
        return {
            "informational_privacy": {
                "description": "Control over personal information and its disclosure",
                "constitutional_basis": "Article 21",
                "scope": ["personal data", "information disclosure", "data sharing", "data processing"],
                "dpdpa_sections": ["section_3", "section_5", "section_8"],
                "puttaswamy_reference": "Privacy of information and the right to control dissemination of personal information",
                "keywords": ["personal data", "information", "disclosure", "sharing", "processing"]
            },
            "bodily_privacy": {
                "description": "Protection of physical self from unauthorized intrusion",
                "constitutional_basis": "Article 21",
                "scope": ["physical examination", "medical procedures", "biometric collection", "body searches"],
                "dpdpa_sections": ["section_5"],
                "puttaswamy_reference": "Bodily integrity and protection from physical intrusion",
                "keywords": ["biometric", "physical", "medical", "body", "examination"]
            },
            "communications_privacy": {
                "description": "Privacy of communications and correspondence",
                "constitutional_basis": "Article 21",
                "scope": ["phone calls", "emails", "messages", "correspondence", "communications"],
                "dpdpa_sections": ["section_5", "section_8"],
                "puttaswamy_reference": "Privacy of communication and correspondence",
                "keywords": ["communication", "correspondence", "messages", "calls", "emails"]
            },
            "territorial_privacy": {
                "description": "Protection of private spaces",
                "constitutional_basis": "Article 21",
                "scope": ["home", "private property", "personal space", "premises"],
                "dpdpa_sections": [],
                "puttaswamy_reference": "Spatial privacy and sanctity of private spaces",
                "keywords": ["home", "premises", "property", "space", "territory"]
            }
        }

    def _initialize_puttaswamy_principles(self) -> List[Dict[str, Any]]:
        """Initialize key principles from Puttaswamy judgment"""
        return [
            {
                "principle": "Privacy as Fundamental Right",
                "description": "Privacy is protected as an intrinsic part of the right to life and personal liberty under Article 21",
                "legal_test": "Three-fold test: legitimate government aim, necessity, and proportionality",
                "implications": ["Data protection laws must meet constitutional standards", "Privacy cannot be compromised arbitrarily"],
                "keywords": ["fundamental right", "article 21", "constitutional protection"]
            },
            {
                "principle": "Informational Self-Determination",
                "description": "Individuals must have control over their personal information",
                "legal_test": "Consent-based processing with legitimate purpose",
                "implications": ["Meaningful consent required", "Purpose limitation necessary"],
                "keywords": ["control", "consent", "self-determination", "autonomy"]
            },
            {
                "principle": "Data Minimization",
                "description": "Collection and processing must be limited to what is necessary",
                "legal_test": "Proportionality test",
                "implications": ["Excessive data collection violates privacy", "Storage limitation required"],
                "keywords": ["minimization", "necessary", "proportional", "limited"]
            },
            {
                "principle": "Transparency and Accountability",
                "description": "Data processing must be transparent and accountable",
                "legal_test": "Clear disclosure of processing activities",
                "implications": ["Privacy notices required", "Data protection impact assessments necessary"],
                "keywords": ["transparency", "accountability", "disclosure", "notice"]
            }
        ]

    def analyze_privacy_implications(self, document_text: str) -> Dict[str, Any]:
        """Comprehensive privacy analysis under Article 21 framework"""
        logger.info("🔒 Starting Article 21 privacy analysis...")

        try:
            # Step 1: Extract privacy-related clauses
            privacy_clauses = self._extract_privacy_clauses(document_text)

            # Step 2: Categorize privacy implications
            privacy_categorization = self._categorize_privacy_implications(privacy_clauses, document_text)

            # Step 3: Apply Puttaswamy principles
            puttaswamy_analysis = self._apply_puttaswamy_principles(privacy_clauses, document_text)

            # Step 4: Analyze constitutional compliance
            constitutional_compliance = self._analyze_constitutional_privacy_compliance(
                privacy_clauses, privacy_categorization, puttaswamy_analysis
            )

            # Step 5: Generate DPDPA mapping
            dpdpa_mapping = self._map_to_dpdpa_provisions(privacy_categorization)

            # Step 6: Calculate privacy risk score
            privacy_risk_score = self._calculate_privacy_risk_score(
                privacy_clauses, constitutional_compliance, dpdpa_mapping
            )

            # Step 7: Generate constitutional reasoning pathway
            constitutional_pathway = self._trace_constitutional_privacy_pathway(privacy_categorization)

            return {
                "privacy_clauses": privacy_clauses,
                "privacy_categorization": privacy_categorization,
                "puttaswamy_analysis": puttaswamy_analysis,
                "constitutional_compliance": constitutional_compliance,
                "dpdpa_mapping": dpdpa_mapping,
                "privacy_risk_score": privacy_risk_score,
                "constitutional_pathway": constitutional_pathway,
                "analysis_timestamp": datetime.now().isoformat(),
                "article_21_compliance": self._assess_article_21_compliance(constitutional_compliance)
            }

        except Exception as e:
            logger.error(f"❌ Privacy analysis failed: {str(e)}")
            return self._generate_privacy_error_response(str(e))

    def _extract_privacy_clauses(self, document_text: str) -> List[Dict[str, Any]]:
        """Extract privacy-related clauses from document"""
        privacy_clauses = []
        sentences = document_text.split('.')

        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if len(sentence) < 10:  # Skip very short sentences
                continue

            clause_analysis = {
                "sentence_id": i,
                "text": sentence,
                "privacy_keywords": [],
                "privacy_categories": [],
                "intensity_score": 0.0,
                "clause_type": "general"
            }

            # Check for privacy keywords
            for category, keywords in self.privacy_keywords.items():
                found_keywords = []
                for keyword in keywords:
                    if keyword.lower() in sentence.lower():
                        found_keywords.append(keyword)
                        clause_analysis["intensity_score"] += 0.1

                if found_keywords:
                    clause_analysis["privacy_keywords"].extend(found_keywords)
                    clause_analysis["privacy_categories"].append(category)

            # Determine clause type
            if clause_analysis["privacy_keywords"]:
                clause_analysis["clause_type"] = self._determine_clause_type(sentence, clause_analysis["privacy_keywords"])

            # Only include clauses with privacy relevance
            if clause_analysis["intensity_score"] > 0:
                privacy_clauses.append(clause_analysis)

        # Sort by intensity score
        privacy_clauses.sort(key=lambda x: x["intensity_score"], reverse=True)
        return privacy_clauses[:20]  # Return top 20 most relevant clauses

    def _determine_clause_type(self, sentence: str, keywords: List[str]) -> str:
        """Determine the type of privacy clause"""
        sentence_lower = sentence.lower()
        
        if any(kw in sentence_lower for kw in ["consent", "authorization", "permission"]):
            return "consent_clause"
        elif any(kw in sentence_lower for kw in ["collect", "process", "store"]):
            return "data_processing_clause"
        elif any(kw in sentence_lower for kw in ["share", "transfer", "disclose"]):
            return "data_sharing_clause"
        elif any(kw in sentence_lower for kw in ["right", "access", "rectify", "delete"]):
            return "rights_clause"
        elif any(kw in sentence_lower for kw in ["security", "protect", "safeguard"]):
            return "security_clause"
        else:
            return "general_privacy_clause"

    def _categorize_privacy_implications(self, privacy_clauses: List[Dict], document_text: str) -> Dict[str, Any]:
        """Categorize privacy implications according to Puttaswamy framework"""
        categorization = {
            "informational_privacy": {"score": 0.0, "clauses": [], "implications": []},
            "bodily_privacy": {"score": 0.0, "clauses": [], "implications": []},
            "communications_privacy": {"score": 0.0, "clauses": [], "implications": []},
            "territorial_privacy": {"score": 0.0, "clauses": [], "implications": []},
            "overall_privacy_impact": "low"
        }

        for clause in privacy_clauses:
            clause_text = clause["text"].lower()

            # Check against each privacy category
            for category_name, category_info in self.privacy_categories.items():
                category_score = 0.0
                category_implications = []

                # Check scope keywords
                for scope_item in category_info["scope"]:
                    if scope_item.lower() in clause_text:
                        category_score += 0.3
                        category_implications.append(f"Affects {scope_item}")

                # Check category-specific keywords
                for keyword in category_info["keywords"]:
                    if keyword.lower() in clause_text:
                        category_score += 0.2

                # Check privacy keywords relevance
                for keyword_category in clause["privacy_categories"]:
                    if self._is_keyword_category_relevant_to_privacy_category(keyword_category, category_name):
                        category_score += 0.2
                        category_implications.append(f"Related to {keyword_category}")

                if category_score > 0:
                    categorization[category_name]["score"] += category_score
                    categorization[category_name]["clauses"].append({
                        "clause_id": clause["sentence_id"],
                        "text": clause["text"],
                        "relevance_score": category_score
                    })
                    categorization[category_name]["implications"].extend(category_implications)

        # Determine overall privacy impact
        total_score = sum(cat["score"] for cat in categorization.values() if isinstance(cat, dict) and "score" in cat)
        if total_score > 3.0:
            categorization["overall_privacy_impact"] = "critical"
        elif total_score > 2.0:
            categorization["overall_privacy_impact"] = "high"
        elif total_score > 1.0:
            categorization["overall_privacy_impact"] = "medium"
        else:
            categorization["overall_privacy_impact"] = "low"

        return categorization

    def _is_keyword_category_relevant_to_privacy_category(self, keyword_category: str, privacy_category: str) -> bool:
        """Check if keyword category is relevant to privacy category"""
        relevance_mapping = {
            "informational_privacy": ["personal_data", "data_processing", "data_rights"],
            "bodily_privacy": ["personal_data", "surveillance"],
            "communications_privacy": ["personal_data", "data_processing", "surveillance"],
            "territorial_privacy": ["surveillance"]
        }
        return keyword_category in relevance_mapping.get(privacy_category, [])

    def _apply_puttaswamy_principles(self, privacy_clauses: List[Dict], document_text: str) -> Dict[str, Any]:
        """Apply Puttaswamy judgment principles to document analysis"""
        principle_analysis = {}

        for principle in self.puttaswamy_principles:
            principle_name = principle["principle"]
            analysis = {
                "principle": principle_name,
                "description": principle["description"],
                "compliance_status": "unknown",
                "compliance_score": 0.0,
                "evidence": [],
                "violations": [],
                "recommendations": []
            }

            # Analyze compliance for each principle
            if principle_name == "Privacy as Fundamental Right":
                analysis = self._analyze_fundamental_right_compliance(analysis, privacy_clauses, document_text)
            elif principle_name == "Informational Self-Determination":
                analysis = self._analyze_self_determination_compliance(analysis, privacy_clauses, document_text)
            elif principle_name == "Data Minimization":
                analysis = self._analyze_minimization_compliance(analysis, privacy_clauses, document_text)
            elif principle_name == "Transparency and Accountability":
                analysis = self._analyze_transparency_compliance(analysis, privacy_clauses, document_text)

            principle_analysis[principle_name] = analysis

        return principle_analysis

    def _analyze_fundamental_right_compliance(self, analysis: Dict, privacy_clauses: List[Dict], document_text: str) -> Dict:
        """Analyze compliance with privacy as fundamental right"""
        score = 0.5  # Base score
        evidence = []
        violations = []
        recommendations = []

        # Check for constitutional references
        if "article 21" in document_text.lower() or "fundamental right" in document_text.lower():
            score += 0.3
            evidence.append("Document references constitutional privacy rights")
        else:
            violations.append("No reference to constitutional basis of privacy rights")
            recommendations.append("Include reference to Article 21 and constitutional privacy framework")

        # Check for privacy protection measures
        protection_terms = ["protect", "safeguard", "secure", "privacy policy", "data protection"]
        protection_count = sum(1 for term in protection_terms if term in document_text.lower())
        
        if protection_count >= 3:
            score += 0.2
            evidence.append("Multiple privacy protection measures mentioned")
        elif protection_count >= 1:
            score += 0.1
        else:
            violations.append("Insufficient privacy protection measures")
            recommendations.append("Implement comprehensive privacy protection measures")

        analysis.update({
            "compliance_score": min(1.0, score),
            "compliance_status": "compliant" if score >= 0.7 else "non_compliant" if score < 0.4 else "partially_compliant",
            "evidence": evidence,
            "violations": violations,
            "recommendations": recommendations
        })

        return analysis

    def _analyze_self_determination_compliance(self, analysis: Dict, privacy_clauses: List[Dict], document_text: str) -> Dict:
        """Analyze compliance with informational self-determination"""
        score = 0.4  # Base score
        evidence = []
        violations = []
        recommendations = []

        # Check for consent mechanisms
        consent_terms = ["consent", "choice", "control", "opt-in", "opt-out"]
        consent_mentions = sum(1 for term in consent_terms if term in document_text.lower())
        
        if consent_mentions >= 3:
            score += 0.4
            evidence.append("Multiple consent and control mechanisms mentioned")
        elif consent_mentions >= 1:
            score += 0.2
            evidence.append("Some consent mechanisms present")
        else:
            violations.append("No clear consent mechanisms identified")
            recommendations.append("Implement clear consent collection and management procedures")

        # Check for user control features
        control_terms = ["withdraw", "modify", "update", "delete", "access"]
        control_count = sum(1 for term in control_terms if term in document_text.lower())
        
        if control_count >= 2:
            score += 0.2
            evidence.append("User control features mentioned")
        else:
            violations.append("Limited user control over personal information")
            recommendations.append("Provide comprehensive user control mechanisms")

        analysis.update({
            "compliance_score": min(1.0, score),
            "compliance_status": "compliant" if score >= 0.7 else "non_compliant" if score < 0.4 else "partially_compliant",
            "evidence": evidence,
            "violations": violations,
            "recommendations": recommendations
        })

        return analysis

    def _analyze_minimization_compliance(self, analysis: Dict, privacy_clauses: List[Dict], document_text: str) -> Dict:
        """Analyze compliance with data minimization principle"""
        score = 0.3  # Base score
        evidence = []
        violations = []
        recommendations = []

        # Check for minimization language
        minimization_terms = ["necessary", "required", "essential", "minimum", "limited", "specific purpose"]
        minimization_count = sum(1 for term in minimization_terms if term in document_text.lower())
        
        if minimization_count >= 3:
            score += 0.4
            evidence.append("Data minimization language present")
        elif minimization_count >= 1:
            score += 0.2
        else:
            violations.append("No data minimization principles mentioned")
            recommendations.append("Implement data minimization practices")

        # Check for retention limitations
        retention_terms = ["retention", "storage period", "delete after", "expire"]
        if any(term in document_text.lower() for term in retention_terms):
            score += 0.3
            evidence.append("Data retention limitations mentioned")
        else:
            violations.append("No data retention limitations specified")
            recommendations.append("Define clear data retention and deletion policies")

        analysis.update({
            "compliance_score": min(1.0, score),
            "compliance_status": "compliant" if score >= 0.7 else "non_compliant" if score < 0.4 else "partially_compliant",
            "evidence": evidence,
            "violations": violations,
            "recommendations": recommendations
        })

        return analysis

    def _analyze_transparency_compliance(self, analysis: Dict, privacy_clauses: List[Dict], document_text: str) -> Dict:
        """Analyze compliance with transparency and accountability"""
        score = 0.4  # Base score
        evidence = []
        violations = []
        recommendations = []

        # Check for transparency measures
        transparency_terms = ["notice", "inform", "disclose", "transparency", "privacy policy"]
        transparency_count = sum(1 for term in transparency_terms if term in document_text.lower())
        
        if transparency_count >= 3:
            score += 0.3
            evidence.append("Multiple transparency measures mentioned")
        elif transparency_count >= 1:
            score += 0.2
        else:
            violations.append("Insufficient transparency measures")
            recommendations.append("Implement comprehensive privacy notices and transparency measures")

        # Check for accountability measures
        accountability_terms = ["responsible", "accountable", "audit", "review", "compliance"]
        accountability_count = sum(1 for term in accountability_terms if term in document_text.lower())
        
        if accountability_count >= 2:
            score += 0.3
            evidence.append("Accountability measures present")
        else:
            violations.append("Limited accountability mechanisms")
            recommendations.append("Establish clear accountability and audit mechanisms")

        analysis.update({
            "compliance_score": min(1.0, score),
            "compliance_status": "compliant" if score >= 0.7 else "non_compliant" if score < 0.4 else "partially_compliant",
            "evidence": evidence,
            "violations": violations,
            "recommendations": recommendations
        })

        return analysis

    def _analyze_constitutional_privacy_compliance(self, privacy_clauses: List[Dict], categorization: Dict, puttaswamy_analysis: Dict) -> Dict[str, Any]:
        """Analyze constitutional compliance of privacy provisions"""
        compliance_analysis = {
            "article_21_compliance": "unknown",
            "constitutional_test_results": {},
            "compliance_score": 0.0,
            "critical_issues": [],
            "recommendations": [],
            "legal_precedents": []
        }

        # Apply three-fold constitutional test from Puttaswamy
        test_results = self._apply_constitutional_test(privacy_clauses, categorization)
        compliance_analysis["constitutional_test_results"] = test_results

        # Calculate compliance score based on test results
        test_scores = [result.get("score", 0) for result in test_results.values()]
        compliance_analysis["compliance_score"] = sum(test_scores) / len(test_scores) if test_scores else 0.0

        # Determine overall compliance status
        if compliance_analysis["compliance_score"] >= 0.8:
            compliance_analysis["article_21_compliance"] = "compliant"
        elif compliance_analysis["compliance_score"] >= 0.6:
            compliance_analysis["article_21_compliance"] = "partially_compliant"
        else:
            compliance_analysis["article_21_compliance"] = "non_compliant"

        # Identify critical issues
        compliance_analysis["critical_issues"] = self._identify_privacy_critical_issues(
            privacy_clauses, test_results, puttaswamy_analysis
        )

        # Generate recommendations
        compliance_analysis["recommendations"] = self._generate_privacy_recommendations(
            compliance_analysis["critical_issues"], test_results
        )

        # Add relevant legal precedents
        compliance_analysis["legal_precedents"] = self._get_relevant_privacy_precedents()

        return compliance_analysis

    def _apply_constitutional_test(self, privacy_clauses: List[Dict], categorization: Dict) -> Dict[str, Any]:
        """Apply three-fold constitutional test: legitimate aim, necessity, proportionality"""
        return {
            "legitimate_government_aim": {
                "test": "Does the privacy limitation serve a legitimate government purpose?",
                "score": self._assess_legitimate_aim(privacy_clauses),
                "reasoning": self._explain_legitimate_aim_assessment(privacy_clauses)
            },
            "necessity": {
                "test": "Is the privacy limitation necessary to achieve the legitimate aim?",
                "score": self._assess_necessity(privacy_clauses, categorization),
                "reasoning": self._explain_necessity_assessment(privacy_clauses)
            },
            "proportionality": {
                "test": "Is the privacy limitation proportionate to the aim sought to be achieved?",
                "score": self._assess_proportionality(privacy_clauses, categorization),
                "reasoning": self._explain_proportionality_assessment(privacy_clauses)
            }
        }

    def _assess_legitimate_aim(self, privacy_clauses: List[Dict]) -> float:
        """Assess whether privacy limitations serve legitimate purpose"""
        legitimate_purposes = [
            "security", "safety", "law enforcement", "public health", 
            "regulatory compliance", "fraud prevention", "service provision"
        ]
        
        purpose_mentions = 0
        total_clauses = max(len(privacy_clauses), 1)
        
        for clause in privacy_clauses:
            clause_text = clause["text"].lower()
            for purpose in legitimate_purposes:
                if purpose in clause_text:
                    purpose_mentions += 1
                    break
        
        return min(1.0, (purpose_mentions / total_clauses) + 0.3)

    def _assess_necessity(self, privacy_clauses: List[Dict], categorization: Dict) -> float:
        """Assess necessity of privacy limitations"""
        necessity_indicators = ["necessary", "required", "essential", "mandatory", "needed"]
        
        necessity_mentions = 0
        for clause in privacy_clauses:
            clause_text = clause["text"].lower()
            if any(indicator in clause_text for indicator in necessity_indicators):
                necessity_mentions += 1
        
        total_clauses = max(len(privacy_clauses), 1)
        base_score = necessity_mentions / total_clauses
        
        # Adjust based on privacy impact
        privacy_impact = categorization.get("overall_privacy_impact", "low")
        impact_adjustment = {
            "critical": -0.2,
            "high": -0.1,
            "medium": 0.0,
            "low": 0.1
        }.get(privacy_impact, 0.0)
        
        return min(1.0, max(0.0, base_score + 0.4 + impact_adjustment))

    def _assess_proportionality(self, privacy_clauses: List[Dict], categorization: Dict) -> float:
        """Assess proportionality of privacy limitations"""
        proportionality_indicators = ["proportionate", "reasonable", "appropriate", "balanced"]
        
        proportionality_mentions = 0
        for clause in privacy_clauses:
            clause_text = clause["text"].lower()
            if any(indicator in clause_text for indicator in proportionality_indicators):
                proportionality_mentions += 1
        
        # Base score from mentions
        total_clauses = max(len(privacy_clauses), 1)
        base_score = (proportionality_mentions / total_clauses) + 0.5
        
        # Adjust based on privacy categories affected
        categories_affected = sum(1 for cat, data in categorization.items() 
                                if isinstance(data, dict) and data.get("score", 0) > 0)
        
        if categories_affected > 3:
            base_score -= 0.2  # More categories affected = less proportionate
        elif categories_affected <= 1:
            base_score += 0.2  # Fewer categories = more proportionate
            
        return min(1.0, max(0.0, base_score))

    def _explain_legitimate_aim_assessment(self, privacy_clauses: List[Dict]) -> str:
        """Explain legitimate aim assessment"""
        return "Assessment based on identification of legitimate purposes for privacy-related provisions in the document."

    def _explain_necessity_assessment(self, privacy_clauses: List[Dict]) -> str:
        """Explain necessity assessment"""
        return "Assessment based on explicit necessity language and justification for privacy limitations."

    def _explain_proportionality_assessment(self, privacy_clauses: List[Dict]) -> str:
        """Explain proportionality assessment"""
        return "Assessment based on balance between privacy limitations and legitimate aims, considering scope of impact."

    def _map_to_dpdpa_provisions(self, categorization: Dict) -> Dict[str, Any]:
        """Map privacy categories to DPDPA provisions"""
        dpdpa_mapping = {
            "relevant_sections": [],
            "compliance_requirements": [],
            "implementation_notes": []
        }

        for category, data in categorization.items():
            if isinstance(data, dict) and data.get("score", 0) > 0:
                if category in self.privacy_categories:
                    sections = self.privacy_categories[category].get("dpdpa_sections", [])
                    dpdpa_mapping["relevant_sections"].extend(sections)

        # Remove duplicates and sort
        dpdpa_mapping["relevant_sections"] = sorted(list(set(dpdpa_mapping["relevant_sections"])))

        # Add compliance requirements based on sections
        for section in dpdpa_mapping["relevant_sections"]:
            if section == "section_5":
                dpdpa_mapping["compliance_requirements"].append("Establish lawful basis for processing")
            elif section == "section_8":
                dpdpa_mapping["compliance_requirements"].append("Implement data fiduciary obligations")

        return dpdpa_mapping

    def _calculate_privacy_risk_score(self, privacy_clauses: List[Dict], constitutional_compliance: Dict, dpdpa_mapping: Dict) -> Dict[str, Any]:
        """Calculate overall privacy risk score"""
        # Base risk calculation
        constitutional_score = constitutional_compliance.get("compliance_score", 0)
        
        # Risk factors
        high_risk_keywords = ["surveillance", "monitoring", "tracking", "profiling", "automated decision"]
        risk_mentions = 0
        
        for clause in privacy_clauses:
            clause_text = clause["text"].lower()
            for keyword in high_risk_keywords:
                if keyword in clause_text:
                    risk_mentions += 1
                    break

        # Calculate risk score (inverted - higher compliance = lower risk)
        base_risk = 1.0 - constitutional_score
        risk_adjustment = min(0.3, risk_mentions * 0.1)
        overall_risk = min(1.0, base_risk + risk_adjustment)

        return {
            "overall_score": round((1.0 - overall_risk) * 100, 2),  # Convert to compliance percentage
            "risk_level": "high" if overall_risk > 0.7 else "medium" if overall_risk > 0.4 else "low",
            "constitutional_component": round(constitutional_score * 100, 2),
            "risk_factors": risk_mentions,
            "calculation_timestamp": datetime.now().isoformat()
        }

    def _trace_constitutional_privacy_pathway(self, categorization: Dict) -> List[Dict[str, Any]]:
        """Trace constitutional reasoning pathway for privacy analysis"""
        pathway = []

        # Step 1: Constitutional source
        pathway.append({
            "step": 1,
            "constitutional_provision": "Article 21",
            "principle": "Right to Life and Personal Liberty",
            "reasoning": "Article 21 protects life and personal liberty, which includes the right to privacy as established in Puttaswamy judgment"
        })

        # Step 2: Privacy right establishment
        pathway.append({
            "step": 2,
            "constitutional_provision": "Article 21 (interpreted)",
            "principle": "Right to Privacy as Fundamental Right",
            "reasoning": "In Puttaswamy v Union of India (2017), the Supreme Court established privacy as an intrinsic part of Article 21",
            "case_reference": "Justice K.S. Puttaswamy (Retd.) v. Union of India, (2017) 10 SCC 1"
        })

        # Step 3: Privacy categorization
        for category, data in categorization.items():
            if isinstance(data, dict) and data.get("score", 0) > 0.5:
                category_info = self.privacy_categories.get(category, {})
                pathway.append({
                    "step": len(pathway) + 1,
                    "constitutional_provision": "Article 21 (privacy dimensions)",
                    "principle": category_info.get("description", category),
                    "reasoning": f"Document provisions affect {category}, which is protected under Article 21 privacy framework",
                    "dpdpa_connection": category_info.get("dpdpa_sections", [])
                })

        # Step 4: DPDPA implementation
        pathway.append({
            "step": len(pathway) + 1,
            "constitutional_provision": "DPDPA 2023",
            "principle": "Statutory Implementation of Privacy Rights",
            "reasoning": "DPDPA 2023 implements constitutional privacy rights through specific data protection provisions",
            "implementation_note": "DPDPA provisions must comply with Article 21 privacy standards established in Puttaswamy"
        })

        return pathway

    def _identify_privacy_critical_issues(self, privacy_clauses: List[Dict], test_results: Dict, puttaswamy_analysis: Dict) -> List[str]:
        """Identify critical privacy issues"""
        critical_issues = []

        # Check constitutional test failures
        for test_name, test_data in test_results.items():
            if test_data.get("score", 0) < 0.5:
                critical_issues.append(f"Failed {test_name} constitutional test")

        # Check Puttaswamy principle violations
        for principle_name, principle_data in puttaswamy_analysis.items():
            if principle_data.get("compliance_score", 0) < 0.4:
                critical_issues.append(f"Non-compliance with {principle_name}")
            
            violations = principle_data.get("violations", [])
            critical_issues.extend(violations[:2])  # Add top 2 violations

        return critical_issues[:5]  # Return top 5 critical issues

    def _generate_privacy_recommendations(self, critical_issues: List[str], test_results: Dict) -> List[str]:
        """Generate privacy compliance recommendations"""
        recommendations = []

        # Address constitutional test failures
        for test_name, test_data in test_results.items():
            if test_data.get("score", 0) < 0.6:
                if test_name == "legitimate_government_aim":
                    recommendations.append("Clearly establish legitimate purposes for privacy-affecting provisions")
                elif test_name == "necessity":
                    recommendations.append("Demonstrate necessity of privacy limitations for achieving stated aims")
                elif test_name == "proportionality":
                    recommendations.append("Ensure privacy limitations are proportionate to legitimate aims")

        # General recommendations
        if len(critical_issues) > 0:
            recommendations.extend([
                "Conduct comprehensive privacy impact assessment",
                "Implement privacy-by-design principles",
                "Establish clear consent mechanisms",
                "Define data minimization practices",
                "Create transparent privacy notices"
            ])

        return recommendations[:7]  # Return top 7 recommendations

    def _get_relevant_privacy_precedents(self) -> List[Dict[str, str]]:
        """Get relevant privacy legal precedents"""
        return [
            {
                "case_name": "Justice K.S. Puttaswamy (Retd.) v. Union of India",
                "year": "2017",
                "significance": "Established privacy as fundamental right under Article 21",
                "relevance": "Constitutional foundation for privacy rights"
            },
            {
                "case_name": "Kharak Singh v. State of U.P.",
                "year": "1963",
                "significance": "Early recognition of privacy dimensions",
                "relevance": "Historical development of privacy jurisprudence"
            },
            {
                "case_name": "District Registrar and Collector v. Canara Bank",
                "year": "2005",
                "significance": "Privacy in information disclosure",
                "relevance": "Informational privacy protection"
            }
        ]

    def _assess_article_21_compliance(self, constitutional_compliance: Dict) -> str:
        """Assess overall Article 21 compliance status"""
        compliance_score = constitutional_compliance.get("compliance_score", 0)
        
        if compliance_score >= 0.8:
            return "high_compliance"
        elif compliance_score >= 0.6:
            return "moderate_compliance"
        elif compliance_score >= 0.4:
            return "low_compliance"
        else:
            return "non_compliance"

    def _generate_privacy_error_response(self, error_message: str) -> Dict[str, Any]:
        """Generate error response for failed privacy analysis"""
        return {
            "error": True,
            "error_message": error_message,
            "privacy_clauses": [],
            "constitutional_compliance": {"article_21_compliance": "error"},
            "privacy_risk_score": {"overall_score": 0, "error": True},
            "analysis_timestamp": datetime.now().isoformat()
        }
