"""
Interactive Legal Q&A Chatbot with Constitutional Knowledge
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from .knowledge_graph.neo4j_manager import ConstitutionalKnowledgeGraph

logger = logging.getLogger(__name__)

class IndianLegalChatbot:
    """Interactive chatbot for legal document Q&A"""
    
    def __init__(self):
        self.groq_llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=1024
        )
        self.kg = ConstitutionalKnowledgeGraph()
        self.memory = ConversationBufferWindowMemory(
            k=10,
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        self.qa_prompt = self._create_qa_prompt()
    
    def _create_qa_prompt(self) -> PromptTemplate:
        """Create specialized prompt for Indian legal Q&A"""
        template = """You are an expert Indian constitutional lawyer and legal analyst. Use the following context and your knowledge of Indian law to answer questions accurately.

Context from documents: {context}

Constitutional Knowledge: You have access to:
- Indian Constitution (Articles 12, 14, 19, 21 and their interpretations)
- Landmark cases: Kesavananda Bharati, Maneka Gandhi, Puttaswamy
- DPDPA 2023 provisions and constitutional alignment
- Privacy rights framework under Article 21

Chat History: {chat_history}

Question: {question}

Instructions:
1. Provide accurate answers based on Indian constitutional law
2. Cite relevant constitutional articles when applicable
3. Reference landmark Supreme Court cases where relevant
4. Explain DPDPA 2023 provisions in constitutional context
5. If unsure, clearly state limitations

Answer:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "chat_history", "question"]
        )
    
    def get_constitutional_context(self, question: str) -> str:
        """Get relevant constitutional context for the question"""
        try:
            # Simple keyword matching for constitutional context
            context_parts = []
            
            if any(word in question.lower() for word in ["privacy", "personal data", "article 21"]):
                article_21 = self.kg.get_article_context(21)
                if article_21:
                    context_parts.append(f"Article 21: {article_21.get('article', {}).get('text', '')}")
            
            if any(word in question.lower() for word in ["equality", "article 14"]):
                article_14 = self.kg.get_article_context(14)
                if article_14:
                    context_parts.append(f"Article 14: {article_14.get('article', {}).get('text', '')}")
            
            if any(word in question.lower() for word in ["speech", "expression", "article 19"]):
                article_19 = self.kg.get_article_context(19)
                if article_19:
                    context_parts.append(f"Article 19: {article_19.get('article', {}).get('text', '')}")
            
            return "\n\n".join(context_parts) if context_parts else "General constitutional principles apply."
            
        except Exception as e:
            logger.error(f"Error getting constitutional context: {str(e)}")
            return "Constitutional framework available for analysis."
    
    def chat(self, question: str, document_context: str = "") -> Dict[str, Any]:
        """Process chat question and return response"""
        try:
            # Get constitutional context
            constitutional_context = self.get_constitutional_context(question)
            
            # Combine document and constitutional context
            full_context = f"{document_context}\n\n{constitutional_context}".strip()
            
            # Get chat history
            chat_history = self.memory.chat_memory.messages if self.memory.chat_memory else []
            
            # Format prompt
            formatted_prompt = self.qa_prompt.format(
                context=full_context,
                chat_history=chat_history,
                question=question
            )
            
            # Get response from LLM
            response = self.groq_llm.invoke(formatted_prompt)
            answer = response.content
            
            # Save to memory
            self.memory.save_context({"question": question}, {"answer": answer})
            
            return {
                "answer": answer,
                "sources": ["Constitutional Framework", "Document Context"] if document_context else ["Constitutional Framework"],
                "timestamp": datetime.now().isoformat(),
                "question": question
            }
            
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            return {
                "answer": "I apologize, but I encountered an error processing your question. Please try rephrasing your question.",
                "sources": [],
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "error": str(e)
            }
    
    def get_chat_history(self) -> List[Dict[str, Any]]:
        """Get formatted chat history"""
        history = []
        if self.memory.chat_memory:
            messages = self.memory.chat_memory.messages
            for i in range(0, len(messages), 2):
                if i + 1 < len(messages):
                    history.append({
                        "question": messages[i].content,
                        "answer": messages[i + 1].content,
                        "timestamp": datetime.now().isoformat()
                    })
        return history
    
    def clear_history(self):
        """Clear chat history"""
        self.memory.clear()
