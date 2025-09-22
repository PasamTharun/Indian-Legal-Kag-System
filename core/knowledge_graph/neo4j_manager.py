"""
Neo4j Knowledge Graph Manager for Constitutional Legal Framework
FIXED VERSION - Ready to Use
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from .neo4j_config import get_neo4j_connection
from .constitutional_articles import CONSTITUTIONAL_ARTICLES, DPDPA_PROVISIONS, LANDMARK_CASES

logger = logging.getLogger(__name__)

class ConstitutionalKnowledgeGraph:
    """Manages constitutional knowledge graph in Neo4j"""
    
    def __init__(self):
        self.neo4j = get_neo4j_connection()
        self.setup_constraints()
    
    def setup_constraints(self):
        """Create database constraints and indexes with FIXED syntax"""
        constraints = [
            "CREATE CONSTRAINT article_id IF NOT EXISTS FOR (a:Article) REQUIRE a.article_id IS UNIQUE",
            "CREATE CONSTRAINT case_id IF NOT EXISTS FOR (c:Case) REQUIRE c.case_id IS UNIQUE", 
            "CREATE CONSTRAINT provision_id IF NOT EXISTS FOR (p:DPDPAProvision) REQUIRE p.provision_id IS UNIQUE",
            "CREATE CONSTRAINT right_id IF NOT EXISTS FOR (r:FundamentalRight) REQUIRE r.right_id IS UNIQUE",
            "CREATE INDEX article_number_index IF NOT EXISTS FOR (a:Article) ON (a.number)",
            "CREATE INDEX case_year_index IF NOT EXISTS FOR (c:Case) ON (c.year)",
            "CREATE INDEX privacy_implications_index IF NOT EXISTS FOR (n:Article) ON (n.privacy_implications)",
            "CREATE INDEX dpdpa_relevance_index IF NOT EXISTS FOR (n:Article) ON (n.dpdpa_relevance)"
        ]
        
        for constraint in constraints:
            try:
                self.neo4j.execute_write_query(constraint)
            except Exception as e:
                logger.warning(f"Constraint creation warning: {e}")
    
    def initialize_constitutional_knowledge(self):
        """Initialize complete constitutional knowledge base"""
        logger.info("🏗️ Initializing Constitutional Knowledge Base...")
        
        try:
            # Clear existing data
            self.neo4j.execute_write_query("MATCH (n) DETACH DELETE n")
            
            # Create constitutional articles
            self._create_constitutional_articles()
            
            # Create landmark cases
            self._create_landmark_cases()
            
            # Create DPDPA provisions
            self._create_dpdpa_provisions()
            
            # Create relationships
            self._create_constitutional_relationships()
            
            # Create privacy-specific nodes
            self._create_privacy_framework()
            
            logger.info("✅ Constitutional Knowledge Base initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize knowledge base: {str(e)}")
            return False
    
    def _create_constitutional_articles(self):
        """Create constitutional article nodes"""
        for article_id, article_data in CONSTITUTIONAL_ARTICLES.items():
            query = """
            CREATE (a:Article:ConstitutionalProvision {
                article_id: $article_id,
                number: $number,
                title: $title,
                text: $text,
                part: $part,
                chapter: $chapter,
                privacy_implications: $privacy_implications,
                dpdpa_relevance: $dpdpa_relevance,
                landmark_cases: $landmark_cases,
                privacy_scope: $privacy_scope
            })
            """
            
            params = {
                "article_id": article_id,
                "number": article_data["number"],
                "title": article_data["title"],
                "text": article_data["text"],
                "part": article_data["part"],
                "chapter": article_data["chapter"],
                "privacy_implications": article_data["privacy_implications"],
                "dpdpa_relevance": article_data["dpdpa_relevance"],
                "landmark_cases": article_data.get("landmark_cases", []),
                "privacy_scope": article_data.get("privacy_scope", [])
            }
            
            self.neo4j.execute_write_query(query, params)
    
    def _create_landmark_cases(self):
        """Create landmark case nodes with ALL required parameters"""
        for case_id, case_data in LANDMARK_CASES.items():
            query = """
            CREATE (c:Case:LegalPrecedent {
                case_id: $case_id,
                name: $name,
                year: $year,
                citation: $citation,
                bench_size: $bench_size,
                significance: $significance,
                articles_interpreted: $articles_interpreted,
                privacy_relevance: $privacy_relevance,
                constitutional_principle: $constitutional_principle
            })
            """
            
            # Ensure all required parameters are provided
            params = {
                "case_id": case_id,
                "name": case_data.get("name", "Unknown Case"),
                "year": case_data.get("year", 2000),
                "citation": case_data.get("citation", "Citation not available"),
                "bench_size": case_data.get("bench_size", 1),
                "significance": case_data.get("significance", "Important case"),
                "articles_interpreted": case_data.get("articles_interpreted", []),
                "privacy_relevance": case_data.get("privacy_relevance", "medium"),
                "constitutional_principle": case_data.get("constitutional_principle", "Constitutional interpretation")
            }
            
            self.neo4j.execute_write_query(query, params)
    
    def _create_dpdpa_provisions(self):
        """Create DPDPA provision nodes"""
        for provision_id, provision_data in DPDPA_PROVISIONS.items():
            query = """
            CREATE (p:DPDPAProvision:Regulation {
                provision_id: $provision_id,
                title: $title,
                text: $text,
                constitutional_basis: $constitutional_basis,
                compliance_requirements: $compliance_requirements
            })
            """
            
            params = {
                "provision_id": provision_id,
                "title": provision_data.get("title", "DPDPA Provision"),
                "text": provision_data.get("text", "DPDPA provision text"),
                "constitutional_basis": provision_data.get("constitutional_basis", []),
                "compliance_requirements": provision_data.get("compliance_requirements", [])
            }
            
            self.neo4j.execute_write_query(query, params)
    
    def _create_constitutional_relationships(self):
        """Create relationships between constitutional entities"""
        
        # Article 21 -> Privacy Right
        privacy_right_query = """
        MATCH (a:Article {article_id: 'article_21'})
        CREATE (r:FundamentalRight {
            right_id: 'privacy_right',
            name: 'Right to Privacy',
            established_in: 'Puttaswamy v Union of India',
            year: 2017,
            scope: ['informational privacy', 'bodily privacy', 'communications privacy', 'territorial privacy'],
            constitutional_source: 'Article 21'
        })
        CREATE (a)-[:PROTECTS]->(r)
        """
        self.neo4j.execute_write_query(privacy_right_query)
        
        # Cases -> Articles relationships
        case_article_relationships = [
            ("kesavananda_bharati", [12, 13, 14, 19, 21]),
            ("maneka_gandhi", [14, 19, 21]),
            ("puttaswamy", [14, 19, 21])
        ]
        
        for case_id, article_numbers in case_article_relationships:
            for article_num in article_numbers:
                # Check if both nodes exist before creating relationship
                query = """
                MATCH (c:Case {case_id: $case_id})
                MATCH (a:Article {number: $article_num})
                CREATE (c)-[:INTERPRETS]->(a)
                """
                try:
                    self.neo4j.execute_write_query(query, {
                        "case_id": case_id,
                        "article_num": article_num
                    })
                except Exception as e:
                    logger.warning(f"Could not link case {case_id} to article {article_num}: {e}")
        
        # DPDPA -> Constitutional basis
        dpdpa_constitutional_links = [
            ("section_3", ["article_21"]),
            ("section_5", ["article_21", "article_14"]),
            ("section_8", ["article_21"])
        ]
        
        for provision_id, articles in dpdpa_constitutional_links:
            for article_id in articles:
                query = """
                MATCH (p:DPDPAProvision {provision_id: $provision_id})
                MATCH (a:Article {article_id: $article_id})
                CREATE (p)-[:IMPLEMENTS]->(a)
                """
                try:
                    self.neo4j.execute_write_query(query, {
                        "provision_id": provision_id,
                        "article_id": article_id
                    })
                except Exception as e:
                    logger.warning(f"Could not link provision {provision_id} to {article_id}: {e}")
    
    def _create_privacy_framework(self):
        """Create privacy-specific knowledge framework"""
        # Privacy categories
        privacy_categories = [
            ("informational_privacy", "Control over personal information and its disclosure"),
            ("bodily_privacy", "Protection of physical self from unauthorized intrusion"),
            ("communications_privacy", "Privacy of communications and correspondence"),
            ("territorial_privacy", "Protection of private spaces")
        ]
        
        for category_id, description in privacy_categories:
            query = """
            CREATE (pc:PrivacyCategory {
                category_id: $category_id,
                description: $description,
                constitutional_source: 'Article 21',
                dpdpa_relevance: 'high'
            })
            """
            self.neo4j.execute_write_query(query, {
                "category_id": category_id,
                "description": description
            })
            
            # Link to privacy right
            link_query = """
            MATCH (pc:PrivacyCategory {category_id: $category_id})
            MATCH (r:FundamentalRight {right_id: 'privacy_right'})
            CREATE (r)-[:ENCOMPASSES]->(pc)
            """
            try:
                self.neo4j.execute_write_query(link_query, {"category_id": category_id})
            except Exception as e:
                logger.warning(f"Could not link privacy category {category_id}: {e}")
    
    def find_constitutional_pathway(self, start_concept: str, end_concept: str, max_hops: int = 4) -> List[Dict]:
        """Find constitutional reasoning pathway between concepts"""
        query = """
        MATCH path = shortestPath((start)-[*1..6]-(end))
        WHERE (start.name CONTAINS $start_concept OR start.title CONTAINS $start_concept)
        AND (end.name CONTAINS $end_concept OR end.title CONTAINS $end_concept)
        RETURN path LIMIT 10
        """
        
        try:
            results = self.neo4j.execute_query(query, {
                "start_concept": start_concept,
                "end_concept": end_concept,
                "max_hops": max_hops
            })
            return results
        except Exception as e:
            logger.error(f"Pathway search failed: {e}")
            return []
    
    def get_article_context(self, article_number: int) -> Dict[str, Any]:
        """Get comprehensive context for a constitutional article"""
        query = """
        MATCH (a:Article {number: $article_number})
        OPTIONAL MATCH (a)<-[:INTERPRETS]-(c:Case)
        OPTIONAL MATCH (a)<-[:IMPLEMENTS]-(p:DPDPAProvision)
        OPTIONAL MATCH (a)-[:PROTECTS]->(r:FundamentalRight)
        RETURN a as article,
               collect(DISTINCT c) as interpreting_cases,
               collect(DISTINCT p) as implementing_provisions,
               collect(DISTINCT r) as protected_rights
        """
        
        try:
            results = self.neo4j.execute_query(query, {"article_number": article_number})
            return results[0] if results else {}
        except Exception as e:
            logger.error(f"Article context query failed: {e}")
            return {}
    
    def analyze_privacy_implications(self, document_concepts: List[str]) -> Dict[str, Any]:
        """Analyze privacy implications of document concepts using knowledge graph"""
        implications = {
            "privacy_articles": [],
            "relevant_cases": [],
            "dpdpa_provisions": [],
            "privacy_categories": [],
            "constitutional_pathways": []
        }
        
        for concept in document_concepts:
            query = """
            MATCH (n)
            WHERE (n.privacy_implications = true OR n.privacy_relevance IN ['high', 'critical'])
            AND (n.text CONTAINS $concept OR n.title CONTAINS $concept OR n.name CONTAINS $concept)
            RETURN n, labels(n) as node_types
            """
            
            try:
                results = self.neo4j.execute_query(query, {"concept": concept})
                
                for result in results:
                    node = result["n"]
                    node_types = result["node_types"]
                    
                    if "Article" in node_types:
                        implications["privacy_articles"].append(node)
                    elif "Case" in node_types:
                        implications["relevant_cases"].append(node)
                    elif "DPDPAProvision" in node_types:
                        implications["dpdpa_provisions"].append(node)
                    elif "PrivacyCategory" in node_types:
                        implications["privacy_categories"].append(node)
                        
            except Exception as e:
                logger.warning(f"Privacy analysis for concept '{concept}' failed: {e}")
        
        return implications
    
    def get_knowledge_graph_stats(self) -> Dict[str, int]:
        """Get knowledge graph statistics"""
        queries = {
            "total_nodes": "MATCH (n) RETURN count(n) as count",
            "total_relationships": "MATCH ()-[r]->() RETURN count(r) as count", 
            "articles": "MATCH (a:Article) RETURN count(a) as count",
            "cases": "MATCH (c:Case) RETURN count(c) as count",
            "dpdpa_provisions": "MATCH (p:DPDPAProvision) RETURN count(p) as count",
            "privacy_nodes": "MATCH (n) WHERE n.privacy_implications = true OR n.privacy_relevance = 'critical' RETURN count(n) as count"
        }
        
        stats = {}
        for stat_name, query in queries.items():
            try:
                result = self.neo4j.execute_query(query)
                stats[stat_name] = result[0]["count"] if result else 0
            except Exception as e:
                logger.warning(f"Stats query '{stat_name}' failed: {e}")
                stats[stat_name] = 0
        
        return stats
