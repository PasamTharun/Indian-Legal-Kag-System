"""
Advanced Graph Builder for Dynamic Knowledge Graph Construction
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import re
from .knowledge_graph.neo4j_manager import ConstitutionalKnowledgeGraph

logger = logging.getLogger(__name__)

class DynamicGraphBuilder:
    """Builds and updates knowledge graph dynamically based on new legal data"""
    
    def __init__(self):
        self.kg = ConstitutionalKnowledgeGraph()
        self.legal_entity_patterns = self._initialize_entity_patterns()
    
    def _initialize_entity_patterns(self) -> Dict[str, List[str]]:
        """Initialize regex patterns for legal entity recognition"""
        return {
            "constitutional_articles": [
                r"Article\s+(\d+)",
                r"Art\.\s*(\d+)",
                r"Section\s+(\d+)\s+of.*Constitution"
            ],
            "legal_cases": [
                r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+v\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
                r"([A-Za-z\s]+)\s+vs?\.\s+([A-Za-z\s]+)",
                r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+case"
            ],
            "dpdpa_provisions": [
                r"Section\s+(\d+).*DPDPA",
                r"DPDPA\s+Section\s+(\d+)",
                r"Data Protection.*Section\s+(\d+)"
            ],
            "privacy_concepts": [
                r"privacy\s+rights?",
                r"personal\s+data",
                r"data\s+protection",
                r"informational\s+privacy",
                r"right\s+to\s+privacy"
            ]
        }
    
    def extract_legal_entities(self, document_text: str) -> Dict[str, List[str]]:
        """Extract legal entities from document text"""
        entities = {
            "articles": [],
            "cases": [],
            "provisions": [],
            "privacy_concepts": []
        }
        
        # Extract constitutional articles
        for pattern in self.legal_entity_patterns["constitutional_articles"]:
            matches = re.findall(pattern, document_text, re.IGNORECASE)
            entities["articles"].extend([f"article_{match}" for match in matches])
        
        # Extract case names
        for pattern in self.legal_entity_patterns["legal_cases"]:
            matches = re.findall(pattern, document_text, re.IGNORECASE)
            entities["cases"].extend([f"{match[0]} v {match[1]}" for match in matches if len(match) > 1])
        
        # Extract DPDPA provisions
        for pattern in self.legal_entity_patterns["dpdpa_provisions"]:
            matches = re.findall(pattern, document_text, re.IGNORECASE)
            entities["provisions"].extend([f"dpdpa_section_{match}" for match in matches])
        
        # Extract privacy concepts
        for pattern in self.legal_entity_patterns["privacy_concepts"]:
            matches = re.findall(pattern, document_text, re.IGNORECASE)
            entities["privacy_concepts"].extend(matches)
        
        return entities
    
    def create_document_knowledge_subgraph(self, document_text: str, document_id: str) -> Dict[str, Any]:
        """Create knowledge subgraph for a specific document"""
        
        # Extract entities
        entities = self.extract_legal_entities(document_text)
        
        # Create document node
        doc_query = """
        CREATE (d:Document {
            document_id: $doc_id,
            created_at: datetime(),
            text_length: $text_length,
            entity_count: $entity_count
        })
        """
        
        self.kg.neo4j.execute_write_query(doc_query, {
            "doc_id": document_id,
            "text_length": len(document_text),
            "entity_count": sum(len(v) for v in entities.values())
        })
        
        # Link document to identified entities
        self._link_document_to_entities(document_id, entities)
        
        return {
            "document_id": document_id,
            "entities_found": entities,
            "subgraph_created": True,
            "timestamp": datetime.now().isoformat()
        }
    
    def _link_document_to_entities(self, document_id: str, entities: Dict[str, List[str]]):
        """Create relationships between document and identified entities"""
        
        # Link to constitutional articles
        for article in entities["articles"]:
            query = """
            MATCH (d:Document {document_id: $doc_id})
            MATCH (a:Article {article_id: $article_id})
            CREATE (d)-[:REFERENCES]->(a)
            """
            self.kg.neo4j.execute_write_query(query, {
                "doc_id": document_id,
                "article_id": article
            })
        
        # Link to DPDPA provisions
        for provision in entities["provisions"]:
            query = """
            MATCH (d:Document {document_id: $doc_id})
            MATCH (p:DPDPAProvision {provision_id: $provision_id})
            CREATE (d)-[:REFERENCES]->(p)
            """
            self.kg.neo4j.execute_write_query(query, {
                "doc_id": document_id,
                "provision_id": provision
            })
        
        # Create privacy concept nodes if not exist and link
        for concept in entities["privacy_concepts"]:
            concept_id = concept.lower().replace(" ", "_")
            
            # Create concept node if not exists
            concept_query = """
            MERGE (pc:PrivacyConcept {concept_id: $concept_id})
            ON CREATE SET pc.name = $concept_name, pc.created_at = datetime()
            """
            self.kg.neo4j.execute_write_query(concept_query, {
                "concept_id": concept_id,
                "concept_name": concept
            })
            
            # Link document to concept
            link_query = """
            MATCH (d:Document {document_id: $doc_id})
            MATCH (pc:PrivacyConcept {concept_id: $concept_id})
            CREATE (d)-[:DISCUSSES]->(pc)
            """
            self.kg.neo4j.execute_write_query(link_query, {
                "doc_id": document_id,
                "concept_id": concept_id
            })
    
    def update_graph_with_new_case(self, case_data: Dict[str, Any]) -> bool:
        """Add new legal case to knowledge graph"""
        try:
            query = """
            CREATE (c:Case:LegalPrecedent {
                case_id: $case_id,
                name: $name,
                year: $year,
                citation: $citation,
                court: $court,
                significance: $significance,
                privacy_relevance: $privacy_relevance,
                added_date: datetime()
            })
            """
            
            self.kg.neo4j.execute_write_query(query, case_data)
            
            # Create relationships to relevant articles
            if "related_articles" in case_data:
                for article_num in case_data["related_articles"]:
                    rel_query = """
                    MATCH (c:Case {case_id: $case_id})
                    MATCH (a:Article {number: $article_num})
                    CREATE (c)-[:INTERPRETS]->(a)
                    """
                    self.kg.neo4j.execute_write_query(rel_query, {
                        "case_id": case_data["case_id"],
                        "article_num": article_num
                    })
            
            logger.info(f"✅ Added new case: {case_data['name']}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to add case: {str(e)}")
            return False
    
    def analyze_graph_evolution(self) -> Dict[str, Any]:
        """Analyze how knowledge graph has evolved"""
        evolution_query = """
        MATCH (n)
        WHERE n.created_at IS NOT NULL OR n.added_date IS NOT NULL
        RETURN 
            labels(n)[0] as node_type,
            count(n) as count,
            min(coalesce(n.created_at, n.added_date)) as earliest,
            max(coalesce(n.created_at, n.added_date)) as latest
        ORDER BY node_type
        """
        
        results = self.kg.neo4j.execute_query(evolution_query)
        
        return {
            "evolution_stats": results,
            "total_dynamic_nodes": sum(r["count"] for r in results),
            "analysis_timestamp": datetime.now().isoformat()
        }
