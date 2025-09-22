"""
SMTP-Based Email Manager for Indian Legal KAG System
Enhanced with multiple provider support and comprehensive email templates
"""
import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Optional, Tuple, Any
import os
from datetime import datetime
import streamlit as st

logger = logging.getLogger(__name__)

class SMTPEmailManager:
    """SMTP-based email manager for sending legal analysis reports"""
    
    def __init__(self):
        self.smtp_config = self._load_smtp_config()
        self.smtp_providers = self._load_smtp_providers()
        self.email_templates = self._initialize_email_templates()
    
    def _load_smtp_config(self) -> Dict[str, Any]:
        """Load SMTP configuration from environment variables"""
        return {
            "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
            "smtp_port": int(os.getenv("SMTP_PORT", "587")),
            "sender_email": os.getenv("SENDER_EMAIL", ""),
            "sender_password": os.getenv("SENDER_PASSWORD", ""),  # App password for Gmail
            "sender_name": os.getenv("SENDER_NAME", "Indian Legal KAG System"),
            "use_tls": os.getenv("USE_TLS", "true").lower() == "true"
        }
    
    def _load_smtp_providers(self) -> Dict[str, Dict[str, Any]]:
        """Load SMTP provider configurations - THIS IS WHERE THE SMTP_CONFIGS GO"""
        return {
            "gmail": {
                "server": "smtp.gmail.com",
                "port": 587,
                "tls": True,
                "description": "Gmail SMTP Server",
                "setup_instructions": "Enable 2FA and generate App Password from Google Account Security settings"
            },
            "outlook": {
                "server": "smtp-mail.outlook.com", 
                "port": 587,
                "tls": True,
                "description": "Outlook/Hotmail SMTP Server",
                "setup_instructions": "Use regular password or App Password for enhanced security"
            },
            "yahoo": {
                "server": "smtp.mail.yahoo.com",
                "port": 587,
                "tls": True,
                "description": "Yahoo Mail SMTP Server",
                "setup_instructions": "Enable Less Secure Apps or generate App Password in Yahoo Account Security"
            },
            "office365": {
                "server": "smtp.office365.com",
                "port": 587,
                "tls": True,
                "description": "Microsoft Office 365 SMTP Server",
                "setup_instructions": "Use organizational credentials with Modern Authentication"
            },
            "custom": {
                "server": "",
                "port": 587,
                "tls": True,
                "description": "Custom SMTP Server",
                "setup_instructions": "Configure manually with your provider-specific settings"
            }
        }
    
    def _initialize_email_templates(self) -> Dict[str, Dict[str, str]]:
        """Initialize email templates for different types of legal reports"""
        return {
            "constitutional_analysis": {
                "subject": "🏛️ Constitutional Analysis Report - Indian Legal KAG System",
                "template_key": "constitutional"
            },
            "privacy_analysis": {
                "subject": "🔒 Privacy Rights Analysis Report (Article 21) - Indian Legal KAG System",
                "template_key": "privacy"
            },
            "dpdpa_compliance": {
                "subject": "📋 DPDPA 2023 Compliance Report - Indian Legal KAG System",
                "template_key": "dpdpa"
            },
            "comprehensive_report": {
                "subject": "⚖️ Comprehensive Legal Analysis Report - Indian Legal KAG System",
                "template_key": "comprehensive"
            },
            "error_report": {
                "subject": "❌ Legal Analysis Error Report - Indian Legal KAG System",
                "template_key": "error"
            }
        }
    
    def get_provider_config(self, provider_name: str) -> Optional[Dict[str, Any]]:
        """Get SMTP configuration for a specific provider"""
        return self.smtp_providers.get(provider_name.lower())
    
    def auto_configure_smtp(self, email_address: str) -> bool:
        """Auto-configure SMTP based on email domain"""
        try:
            domain = email_address.split('@')[1].lower()
            
            # Map common domains to providers
            domain_mapping = {
                'gmail.com': 'gmail',
                'googlemail.com': 'gmail',
                'outlook.com': 'outlook',
                'hotmail.com': 'outlook',
                'live.com': 'outlook',
                'msn.com': 'outlook',
                'yahoo.com': 'yahoo',
                'yahoo.co.in': 'yahoo',
                'yahoo.co.uk': 'yahoo',
                'rocketmail.com': 'yahoo'
            }
            
            provider = domain_mapping.get(domain)
            if provider:
                provider_config = self.get_provider_config(provider)
                if provider_config:
                    # Update SMTP config with provider settings
                    self.smtp_config.update({
                        "smtp_server": provider_config["server"],
                        "smtp_port": provider_config["port"],
                        "use_tls": provider_config["tls"]
                    })
                    
                    logger.info(f"✅ Auto-configured SMTP for {provider} ({domain})")
                    return True
            
            logger.warning(f"⚠️ No auto-configuration available for domain: {domain}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Auto-configuration failed: {str(e)}")
            return False
    
    def list_supported_providers(self) -> List[Dict[str, str]]:
        """List all supported SMTP providers"""
        return [
            {
                "name": name,
                "server": config["server"],
                "port": str(config["port"]),
                "description": config["description"],
                "setup_instructions": config["setup_instructions"]
            }
            for name, config in self.smtp_providers.items()
        ]
    
    def send_legal_analysis_email(
        self,
        recipient_email: str,
        analysis_results: Dict[str, Any],
        report_type: str = "comprehensive_report",
        attachment_data: Optional[bytes] = None,
        attachment_filename: str = "legal_analysis_report.pdf"
    ) -> Tuple[bool, str]:
        """
        Send legal analysis report via SMTP
        
        Args:
            recipient_email: Recipient's email address
            analysis_results: Dictionary containing analysis results
            report_type: Type of report (constitutional_analysis, privacy_analysis, etc.)
            attachment_data: PDF report as bytes
            attachment_filename: Name for the attachment file
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        
        try:
            # Validate SMTP configuration
            if not self._validate_smtp_config():
                return False, "❌ SMTP configuration incomplete. Please check environment variables."
            
            # Create email message
            message = self._create_email_message(
                recipient_email,
                analysis_results,
                report_type
            )
            
            # Add attachment if provided
            if attachment_data:
                self._add_pdf_attachment(message, attachment_data, attachment_filename)
            
            # Send email
            success, result_message = self._send_email_smtp(message, recipient_email)
            
            if success:
                logger.info(f"✅ Email sent successfully to {recipient_email}")
                return True, f"✅ Legal analysis report sent successfully to {recipient_email}"
            else:
                logger.error(f"❌ Failed to send email to {recipient_email}: {result_message}")
                return False, f"❌ Failed to send email: {result_message}"
                
        except Exception as e:
            logger.error(f"❌ Email sending error: {str(e)}")
            return False, f"❌ Email sending failed: {str(e)}"
    
    def _validate_smtp_config(self) -> bool:
        """Validate SMTP configuration"""
        required_fields = ["smtp_server", "sender_email", "sender_password"]
        
        for field in required_fields:
            if not self.smtp_config.get(field):
                logger.error(f"❌ Missing SMTP configuration: {field}")
                return False
        
        return True
    
    def _create_email_message(
        self,
        recipient_email: str,
        analysis_results: Dict[str, Any],
        report_type: str
    ) -> MIMEMultipart:
        """Create email message with appropriate template"""
        
        # Get email template info
        template_info = self.email_templates.get(report_type, self.email_templates["comprehensive_report"])
        
        # Create message
        message = MIMEMultipart("alternative")
        message["From"] = f"{self.smtp_config['sender_name']} <{self.smtp_config['sender_email']}>"
        message["To"] = recipient_email
        message["Subject"] = template_info["subject"]
        
        # Generate email content
        html_content = self._generate_email_html(analysis_results, template_info["template_key"])
        text_content = self._generate_email_text(analysis_results, template_info["template_key"])
        
        # Add both text and HTML parts
        text_part = MIMEText(text_content, "plain", "utf-8")
        html_part = MIMEText(html_content, "html", "utf-8")
        
        message.attach(text_part)
        message.attach(html_part)
        
        return message
    
    def _generate_email_html(self, analysis_results: Dict[str, Any], template_key: str) -> str:
        """Generate HTML email content based on analysis results"""
        
        # Get analysis summary
        compliance_score = analysis_results.get("compliance_score", {})
        constitutional_analysis = analysis_results.get("constitutional_analysis", {})
        privacy_analysis = analysis_results.get("privacy_analysis", {})
        dpdpa_analysis = analysis_results.get("dpdpa_analysis", {})
        
        # Base HTML template
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Indian Legal Analysis Report</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px; }}
                .header h1 {{ margin: 0; font-size: 28px; }}
                .header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
                .section {{ background: #f8f9fa; margin: 20px 0; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; }}
                .section h2 {{ color: #667eea; margin-top: 0; }}
                .score-box {{ background: white; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .score-high {{ border-left: 4px solid #28a745; }}
                .score-medium {{ border-left: 4px solid #ffc107; }}
                .score-low {{ border-left: 4px solid #dc3545; }}
                .footer {{ text-align: center; padding: 20px; color: #666; border-top: 1px solid #ddd; margin-top: 30px; }}
                .indian-flag {{ color: #FF9933; }}
                .constitutional {{ color: #138808; }}
                .privacy {{ color: #000080; }}
                ul {{ padding-left: 20px; }}
                li {{ margin: 5px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1><span class="indian-flag">🇮🇳</span> Indian Legal KAG Analysis Report</h1>
                    <p>Constitutional Reasoning & DPDPA Compliance Analysis</p>
                </div>
        """
        
        # Add content based on template type
        overall_score = compliance_score.get("overall_score", 0)
        score_class = "score-high" if overall_score >= 80 else "score-medium" if overall_score >= 60 else "score-low"
        
        html_template += f"""
        <div class="section">
            <h2>📊 Analysis Summary</h2>
            <div class="score-box {score_class}">
                <h3>Overall Legal Compliance Score: {overall_score}%</h3>
                <p>Multi-dimensional analysis covering constitutional, privacy, and regulatory compliance.</p>
            </div>
            
            <h3>Key Analysis Components:</h3>
            <ul>
                <li><strong class="constitutional">🏛️ Constitutional Analysis:</strong> Examined against Indian Constitutional framework with precedent analysis</li>
                <li><strong class="privacy">🔒 Article 21 Privacy Rights:</strong> Assessed under Puttaswamy judgment framework</li>
                <li><strong>📋 DPDPA 2023 Compliance:</strong> Evaluated for data protection regulatory compliance</li>
                <li><strong>⚖️ Legal Reasoning Pathways:</strong> Constitutional reasoning chains for legal practitioners</li>
            </ul>
        </div>
        """
        
        # Add footer
        html_template += f"""
                <div class="footer">
                    <p><strong>Generated by Indian Legal KAG System</strong></p>
                    <p>Knowledge Augmented Generation for Indian Constitutional Law</p>
                    <p><em>Report generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p IST')}</em></p>
                    <p style="font-size: 12px; color: #999;">
                        This analysis is for informational purposes only and does not constitute legal advice.
                        Please consult with qualified legal professionals for specific legal matters.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def _generate_email_text(self, analysis_results: Dict[str, Any], template_key: str) -> str:
        """Generate plain text email content"""
        
        overall_score = analysis_results.get("compliance_score", {}).get("overall_score", 0)
        
        text_content = f"""
INDIAN LEGAL KAG ANALYSIS REPORT
===============================

Dear Legal Professional,

Please find below the summary of your legal document analysis conducted using our Knowledge Augmented Generation system specifically designed for Indian Constitutional Law.

ANALYSIS SUMMARY:
-----------------
Overall Legal Compliance Score: {overall_score}%

This comprehensive analysis examines your document against:

1. CONSTITUTIONAL FRAMEWORK: Indian Constitution articles, fundamental rights, and directive principles
2. PRIVACY RIGHTS: Article 21 analysis based on Puttaswamy judgment (2017)
3. DPDPA 2023 COMPLIANCE: Digital Personal Data Protection Act requirements
4. LEGAL PRECEDENTS: Supreme Court cases and established jurisprudence

CONSTITUTIONAL REASONING:
------------------------
Our KAG system applies constitutional reasoning pathways that mirror how senior legal practitioners analyze Indian law, providing:

- Multi-layer constitutional hierarchy assessment
- Precedent-based legal reasoning
- Privacy rights framework analysis
- Regulatory compliance verification

DETAILED REPORT:
----------------
A comprehensive PDF report with detailed analysis, constitutional reasoning pathways, and compliance recommendations has been attached to this email.

IMPORTANT DISCLAIMER:
--------------------
This analysis is generated by an AI system for informational purposes only and does not constitute legal advice. Please consult with qualified legal professionals for specific legal matters.

Best regards,
Indian Legal KAG System
Knowledge Augmented Generation for Constitutional Law

Report generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p IST')}

---
© 2025 Indian Legal KAG System - All Rights Reserved
        """
        
        return text_content
    
    def _add_pdf_attachment(self, message: MIMEMultipart, attachment_data: bytes, filename: str):
        """Add PDF attachment to email message"""
        
        try:
            # Create attachment
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(attachment_data)
            
            # Encode attachment
            encoders.encode_base64(attachment)
            
            # Add header
            attachment.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}'
            )
            
            # Attach to message
            message.attach(attachment)
            
            logger.info(f"✅ PDF attachment added: {filename}")
            
        except Exception as e:
            logger.error(f"❌ Failed to add PDF attachment: {str(e)}")
    
    def _send_email_smtp(self, message: MIMEMultipart, recipient_email: str) -> Tuple[bool, str]:
        """Send email using SMTP with enhanced security"""
        
        try:
            # Create secure SSL context
            context = ssl.create_default_context()
            
            # Create SMTP session
            server = smtplib.SMTP(self.smtp_config["smtp_server"], self.smtp_config["smtp_port"])
            
            # Enable TLS if configured
            if self.smtp_config["use_tls"]:
                server.starttls(context=context)
            
            # Login to server
            server.login(self.smtp_config["sender_email"], self.smtp_config["sender_password"])
            
            # Send email
            text = message.as_string()
            server.sendmail(self.smtp_config["sender_email"], recipient_email, text)
            
            # Quit server
            server.quit()
            
            return True, "Email sent successfully"
            
        except smtplib.SMTPAuthenticationError as e:
            return False, f"SMTP Authentication failed: {str(e)}. Please check your App Password."
        except smtplib.SMTPRecipientsRefused as e:
            return False, f"Recipient refused: {str(e)}"
        except smtplib.SMTPServerDisconnected as e:
            return False, f"SMTP server disconnected: {str(e)}"
        except Exception as e:
            return False, f"SMTP error: {str(e)}"
    
    def test_smtp_connection(self) -> Tuple[bool, str]:
        """Test SMTP connection and authentication"""
        
        try:
            if not self._validate_smtp_config():
                return False, "SMTP configuration incomplete"
            
            # Create secure SSL context
            context = ssl.create_default_context()
            
            # Test connection
            server = smtplib.SMTP(self.smtp_config["smtp_server"], self.smtp_config["smtp_port"])
            
            if self.smtp_config["use_tls"]:
                server.starttls(context=context)
            
            server.login(self.smtp_config["sender_email"], self.smtp_config["sender_password"])
            server.quit()
            
            return True, "✅ SMTP connection and authentication successful"
            
        except smtplib.SMTPAuthenticationError as e:
            return False, f"❌ Authentication failed: {str(e)}. Please check your App Password."
        except Exception as e:
            return False, f"❌ SMTP connection failed: {str(e)}"
    
    def send_test_email(self, recipient_email: str) -> Tuple[bool, str]:
        """Send a test email to verify SMTP configuration"""
        
        try:
            # Create simple test message
            message = MIMEMultipart()
            message["From"] = f"{self.smtp_config['sender_name']} <{self.smtp_config['sender_email']}>"
            message["To"] = recipient_email
            message["Subject"] = "🧪 Test Email - Indian Legal KAG System"
            
            # Test email body
            test_body = f"""
Hello!

This is a test email from the Indian Legal KAG System to verify SMTP configuration.

✅ SMTP Server: {self.smtp_config['smtp_server']}:{self.smtp_config['smtp_port']}
✅ TLS Enabled: {self.smtp_config['use_tls']}
✅ Sender: {self.smtp_config['sender_email']}

If you receive this email, your SMTP configuration is working correctly!

Best regards,
Indian Legal KAG System

Sent on: {datetime.now().strftime('%B %d, %Y at %I:%M %p IST')}
            """
            
            message.attach(MIMEText(test_body, "plain"))
            
            # Send test email
            success, result_message = self._send_email_smtp(message, recipient_email)
            
            if success:
                return True, f"✅ Test email sent successfully to {recipient_email}"
            else:
                return False, f"❌ Test email failed: {result_message}"
                
        except Exception as e:
            return False, f"❌ Test email error: {str(e)}"

# Streamlit cache for email manager instance
@st.cache_resource
def get_smtp_email_manager():
    """Get cached SMTP email manager instance"""
    return SMTPEmailManager()

# Example usage and testing (remove in production)
if __name__ == "__main__":
    # Initialize email manager
    email_manager = SMTPEmailManager()
    
    # List supported providers
    print("📧 Supported SMTP Providers:")
    for provider in email_manager.list_supported_providers():
        print(f"• {provider['name'].upper()}: {provider['description']}")
        print(f"  Server: {provider['server']}:{provider['port']}")
        print(f"  Setup: {provider['setup_instructions']}")
        print()
    
    # Test SMTP connection (requires valid environment variables)
    success, message = email_manager.test_smtp_connection()
    print(f"🔗 SMTP Connection Test: {message}")
    
    # Auto-configure example
    if email_manager.auto_configure_smtp("example@gmail.com"):
        print("✅ Auto-configured for Gmail")
    
    print("\n📝 To use this SMTP manager:")
    print("1. Set up environment variables in .env file")
    print("2. For Gmail: Enable 2FA and generate App Password")
    print("3. Use the send_legal_analysis_email() method in your app")
