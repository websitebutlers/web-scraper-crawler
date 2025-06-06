import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin, urlparse
from collections import Counter
from urllib.robotparser import RobotFileParser

class SeoScraper:
    def __init__(self, user_agent=None, timeout=30, respect_robots=True):
        self.session = requests.Session()
        self.timeout = timeout
        self.respect_robots = respect_robots
        self.session.headers.update({
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def check_robots_txt(self, url):
        """Check if URL is allowed by robots.txt"""
        if not self.respect_robots:
            return True, "Robots.txt checking disabled"

        try:
            parsed_url = urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()

            user_agent = self.session.headers.get('User-Agent', '*')
            can_fetch = rp.can_fetch(user_agent, url)

            if can_fetch:
                return True, "Allowed by robots.txt"
            else:
                return False, f"Blocked by robots.txt ({robots_url})"

        except Exception as e:
            # If we can't read robots.txt, assume it's allowed
            return True, f"Could not read robots.txt: {str(e)}"
    
    def analyze_url(self, url):
        """Perform comprehensive SEO analysis of a URL"""
        try:
            # Validate URL format
            if not url or not isinstance(url, str):
                raise Exception("Invalid URL provided")

            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            print(f"Analyzing URL: {url}")  # Debug logging

            # Check robots.txt if respect_robots is enabled
            robots_allowed, robots_message = self.check_robots_txt(url)
            print(f"Robots.txt check: {robots_message}")  # Debug logging

            if not robots_allowed:
                raise Exception(f"Access denied by robots.txt: {robots_message}")

            start_time = time.time()
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            load_time = time.time() - start_time

            print(f"Response status: {response.status_code}")  # Debug logging

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.reason}")

            soup = BeautifulSoup(response.content, 'html.parser')
            
            analysis = {
                'url': url,
                'title': self._get_title(soup),
                'meta_description': self._get_meta_description(soup),
                'h1_tags': self._get_heading_tags(soup, 'h1'),
                'h2_tags': self._get_heading_tags(soup, 'h2'),
                'keywords': self._extract_keywords(soup),
                'word_count': self._get_word_count(soup),
                'load_time': round(load_time, 2),
                'mobile_friendly': self._check_mobile_friendly(soup),
                'images_without_alt': self._check_images_alt(soup),
                'internal_links': self._count_internal_links(soup, url),
                'external_links': self._count_external_links(soup, url),
                'robots_txt_status': robots_message,
                'respect_robots': self.respect_robots
            }
            
            return analysis
            
        except Exception as e:
            raise Exception(f"Error analyzing {url}: {str(e)}")
    
    def _get_title(self, soup):
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else None
    
    def _get_meta_description(self, soup):
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        return meta_desc.get('content', '').strip() if meta_desc else None
    
    def _get_heading_tags(self, soup, tag_name):
        tags = soup.find_all(tag_name)
        return [tag.get_text().strip() for tag in tags]
    
    def _extract_keywords(self, soup):
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        # Clean and split text
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Count word frequency
        word_freq = Counter(words)
        
        # Return top 20 keywords
        return dict(word_freq.most_common(20))
    
    def _get_word_count(self, soup):
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        words = re.findall(r'\b\w+\b', text)
        return len(words)
    
    def _check_mobile_friendly(self, soup):
        viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
        return viewport_meta is not None
    
    def _check_images_alt(self, soup):
        images = soup.find_all('img')
        images_without_alt = []
        
        for img in images:
            if not img.get('alt'):
                src = img.get('src', 'No src attribute')
                images_without_alt.append(src)
        
        return images_without_alt
    
    def _count_internal_links(self, soup, base_url):
        domain = urlparse(base_url).netloc
        links = soup.find_all('a', href=True)
        internal_count = 0
        
        for link in links:
            href = link['href']
            if href.startswith('/') or domain in href:
                internal_count += 1
        
        return internal_count
    
    def _count_external_links(self, soup, base_url):
        domain = urlparse(base_url).netloc
        links = soup.find_all('a', href=True)
        external_count = 0
        
        for link in links:
            href = link['href']
            if href.startswith('http') and domain not in href:
                external_count += 1
        
        return external_count
