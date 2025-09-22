"""
Test Neo4j Connection
"""
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

def test_connection():
    uri = os.getenv("NEO4J_URI", "neo4j://127.0.0.1:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")
    
    print(f"Testing connection to: {uri}")
    print(f"Username: {user}")
    
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        
        with driver.session() as session:
            result = session.run("RETURN 'Connection successful!' as message")
            record = result.single()
            print(f"✅ {record['message']}")
            
        # Test basic query
        with driver.session() as session:
            result = session.run("MATCH (n) RETURN count(n) as node_count")
            record = result.single()
            print(f"✅ Current nodes in database: {record['node_count']}")
            
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔌 Testing Neo4j Connection...")
    success = test_connection()
    if success:
        print("🎉 Ready to initialize knowledge graph!")
    else:
        print("❌ Fix connection issues before proceeding.")
