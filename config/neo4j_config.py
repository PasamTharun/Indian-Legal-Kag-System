"""
Neo4j Database Configuration - FIXED VERSION (No Invalid Config Keys)
"""

import os
import logging
from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional
import streamlit as st
import time

logger = logging.getLogger(__name__)

class Neo4jConnection:
    def __init__(self):
        # Force bolt:// protocol to avoid routing issues
        base_uri = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
        
        # Ensure we're using bolt:// protocol
        if base_uri.startswith("neo4j://"):
            self.uri = base_uri.replace("neo4j://", "bolt://")
            logger.info(f"🔄 Changed protocol from neo4j:// to bolt://")
        else:
            self.uri = base_uri
            
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = None
        self.last_connection_time = 0
        self._connect()

    def _connect(self):
        """Establish connection with valid config parameters only"""
        try:
            # Close existing connection if any
            if self.driver:
                try:
                    self.driver.close()
                except:
                    pass
                    
            logger.info(f"🔌 (Re)connecting to Neo4j at: {self.uri}")
            
            # Use ONLY valid Neo4j driver parameters
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
                max_connection_lifetime=30 * 60,  # 30 minutes
                max_connection_pool_size=10,
                connection_acquisition_timeout=30
                # Removed invalid parameters: max_retry_time, initial_retry_delay, multiplier, jitter_factor
            )

            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1").consume()
                
            self.last_connection_time = time.time()
            logger.info("✅ Successfully (re)connected to Neo4j database")

        except Exception as e:
            logger.error(f"❌ Failed to connect to Neo4j: {str(e)}")
            if 'st' in dir() and hasattr(st, 'error'):
                st.error(f"Database connection failed: {str(e)}")
            raise

    def _is_connection_stale(self) -> bool:
        """Check if connection might be stale (older than 25 minutes)"""
        if not self.driver or not self.last_connection_time:
            return True
        return (time.time() - self.last_connection_time) > (25 * 60)

    def _ensure_connection(self):
        """Ensure we have a healthy connection"""
        if self._is_connection_stale() or not self.check_health():
            logger.info("🔄 Connection appears stale, reconnecting...")
            self._connect()

    def execute_query(self, query: str, parameters: dict = None, max_retries: int = 3) -> List[Dict[str, Any]]:
        """Execute Cypher query with retry logic for stale connections"""
        for attempt in range(max_retries):
            try:
                # Ensure we have a good connection
                self._ensure_connection()
                
                with self.driver.session() as session:
                    result = session.run(query, parameters or {})
                    return [record.data() for record in result]
                    
            except Exception as e:
                logger.warning(f"Query attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                
                if attempt < max_retries - 1:
                    # Try to reconnect for next attempt
                    try:
                        self._connect()
                        time.sleep(1)  # Brief pause before retry
                    except Exception as reconnect_error:
                        logger.warning(f"Reconnection attempt failed: {str(reconnect_error)}")
                else:
                    logger.error(f"Query failed after {max_retries} attempts: {query[:100]}...")
                    return []
        
        return []

    def execute_write_query(self, query: str, parameters: dict = None, max_retries: int = 3) -> bool:
        """Execute write query with retry logic"""
        for attempt in range(max_retries):
            try:
                # Ensure we have a good connection
                self._ensure_connection()
                
                with self.driver.session() as session:
                    session.run(query, parameters or {})
                    return True
                    
            except Exception as e:
                logger.warning(f"Write query attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                
                if attempt < max_retries - 1:
                    try:
                        self._connect()
                        time.sleep(1)
                    except:
                        pass
                else:
                    logger.error(f"Write query failed after {max_retries} attempts")
                    return False
        
        return False

    def check_health(self) -> bool:
        """Check database health"""
        try:
            if not self.driver:
                return False
            with self.driver.session() as session:
                session.run("RETURN 'healthy' as status").consume()
            return True
        except:
            return False

    def close(self):
        """Close database connection"""
        if self.driver:
            try:
                self.driver.close()
                logger.info("📴 Neo4j connection closed")
            except:
                pass
            finally:
                self.driver = None

# Enhanced connection getter with error handling
@st.cache_resource
def get_neo4j_connection():
    """Get cached Neo4j connection with proper error handling"""
    try:
        return Neo4jConnection()
    except Exception as e:
        logger.error(f"Failed to create Neo4j connection: {str(e)}")
        return None  # Return None instead of raising exception

def refresh_neo4j_connection():
    """Manually refresh Neo4j connection (clears cache)"""
    st.cache_resource.clear()
    logger.info("🔄 Neo4j connection cache cleared")
