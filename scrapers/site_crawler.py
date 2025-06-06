import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET
from collections import deque
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class SiteCrawler:
    def __init__(self, user_agent=None, timeout=30, respect_robots=True, max_workers=5):
        self.session = requests.Session()
        self.timeout = timeout
        self.respect_robots = respect_robots
        self.max_workers = max_workers
        self.session.headers.update({
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.discovered_urls = set()
        self.crawled_urls = set()
        self.robots_cache = {}
        self.progress_callback = None
    
    def set_progress_callback(self, callback):
        """Set a callback function to track crawling progress"""
        self.progress_callback = callback
    
    def check_robots_txt(self, url):
        """Check if URL is allowed by robots.txt (cached)"""
        if not self.respect_robots:
            return True, "Robots.txt checking disabled"
        
        try:
            parsed_url = urlparse(url)
            domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            if domain not in self.robots_cache:
                robots_url = f"{domain}/robots.txt"
                rp = RobotFileParser()
                rp.set_url(robots_url)
                rp.read()
                self.robots_cache[domain] = rp
            
            rp = self.robots_cache[domain]
            user_agent = self.session.headers.get('User-Agent', '*')
            can_fetch = rp.can_fetch(user_agent, url)
            
            if can_fetch:
                return True, "Allowed by robots.txt"
            else:
                return False, f"Blocked by robots.txt"
                
        except Exception as e:
            return True, f"Could not read robots.txt: {str(e)}"
    
    def normalize_url(self, url, base_url):
        """Normalize URL and make it absolute"""
        if not url:
            return None
        
        # Handle relative URLs
        if url.startswith('//'):
            url = urlparse(base_url).scheme + ':' + url
        elif url.startswith('/'):
            parsed_base = urlparse(base_url)
            url = f"{parsed_base.scheme}://{parsed_base.netloc}{url}"
        elif not url.startswith(('http://', 'https://')):
            url = urljoin(base_url, url)
        
        # Parse and clean URL
        parsed = urlparse(url)
        
        # Remove fragment
        cleaned = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            ''  # Remove fragment
        ))
        
        return cleaned
    
    def is_same_domain(self, url, base_url):
        """Check if URL belongs to the same domain"""
        return urlparse(url).netloc == urlparse(base_url).netloc
    
    def discover_urls_from_sitemap(self, base_url):
        """Discover URLs from sitemap.xml"""
        discovered = set()
        
        try:
            parsed_base = urlparse(base_url)
            sitemap_urls = [
                f"{parsed_base.scheme}://{parsed_base.netloc}/sitemap.xml",
                f"{parsed_base.scheme}://{parsed_base.netloc}/sitemap_index.xml",
                f"{parsed_base.scheme}://{parsed_base.netloc}/robots.txt"  # Check for sitemap in robots.txt
            ]
            
            for sitemap_url in sitemap_urls:
                try:
                    response = self.session.get(sitemap_url, timeout=self.timeout)
                    if response.status_code == 200:
                        if 'sitemap.xml' in sitemap_url:
                            urls = self._parse_sitemap(response.content)
                            discovered.update(urls)
                        elif 'robots.txt' in sitemap_url:
                            # Look for sitemap declarations in robots.txt
                            for line in response.text.split('\n'):
                                if line.lower().startswith('sitemap:'):
                                    sitemap_ref = line.split(':', 1)[1].strip()
                                    try:
                                        sitemap_response = self.session.get(sitemap_ref, timeout=self.timeout)
                                        if sitemap_response.status_code == 200:
                                            urls = self._parse_sitemap(sitemap_response.content)
                                            discovered.update(urls)
                                    except:
                                        continue
                except:
                    continue
                    
        except Exception as e:
            print(f"Error discovering URLs from sitemap: {e}")
        
        return discovered
    
    def _parse_sitemap(self, xml_content):
        """Parse sitemap XML and extract URLs"""
        urls = set()
        
        try:
            root = ET.fromstring(xml_content)
            
            # Handle sitemap index
            for sitemap in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
                loc = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                if loc is not None:
                    # Recursively fetch sitemap
                    try:
                        response = self.session.get(loc.text, timeout=self.timeout)
                        if response.status_code == 200:
                            urls.update(self._parse_sitemap(response.content))
                    except:
                        continue
            
            # Handle URL entries
            for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                if loc is not None:
                    urls.add(loc.text)
                    
        except ET.ParseError:
            # Try to extract URLs with regex if XML parsing fails
            url_pattern = r'<loc>(.*?)</loc>'
            matches = re.findall(url_pattern, xml_content.decode('utf-8', errors='ignore'))
            urls.update(matches)
        except Exception as e:
            print(f"Error parsing sitemap: {e}")
        
        return urls
    
    def discover_urls_from_page(self, url):
        """Discover URLs by crawling a page and extracting links"""
        discovered = set()
        
        try:
            robots_allowed, _ = self.check_robots_txt(url)
            if not robots_allowed:
                return discovered
            
            response = self.session.get(url, timeout=self.timeout)
            if response.status_code != 200:
                return discovered
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract all links
            for link in soup.find_all('a', href=True):
                href = link['href']
                normalized_url = self.normalize_url(href, url)
                
                if normalized_url and self.is_same_domain(normalized_url, url):
                    discovered.add(normalized_url)
            
        except Exception as e:
            print(f"Error discovering URLs from {url}: {e}")
        
        return discovered
    
    def crawl_site(self, base_url, max_urls=100, max_depth=3):
        """
        Crawl an entire site and return discovered URLs
        
        Args:
            base_url: Starting URL
            max_urls: Maximum number of URLs to crawl
            max_depth: Maximum crawl depth
        
        Returns:
            List of discovered URLs
        """
        print(f"Starting site crawl for: {base_url}")
        
        # Normalize base URL
        base_url = self.normalize_url(base_url, base_url)
        
        # Initialize
        self.discovered_urls = set()
        self.crawled_urls = set()
        
        # Discover URLs from sitemap first
        print("Discovering URLs from sitemap...")
        sitemap_urls = self.discover_urls_from_sitemap(base_url)
        self.discovered_urls.update(sitemap_urls)
        print(f"Found {len(sitemap_urls)} URLs in sitemap")
        
        # Add base URL to start crawling
        self.discovered_urls.add(base_url)
        
        # Crawl URLs level by level
        current_level = {base_url}
        
        for depth in range(max_depth):
            if len(self.crawled_urls) >= max_urls:
                break
            
            print(f"Crawling depth {depth + 1}, {len(current_level)} URLs to process")
            next_level = set()
            
            # Process current level URLs
            for url in current_level:
                if len(self.crawled_urls) >= max_urls:
                    break
                
                if url in self.crawled_urls:
                    continue
                
                # Discover new URLs from this page
                new_urls = self.discover_urls_from_page(url)
                self.discovered_urls.update(new_urls)
                next_level.update(new_urls - self.crawled_urls)
                
                self.crawled_urls.add(url)
                
                # Progress callback
                if self.progress_callback:
                    self.progress_callback(len(self.crawled_urls), len(self.discovered_urls))
                
                # Be respectful - add delay
                time.sleep(0.5)
            
            current_level = next_level
        
        # Return final list of discovered URLs (limited by max_urls)
        final_urls = list(self.discovered_urls)[:max_urls]
        print(f"Crawl completed. Discovered {len(self.discovered_urls)} URLs, returning {len(final_urls)}")
        
        return final_urls
