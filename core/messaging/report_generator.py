"""
Enhanced Report Generator using Groq API for Indian Legal KAG System
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from io import BytesIO, StringIO
import os
from fpdf import FPDF
import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

logger = logging.getLogger(__name__)

class IndianLegalReportGenerator:
    """Enhanced report generator for Indian legal analysis using Groq API"""
    
    def __init__(self):
        self.groq_llm = self._initialize_groq_llm()
        self.report_templates = self._initialize_report_templates()
    
    @st.cache_resource
    def _initialize_groq_llm(_self):  # ✅ Underscore prefix tells Streamlit not to hash 
        """Initialize Groq LLM"""
        try:
            return ChatGroq(
                model_name="llama-3.3-70b-versatile",
                api_key=os.getenv("GROQ_API_KEY"),
                request_timeout=60,
                temperature=0.1  # Low temperature for consistent legal analysis
            )
        except Exception as e:
            logger.error(f"Failed to initialize Groq LLM: {str(e)}")
            return None
    
    def _initialize_report_templates(self) -> Dict[str, str]:
        """Initialize report generation templates for Groq"""
        return {
            "constitutional_summary": """
            You are an expert in Indian Constitutional Law. Based on the following constitutional analysis data, generate a comprehensive summary that explains the constitutional implications in clear, professional language suitable for legal practitioners.

            Analysis Data: {analysis_data}

            Generate a summary that includes:
            1. Key constitutional articles identified and their relevance
            2. Constitutional reasoning pathways
            3. Compliance assessment with Indian constitutional framework
            4. References to relevant Supreme Court precedents
            5. Practical implications for legal practice

            Format the response in clear paragraphs with proper legal terminology.
            """,
            
            "privacy_summary": """
            You are an expert in Indian Privacy Law and Article 21 jurisprudence. Based on the following privacy analysis data, generate a comprehensive summary explaining the privacy implications under Indian Constitutional framework.

            Analysis Data: {analysis_data}

            Generate a summary that includes:
            1. Article 21 privacy rights analysis based on Puttaswamy judgment
            2. Four dimensions of privacy (informational, bodily, communications, territorial)
            3. Constitutional compliance assessment
            4. Practical privacy implications
            5. Recommendations for privacy protection

            Use the framework established in Justice K.S. Puttaswamy (Retd.) v. Union of India (2017).
            """,
            
            "dpdpa_summary": """
            You are an expert in DPDPA 2023 and Indian data protection law. Based on the following DPDPA compliance analysis, generate a comprehensive summary explaining the compliance status and requirements.

            Analysis Data: {analysis_data}

            Generate a summary that includes:
            1. DPDPA 2023 compliance assessment
            2. Key sections analyzed (Section 5, 8, 11)
            3. Constitutional alignment with Article 21
            4. Compliance gaps and recommendations
            5. Practical steps for DPDPA compliance

            Reference the Digital Personal Data Protection Act 2023 and its constitutional foundation.
            """,
            
            "comprehensive_executive_summary": """
            You are a senior legal expert specializing in Indian Constitutional Law, Privacy Rights, and Data Protection. Based on the comprehensive legal analysis provided, generate an executive summary suitable for legal practitioners and business stakeholders.

            Analysis Data: {analysis_data}

            Generate an executive summary that includes:
            1. Overall legal compliance status
            2. Key constitutional, privacy, and regulatory findings
            3. Critical risk areas and recommendations
            4. Business and legal implications
            5. Next steps and action items

            Write in a professional tone suitable for legal and business audiences.
            """
        }
    
    def generate_comprehensive_report(
        self,
        analysis_results: Dict[str, Any],
        document_metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive PDF report with AI-enhanced summaries"""
        
        try:
            logger.info("🔄 Generating comprehensive legal report...")
            
            # Generate AI-enhanced summaries using Groq
            ai_summaries = self._generate_ai_summaries(analysis_results)
            
            # Create PDF report
            pdf_buffer = self._create_pdf_report(analysis_results, ai_summaries, document_metadata)
            
            # Generate report metadata
            report_metadata = self._generate_report_metadata(analysis_results, document_metadata)
            
            logger.info("✅ Comprehensive report generated successfully")
            
            return {
                "pdf_buffer": pdf_buffer,
                "ai_summaries": ai_summaries,
                "report_metadata": report_metadata,
                "generation_timestamp": datetime.now().isoformat(),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"❌ Report generation failed: {str(e)}")
            return {
                "pdf_buffer": None,
                "error": str(e),
                "generation_timestamp": datetime.now().isoformat(),
                "success": False
            }
    
    def _generate_ai_summaries(self, analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """Generate AI-enhanced summaries using Groq LLM"""
        
        ai_summaries = {}
        
        if not self.groq_llm:
            logger.warning("⚠️ Groq LLM not available, using template summaries")
            return self._generate_template_summaries(analysis_results)
        
        try:
            # Constitutional Analysis Summary
            if "constitutional_analysis" in analysis_results:
                constitutional_prompt = PromptTemplate.from_template(
                    self.report_templates["constitutional_summary"]
                )
                
                constitutional_chain = constitutional_prompt | self.groq_llm
                ai_summaries["constitutional"] = constitutional_chain.invoke({
                    "analysis_data": str(analysis_results["constitutional_analysis"])
                }).content
            
            # Privacy Analysis Summary
            if "privacy_analysis" in analysis_results:
                privacy_prompt = PromptTemplate.from_template(
                    self.report_templates["privacy_summary"]
                )
                
                privacy_chain = privacy_prompt | self.groq_llm
                ai_summaries["privacy"] = privacy_chain.invoke({
                    "analysis_data": str(analysis_results["privacy_analysis"])
                }).content
            
            # DPDPA Compliance Summary
            if "dpdpa_analysis" in analysis_results:
                dpdpa_prompt = PromptTemplate.from_template(
                    self.report_templates["dpdpa_summary"]
                )
                
                dpdpa_chain = dpdpa_prompt | self.groq_llm
                ai_summaries["dpdpa"] = dpdpa_chain.invoke({
                    "analysis_data": str(analysis_results["dpdpa_analysis"])
                }).content
            
            # Executive Summary
            executive_prompt = PromptTemplate.from_template(
                self.report_templates["comprehensive_executive_summary"]
            )
            
            executive_chain = executive_prompt | self.groq_llm
            ai_summaries["executive"] = executive_chain.invoke({
                "analysis_data": str(analysis_results)
            }).content
            
            logger.info("✅ AI summaries generated successfully")
            
        except Exception as e:
            logger.error(f"❌ AI summary generation failed: {str(e)}")
            # Fallback to template summaries
            ai_summaries = self._generate_template_summaries(analysis_results)
        
        return ai_summaries
    
    def _generate_template_summaries(self, analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """Generate fallback template summaries when AI is not available"""
        
        summaries = {}
        
        # Constitutional summary
        if "constitutional_analysis" in analysis_results:
            constitutional = analysis_results["constitutional_analysis"]
            articles = constitutional.get("constitutional_articles", [])
            compliance_score = constitutional.get("compliance_score", {}).get("overall_score", 0)
            
            summaries["constitutional"] = f"""
CONSTITUTIONAL ANALYSIS SUMMARY

This document has been analyzed against the Indian Constitutional framework with a compliance score of {compliance_score}%.

Key Constitutional Articles Identified:
{chr(10).join([f"• Article {article.get('article_id', '').replace('article_', '')}: {article.get('implication_type', 'Constitutional provision')}" for article in articles[:5]])}

The analysis applies constitutional reasoning based on landmark Supreme Court judgments including Kesavananda Bharati (Basic Structure Doctrine), Maneka Gandhi (Article 21 expansion), and Puttaswamy (Right to Privacy).

Constitutional Hierarchy Assessment: The document provisions have been evaluated for consistency with fundamental rights (Part III) and their relationship with directive principles (Part IV) of the Constitution.
"""
        
        # Privacy summary
        if "privacy_analysis" in analysis_results:
            privacy = analysis_results["privacy_analysis"]
            article_21_compliance = privacy.get("constitutional_compliance", {}).get("article_21_compliance", "unknown")
            
            summaries["privacy"] = f"""
ARTICLE 21 PRIVACY RIGHTS ANALYSIS

Privacy Compliance Status: {article_21_compliance.replace('_', ' ').title()}

Based on the constitutional framework established in Justice K.S. Puttaswamy (Retd.) v. Union of India (2017), this analysis examines four dimensions of privacy:

1. Informational Privacy: Control over personal information and its disclosure
2. Bodily Privacy: Protection of physical self from unauthorized intrusion  
3. Communications Privacy: Privacy of communications and correspondence
4. Territorial Privacy: Protection of private spaces

The analysis applies the three-fold constitutional test: legitimate government aim, necessity, and proportionality as established in privacy jurisprudence.
"""
        
        # DPDPA summary
        if "dpdpa_analysis" in analysis_results:
            dpdpa = analysis_results["dpdpa_analysis"]
            overall_score = dpdpa.get("dpdpa_compliance_summary", {}).get("overall_score", 0)
            
            summaries["dpdpa"] = f"""
DPDPA 2023 COMPLIANCE ANALYSIS

DPDPA Compliance Score: {overall_score}%

This analysis assesses compliance with the Digital Personal Data Protection Act 2023, India's comprehensive data protection legislation. Key areas evaluated:

• Section 5: Grounds for processing personal data
• Section 8: Duties of Data Fiduciary  
• Section 11: Rights of Data Principal

Constitutional Integration: The DPDPA analysis ensures alignment with Article 21 privacy rights as established in the Puttaswamy judgment, maintaining constitutional consistency in data protection measures.
"""
        
        # Executive summary
        overall_score = analysis_results.get("compliance_score", {}).get("overall_score", 0)
        summaries["executive"] = f"""
EXECUTIVE SUMMARY

Overall Legal Compliance Score: {overall_score}%

This comprehensive analysis evaluates the document against India's constitutional framework, privacy rights jurisprudence, and data protection regulations. The analysis employs Knowledge Augmented Generation (KAG) to provide constitutional reasoning pathways that mirror how senior legal practitioners analyze Indian law.

Key Findings:
• Constitutional compliance assessed against fundamental rights and directive principles
• Privacy rights analysis based on Article 21 and Puttaswamy judgment framework
• DPDPA 2023 compliance evaluation with constitutional backing
• Multi-layer reasoning considering constitutional hierarchy and precedent authority

Recommendations: Detailed compliance recommendations and constitutional reasoning are provided in the full analysis sections below.
"""
        
        return summaries
    
    def _create_pdf_report(
        self,
        analysis_results: Dict[str, Any],
        ai_summaries: Dict[str, str],
        document_metadata: Dict[str, Any] = None
    ) -> BytesIO:
        """Create comprehensive PDF report"""
        
        try:
            pdf = FPDF()
            pdf.add_page()
            
            # Set fonts
            pdf.set_font("Arial", "B", 16)
            
            # Header
            pdf.cell(0, 10, "Indian Legal Knowledge Augmented Generation (KAG) Analysis Report", 0, 1, "C")
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p IST')}", 0, 1, "C")
            pdf.ln(10)
            
            # Document metadata section
            if document_metadata:
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, "Document Information", 0, 1)
                pdf.set_font("Arial", "", 11)
                
                doc_type = document_metadata.get("document_type", "Unknown")
                total_pages = document_metadata.get("total_pages", "N/A")
                
                pdf.cell(0, 8, f"Document Type: {doc_type}", 0, 1)
                pdf.cell(0, 8, f"Total Pages: {total_pages}", 0, 1)
                pdf.ln(5)
            
            # Executive Summary
            if "executive" in ai_summaries:
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, "Executive Summary", 0, 1)
                pdf.set_font("Arial", "", 11)
                self._add_text_to_pdf(pdf, ai_summaries["executive"])
                pdf.ln(10)
            
            # Constitutional Analysis
            if "constitutional" in ai_summaries:
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, "Constitutional Analysis", 0, 1)
                pdf.set_font("Arial", "", 11)
                self._add_text_to_pdf(pdf, ai_summaries["constitutional"])
                pdf.ln(10)
            
            # Privacy Analysis
            if "privacy" in ai_summaries:
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, "Article 21 Privacy Rights Analysis", 0, 1)
                pdf.set_font("Arial", "", 11)
                self._add_text_to_pdf(pdf, ai_summaries["privacy"])
                pdf.ln(10)
            
            # DPDPA Analysis
            if "dpdpa" in ai_summaries:
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, "DPDPA 2023 Compliance Analysis", 0, 1)
                pdf.set_font("Arial", "", 11)
                self._add_text_to_pdf(pdf, ai_summaries["dpdpa"])
                pdf.ln(10)
            
            # Detailed Analysis Sections
            self._add_detailed_analysis_sections(pdf, analysis_results)
            
            # Footer
            pdf.ln(10)
            pdf.set_font("Arial", "I", 10)
            pdf.cell(0, 8, "This report is generated by Indian Legal KAG System for informational purposes only.", 0, 1, "C")
            pdf.cell(0, 8, "Please consult qualified legal professionals for specific legal advice.", 0, 1, "C")
            
            # Generate PDF
            pdf_output = pdf.output(dest="S").encode("latin1")
            return BytesIO(pdf_output)
            
        except Exception as e:
            logger.error(f"❌ PDF creation failed: {str(e)}")
            return BytesIO(b"Error generating PDF report")
    
    def _add_text_to_pdf(self, pdf: FPDF, text: str):
        """Add text to PDF with proper encoding"""
        # Clean text for PDF compatibility
        clean_text = text.replace("•", "*").replace("\u2022", "*")
        clean_text = ''.join(c for c in clean_text if ord(c) < 256)
        
        # Add text with word wrapping
        pdf.multi_cell(0, 6, clean_text)
    
    def _add_detailed_analysis_sections(self, pdf: FPDF, analysis_results: Dict[str, Any]):
        """Add detailed analysis sections to PDF"""
        
        # Compliance Score Details
        if "compliance_score" in analysis_results:
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Detailed Compliance Scores", 0, 1)
            pdf.set_font("Arial", "", 11)
            
            compliance_score = analysis_results["compliance_score"]
            overall = compliance_score.get("overall_score", 0)
            components = compliance_score.get("component_scores", {})
            
            pdf.cell(0, 8, f"Overall Score: {overall}%", 0, 1)
            pdf.ln(3)
            
            for component, score in components.items():
                pdf.cell(0, 6, f"• {component.replace('_', ' ').title()}: {score}%", 0, 1)
            
            pdf.ln(10)
        
        # Constitutional Pathways
        if "constitutional_analysis" in analysis_results:
            constitutional = analysis_results["constitutional_analysis"]
            pathways = constitutional.get("constitutional_pathways", [])
            
            if pathways:
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, "Constitutional Reasoning Pathways", 0, 1)
                pdf.set_font("Arial", "", 11)
                
                for i, pathway in enumerate(pathways[:3], 1):
                    pdf.cell(0, 8, f"Pathway {i}:", 0, 1)
                    pathway_strength = pathway.get("pathway_strength", 0)
                    pdf.cell(0, 6, f"  Strength: {pathway_strength:.2f}", 0, 1)
                    
                    reasoning_chain = pathway.get("reasoning_chain", [])
                    if reasoning_chain:
                        for step in reasoning_chain[:3]:
                            step_text = str(step)[:80] + "..." if len(str(step)) > 80 else str(step)
                            clean_step = ''.join(c for c in step_text if ord(c) < 256)
                            pdf.cell(0, 6, f"  • {clean_step}", 0, 1)
                    pdf.ln(3)
    
    def _generate_report_metadata(
        self,
        analysis_results: Dict[str, Any],
        document_metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Generate report metadata"""
        
        metadata = {
            "report_type": "comprehensive_legal_analysis",
            "generation_timestamp": datetime.now().isoformat(),
            "system_version": "Indian Legal KAG v1.0",
            "analysis_components": list(analysis_results.keys()),
            "groq_llm_used": self.groq_llm is not None,
            "report_language": "English",
            "jurisdiction": "India",
            "constitutional_framework": "Indian Constitution",
            "privacy_framework": "Article 21 (Puttaswamy Judgment)",
            "data_protection_framework": "DPDPA 2023"
        }
        
        if document_metadata:
            metadata["document_metadata"] = document_metadata
        
        # Add analysis summary
        if "compliance_score" in analysis_results:
            metadata["overall_compliance_score"] = analysis_results["compliance_score"].get("overall_score", 0)
        
        return metadata
