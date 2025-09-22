# 🇮🇳 Indian Legal Knowledge Augmented Generation (KAG) System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.43.2-red.svg)](https://streamlit.io/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.15.0-blue.svg)](https://neo4j.com/)

## 📋 Overview

The **Indian Legal KAG System** is an advanced AI-powered platform that combines Knowledge Augmented Generation (KAG) with constitutional law expertise to provide comprehensive legal document analysis, constitutional reasoning, and privacy compliance assessment specifically tailored for Indian legal framework.

### 🎯 Key Features

- **📄 Intelligent Document Analysis** - AI-powered legal document processing and classification
- **🏛️ Constitutional Reasoning Engine** - Deep analysis using Indian Constitution Articles
- **🔒 Privacy Compliance Assessment** - DPDPA 2023 compliance checking with Article 21 alignment
- **📊 Comprehensive Scoring System** - Multi-dimensional legal framework scoring
- **🤖 Interactive Legal Chatbot** - AI-powered Q&A with constitutional knowledge
- **📋 Document Summarization** - Automated legal document summarization
- **🌐 Regulatory Updates** - Real-time Indian legal updates scraping
- **📧 Automated Report Generation** - Professional legal analysis reports
- **🔍 Knowledge Graph Explorer** - Visual constitutional knowledge relationships

## 🛠️ Tech Stack

### Core Framework
- **Backend**: Python 3.8+
- **Frontend**: Streamlit 1.43.2
- **Database**: Neo4j 5.15.0 (Graph Database)
- **Additional Graph Tools**: py2neo 2021.2.4, NetworkX 3.2.1

### AI & Machine Learning
- **LLM Framework**: LangChain 0.3.20 with LangChain-Groq 0.2.5
- **Deep Learning**: PyTorch 2.0.1 (CPU optimized)
- **NLP Libraries**: 
  - Transformers 4.30.2 (Hugging Face)
  - Sentence-Transformers 2.2.2
  - spaCy 3.7.2
  - NLTK 3.9.1
- **ML Libraries**: scikit-learn 1.3.2, NumPy 1.24.4, SciPy 1.10.1

### Document Processing
- **PDF Processing**: PyMuPDF 1.25.3
- **OCR**: EasyOCR 1.7.0
- **Computer Vision**: OpenCV-Python-Headless 4.7.0.72
- **Image Processing**: Pillow 9.0.0+

### Data & Visualization
- **Data Processing**: Pandas 2.2.3
- **Visualization**: Plotly 6.0.0, Altair 5.5.0
- **Report Generation**: FPDF 1.7.2

### Communication & Utilities
- **Email Services**: SendGrid 6.11.0
- **Environment Management**: python-dotenv 1.0.1
- **Data Validation**: Pydantic 2.10.6
- **Date Utilities**: python-dateutil 2.9.0.post0

## 🏗️ Architecture

```
📁 Indian-Legal-KAG-System/
├── 📁 analysis_frameworks/          # Advanced legal analysis engines
│   ├── document_classifier.py      # AI document classification
│   ├── framework_engine.py         # Adaptive legal framework engine
│   └── scoring_engine.py          # Universal legal scoring system
├── 📁 config/                      # Configuration modules
│   ├── constitutional_articles.py  # All 395 constitutional articles
│   └── neo4j_config.py            # Neo4j database configuration
├── 📁 core/                        # Core system modules
│   ├── 📁 chatbot/                 # Interactive AI chatbot
│   ├── 📁 kag_engine/             # Knowledge Augmented Generation engines
│   │   ├── constitutional_reasoning.py  # Constitutional analysis
│   │   ├── dpdpa_compliance.py         # DPDPA 2023 compliance
│   │   └── privacy_analyzer.py         # Article 21 privacy analysis
│   ├── 📁 knowledge_graph/         # Neo4j knowledge graph management
│   ├── 📁 messaging/              # Email and report generation
│   ├── 📁 processors/             # Document processing engines
│   ├── 📁 scrapers/               # Regulatory updates scraper
│   └── 📁 summarization/          # Legal document summarization
├── 📁 data/                       # Legal datasets
│   └── 📁 constitutional_data/    # Constitutional knowledge base
├── 📁 scripts/                    # Utility scripts
├── 📁 static/                     # Frontend assets
├── 📁 tests/                      # Test suites
├── 📁 utils/                      # Utility functions
└── app.py                         # Main Streamlit application
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Neo4j Database (local or cloud)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/badrinath-26/Indian-Legal-Kag-system.git
cd Indian-Legal-Kag-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# Groq API (for LLM)
GROQ_API_KEY=your_groq_api_key

# Email Configuration (optional)
SENDGRID_API_KEY=your_sendgrid_key
SENDER_EMAIL=your_email@domain.com

# Additional API keys as needed
HUGGINGFACE_API_KEY=your_hf_key
```

### 5. Database Setup
```bash
# Start Neo4j database
# Install Neo4j Desktop or use Neo4j Aura (cloud)

# Test connection
python test_neo4j_connection.py
```

### 6. Run the Application
```bash
streamlit run app.py
```

## 📖 Usage Guide

### 1. Document Analysis
- Upload legal documents (PDF, DOCX, TXT)
- Select analysis framework (Constitutional, Privacy, DPDPA)
- Get comprehensive AI-powered analysis with scoring

### 2. Constitutional Reasoning
- Analyze documents against Indian Constitution
- Get specific article references and legal precedents
- Understand constitutional implications

### 3. Privacy Compliance
- DPDPA 2023 compliance assessment
- Article 21 privacy rights analysis
- Automated compliance scoring

### 4. Interactive Chatbot
- Ask legal questions in natural language
- Get AI-powered responses with constitutional references
- Explore legal concepts interactively

### 5. Knowledge Graph Explorer
- Visualize constitutional relationships
- Explore interconnected legal concepts
- Navigate through legal precedents

## 🔧 API Endpoints

The system provides RESTful APIs for integration:

- `POST /api/analyze` - Document analysis
- `GET /api/constitutional/{article_id}` - Constitutional article retrieval
- `POST /api/privacy-check` - Privacy compliance assessment
- `GET /api/knowledge-graph` - Knowledge graph data
- `POST /api/summarize` - Document summarization

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_basic_functionality.py

# Test Neo4j connection
python test_neo4j_connection.py
```

## 📊 Key Components

### 1. Constitutional Reasoning Engine
- Analyzes documents against all 395 constitutional articles
- Provides legal precedent matching
- Generates constitutional compliance scores

### 2. DPDPA Compliance Engine
- Comprehensive DPDPA 2023 analysis
- Privacy impact assessment
- Automated compliance reporting

### 3. Knowledge Graph System
- Neo4j-powered constitutional knowledge base
- Interconnected legal concepts and precedents
- Graph-based reasoning and queries

### 4. Document Processing Pipeline
- Multi-format document support
- OCR for scanned documents
- AI-powered content extraction and classification

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Indian Constitution**: Source of all constitutional articles and provisions
- **DPDPA 2023**: Digital Personal Data Protection Act
- **Neo4j**: Graph database technology
- **Hugging Face**: AI/ML models and transformers
- **LangChain**: LLM framework and tools
- **Streamlit**: Web application framework

## 📞 Support

For support, please open an issue on GitHub or contact:
- **Email**: [your-email@domain.com]
- **GitHub**: [@badrinath-26](https://github.com/badrinath-26)

## 🔮 Future Enhancements

- [ ] Multi-language support (Hindi, Tamil, Bengali)
- [ ] Integration with Supreme Court and High Court databases
- [ ] Real-time legal news and updates
- [ ] Mobile application development
- [ ] Advanced visualization dashboards
- [ ] API rate limiting and authentication
- [ ] Docker containerization
- [ ] Cloud deployment automation

---

**Made with ❤️ for the Indian Legal Community**

*Empowering legal professionals with AI-driven constitutional analysis and compliance assessment.*