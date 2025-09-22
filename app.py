# """
# Indian Legal KAG System - Complete Enhanced Streamlit Application
# With Advanced Classification, Framework Selection, and Comprehensive Scoring
# """

# import streamlit as st
# import os
# from datetime import datetime
# import logging
# from io import BytesIO

# # Import core modules
# from config.neo4j_config import get_neo4j_connection
# from core.knowledge_graph.neo4j_manager import ConstitutionalKnowledgeGraph
# from core.kag_engine.constitutional_reasoning import ConstitutionalReasoningEngine
# from core.kag_engine.privacy_analyzer import Article21PrivacyAnalyzer
# from core.kag_engine.dpdpa_compliance import DPDPAComplianceEngine
# from core.processors.document_processor import IndianLegalDocumentProcessor
# from core.messaging.smtp_manager import SMTPEmailManager
# from core.messaging.report_generator import IndianLegalReportGenerator

# # Import Enhanced Analysis Components
# from analysis_frameworks.framework_engine import AdaptiveLegalFrameworkEngine
# from analysis_frameworks.scoring_engine import UniversalLegalScoringEngine

# # Import NEW features
# from core.chatbot.legal_chatbot import IndianLegalChatbot
# from core.summarization.legal_summarizer import LegalDocumentSummarizer
# from core.scrapers.regulatory_scraper import IndianRegulatoryUpdatesScraper

# from utils.indian_legal_utils import initialize_indian_legal_session_state, validate_environment_variables

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Page config
# st.set_page_config(
#     page_title="Indian Legal KAG System",
#     page_icon="⚖️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# def main():
#     """Main application function"""
    
#     # Initialize session state
#     initialize_indian_legal_session_state()
    
#     # App header
#     st.title("🇮🇳 Indian Legal Knowledge Augmented Generation (KAG) System")
#     st.markdown("**Enhanced with Advanced AI Classification & Comprehensive Legal Analysis**")
    
#     # Sidebar for configuration
#     with st.sidebar:
#         st.header("⚙️ System Configuration")
        
#         # Environment validation
#         env_status = validate_environment_variables()
#         for component, status in env_status.items():
#             if status:
#                 st.success(f"✅ {component.upper()} configured")
#             else:
#                 st.error(f"❌ {component.upper()} not configured")
        
#         # System initialization
#         if st.button("🚀 Initialize Knowledge Graph"):
#             with st.spinner("Initializing constitutional knowledge base..."):
#                 try:
#                     kg = ConstitutionalKnowledgeGraph()
#                     success = kg.initialize_constitutional_knowledge()
#                     if success:
#                         st.session_state.kg_initialized = True
#                         st.success("✅ Knowledge graph initialized!")
#                     else:
#                         st.error("❌ Knowledge graph initialization failed")
#                 except Exception as e:
#                     st.error(f"❌ Initialization error: {str(e)}")
    
#     # Enhanced Main content tabs
#     tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
#         "📄 Document Analysis",
#         "📊 Results Dashboard",
#         "🎯 Framework Analysis",
#         "🤖 Interactive Q&A",
#         "📋 Document Summarization",
#         "🌐 Regulatory Updates",
#         "📧 Report Generation",
#         "🔍 Knowledge Graph Explorer",
#         "⚙️ System Status"
#     ])
    
#     with tab1:
#         document_analysis_tab()
#     with tab2:
#         results_dashboard_tab()
#     with tab3:
#         framework_analysis_tab()
#     with tab4:
#         interactive_qa_tab()
#     with tab5:
#         document_summarization_tab()
#     with tab6:
#         regulatory_updates_tab()
#     with tab7:
#         report_generation_tab()
#     with tab8:
#         knowledge_graph_tab()
#     with tab9:
#         system_status_tab()

# def document_analysis_tab():
#     """Enhanced document analysis with advanced AI classification"""
#     st.header("📄 Advanced Legal Document Analysis")
    
#     # File upload
#     uploaded_file = st.file_uploader(
#         "Upload Legal Document (PDF)",
#         type=["pdf"],
#         help="Upload Indian legal documents for comprehensive constitutional and privacy analysis"
#     )
    
#     if uploaded_file is not None:
#         col1, col2 = st.columns([3, 1])
        
#         with col1:
#             st.info(f"📁 **File:** {uploaded_file.name} ({uploaded_file.size:,} bytes)")
        
#         with col2:
#             analyze_button = st.button("🔍 Analyze Document", type="primary")
        
#         if analyze_button:
#             with st.spinner("🔄 Performing comprehensive legal analysis..."):
#                 try:
#                     # Initialize ALL processors including enhanced engines
#                     doc_processor = IndianLegalDocumentProcessor()
#                     framework_engine = AdaptiveLegalFrameworkEngine()
#                     scoring_engine = UniversalLegalScoringEngine()
#                     constitutional_engine = ConstitutionalReasoningEngine()
#                     privacy_analyzer = Article21PrivacyAnalyzer()
#                     dpdpa_engine = DPDPAComplianceEngine()
                    
#                     # Step 1: Advanced Document Processing
#                     st.write("📝 Processing with advanced AI classification...")
#                     processing_result = doc_processor.process_document_complete(BytesIO(uploaded_file.read()))
                    
#                     if not processing_result["success"]:
#                         st.error(f"❌ Failed to process document: {processing_result.get('error', 'Unknown error')}")
#                         return
                    
#                     # Step 2: Enhanced Framework Selection
#                     st.write("🎯 Selecting optimal legal frameworks...")
#                     framework_selection = framework_engine.select_frameworks(
#                         document_type=processing_result["document_classification"]["primary_type"],
#                         confidence=processing_result["document_classification"]["confidence"],
#                         content_indicators=processing_result["indian_legal_indicators"]
#                     )
                    
#                     # Step 3: Comprehensive Scoring
#                     st.write("📊 Calculating comprehensive compliance scores...")
#                     comprehensive_scores = scoring_engine.calculate_comprehensive_score(
#                         document_analysis=processing_result,
#                         frameworks_applied=framework_selection["selected_frameworks"]
#                     )
                    
#                     # Store enhanced results
#                     st.session_state.processing_result = processing_result
#                     st.session_state.framework_selection = framework_selection
#                     st.session_state.comprehensive_scores = comprehensive_scores
                    
#                     # Step 4: Traditional Legal Analysis (Enhanced)
#                     st.write("🏛️ Performing constitutional analysis...")
#                     full_text = "\n".join([chunk["text"] for chunk in processing_result["enhanced_chunks"]])
#                     constitutional_analysis = constitutional_engine.analyze_document_constitutionality(full_text)
                    
#                     st.write("🔒 Analyzing Article 21 privacy implications...")
#                     privacy_analysis = privacy_analyzer.analyze_privacy_implications(full_text)
                    
#                     st.write("📋 Assessing DPDPA 2023 compliance...")
#                     dpdpa_analysis = dpdpa_engine.assess_dpdpa_compliance(full_text, privacy_analysis)
                    
#                     # Store traditional results
#                     st.session_state.constitutional_analysis = constitutional_analysis
#                     st.session_state.privacy_analysis = privacy_analysis
#                     st.session_state.dpdpa_analysis = dpdpa_analysis
                    
#                     # Calculate overall compliance
#                     overall_score = calculate_overall_compliance(
#                         constitutional_analysis, privacy_analysis, dpdpa_analysis
#                     )
#                     st.session_state.compliance_score = overall_score
#                     st.session_state.document_processed = True
                    
#                     # Display immediate results
#                     st.success("✅ Complete legal analysis finished!")
                    
#                     # Quick results preview
#                     col1, col2, col3, col4 = st.columns(4)
#                     with col1:
#                         st.metric("Document Type", 
#                                 processing_result["document_classification"]["primary_type"].replace('_', ' ').title())
#                     with col2:
#                         st.metric("Classification Confidence", 
#                                 f"{processing_result['document_classification']['confidence']:.1%}")
#                     with col3:
#                         st.metric("Frameworks Applied", len(framework_selection["selected_frameworks"]))
#                     with col4:
#                         st.metric("Overall Score", f"{comprehensive_scores['overall_score']:.1f}%")
                    
#                     st.rerun()
                    
#                 except Exception as e:
#                     st.error(f"❌ Analysis failed: {str(e)}")
#                     logger.error(f"Document analysis error: {str(e)}")

# def results_dashboard_tab():
#     """Enhanced results dashboard with comprehensive metrics"""
#     st.header("📊 Enhanced Analysis Results Dashboard")
    
#     if not st.session_state.get('document_processed'):
#         st.info("📄 Please upload and analyze a document first")
#         return
    
#     # Enhanced Classification Results
#     if 'processing_result' in st.session_state:
#         st.subheader("🎯 Advanced Document Classification")
#         processing = st.session_state.processing_result
#         classification = processing["document_classification"]
        
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             st.metric("Document Type", classification["primary_type"].replace('_', ' ').title())
#         with col2:
#             st.metric("Confidence", f"{classification['confidence']:.1%}")
#         with col3:
#             st.metric("Confidence Level", classification.get("confidence_level", "unknown").title())
#         with col4:
#             st.metric("Classification Method", "Advanced ML")
        
#         # Alternative classifications
#         if classification.get("alternative_classifications"):
#             with st.expander("🔍 Alternative Classifications"):
#                 for i, alt in enumerate(classification["alternative_classifications"][:3], 1):
#                     st.write(f"{i}. **{alt['document_type'].replace('_', ' ').title()}**: {alt['confidence']:.1%} confidence ({alt['confidence_level']})")
    
#     # Framework Selection Results
#     if 'framework_selection' in st.session_state:
#         st.subheader("🎯 Selected Legal Frameworks")
#         selection = st.session_state.framework_selection
        
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.metric("Frameworks Selected", len(selection["selected_frameworks"]))
#         with col2:
#             st.metric("Selection Confidence", f"{selection['selection_confidence']:.1%}")
#         with col3:
#             st.metric("Document Category", selection["document_type"].replace('_', ' ').title())
        
#         # Framework details
#         with st.expander("🔍 Framework Selection Reasoning"):
#             for framework in selection["selected_frameworks"]:
#                 reason = selection["selection_reasons"].get(framework, "Selected for comprehensive analysis")
#                 st.write(f"• **{framework.replace('_', ' ').title()}**: {reason}")
    
#     # Comprehensive Scoring Results
#     if 'comprehensive_scores' in st.session_state:
#         st.subheader("⚖️ Comprehensive Compliance Analysis")
#         scores = st.session_state.comprehensive_scores
        
#         # Main metrics
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             st.metric("Overall Score", f"{scores['overall_score']:.1f}%")
#         with col2:
#             st.metric("Compliance Level", scores['compliance_level'].replace('_', ' ').title())
#         with col3:
#             st.metric("Analysis Confidence", f"{scores['confidence_level']:.1%}")
#         with col4:
#             risk_level = scores['risk_assessment']['overall_risk_level']
#             st.metric("Risk Level", risk_level.replace('_', ' ').title())
        
#         # Category scores breakdown
#         if scores.get('category_scores'):
#             st.subheader("📋 Detailed Category Analysis")
#             for category, score_data in scores['category_scores'].items():
#                 with st.expander(f"📊 {category.replace('_', ' ').title()} - {score_data['score']:.1f}%"):
#                     st.write(f"**Framework:** {score_data.get('framework', 'N/A').replace('_', ' ').title()}")
#                     st.write(f"**Score:** {score_data['score']:.1f}%")
                    
#                     if score_data.get('issues'):
#                         st.write("**Issues Identified:**")
#                         for issue in score_data['issues'][:3]:  # Show top 3
#                             st.error(f"• {issue}")
                    
#                     if score_data.get('recommendations'):
#                         st.write("**Recommendations:**")
#                         for rec in score_data['recommendations'][:3]:  # Show top 3
#                             st.info(f"• {rec}")
    
#     # Traditional Analysis Results (Constitutional, Privacy, DPDPA)
#     if 'constitutional_analysis' in st.session_state:
#         st.subheader("🏛️ Constitutional Analysis Summary")
#         constitutional = st.session_state.constitutional_analysis
#         articles = constitutional.get('constitutional_articles', [])
        
#         if articles:
#             st.write("**Key Constitutional Articles Identified:**")
#             for article in articles[:5]:
#                 article_id = article.get('article_id', '').replace('article_', '')
#                 relevance = article.get('relevance_score', 0)
#                 implication = article.get('implication_type', 'Constitutional provision')
#                 st.write(f"• **Article {article_id}**: {implication} (Relevance: {relevance:.2f})")

# def framework_analysis_tab():
#     """Detailed framework and scoring analysis"""
#     st.header("🎯 Legal Framework Analysis Details")
    
#     if not st.session_state.get('framework_selection'):
#         st.info("📄 Please analyze a document first to see framework selection")
#         return
    
#     selection = st.session_state.framework_selection
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.subheader("📋 Selected Frameworks Details")
        
#         # Initialize framework engine for details
#         framework_engine = AdaptiveLegalFrameworkEngine()
        
#         for framework in selection["selected_frameworks"]:
#             with st.expander(f"📖 {framework.replace('_', ' ').title()}"):
#                 details = framework_engine.get_framework_details(framework)
                
#                 st.write(f"**Description:** {details.get('description', 'N/A')}")
#                 st.write(f"**Priority:** {details.get('priority', 'N/A')}")
                
#                 if 'analysis_methods' in details:
#                     st.write("**Analysis Methods:**")
#                     for method in details['analysis_methods']:
#                         st.write(f"• {method.replace('_', ' ').title()}")
                
#                 if 'constitutional_articles_details' in details:
#                     st.write("**Key Constitutional Articles:**")
#                     for article_num, article_info in details['constitutional_articles_details'].items():
#                         st.write(f"• **Article {article_num}**: {article_info['title']}")
                
#                 # Selection reasoning
#                 reason = selection["selection_reasons"].get(framework, "No specific reason provided")
#                 st.write(f"**Selection Reason:** {reason}")
    
#     with col2:
#         if 'comprehensive_scores' in st.session_state:
#             st.subheader("🎯 Risk Assessment")
#             scores = st.session_state.comprehensive_scores
            
#             # Risk assessment details
#             risk_data = scores.get('risk_assessment', {})
#             if risk_data.get('category_risks'):
#                 for category, risk_info in risk_data['category_risks'].items():
#                     risk_level = risk_info['risk_level']
#                     risk_color = {
#                         'very_low': '🟢',
#                         'low': '🔵', 
#                         'medium': '🟡',
#                         'high': '🟠',
#                         'very_high': '🔴'
#                     }.get(risk_level, '⚪')
                    
#                     st.write(f"{risk_color} **{category.replace('_', ' ').title()}**")
#                     st.write(f"Risk Level: {risk_level.replace('_', ' ').title()}")
#                     st.write(f"Score: {risk_info['score']:.1f}%")
#                     st.write("---")
            
#             # Critical risks summary
#             if risk_data.get('critical_risks'):
#                 st.subheader("⚠️ Critical Risks")
#                 for risk in risk_data['critical_risks']:
#                     st.error(f"**{risk['category'].replace('_', ' ').title()}**: {risk['risk_level'].replace('_', ' ').title()} risk")

# def interactive_qa_tab():
#     """Interactive Q&A chatbot interface"""
#     st.header("🤖 Interactive Legal Q&A Assistant")
    
#     # Initialize chatbot
#     if 'chatbot' not in st.session_state:
#         try:
#             st.session_state.chatbot = IndianLegalChatbot()
#         except Exception as e:
#             st.error(f"❌ Error initializing chatbot: {str(e)}")
#             st.info("Please ensure GROQ_API_KEY is configured in your .env file")
#             return
    
#     # Chat interface
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         st.subheader("💬 Ask Your Legal Questions")
        
#         # Question input
#         question = st.text_input("Enter your question about constitutional law, privacy rights, or DPDPA compliance:")
        
#         col_ask, col_clear = st.columns([2, 1])
        
#         with col_ask:
#             if st.button("🔍 Ask Question", type="primary") and question:
#                 with st.spinner("🤔 Analyzing and generating response..."):
#                     try:
#                         # Get document context if available
#                         document_context = ""
#                         if st.session_state.get('processing_result'):
#                             chunks = st.session_state.processing_result.get('enhanced_chunks', [])
#                             if chunks:
#                                 document_context = chunks[0].get('text', '')[:2000]
                        
#                         response = st.session_state.chatbot.chat(question, document_context)
                        
#                         st.success("✅ Response generated!")
                        
#                         # Display response
#                         with st.container():
#                             st.markdown("### 💭 Question")
#                             st.write(question)
                            
#                             st.markdown("### 🎯 Answer")
#                             st.write(response['answer'])
                            
#                             if response.get('sources'):
#                                 st.markdown("### 📚 Sources")
#                                 st.write(', '.join(response['sources']))
                    
#                     except Exception as e:
#                         st.error(f"❌ Error processing question: {str(e)}")
        
#         with col_clear:
#             if st.button("🗑️ Clear History"):
#                 if hasattr(st.session_state, 'chatbot'):
#                     st.session_state.chatbot.clear_history()
#                     st.success("🧹 Chat history cleared!")
#                     st.rerun()
    
#     with col2:
#         st.subheader("💡 Sample Questions")
        
#         sample_questions = [
#             "What does Article 21 say about privacy rights?",
#             "How does DPDPA 2023 relate to constitutional rights?",
#             "What are the key principles from Puttaswamy judgment?",
#             "What is the constitutional basis for data protection?",
#             "How do fundamental rights apply to this document?",
#             "Explain Article 14 equality principle",
#             "What are data fiduciary obligations under DPDPA?"
#         ]
        
#         for i, q in enumerate(sample_questions):
#             if st.button(q, key=f"sample_{i}"):
#                 st.info(f"Selected: {q}")
#                 st.info("👆 Copy this question to the input field above")

# def document_summarization_tab():
#     """Document summarization interface"""
#     st.header("📋 Advanced Document Summarization")
    
#     if not st.session_state.get('processing_result'):
#         st.info("📄 Please upload and analyze a document first")
#         return
    
#     # Initialize summarizer
#     if 'summarizer' not in st.session_state:
#         try:
#             st.session_state.summarizer = LegalDocumentSummarizer()
#         except Exception as e:
#             st.error(f"❌ Error initializing summarizer: {str(e)}")
#             return
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.subheader("📄 Document Summary Options")
        
#         summary_type = st.selectbox(
#             "Choose Summary Type",
#             ["executive", "detailed", "constitutional", "privacy"],
#             format_func=lambda x: {
#                 "executive": "📋 Executive Summary",
#                 "detailed": "📑 Detailed Analysis",
#                 "constitutional": "🏛️ Constitutional Analysis",
#                 "privacy": "🔒 Privacy Analysis"
#             }[x]
#         )
        
#         if st.button("📝 Generate Summary", type="primary"):
#             with st.spinner(f"🔄 Generating {summary_type} summary..."):
#                 try:
#                     # Extract text from chunks
#                     chunks = st.session_state.processing_result.get('enhanced_chunks', [])
#                     full_text = "\n".join([chunk.get('text', '') for chunk in chunks])
                    
#                     summary_result = st.session_state.summarizer.summarize_document(
#                         full_text, summary_type
#                     )
                    
#                     st.session_state[f'{summary_type}_summary'] = summary_result
#                     st.success("✅ Summary generated!")
#                 except Exception as e:
#                     st.error(f"❌ Summary generation failed: {str(e)}")
        
#         # Display generated summary
#         if st.session_state.get(f'{summary_type}_summary'):
#             result = st.session_state[f'{summary_type}_summary']
            
#             st.subheader(f"📋 {summary_type.title()} Summary")
            
#             if 'error' not in result:
#                 st.write(result['summary'])
                
#                 with st.expander("📊 Summary Statistics"):
#                     st.write(f"**Word Count:** {result.get('word_count', 'N/A')}")
#                     st.write(f"**Source Length:** {result.get('source_length', 'N/A')} characters")
#                     st.write(f"**Generated:** {result.get('timestamp', 'N/A')}")
#             else:
#                 st.error(f"Error generating summary: {result.get('error', 'Unknown error')}")
    
#     with col2:
#         st.subheader("🚀 Quick Actions")
        
#         if st.button("📋 Generate All Summaries"):
#             with st.spinner("🔄 Generating all summary types..."):
#                 try:
#                     chunks = st.session_state.processing_result.get('enhanced_chunks', [])
#                     full_text = "\n".join([chunk.get('text', '') for chunk in chunks])
                    
#                     all_summaries = st.session_state.summarizer.generate_all_summaries(full_text)
#                     st.session_state.all_summaries = all_summaries
#                     st.success("✅ All summaries generated!")
#                 except Exception as e:
#                     st.error(f"❌ Error generating summaries: {str(e)}")

# def regulatory_updates_tab():
#     """Regulatory updates and compliance monitoring"""
#     st.header("🌐 Indian Legal & Regulatory Updates")
    
#     # Initialize scraper
#     if 'scraper' not in st.session_state:
#         st.session_state.scraper = IndianRegulatoryUpdatesScraper()
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         st.subheader("📊 Recent Legal Updates")
        
#         # Filter options
#         category_filter = st.selectbox(
#             "Filter by Category",
#             ["all", "constitutional", "privacy", "general"],
#             format_func=lambda x: {
#                 "all": "🌐 All Updates",
#                 "constitutional": "🏛️ Constitutional Updates",
#                 "privacy": "🔒 Privacy & Data Protection",
#                 "general": "📋 General Legal Updates"
#             }[x]
#         )
        
#         days_filter = st.slider("Days to look back", 7, 90, 30)
        
#         if st.button("🔄 Fetch Latest Updates", type="primary"):
#             with st.spinner("🌐 Scraping legal sources..."):
#                 try:
#                     updates = st.session_state.scraper.get_filtered_updates(
#                         category=category_filter,
#                         days_back=days_filter
#                     )
#                     st.session_state.regulatory_updates = updates
#                     st.success(f"✅ Found {len(updates)} updates!")
#                 except Exception as e:
#                     st.error(f"❌ Error fetching updates: {str(e)}")
#                     st.info("Note: Some legal websites may restrict automated access")
        
#         # Display updates
#         if st.session_state.get('regulatory_updates'):
#             updates = st.session_state.regulatory_updates
            
#             if updates:
#                 st.subheader(f"📋 {len(updates)} Recent Updates")
                
#                 for i, update in enumerate(updates[:20]):  # Show first 20
#                     with st.expander(f"📄 {update['source']} - {update['title'][:60]}..."):
#                         st.write(f"**Title:** {update['title']}")
#                         st.write(f"**Source:** {update['source']}")
#                         st.write(f"**Type:** {update['type']}")
#                         st.write(f"**Date:** {update['scraped_date']}")
                        
#                         if update.get('link') and update['link'] != '':
#                             st.write(f"**Link:** [View Source]({update['link']})")
#             else:
#                 st.info("No updates found for the selected criteria")
    
#     with col2:
#         st.subheader("⚙️ Monitoring Features")
        
#         st.info("🔔 **Monitored Sources:**")
#         st.write("• Supreme Court of India")
#         st.write("• Ministry of Law & Justice")
#         st.write("• Parliament Proceedings")
#         st.write("• Constitutional Updates")
#         st.write("• Privacy Law Changes")

# def report_generation_tab():
#     """Report generation and email interface"""
#     st.header("📧 Enhanced Report Generation")
    
#     if not st.session_state.get('document_processed'):
#         st.info("📄 Please analyze a document first")
#         return
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.subheader("📄 Generate Comprehensive PDF Report")
        
#         report_type = st.selectbox(
#             "Report Type",
#             ["comprehensive_analysis", "constitutional_focus", "privacy_focus", "dpdpa_compliance"]
#         )
        
#         if st.button("📄 Generate Enhanced PDF Report"):
#             with st.spinner("🔄 Generating comprehensive report..."):
#                 try:
#                     report_generator = IndianLegalReportGenerator()
                    
#                     # Collect all analysis results
#                     analysis_results = {
#                         'processing_result': st.session_state.get('processing_result', {}),
#                         'framework_selection': st.session_state.get('framework_selection', {}),
#                         'comprehensive_scores': st.session_state.get('comprehensive_scores', {}),
#                         'constitutional_analysis': st.session_state.get('constitutional_analysis', {}),
#                         'privacy_analysis': st.session_state.get('privacy_analysis', {}),
#                         'dpdpa_analysis': st.session_state.get('dpdpa_analysis', {}),
#                         'compliance_score': st.session_state.get('compliance_score', {})
#                     }
                    
#                     report_result = report_generator.generate_comprehensive_report(
#                         analysis_results,
#                         st.session_state.get('processing_result', {}).get('metadata', {})
#                     )
                    
#                     if report_result['success']:
#                         st.session_state.comprehensive_report = report_result['pdf_buffer']
#                         st.success("✅ Enhanced PDF report generated successfully!")
                        
#                         # Download button
#                         st.download_button(
#                             label="📥 Download Enhanced PDF Report",
#                             data=report_result['pdf_buffer'].getvalue(),
#                             file_name=f"enhanced_legal_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
#                             mime="application/pdf"
#                         )
#                     else:
#                         st.error(f"❌ Report generation failed: {report_result.get('error', 'Unknown error')}")
                        
#                 except Exception as e:
#                     st.error(f"❌ Report generation error: {str(e)}")
    
#     with col2:
#         st.subheader("📊 Report Features")
        
#         st.info("📋 **Enhanced Report Includes:**")
#         st.write("• Advanced Document Classification")
#         st.write("• Framework Selection Reasoning")
#         st.write("• Comprehensive Compliance Scoring")
#         st.write("• Risk Assessment Matrix")
#         st.write("• Constitutional Analysis")
#         st.write("• Privacy Rights Assessment")
#         st.write("• DPDPA Compliance Review")
#         st.write("• Actionable Recommendations")

# def knowledge_graph_tab():
#     """Knowledge graph explorer interface"""
#     st.header("🔍 Constitutional Knowledge Graph Explorer")
    
#     try:
#         kg = ConstitutionalKnowledgeGraph()
        
#         # Graph statistics
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.subheader("📊 Knowledge Graph Statistics")
#             stats = kg.get_knowledge_graph_stats()
#             for stat_name, count in stats.items():
#                 st.metric(stat_name.replace('_', ' ').title(), count)
        
#         with col2:
#             st.subheader("🔍 Pathway Explorer")
#             start_concept = st.text_input("Start Concept", placeholder="article_21")
#             end_concept = st.text_input("End Concept", placeholder="privacy_right")
#             max_hops = st.slider("Maximum Hops", 1, 6, 3)
            
#             if st.button("🔍 Find Constitutional Pathway") and start_concept and end_concept:
#                 pathways = kg.find_constitutional_pathway(start_concept, end_concept, max_hops)
                
#                 if pathways:
#                     st.subheader(f"🛤️ Constitutional Pathways ({len(pathways)} found)")
#                     for i, pathway in enumerate(pathways[:3], 1):
#                         with st.expander(f"Pathway {i}"):
#                             st.write("Constitutional reasoning pathway found between concepts")
#                 else:
#                     st.info("No pathways found between the specified concepts")
                    
#     except Exception as e:
#         st.error(f"❌ Knowledge graph error: {str(e)}")

# def system_status_tab():
#     """Enhanced system status and monitoring"""
#     st.header("⚙️ Enhanced System Status & Monitoring")
    
#     # Environment variables status
#     st.subheader("🔧 Environment Configuration")
#     env_status = validate_environment_variables()
    
#     for component, status in env_status.items():
#         col1, col2 = st.columns([3, 1])
#         with col1:
#             st.write(f"**{component.upper()} Configuration**")
#         with col2:
#             if status:
#                 st.success("✅ Configured")
#             else:
#                 st.error("❌ Missing")
    
#     # Enhanced system health
#     st.subheader("🏥 System Health Dashboard")
    
#     if st.button("🔍 Run Comprehensive Health Checks"):
#         with st.spinner("Checking all system components..."):
#             health_results = {}
            
#             # Check document processor
#             try:
#                 doc_processor = IndianLegalDocumentProcessor()
#                 health_results['document_processor'] = True
#             except Exception as e:
#                 health_results['document_processor'] = False
#                 st.error(f"Document Processor error: {str(e)}")
            
#             # Check framework engine
#             try:
#                 framework_engine = AdaptiveLegalFrameworkEngine()
#                 health_results['framework_engine'] = True
#             except Exception as e:
#                 health_results['framework_engine'] = False
#                 st.error(f"Framework Engine error: {str(e)}")
            
#             # Check scoring engine
#             try:
#                 scoring_engine = UniversalLegalScoringEngine()
#                 health_results['scoring_engine'] = True
#             except Exception as e:
#                 health_results['scoring_engine'] = False
#                 st.error(f"Scoring Engine error: {str(e)}")
            
#             # Neo4j connection
#             try:
#                 neo4j_conn = get_neo4j_connection()
#                 health_results['neo4j'] = True
#             except Exception as e:
#                 health_results['neo4j'] = False
#                 st.error(f"Neo4j error: {str(e)}")
            
#             # Display results
#             st.subheader("📊 Health Check Results")
#             for component, status in health_results.items():
#                 col1, col2 = st.columns([3, 1])
#                 with col1:
#                     st.write(f"**{component.replace('_', ' ').title()}**")
#                 with col2:
#                     if status:
#                         st.success("✅ Healthy")
#                     else:
#                         st.error("❌ Failed")

# def calculate_overall_compliance(constitutional_analysis, privacy_analysis, dpdpa_analysis):
#     """Calculate overall compliance score"""
#     scores = {
#         'constitutional_score': constitutional_analysis.get('compliance_score', {}).get('overall_score', 0),
#         'privacy_score': privacy_analysis.get('privacy_risk_score', {}).get('overall_score', 0),
#         'dpdpa_score': dpdpa_analysis.get('dpdpa_compliance_summary', {}).get('overall_score', 0)
#     }
    
#     # Weighted average
#     overall_score = (
#         scores['constitutional_score'] * 0.4 +
#         scores['privacy_score'] * 0.3 +
#         scores['dpdpa_score'] * 0.3
#     )
    
#     return {
#         'overall_score': overall_score,
#         'constitutional_score': scores['constitutional_score'],
#         'privacy_score': scores['privacy_score'],
#         'dpdpa_score': scores['dpdpa_score'],
#         'calculation_timestamp': datetime.now().isoformat()
#     }

# if __name__ == "__main__":
#     main()

"""
Indian Legal KAG System - Complete Enhanced Streamlit Application
With Advanced Classification, Framework Selection, OCR Fallback, and Comprehensive Scoring
Updated for Enhanced Document Processor with Multiple Extraction Methods
"""

import streamlit as st
import os
from datetime import datetime
import logging
from io import BytesIO

# Import core modules
from .neo4j_config import get_neo4j_connection
from .knowledge_graph.neo4j_manager import ConstitutionalKnowledgeGraph
from .kag_engine.constitutional_reasoning import ConstitutionalReasoningEngine
from .kag_engine.privacy_analyzer import Article21PrivacyAnalyzer
from .kag_engine.dpdpa_compliance import DPDPAComplianceEngine
from .processors.document_processor import IndianLegalDocumentProcessor
from .messaging.smtp_manager import SMTPEmailManager
from .messaging.report_generator import IndianLegalReportGenerator

# Import Enhanced Analysis Components
from .framework_engine import AdaptiveLegalFrameworkEngine
from .scoring_engine import UniversalLegalScoringEngine

# Import NEW features
from .chatbot.legal_chatbot import IndianLegalChatbot
from .summarization.legal_summarizer import LegalDocumentSummarizer
from .scrapers.regulatory_scraper import IndianRegulatoryUpdatesScraper

from .indian_legal_utils import initialize_indian_legal_session_state, validate_environment_variables

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check OCR availability
try:
    import easyocr
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="Indian Legal KAG System",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function"""
    
    # Initialize session state
    initialize_indian_legal_session_state()
    
    # App header
    st.title("🇮🇳 Indian Legal Knowledge Augmented Generation (KAG) System")
    st.markdown("**Enhanced with Advanced AI Classification, OCR Fallback & Comprehensive Legal Analysis**")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ System Configuration")
        
        # Environment validation
        env_status = validate_environment_variables()
        for component, status in env_status.items():
            if status:
                st.success(f"✅ {component.upper()} configured")
            else:
                st.error(f"❌ {component.upper()} not configured")
        
        # OCR Status
        st.divider()
        st.subheader("🔍 OCR Status")
        if OCR_AVAILABLE:
            st.success("✅ OCR Available (EasyOCR)")
            st.info("📄 Can process scanned documents")
        else:
            st.warning("⚠️ OCR Not Available")
            st.info("Install with: `pip install easyocr`")
        
        # System initialization
        st.divider()
        if st.button("🚀 Initialize Knowledge Graph"):
            with st.spinner("Initializing constitutional knowledge base..."):
                try:
                    kg = ConstitutionalKnowledgeGraph()
                    success = kg.initialize_constitutional_knowledge()
                    if success:
                        st.session_state.kg_initialized = True
                        st.success("✅ Knowledge graph initialized!")
                    else:
                        st.error("❌ Knowledge graph initialization failed")
                except Exception as e:
                    st.error(f"❌ Initialization error: {str(e)}")
    
    # Enhanced Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "📄 Document Analysis",
        "📊 Results Dashboard", 
        "🎯 Framework Analysis",
        "🤖 Interactive Q&A",
        "📋 Document Summarization",
        "🌐 Regulatory Updates",
        "📧 Report Generation",
        "🔍 Knowledge Graph Explorer",
        "⚙️ System Status"
    ])
    
    with tab1:
        document_analysis_tab()
    with tab2:
        results_dashboard_tab()
    with tab3:
        framework_analysis_tab()
    with tab4:
        interactive_qa_tab()
    with tab5:
        document_summarization_tab()
    with tab6:
        regulatory_updates_tab()
    with tab7:
        report_generation_tab()
    with tab8:
        knowledge_graph_tab()
    with tab9:
        system_status_tab()

def document_analysis_tab():
    """Enhanced document analysis with advanced AI classification and OCR fallback"""
    st.header("📄 Advanced Legal Document Analysis with OCR Support")
    
    # Info about supported document types
    with st.expander("ℹ️ Document Processing Capabilities"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**✅ Supported Processing Methods:**")
            st.write("• Text-based PDFs (Primary)")
            st.write("• Alternative PyMuPDF extraction")
            if OCR_AVAILABLE:
                st.write("• OCR for scanned documents")
                st.write("• English & Hindi text recognition")
            else:
                st.write("• ⚠️ OCR unavailable (install easyocr)")
        
        with col2:
            st.write("**📋 Document Types Analyzed:**")
            st.write("• Constitutional documents")
            st.write("• Government notifications")
            st.write("• Privacy policies") 
            st.write("• Legal contracts")
            st.write("• Court judgments")
            st.write("• DPDPA compliance documents")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Legal Document (PDF)",
        type=["pdf"],
        help="Upload Indian legal documents for comprehensive constitutional and privacy analysis. Supports both text-based and scanned PDFs."
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info(f"📁 **File:** {uploaded_file.name} ({uploaded_file.size:,} bytes)")
        
        with col2:
            analyze_button = st.button("🔍 Analyze Document", type="primary")
        
        if analyze_button:
            with st.spinner("🔄 Performing comprehensive legal analysis with multiple extraction methods..."):
                try:
                    # Initialize ALL processors including enhanced engines
                    doc_processor = IndianLegalDocumentProcessor()
                    framework_engine = AdaptiveLegalFrameworkEngine()
                    scoring_engine = UniversalLegalScoringEngine()
                    constitutional_engine = ConstitutionalReasoningEngine()
                    privacy_analyzer = Article21PrivacyAnalyzer()
                    dpdpa_engine = DPDPAComplianceEngine()
                    
                    # Step 1: Enhanced Document Processing with multiple extraction methods
                    st.write("📝 Processing with enhanced AI classification and OCR fallback...")
                    processing_result = doc_processor.process_document_complete(BytesIO(uploaded_file.read()))
                    
                    # Enhanced error handling for extraction failures
                    if not processing_result["success"]:
                        st.error(f"❌ Failed to process document: {processing_result.get('error', 'Unknown error')}")
                        
                        # Show extraction details and recommendations
                        if 'extraction_details' in processing_result:
                            with st.expander("🔍 Extraction Troubleshooting"):
                                details = processing_result['extraction_details']
                                
                                st.write("**Attempted Methods:**")
                                for method in details.get('attempted_methods', []):
                                    st.write(f"• {method.replace('_', ' ').title()}")
                                
                                st.write(f"**OCR Available:** {'✅ Yes' if details.get('ocr_available') else '❌ No'}")
                                
                                if 'validation_info' in processing_result.get('metadata', {}):
                                    validation = processing_result['metadata']['validation_info']
                                    st.write("**PDF Validation:**")
                                    st.write(f"• File Size: {validation.get('file_size', 0):,} bytes")
                                    st.write(f"• Page Count: {validation.get('page_count', 0)}")
                                    st.write(f"• Has Text: {'✅' if validation.get('has_text') else '❌'}")
                                    st.write(f"• Is Encrypted: {'❌ Yes' if validation.get('is_encrypted') else '✅ No'}")
                                    
                                    if validation.get('validation_errors'):
                                        st.write("**Validation Errors:**")
                                        for error in validation['validation_errors']:
                                            st.error(f"• {error}")
                        
                        # Show recommendations
                        if 'recommendations' in processing_result:
                            st.write("**💡 Recommendations:**")
                            for rec in processing_result['recommendations']:
                                st.info(f"• {rec}")
                        
                        return
                    
                    # Step 2: Enhanced Framework Selection
                    st.write("🎯 Selecting optimal legal frameworks...")
                    framework_selection = framework_engine.select_frameworks(
                        document_type=processing_result["document_classification"]["primary_type"],
                        confidence=processing_result["document_classification"]["confidence"],
                        content_indicators=processing_result["indian_legal_indicators"]
                    )
                    
                    # Step 3: Comprehensive Scoring
                    st.write("📊 Calculating comprehensive compliance scores...")
                    comprehensive_scores = scoring_engine.calculate_comprehensive_score(
                        document_analysis=processing_result,
                        frameworks_applied=framework_selection["selected_frameworks"]
                    )
                    
                    # Store enhanced results
                    st.session_state.processing_result = processing_result
                    st.session_state.framework_selection = framework_selection
                    st.session_state.comprehensive_scores = comprehensive_scores
                    
                    # Step 4: Traditional Legal Analysis (Enhanced)
                    st.write("🏛️ Performing constitutional analysis...")
                    full_text = "\n".join([chunk["text"] for chunk in processing_result["enhanced_chunks"]])
                    constitutional_analysis = constitutional_engine.analyze_document_constitutionality(full_text)
                    
                    st.write("🔒 Analyzing Article 21 privacy implications...")
                    privacy_analysis = privacy_analyzer.analyze_privacy_implications(full_text)
                    
                    st.write("📋 Assessing DPDPA 2023 compliance...")
                    dpdpa_analysis = dpdpa_engine.assess_dpdpa_compliance(full_text, privacy_analysis)
                    
                    # Store traditional results
                    st.session_state.constitutional_analysis = constitutional_analysis
                    st.session_state.privacy_analysis = privacy_analysis
                    st.session_state.dpdpa_analysis = dpdpa_analysis
                    
                    # Calculate overall compliance
                    overall_score = calculate_overall_compliance(
                        constitutional_analysis, privacy_analysis, dpdpa_analysis
                    )
                    st.session_state.compliance_score = overall_score
                    st.session_state.document_processed = True
                    
                    # Display immediate results with extraction method info
                    st.success("✅ Complete legal analysis finished!")
                    
                    # Quick results preview with extraction details
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Document Type", 
                                processing_result["document_classification"]["primary_type"].replace('_', ' ').title())
                    with col2:
                        st.metric("Classification Confidence", 
                                f"{processing_result['document_classification']['confidence']:.1%}")
                    with col3:
                        extraction_method = processing_result["metadata"].get("extraction_method", "unknown")
                        method_display = {
                            "primary_pymupdf": "📄 Text Extraction",
                            "alternative_pymupdf": "🔄 Alternative Method",
                            "ocr_fallback": "🔍 OCR Extraction"
                        }.get(extraction_method, "❓ Unknown")
                        st.metric("Extraction Method", method_display)
                    with col4:
                        st.metric("Overall Score", f"{comprehensive_scores['overall_score']:.1f}%")
                    
                    # Show extraction success details
                    if processing_result["metadata"]["extraction_success"]:
                        text_length = processing_result["processing_stats"]["text_length"]
                        pages = processing_result["processing_stats"]["total_pages"]
                        st.info(f"✅ Successfully extracted {text_length:,} characters from {pages} pages using {extraction_method.replace('_', ' ').title()}")
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
                    logger.error(f"Document analysis error: {str(e)}")
                    
                    # Additional error context
                    st.write("**🔧 Troubleshooting Tips:**")
                    st.info("• Ensure the PDF is not password-protected")
                    st.info("• Try a different PDF file")
                    if not OCR_AVAILABLE:
                        st.info("• Install OCR support: `pip install easyocr`")
                    st.info("• Check system logs for detailed error information")

def results_dashboard_tab():
    """Enhanced results dashboard with comprehensive metrics and extraction details"""
    st.header("📊 Enhanced Analysis Results Dashboard")
    
    if not st.session_state.get('document_processed'):
        st.info("📄 Please upload and analyze a document first")
        return
    
    # Document Processing Status
    if 'processing_result' in st.session_state:
        processing = st.session_state.processing_result
        
        st.subheader("📋 Document Processing Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            extraction_method = processing["metadata"].get("extraction_method", "unknown")
            method_icons = {
                "primary_pymupdf": "📄",
                "alternative_pymupdf": "🔄", 
                "ocr_fallback": "🔍"
            }
            icon = method_icons.get(extraction_method, "❓")
            st.metric("Extraction Method", f"{icon} {extraction_method.replace('_', ' ').title()}")
        
        with col2:
            pages = processing["processing_stats"]["total_pages"]
            st.metric("Document Pages", pages)
        
        with col3:
            text_length = processing["processing_stats"]["text_length"]
            st.metric("Text Length", f"{text_length:,} chars")
        
        with col4:
            chunks = processing["processing_stats"]["total_chunks"]
            st.metric("Text Chunks", chunks)
        
        # Validation and extraction details
        if processing["metadata"].get("validation_info"):
            with st.expander("🔍 Document Validation & Extraction Details"):
                validation = processing["metadata"]["validation_info"]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**PDF Validation Results:**")
                    st.write(f"• File Size: {validation.get('file_size', 0):,} bytes")
                    st.write(f"• Valid PDF: {'✅' if validation.get('is_valid', False) else '❌'}")
                    st.write(f"• Has Text: {'✅' if validation.get('has_text', False) else '❌'}")
                    st.write(f"• Encrypted: {'❌ Yes' if validation.get('is_encrypted', False) else '✅ No'}")
                
                with col2:
                    st.write("**Extraction Process:**")
                    st.write(f"• Method Used: {extraction_method.replace('_', ' ').title()}")
                    st.write(f"• Success: {'✅' if processing['metadata']['extraction_success'] else '❌'}")
                    st.write(f"• OCR Available: {'✅' if OCR_AVAILABLE else '❌'}")
                    if extraction_method == "ocr_fallback":
                        st.info("🔍 Document was processed using OCR (scanned/image-based PDF)")
    
    # Enhanced Classification Results
    if 'processing_result' in st.session_state:
        st.subheader("🎯 Advanced Document Classification")
        processing = st.session_state.processing_result
        classification = processing["document_classification"]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Document Type", classification["primary_type"].replace('_', ' ').title())
        with col2:
            st.metric("Confidence", f"{classification['confidence']:.1%}")
        with col3:
            st.metric("Confidence Level", classification.get("confidence_level", "unknown").title())
        with col4:
            st.metric("Classification Method", "Advanced ML")
        
        # Alternative classifications
        if classification.get("alternative_classifications"):
            with st.expander("🔍 Alternative Classifications"):
                for i, alt in enumerate(classification["alternative_classifications"][:3], 1):
                    st.write(f"{i}. **{alt['document_type'].replace('_', ' ').title()}**: {alt['confidence']:.1%} confidence ({alt['confidence_level']})")
    
    # Framework Selection Results
    if 'framework_selection' in st.session_state:
        st.subheader("🎯 Selected Legal Frameworks")
        selection = st.session_state.framework_selection
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Frameworks Selected", len(selection["selected_frameworks"]))
        with col2:
            st.metric("Selection Confidence", f"{selection['selection_confidence']:.1%}")
        with col3:
            st.metric("Document Category", selection["document_type"].replace('_', ' ').title())
        
        # Framework details
        with st.expander("🔍 Framework Selection Reasoning"):
            for framework in selection["selected_frameworks"]:
                reason = selection["selection_reasons"].get(framework, "Selected for comprehensive analysis")
                st.write(f"• **{framework.replace('_', ' ').title()}**: {reason}")
    
    # Comprehensive Scoring Results
    if 'comprehensive_scores' in st.session_state:
        st.subheader("⚖️ Comprehensive Compliance Analysis")
        scores = st.session_state.comprehensive_scores
        
        # Main metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Overall Score", f"{scores['overall_score']:.1f}%")
        with col2:
            st.metric("Compliance Level", scores['compliance_level'].replace('_', ' ').title())
        with col3:
            st.metric("Analysis Confidence", f"{scores['confidence_level']:.1%}")
        with col4:
            risk_level = scores['risk_assessment']['overall_risk_level']
            st.metric("Risk Level", risk_level.replace('_', ' ').title())
        
        # Category scores breakdown
        if scores.get('category_scores'):
            st.subheader("📋 Detailed Category Analysis")
            for category, score_data in scores['category_scores'].items():
                with st.expander(f"📊 {category.replace('_', ' ').title()} - {score_data['score']:.1f}%"):
                    st.write(f"**Framework:** {score_data.get('framework', 'N/A').replace('_', ' ').title()}")
                    st.write(f"**Score:** {score_data['score']:.1f}%")
                    
                    if score_data.get('issues'):
                        st.write("**Issues Identified:**")
                        for issue in score_data['issues'][:3]:  # Show top 3
                            st.error(f"• {issue}")
                    
                    if score_data.get('recommendations'):
                        st.write("**Recommendations:**")
                        for rec in score_data['recommendations'][:3]:  # Show top 3
                            st.info(f"• {rec}")
    
    # Traditional Analysis Results (Constitutional, Privacy, DPDPA)
    if 'constitutional_analysis' in st.session_state:
        st.subheader("🏛️ Constitutional Analysis Summary")
        constitutional = st.session_state.constitutional_analysis
        articles = constitutional.get('constitutional_articles', [])
        
        if articles:
            st.write("**Key Constitutional Articles Identified:**")
            for article in articles[:5]:
                article_id = article.get('article_id', '').replace('article_', '')
                relevance = article.get('relevance_score', 0)
                implication = article.get('implication_type', 'Constitutional provision')
                st.write(f"• **Article {article_id}**: {implication} (Relevance: {relevance:.2f})")

def framework_analysis_tab():
    """Detailed framework and scoring analysis"""
    st.header("🎯 Legal Framework Analysis Details")
    
    if not st.session_state.get('framework_selection'):
        st.info("📄 Please analyze a document first to see framework selection")
        return
    
    selection = st.session_state.framework_selection
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Selected Frameworks Details")
        
        # Initialize framework engine for details
        framework_engine = AdaptiveLegalFrameworkEngine()
        
        for framework in selection["selected_frameworks"]:
            with st.expander(f"📖 {framework.replace('_', ' ').title()}"):
                details = framework_engine.get_framework_details(framework)
                
                st.write(f"**Description:** {details.get('description', 'N/A')}")
                st.write(f"**Priority:** {details.get('priority', 'N/A')}")
                
                if 'analysis_methods' in details:
                    st.write("**Analysis Methods:**")
                    for method in details['analysis_methods']:
                        st.write(f"• {method.replace('_', ' ').title()}")
                
                if 'constitutional_articles_details' in details:
                    st.write("**Key Constitutional Articles:**")
                    for article_num, article_info in details['constitutional_articles_details'].items():
                        st.write(f"• **Article {article_num}**: {article_info['title']}")
                
                # Selection reasoning
                reason = selection["selection_reasons"].get(framework, "No specific reason provided")
                st.write(f"**Selection Reason:** {reason}")
    
    with col2:
        if 'comprehensive_scores' in st.session_state:
            st.subheader("🎯 Risk Assessment")
            scores = st.session_state.comprehensive_scores
            
            # Risk assessment details
            risk_data = scores.get('risk_assessment', {})
            if risk_data.get('category_risks'):
                for category, risk_info in risk_data['category_risks'].items():
                    risk_level = risk_info['risk_level']
                    risk_color = {
                        'very_low': '🟢',
                        'low': '🔵', 
                        'medium': '🟡',
                        'high': '🟠',
                        'very_high': '🔴'
                    }.get(risk_level, '⚪')
                    
                    st.write(f"{risk_color} **{category.replace('_', ' ').title()}**")
                    st.write(f"Risk Level: {risk_level.replace('_', ' ').title()}")
                    st.write(f"Score: {risk_info['score']:.1f}%")
                    st.write("---")
            
            # Critical risks summary
            if risk_data.get('critical_risks'):
                st.subheader("⚠️ Critical Risks")
                for risk in risk_data['critical_risks']:
                    st.error(f"**{risk['category'].replace('_', ' ').title()}**: {risk['risk_level'].replace('_', ' ').title()} risk")

def interactive_qa_tab():
    """Interactive Q&A chatbot interface"""
    st.header("🤖 Interactive Legal Q&A Assistant")
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        try:
            st.session_state.chatbot = IndianLegalChatbot()
        except Exception as e:
            st.error(f"❌ Error initializing chatbot: {str(e)}")
            st.info("Please ensure GROQ_API_KEY is configured in your .env file")
            return
    
    # Chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("💬 Ask Your Legal Questions")
        
        # Question input
        question = st.text_input("Enter your question about constitutional law, privacy rights, or DPDPA compliance:")
        
        col_ask, col_clear = st.columns([2, 1])
        
        with col_ask:
            if st.button("🔍 Ask Question", type="primary") and question:
                with st.spinner("🤔 Analyzing and generating response..."):
                    try:
                        # Get document context if available
                        document_context = ""
                        if st.session_state.get('processing_result'):
                            chunks = st.session_state.processing_result.get('enhanced_chunks', [])
                            if chunks:
                                document_context = chunks[0].get('text', '')[:2000]
                        
                        response = st.session_state.chatbot.chat(question, document_context)
                        
                        st.success("✅ Response generated!")
                        
                        # Display response
                        with st.container():
                            st.markdown("### 💭 Question")
                            st.write(question)
                            
                            st.markdown("### 🎯 Answer")
                            st.write(response['answer'])
                            
                            if response.get('sources'):
                                st.markdown("### 📚 Sources")
                                st.write(', '.join(response['sources']))
                    
                    except Exception as e:
                        st.error(f"❌ Error processing question: {str(e)}")
        
        with col_clear:
            if st.button("🗑️ Clear History"):
                if hasattr(st.session_state, 'chatbot'):
                    st.session_state.chatbot.clear_history()
                    st.success("🧹 Chat history cleared!")
                    st.rerun()
    
    with col2:
        st.subheader("💡 Sample Questions")
        
        sample_questions = [
            "What does Article 21 say about privacy rights?",
            "How does DPDPA 2023 relate to constitutional rights?", 
            "What are the key principles from Puttaswamy judgment?",
            "What is the constitutional basis for data protection?",
            "How do fundamental rights apply to this document?",
            "Explain Article 14 equality principle",
            "What are data fiduciary obligations under DPDPA?"
        ]
        
        for i, q in enumerate(sample_questions):
            if st.button(q, key=f"sample_{i}"):
                st.info(f"Selected: {q}")
                st.info("👆 Copy this question to the input field above")

def document_summarization_tab():
    """Document summarization interface"""
    st.header("📋 Advanced Document Summarization")
    
    if not st.session_state.get('processing_result'):
        st.info("📄 Please upload and analyze a document first")
        return
    
    # Show extraction method info
    if st.session_state.processing_result["metadata"].get("extraction_method"):
        method = st.session_state.processing_result["metadata"]["extraction_method"]
        method_display = {
            "primary_pymupdf": "📄 Text-based PDF",
            "alternative_pymupdf": "🔄 Enhanced extraction",
            "ocr_fallback": "🔍 OCR-processed document"
        }.get(method, method)
        st.info(f"Document processed using: {method_display}")
    
    # Initialize summarizer
    if 'summarizer' not in st.session_state:
        try:
            st.session_state.summarizer = LegalDocumentSummarizer()
        except Exception as e:
            st.error(f"❌ Error initializing summarizer: {str(e)}")
            return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📄 Document Summary Options")
        
        summary_type = st.selectbox(
            "Choose Summary Type",
            ["executive", "detailed", "constitutional", "privacy"],
            format_func=lambda x: {
                "executive": "📋 Executive Summary",
                "detailed": "📑 Detailed Analysis",
                "constitutional": "🏛️ Constitutional Analysis",
                "privacy": "🔒 Privacy Analysis"
            }[x]
        )
        
        if st.button("📝 Generate Summary", type="primary"):
            with st.spinner(f"🔄 Generating {summary_type} summary..."):
                try:
                    # Extract text from chunks
                    chunks = st.session_state.processing_result.get('enhanced_chunks', [])
                    full_text = "\n".join([chunk.get('text', '') for chunk in chunks])
                    
                    summary_result = st.session_state.summarizer.summarize_document(
                        full_text, summary_type
                    )
                    
                    st.session_state[f'{summary_type}_summary'] = summary_result
                    st.success("✅ Summary generated!")
                except Exception as e:
                    st.error(f"❌ Summary generation failed: {str(e)}")
        
        # Display generated summary
        if st.session_state.get(f'{summary_type}_summary'):
            result = st.session_state[f'{summary_type}_summary']
            
            st.subheader(f"📋 {summary_type.title()} Summary")
            
            if 'error' not in result:
                st.write(result['summary'])
                
                with st.expander("📊 Summary Statistics"):
                    st.write(f"**Word Count:** {result.get('word_count', 'N/A')}")
                    st.write(f"**Source Length:** {result.get('source_length', 'N/A')} characters")
                    st.write(f"**Generated:** {result.get('timestamp', 'N/A')}")
            else:
                st.error(f"Error generating summary: {result.get('error', 'Unknown error')}")
    
    with col2:
        st.subheader("🚀 Quick Actions")
        
        if st.button("📋 Generate All Summaries"):
            with st.spinner("🔄 Generating all summary types..."):
                try:
                    chunks = st.session_state.processing_result.get('enhanced_chunks', [])
                    full_text = "\n".join([chunk.get('text', '') for chunk in chunks])
                    
                    all_summaries = st.session_state.summarizer.generate_all_summaries(full_text)
                    st.session_state.all_summaries = all_summaries
                    st.success("✅ All summaries generated!")
                except Exception as e:
                    st.error(f"❌ Error generating summaries: {str(e)}")

def regulatory_updates_tab():
    """Regulatory updates and compliance monitoring"""
    st.header("🌐 Indian Legal & Regulatory Updates")
    
    # Initialize scraper
    if 'scraper' not in st.session_state:
        st.session_state.scraper = IndianRegulatoryUpdatesScraper()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📊 Recent Legal Updates")
        
        # Filter options
        category_filter = st.selectbox(
            "Filter by Category",
            ["all", "constitutional", "privacy", "general"],
            format_func=lambda x: {
                "all": "🌐 All Updates",
                "constitutional": "🏛️ Constitutional Updates",
                "privacy": "🔒 Privacy & Data Protection",
                "general": "📋 General Legal Updates"
            }[x]
        )
        
        days_filter = st.slider("Days to look back", 7, 90, 30)
        
        if st.button("🔄 Fetch Latest Updates", type="primary"):
            with st.spinner("🌐 Scraping legal sources..."):
                try:
                    updates = st.session_state.scraper.get_filtered_updates(
                        category=category_filter,
                        days_back=days_filter
                    )
                    st.session_state.regulatory_updates = updates
                    st.success(f"✅ Found {len(updates)} updates!")
                except Exception as e:
                    st.error(f"❌ Error fetching updates: {str(e)}")
                    st.info("Note: Some legal websites may restrict automated access")
        
        # Display updates
        if st.session_state.get('regulatory_updates'):
            updates = st.session_state.regulatory_updates
            
            if updates:
                st.subheader(f"📋 {len(updates)} Recent Updates")
                
                for i, update in enumerate(updates[:20]):  # Show first 20
                    with st.expander(f"📄 {update['source']} - {update['title'][:60]}..."):
                        st.write(f"**Title:** {update['title']}")
                        st.write(f"**Source:** {update['source']}")
                        st.write(f"**Type:** {update['type']}")
                        st.write(f"**Date:** {update['scraped_date']}")
                        
                        if update.get('link') and update['link'] != '':
                            st.write(f"**Link:** [View Source]({update['link']})")
            else:
                st.info("No updates found for the selected criteria")
    
    with col2:
        st.subheader("⚙️ Monitoring Features")
        
        st.info("🔔 **Monitored Sources:**")
        st.write("• Supreme Court of India")
        st.write("• Ministry of Law & Justice")
        st.write("• Parliament Proceedings")
        st.write("• Constitutional Updates")
        st.write("• Privacy Law Changes")

def report_generation_tab():
    """Report generation and email interface"""
    st.header("📧 Enhanced Report Generation")
    
    if not st.session_state.get('document_processed'):
        st.info("📄 Please analyze a document first")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📄 Generate Comprehensive PDF Report")
        
        # Show extraction method in report options
        if st.session_state.processing_result["metadata"].get("extraction_method"):
            method = st.session_state.processing_result["metadata"]["extraction_method"]
            st.info(f"Report will include extraction method: {method.replace('_', ' ').title()}")
        
        report_type = st.selectbox(
            "Report Type",
            ["comprehensive_analysis", "constitutional_focus", "privacy_focus", "dpdpa_compliance"]
        )
        
        if st.button("📄 Generate Enhanced PDF Report"):
            with st.spinner("🔄 Generating comprehensive report..."):
                try:
                    report_generator = IndianLegalReportGenerator()
                    
                    # Collect all analysis results including extraction details
                    analysis_results = {
                        'processing_result': st.session_state.get('processing_result', {}),
                        'framework_selection': st.session_state.get('framework_selection', {}),
                        'comprehensive_scores': st.session_state.get('comprehensive_scores', {}),
                        'constitutional_analysis': st.session_state.get('constitutional_analysis', {}),
                        'privacy_analysis': st.session_state.get('privacy_analysis', {}),
                        'dpdpa_analysis': st.session_state.get('dpdpa_analysis', {}),
                        'compliance_score': st.session_state.get('compliance_score', {})
                    }
                    
                    report_result = report_generator.generate_comprehensive_report(
                        analysis_results,
                        st.session_state.get('processing_result', {}).get('metadata', {})
                    )
                    
                    if report_result['success']:
                        st.session_state.comprehensive_report = report_result['pdf_buffer']
                        st.success("✅ Enhanced PDF report generated successfully!")
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Enhanced PDF Report",
                            data=report_result['pdf_buffer'].getvalue(),
                            file_name=f"enhanced_legal_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error(f"❌ Report generation failed: {report_result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"❌ Report generation error: {str(e)}")
    
    with col2:
        st.subheader("📊 Report Features")
        
        st.info("📋 **Enhanced Report Includes:**")
        st.write("• Advanced Document Classification")
        st.write("• Extraction Method Details")
        st.write("• Framework Selection Reasoning")
        st.write("• Comprehensive Compliance Scoring")
        st.write("• Risk Assessment Matrix")
        st.write("• Constitutional Analysis")
        st.write("• Privacy Rights Assessment")
        st.write("• DPDPA Compliance Review")
        st.write("• Document Processing Statistics")
        st.write("• Actionable Recommendations")

def knowledge_graph_tab():
    """Knowledge graph explorer interface"""
    st.header("🔍 Constitutional Knowledge Graph Explorer")
    
    try:
        kg = ConstitutionalKnowledgeGraph()
        
        # Graph statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Knowledge Graph Statistics")
            stats = kg.get_knowledge_graph_stats()
            for stat_name, count in stats.items():
                st.metric(stat_name.replace('_', ' ').title(), count)
        
        with col2:
            st.subheader("🔍 Pathway Explorer")
            start_concept = st.text_input("Start Concept", placeholder="article_21")
            end_concept = st.text_input("End Concept", placeholder="privacy_right")
            max_hops = st.slider("Maximum Hops", 1, 6, 3)
            
            if st.button("🔍 Find Constitutional Pathway") and start_concept and end_concept:
                pathways = kg.find_constitutional_pathway(start_concept, end_concept, max_hops)
                
                if pathways:
                    st.subheader(f"🛤️ Constitutional Pathways ({len(pathways)} found)")
                    for i, pathway in enumerate(pathways[:3], 1):
                        with st.expander(f"Pathway {i}"):
                            st.write("Constitutional reasoning pathway found between concepts")
                else:
                    st.info("No pathways found between the specified concepts")
                    
    except Exception as e:
        st.error(f"❌ Knowledge graph error: {str(e)}")

def system_status_tab():
    """Enhanced system status and monitoring with OCR status"""
    st.header("⚙️ Enhanced System Status & Monitoring")
    
    # Environment variables status
    st.subheader("🔧 Environment Configuration")
    env_status = validate_environment_variables()
    
    for component, status in env_status.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{component.upper()} Configuration**")
        with col2:
            if status:
                st.success("✅ Configured")
            else:
                st.error("❌ Missing")
    
    # OCR Status
    st.subheader("🔍 OCR & Document Processing Status")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**EasyOCR Library**")
    with col2:
        if OCR_AVAILABLE:
            st.success("✅ Available")
        else:
            st.error("❌ Not Installed")
    
    if not OCR_AVAILABLE:
        st.warning("⚠️ Install OCR support for scanned documents: `pip install easyocr`")
    else:
        st.info("✅ System can process both text-based and scanned PDF documents")
    
    # Enhanced system health
    st.subheader("🏥 System Health Dashboard")
    
    if st.button("🔍 Run Comprehensive Health Checks"):
        with st.spinner("Checking all system components..."):
            health_results = {}
            
            # Check enhanced document processor
            try:
                doc_processor = IndianLegalDocumentProcessor()
                health_results['document_processor'] = True
                
                # Check OCR availability within processor
                if doc_processor.ocr_reader is not None:
                    health_results['ocr_integration'] = True
                else:
                    health_results['ocr_integration'] = False
                    
            except Exception as e:
                health_results['document_processor'] = False
                health_results['ocr_integration'] = False
                st.error(f"Document Processor error: {str(e)}")
            
            # Check framework engine
            try:
                framework_engine = AdaptiveLegalFrameworkEngine()
                health_results['framework_engine'] = True
            except Exception as e:
                health_results['framework_engine'] = False
                st.error(f"Framework Engine error: {str(e)}")
            
            # Check scoring engine
            try:
                scoring_engine = UniversalLegalScoringEngine()
                health_results['scoring_engine'] = True
            except Exception as e:
                health_results['scoring_engine'] = False
                st.error(f"Scoring Engine error: {str(e)}")
            
            # Neo4j connection
            try:
                neo4j_conn = get_neo4j_connection()
                health_results['neo4j'] = True
            except Exception as e:
                health_results['neo4j'] = False
                st.error(f"Neo4j error: {str(e)}")
            
            # Display results
            st.subheader("📊 Health Check Results")
            for component, status in health_results.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{component.replace('_', ' ').title()}**")
                with col2:
                    if status:
                        st.success("✅ Healthy")
                    else:
                        st.error("❌ Failed")
            
            # Processing capabilities summary
            st.subheader("📄 Document Processing Capabilities")
            capabilities = []
            if health_results.get('document_processor'):
                capabilities.append("✅ Text-based PDF processing")
                capabilities.append("✅ Alternative extraction methods")
            
            if health_results.get('ocr_integration') and OCR_AVAILABLE:
                capabilities.append("✅ OCR processing for scanned documents")
                capabilities.append("✅ Multi-language support (English + Hindi)")
            else:
                capabilities.append("❌ OCR processing unavailable")
            
            for capability in capabilities:
                st.write(capability)

def calculate_overall_compliance(constitutional_analysis, privacy_analysis, dpdpa_analysis):
    """Calculate overall compliance score"""
    scores = {
        'constitutional_score': constitutional_analysis.get('compliance_score', {}).get('overall_score', 0),
        'privacy_score': privacy_analysis.get('privacy_risk_score', {}).get('overall_score', 0),
        'dpdpa_score': dpdpa_analysis.get('dpdpa_compliance_summary', {}).get('overall_score', 0)
    }
    
    # Weighted average
    overall_score = (
        scores['constitutional_score'] * 0.4 +
        scores['privacy_score'] * 0.3 +
        scores['dpdpa_score'] * 0.3
    )
    
    return {
        'overall_score': overall_score,
        'constitutional_score': scores['constitutional_score'],
        'privacy_score': scores['privacy_score'],
        'dpdpa_score': scores['dpdpa_score'],
        'calculation_timestamp': datetime.now().isoformat()
    }

if __name__ == "__main__":
    main()
