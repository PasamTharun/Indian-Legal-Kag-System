"""
Web Scraper for Indian Legal and Regulatory Updates
"""

import logging
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re
from urllib.parse import urljoin, urlparse
import time

logger = logging.getLogger(__name__)

class IndianRegulatoryUpdatesScraper:
    """Scraper for Indian legal and regulatory updates"""
    
    def __init__(self):
        self.sources = {
            "supreme_court": {
                "name": "Supreme Court of India",
                "url": "https://main.sci.gov.in/judgments",
                "selector": ".judgment-list",
                "type": "judgments"
            },
            "india_code": {
                "name": "India Code Legislative Updates",
                "url": "https://www.indiacode.nic.in/",
                "type": "legislation"
            },
            "parliament": {
                "name": "Parliament of India",
                "url": "https://loksabha.nic.in/",
                "type": "parliamentary"
            }
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        self.constitutional_keywords = [
            "constitutional", "fundamental rights", "article 21", "privacy", 
            "data protection", "DPDPA", "supreme court", "constitutional amendment"
        ]
        
        self.privacy_keywords = [
            "privacy", "personal data", "data protection", "DPDPA 2023",
            "article 21", "puttaswamy", "information privacy"
        ]
    
    def scrape_all_sources(self) -> Dict[str, Any]:
        """Scrape all configured sources for updates"""
        
        all_updates = {
            "scraping_timestamp": datetime.now().isoformat(),
            "sources_scraped": [],
            "total_updates": 0,
            "constitutional_updates": [],
            "privacy_updates": [],
            "general_updates": [],
            "errors": []
        }
        
        for source_id, source_config in self.sources.items():
            try:
                logger.info(f"Scraping {source_config['name']}...")
                updates = self.scrape_source(source_id, source_config)
                
                all_updates["sources_scraped"].append(source_config["name"])
                all_updates["total_updates"] += len(updates)
                
                # Categorize updates
                for update in updates:
                    if self._is_constitutional_update(update):
                        all_updates["constitutional_updates"].append(update)
                    elif self._is_privacy_update(update):
                        all_updates["privacy_updates"].append(update)
                    else:
                        all_updates["general_updates"].append(update)
                
                time.sleep(2)  # Be respectful to servers
                
            except Exception as e:
                error_msg = f"Error scraping {source_config['name']}: {str(e)}"
                logger.error(error_msg)
                all_updates["errors"].append(error_msg)
        
        return all_updates
    
    def scrape_source(self, source_id: str, source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scrape a specific source for updates"""
        
        try:
            response = requests.get(source_config["url"], headers=self.headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            updates = []
            
            if source_id == "supreme_court":
                updates = self._scrape_supreme_court(soup, source_config)
            elif source_id == "india_code":
                updates = self._scrape_india_code(soup, source_config)
            elif source_id == "parliament":
                updates = self._scrape_parliament(soup, source_config)
            
            return updates
            
        except Exception as e:
            logger.error(f"Error scraping {source_config['name']}: {str(e)}")
            return []
    
    def _scrape_supreme_court(self, soup: BeautifulSoup, source_config: Dict) -> List[Dict[str, Any]]:
        """Scrape Supreme Court judgments and orders"""
        
        updates = []
        
        # Look for judgment links and titles
        judgment_elements = soup.find_all(['a', 'div'], class_=re.compile(r'judgment|case|order', re.I))
        
        for element in judgment_elements[:10]:  # Limit to recent 10
            try:
                title = element.get_text(strip=True)
                if len(title) > 20:  # Filter out very short texts
                    
                    link = element.get('href', '')
                    if link and not link.startswith('http'):
                        link = urljoin(source_config["url"], link)
                    
                    update = {
                        "title": title,
                        "link": link,
                        "source": source_config["name"],
                        "type": "judgment",
                        "scraped_date": datetime.now().isoformat(),
                        "summary": title[:200] + "..." if len(title) > 200 else title
                    }
                    
                    updates.append(update)
                    
            except Exception as e:
                logger.warning(f"Error processing Supreme Court element: {str(e)}")
                continue
        
        return updates
    
    def _scrape_india_code(self, soup: BeautifulSoup, source_config: Dict) -> List[Dict[str, Any]]:
        """Scrape legislative updates"""
        
        updates = []
        
        # Look for legislative updates, amendments, new acts
        legislative_elements = soup.find_all(['a', 'div'], text=re.compile(r'act|amendment|bill|legislation', re.I))
        
        for element in legislative_elements[:10]:
            try:
                title = element.get_text(strip=True)
                if len(title) > 15:
                    
                    link = element.get('href', '') if element.name == 'a' else ''
                    if link and not link.startswith('http'):
                        link = urljoin(source_config["url"], link)
                    
                    update = {
                        "title": title,
                        "link": link,
                        "source": source_config["name"],
                        "type": "legislation",
                        "scraped_date": datetime.now().isoformat(),
                        "summary": title[:200] + "..." if len(title) > 200 else title
                    }
                    
                    updates.append(update)
                    
            except Exception as e:
                logger.warning(f"Error processing India Code element: {str(e)}")
                continue
        
        return updates
    
    def _scrape_parliament(self, soup: BeautifulSoup, source_config: Dict) -> List[Dict[str, Any]]:
        """Scrape parliamentary updates"""
        
        updates = []
        
        # Look for parliamentary proceedings, bills, questions
        parliamentary_elements = soup.find_all(['a', 'div'], text=re.compile(r'bill|question|proceeding|debate', re.I))
        
        for element in parliamentary_elements[:10]:
            try:
                title = element.get_text(strip=True)
                if len(title) > 15:
                    
                    link = element.get('href', '') if element.name == 'a' else ''
                    if link and not link.startswith('http'):
                        link = urljoin(source_config["url"], link)
                    
                    update = {
                        "title": title,
                        "link": link,
                        "source": source_config["name"],
                        "type": "parliamentary",
                        "scraped_date": datetime.now().isoformat(),
                        "summary": title[:200] + "..." if len(title) > 200 else title
                    }
                    
                    updates.append(update)
                    
            except Exception as e:
                logger.warning(f"Error processing Parliament element: {str(e)}")
                continue
        
        return updates
    
    def _is_constitutional_update(self, update: Dict[str, Any]) -> bool:
        """Check if update is related to constitutional matters"""
        
        text = f"{update.get('title', '')} {update.get('summary', '')}".lower()
        return any(keyword in text for keyword in self.constitutional_keywords)
    
    def _is_privacy_update(self, update: Dict[str, Any]) -> bool:
        """Check if update is related to privacy/data protection"""
        
        text = f"{update.get('title', '')} {update.get('summary', '')}".lower()
        return any(keyword in text for keyword in self.privacy_keywords)
    
    def get_filtered_updates(self, category: str = "all", days_back: int = 30) -> List[Dict[str, Any]]:
        """Get filtered updates based on category and timeframe"""
        
        all_updates = self.scrape_all_sources()
        
        if category == "constitutional":
            filtered_updates = all_updates["constitutional_updates"]
        elif category == "privacy":
            filtered_updates = all_updates["privacy_updates"]
        elif category == "general":
            filtered_updates = all_updates["general_updates"]
        else:
            filtered_updates = (all_updates["constitutional_updates"] + 
                              all_updates["privacy_updates"] + 
                              all_updates["general_updates"])
        
        # Filter by date if needed
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        recent_updates = []
        for update in filtered_updates:
            try:
                update_date = datetime.fromisoformat(update["scraped_date"].replace('Z', '+00:00'))
                if update_date >= cutoff_date:
                    recent_updates.append(update)
            except:
                recent_updates.append(update)  # Include if date parsing fails
        
        return recent_updates
