"""
Constitutional Reasoning Engine - Core KAG Logic
Enhanced with Complete Implementation
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import networkx as nx
from .knowledge_graph.neo4j_manager import ConstitutionalKnowledgeGraph
from .knowledge_graph.graph_builder import DynamicGraphBuilder

logger = logging.getLogger(__name__)

class ConstitutionalReasoningEngine:
    """Main reasoning engine for constitutional analysis using knowledge graphs"""
    
    def __init__(self):
        self.kg = ConstitutionalKnowledgeGraph()
        self.graph_builder = DynamicGraphBuilder()
        self.reasoning_weights = self._initialize_reasoning_weights()
    
    def _initialize_reasoning_weights(self) -> Dict[str, float]:
        """Initialize weights for different types of constitutional reasoning"""
        return {
            "fundamental_rights": 1.0,
            "privacy_implications": 0.9,
            "dpdpa_relevance": 0.8,
            "landmark_precedent": 0.85,
            "constitutional_consistency": 0.95,
            "judicial_interpretation": 0.8
        }
    
    def analyze_document_constitutionality(self, document_text: str, document_id: str = None) -> Dict[str, Any]:
        """
        Comprehensive constitutional analysis using KAG approach
        """
        if not document_id:
            document_id = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(f"🏛️ Starting constitutional analysis for document: {document_id}")
        
        try:
            # Step 1: Extract legal entities and create document subgraph
            subgraph_info = self.graph_builder.create_document_knowledge_subgraph(
                document_text, document_id
            )
            
            # Step 2: Identify constitutional articles
            constitutional_articles = self._identify_constitutional_articles(
                document_text, subgraph_info["entities_found"]
            )
            
            # Step 3: Analyze constitutional pathways
            constitutional_pathways = self._analyze_constitutional_pathways(
                constitutional_articles, document_id
            )
            
            # Step 4: Assess constitutional hierarchy and conflicts
            hierarchy_analysis = self._assess_constitutional_hierarchy(
                constitutional_pathways
            )
            
            # Step 5: Generate constitutional reasoning report
            reasoning_report = self._generate_constitutional_reasoning(
                constitutional_articles, constitutional_pathways, hierarchy_analysis
            )
            
            # Step 6: Calculate overall constitutional compliance score
            compliance_score = self._calculate_constitutional_compliance_score(
                constitutional_articles, constitutional_pathways, hierarchy_analysis
            )
            
            return {
                "document_id": document_id,
                "constitutional_articles": constitutional_articles,
                "constitutional_pathways": constitutional_pathways,
                "hierarchy_analysis": hierarchy_analysis,
                "reasoning_report": reasoning_report,
                "compliance_score": compliance_score,
                "analysis_timestamp": datetime.now().isoformat(),
                "entities_extracted": subgraph_info["entities_found"]
            }
            
        except Exception as e:
            logger.error(f"❌ Constitutional analysis failed: {str(e)}")
            return self._generate_error_response(document_id, str(e))
    
    def _identify_constitutional_articles(self, document_text: str, entities: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Identify and analyze relevant constitutional articles"""
        articles_analysis = []
        
        # Direct article references from entities
        for article_id in entities.get("articles", []):
            article_context = self.kg.get_article_context(
                int(article_id.replace("article_", ""))
            )
            
            if article_context:
                articles_analysis.append({
                    "article_id": article_id,
                    "relevance_score": self._calculate_article_relevance(
                        article_context, document_text
                    ),
                    "context": article_context,
                    "implication_type": self._determine_implication_type(
                        article_context, document_text
                    )
                })
        
        # Infer additional relevant articles through graph reasoning
        inferred_articles = self._infer_relevant_articles(document_text, entities)
        articles_analysis.extend(inferred_articles)
        
        # Sort by relevance score
        articles_analysis.sort(key=lambda x: x["relevance_score"], reverse=True)
        return articles_analysis[:10]  # Top 10 most relevant articles
    
    def _analyze_constitutional_pathways(self, articles: List[Dict[str, Any]], document_id: str) -> List[Dict[str, Any]]:
        """Analyze constitutional reasoning pathways using graph traversal"""
        pathways = []
        
        # For each identified article, find pathways to privacy and DPDPA compliance
        for article in articles:
            article_id = article["article_id"]
            
            # Find pathway to privacy rights
            privacy_pathways = self.kg.find_constitutional_pathway(
                article_id, "privacy_right", max_hops=3
            )
            
            # Find pathway to DPDPA provisions
            dpdpa_pathways = self.kg.find_constitutional_pathway(
                article_id, "section_5", max_hops=4
            )
            
            # Combine and analyze pathways
            for pathway in privacy_pathways + dpdpa_pathways:
                pathway_analysis = self._analyze_individual_pathway(pathway)
                pathway_analysis["source_article"] = article_id
                pathway_analysis["document_id"] = document_id
                pathways.append(pathway_analysis)
        
        return pathways
    
    def _analyze_individual_pathway(self, pathway_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze individual constitutional pathway"""
        if not pathway_data.get("pathway_nodes"):
            return {"error": "No pathway nodes found", "pathway_strength": 0.0}
        
        pathway_nodes = pathway_data["pathway_nodes"]
        relationship_types = pathway_data.get("relationship_types", [])
        
        # Calculate pathway strength based on node types and relationships
        pathway_strength = self._calculate_pathway_strength(pathway_nodes, relationship_types)
        
        # Generate reasoning chain
        reasoning_chain = self._generate_reasoning_chain(pathway_nodes, relationship_types)
        
        # Assess legal validity
        legal_validity = self._assess_pathway_legal_validity(pathway_nodes)
        
        return {
            "pathway_nodes": pathway_nodes,
            "relationship_types": relationship_types,
            "pathway_strength": pathway_strength,
            "reasoning_chain": reasoning_chain,
            "legal_validity": legal_validity,
            "pathway_length": len(pathway_nodes)
        }
    
    def _assess_constitutional_hierarchy(self, pathways: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess constitutional hierarchy and potential conflicts"""
        hierarchy_assessment = {
            "fundamental_rights_involved": [],
            "directive_principles_involved": [],
            "potential_conflicts": [],
            "hierarchy_compliance": True,
            "resolution_approach": []
        }
        
        # Identify different levels of constitutional provisions involved
        for pathway in pathways:
            for node in pathway.get("pathway_nodes", []):
                node_type = node.get("type", "")
                if node_type == "Article":
                    # Check if fundamental right or directive principle
                    article_num = self._extract_article_number(node.get("id", ""))
                    if 12 <= article_num <= 35:
                        hierarchy_assessment["fundamental_rights_involved"].append(article_num)
                    elif 36 <= article_num <= 51:
                        hierarchy_assessment["directive_principles_involved"].append(article_num)
        
        # Check for potential conflicts
        hierarchy_assessment["potential_conflicts"] = self._identify_constitutional_conflicts(
            hierarchy_assessment["fundamental_rights_involved"],
            hierarchy_assessment["directive_principles_involved"]
        )
        
        # Determine resolution approach
        if hierarchy_assessment["potential_conflicts"]:
            hierarchy_assessment["resolution_approach"] = self._determine_conflict_resolution(
                hierarchy_assessment["potential_conflicts"]
            )
        
        return hierarchy_assessment
    
    def _generate_constitutional_reasoning(self, articles: List[Dict], pathways: List[Dict], hierarchy: Dict) -> Dict[str, Any]:
        """Generate comprehensive constitutional reasoning report"""
        reasoning_report = {
            "executive_summary": "",
            "detailed_analysis": {},
            "key_constitutional_principles": [],
            "precedent_analysis": [],
            "compliance_recommendations": []
        }
        
        # Generate executive summary
        reasoning_report["executive_summary"] = self._generate_executive_summary(
            articles, pathways, hierarchy
        )
        
        # Detailed analysis for each constitutional aspect
        reasoning_report["detailed_analysis"] = {
            "article_analysis": self._generate_article_analysis(articles),
            "pathway_analysis": self._generate_pathway_analysis(pathways),
            "hierarchy_analysis": hierarchy,
            "privacy_implications": self._analyze_privacy_implications_detailed(articles, pathways)
        }
        
        # Identify key constitutional principles
        reasoning_report["key_constitutional_principles"] = self._identify_key_principles(pathways)
        
        # Precedent analysis
        reasoning_report["precedent_analysis"] = self._analyze_precedents(articles)
        
        # Compliance recommendations
        reasoning_report["compliance_recommendations"] = self._generate_compliance_recommendations(
            articles, pathways, hierarchy
        )
        
        return reasoning_report
    
    def _calculate_constitutional_compliance_score(self, articles: List[Dict], pathways: List[Dict], hierarchy: Dict) -> Dict[str, Any]:
        """Calculate overall constitutional compliance score"""
        score_components = {
            "article_compliance": 0.0,
            "pathway_strength": 0.0,
            "hierarchy_consistency": 0.0,
            "privacy_compliance": 0.0,
            "precedent_alignment": 0.0
        }
        
        # Article compliance score
        if articles:
            article_scores = [article.get("relevance_score", 0) for article in articles]
            score_components["article_compliance"] = sum(article_scores) / len(article_scores)
        
        # Pathway strength score
        if pathways:
            pathway_scores = [pathway.get("pathway_strength", 0) for pathway in pathways]
            score_components["pathway_strength"] = sum(pathway_scores) / len(pathway_scores)
        
        # Hierarchy consistency score
        score_components["hierarchy_consistency"] = 1.0 if hierarchy.get("hierarchy_compliance", False) else 0.5
        
        # Privacy compliance score (Article 21 specific)
        score_components["privacy_compliance"] = self._calculate_privacy_compliance_score(articles, pathways)
        
        # Precedent alignment score
        score_components["precedent_alignment"] = self._calculate_precedent_alignment_score(articles)
        
        # Calculate weighted overall score
        weights = {
            "article_compliance": 0.25,
            "pathway_strength": 0.20,
            "hierarchy_consistency": 0.20,
            "privacy_compliance": 0.20,
            "precedent_alignment": 0.15
        }
        
        overall_score = sum(
            score_components[component] * weight
            for component, weight in weights.items()
        )
        
        return {
            "overall_score": round(overall_score * 100, 2),  # Convert to percentage
            "component_scores": {k: round(v * 100, 2) for k, v in score_components.items()},
            "score_interpretation": self._interpret_compliance_score(overall_score * 100),
            "calculation_timestamp": datetime.now().isoformat()
        }
    
    # Helper methods implementation
    def _calculate_article_relevance(self, article_context: Dict, document_text: str) -> float:
        """Calculate relevance score for constitutional article"""
        base_score = 0.5
        
        # Boost score based on privacy implications
        if article_context.get("article", {}).get("privacy_implications", False):
            base_score += 0.3
        
        # Boost score based on DPDPA relevance
        dpdpa_relevance = article_context.get("article", {}).get("dpdpa_relevance", "low")
        if dpdpa_relevance == "critical":
            base_score += 0.4
        elif dpdpa_relevance == "high":
            base_score += 0.3
        elif dpdpa_relevance == "medium":
            base_score += 0.2
        
        return min(base_score, 1.0)
    
    def _determine_implication_type(self, article_context: Dict, document_text: str) -> str:
        """Determine type of constitutional implication"""
        article = article_context.get("article", {})
        if article.get("privacy_implications", False):
            return "privacy_rights"
        elif article.get("number", 0) in range(12, 36):
            return "fundamental_rights"
        elif article.get("number", 0) in range(36, 52):
            return "directive_principles"
        else:
            return "other_constitutional"
    
    def _infer_relevant_articles(self, document_text: str, entities: Dict) -> List[Dict]:
        """Infer additional relevant articles through contextual analysis"""
        inferred = []
        
        # If privacy concepts are mentioned, infer Article 21
        if entities.get("privacy_concepts"):
            article_context = self.kg.get_article_context(21)
            if article_context:
                inferred.append({
                    "article_id": "article_21",
                    "relevance_score": 0.8,
                    "context": article_context,
                    "implication_type": "privacy_rights",
                    "inference_reason": "Privacy concepts detected"
                })
        
        return inferred
    
    def _calculate_pathway_strength(self, pathway_nodes: List[Dict], relationship_types: List[str]) -> float:
        """Calculate strength of constitutional pathway"""
        if not pathway_nodes:
            return 0.0
        
        # Base strength inversely related to path length
        base_strength = 1.0 / len(pathway_nodes)
        
        # Boost for high-relevance nodes
        relevance_boost = 0.0
        for node in pathway_nodes:
            relevance = node.get("relevance", "medium")
            if relevance == "critical":
                relevance_boost += 0.3
            elif relevance == "high":
                relevance_boost += 0.2
            elif relevance == "medium":
                relevance_boost += 0.1
        
        # Boost for strong relationship types
        relationship_boost = 0.0
        strong_relationships = ["PROTECTS", "IMPLEMENTS", "INTERPRETS"]
        for rel_type in relationship_types:
            if rel_type in strong_relationships:
                relationship_boost += 0.1
        
        return min(1.0, base_strength + relevance_boost + relationship_boost)
    
    def _generate_reasoning_chain(self, pathway_nodes: List[Dict], relationship_types: List[str]) -> List[str]:
        """Generate reasoning chain from pathway"""
        reasoning_chain = []
        for i, node in enumerate(pathway_nodes):
            node_type = node.get("type", "Unknown")
            node_name = node.get("name", "Unknown")
            if i == 0:
                reasoning_chain.append(f"Starting from {node_type}: {node_name}")
            else:
                rel_type = relationship_types[i-1] if i-1 < len(relationship_types) else "RELATES_TO"
                reasoning_chain.append(f"{rel_type} {node_type}: {node_name}")
        return reasoning_chain
    
    def _assess_pathway_legal_validity(self, pathway_nodes: List[Dict]) -> str:
        """Assess legal validity of constitutional pathway"""
        if len(pathway_nodes) <= 2:
            return "strong"
        elif len(pathway_nodes) <= 4:
            return "moderate"
        else:
            return "weak"
    
    def _extract_article_number(self, article_id: str) -> int:
        """Extract article number from article ID"""
        try:
            return int(article_id.replace("article_", ""))
        except:
            return 0
    
    def _identify_constitutional_conflicts(self, fundamental_rights: List[int], directive_principles: List[int]) -> List[str]:
        """Identify potential constitutional conflicts"""
        conflicts = []
        
        # Check for common conflicts
        if 14 in fundamental_rights and any(dp in range(38, 48) for dp in directive_principles):
            conflicts.append("Potential conflict between equality (Art 14) and social justice directives")
        
        if 19 in fundamental_rights and 39 in directive_principles:
            conflicts.append("Potential conflict between freedom of trade and equal distribution")
        
        # Additional conflicts
        if 19 in fundamental_rights and 47 in directive_principles:
            conflicts.append("Potential conflict between freedom of trade (Art 19) and prohibition of intoxicants (Art 47)")
        
        if 21 in fundamental_rights and 47 in directive_principles:
            conflicts.append("Potential conflict between personal liberty (Art 21) and state health policies (Art 47)")
        
        if 25 in fundamental_rights and any(dp in [44, 48] for dp in directive_principles):
            conflicts.append("Potential conflict between religious freedom (Art 25) and secular education policies")
        
        return conflicts
    
    def _determine_conflict_resolution(self, conflicts: List[str]) -> List[str]:
        """Determine approaches to resolve constitutional conflicts"""
        resolutions = []
        for conflict in conflicts:
            if "equality" in conflict.lower():
                resolutions.append("Apply harmonious construction principle")
            elif "trade" in conflict.lower():
                resolutions.append("Apply proportionality test")
            else:
                resolutions.append("Apply balancing of interests approach")
        return resolutions
    
    def _generate_executive_summary(self, articles: List[Dict], pathways: List[Dict], hierarchy: Dict) -> str:
        """Generate executive summary of constitutional analysis"""
        summary = f"Constitutional analysis identified {len(articles)} relevant articles "
        summary += f"with {len(pathways)} reasoning pathways. "
        if hierarchy.get("potential_conflicts"):
            summary += f"Found {len(hierarchy['potential_conflicts'])} potential conflicts requiring resolution. "
        if any(article.get("implication_type") == "privacy_rights" for article in articles):
            summary += "Privacy rights implications identified under Article 21 framework."
        return summary
    
    def _generate_article_analysis(self, articles: List[Dict]) -> Dict[str, Any]:
        """Generate detailed article analysis"""
        return {
            "total_articles": len(articles),
            "article_breakdown": {
                "fundamental_rights": len([a for a in articles if a.get("implication_type") == "fundamental_rights"]),
                "privacy_rights": len([a for a in articles if a.get("implication_type") == "privacy_rights"]),
                "constitutional_provision": len([a for a in articles if a.get("implication_type") == "constitutional_provision"])
            },
            "highest_relevance": max([a.get("relevance_score", 0) for a in articles]) if articles else 0
        }
    
    def _generate_pathway_analysis(self, pathways: List[Dict]) -> Dict[str, Any]:
        """Generate pathway analysis summary"""
        if not pathways:
            return {"total_pathways": 0}
        
        return {
            "total_pathways": len(pathways),
            "average_strength": sum([p.get("pathway_strength", 0) for p in pathways]) / len(pathways),
            "strongest_pathway": max([p.get("pathway_strength", 0) for p in pathways]),
            "pathway_validity": {
                validity: len([p for p in pathways if p.get("legal_validity") == validity])
                for validity in ["strong", "moderate", "weak"]
            }
        }
    
    def _analyze_privacy_implications_detailed(self, articles: List[Dict], pathways: List[Dict]) -> Dict[str, Any]:
        """Detailed privacy implications analysis"""
        privacy_articles = [a for a in articles if a.get("implication_type") == "privacy_rights"]
        privacy_pathways = [p for p in pathways if "privacy" in str(p).lower()]
        
        return {
            "privacy_article_count": len(privacy_articles),
            "privacy_pathway_count": len(privacy_pathways),
            "article_21_involved": any("article_21" in a.get("article_id", "") for a in privacy_articles),
            "privacy_scope_covered": list(set([
                scope for article in privacy_articles
                for scope in article.get("context", {}).get("article", {}).get("privacy_scope", [])
            ]))
        }
    
    def _identify_key_principles(self, pathways: List[Dict]) -> List[str]:
        """Identify key constitutional principles from pathways"""
        principles = set()
        for pathway in pathways:
            for node in pathway.get("pathway_nodes", []):
                node_type = node.get("type", "")
                if node_type == "FundamentalRight":
                    principles.add("Fundamental Rights Protection")
                elif node_type == "Article" and "21" in str(node.get("id", "")):
                    principles.add("Right to Life and Personal Liberty")
                elif node_type == "Case":
                    principles.add("Judicial Precedent")
        return list(principles)
    
    def _analyze_precedents(self, articles: List[Dict]) -> List[Dict[str, Any]]:
        """Analyze relevant legal precedents"""
        precedents = []
        for article in articles:
            article_context = article.get("context", {})
            cases = article_context.get("interpreting_cases", [])
            for case in cases:
                precedents.append({
                    "case_name": case.get("name", "Unknown"),
                    "significance": case.get("significance", "Unknown"),
                    "relevance_to_article": article.get("article_id", "Unknown")
                })
        return precedents[:5]  # Top 5 most relevant
    
    def _generate_compliance_recommendations(self, articles: List[Dict], pathways: List[Dict], hierarchy: Dict) -> List[str]:
        """Generate compliance recommendations"""
        recommendations = []
        
        # Article-based recommendations
        if any(a.get("relevance_score", 0) < 0.6 for a in articles):
            recommendations.append("Strengthen constitutional basis for provisions")
        
        # Pathway-based recommendations
        weak_pathways = [p for p in pathways if p.get("pathway_strength", 0) < 0.5]
        if weak_pathways:
            recommendations.append("Reinforce constitutional reasoning pathways")
        
        # Hierarchy-based recommendations
        if hierarchy.get("potential_conflicts"):
            recommendations.append("Address constitutional conflicts through harmonious construction")
        
        return recommendations
    
    def _calculate_privacy_compliance_score(self, articles: List[Dict], pathways: List[Dict]) -> float:
        """Calculate privacy-specific compliance score"""
        privacy_articles = [a for a in articles if a.get("implication_type") == "privacy_rights"]
        if not privacy_articles:
            return 0.5  # Neutral score if no privacy articles
        
        # Average relevance score of privacy articles
        privacy_scores = [a.get("relevance_score", 0) for a in privacy_articles]
        return sum(privacy_scores) / len(privacy_scores)
    
    def _calculate_precedent_alignment_score(self, articles: List[Dict]) -> float:
        """Calculate precedent alignment score"""
        total_cases = 0
        high_significance_cases = 0
        
        for article in articles:
            cases = article.get("context", {}).get("interpreting_cases", [])
            total_cases += len(cases)
            for case in cases:
                if case.get("significance", "").lower() in ["landmark", "constitutional", "precedent"]:
                    high_significance_cases += 1
        
        if total_cases == 0:
            return 0.7  # Default score
        
        return min(1.0, high_significance_cases / total_cases + 0.3)
    
    def _interpret_compliance_score(self, score: float) -> str:
        """Interpret compliance score"""
        if score >= 80:
            return "High constitutional compliance with strong legal foundation"
        elif score >= 60:
            return "Moderate compliance with some areas for improvement"
        elif score >= 40:
            return "Low compliance requiring significant constitutional review"
        else:
            return "Poor compliance with major constitutional concerns"
    
    def _generate_error_response(self, document_id: str, error_message: str) -> Dict[str, Any]:
        """Generate error response for failed analysis"""
        return {
            "document_id": document_id,
            "error": True,
            "error_message": error_message,
            "constitutional_articles": [],
            "constitutional_pathways": [],
            "compliance_score": {"overall_score": 0, "error": True},
            "analysis_timestamp": datetime.now().isoformat()
        }
