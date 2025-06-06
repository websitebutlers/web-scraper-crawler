import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

class ProductScraper:
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
    
    def scrape_product(self, url):
        """Scrape product information from a URL"""
        try:
            # Check robots.txt if respect_robots is enabled
            robots_allowed, robots_message = self.check_robots_txt(url)
            print(f"Robots.txt check: {robots_message}")  # Debug logging

            if not robots_allowed:
                raise Exception(f"Access denied by robots.txt: {robots_message}")

            response = self.session.get(url, timeout=self.timeout)

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.reason}")

            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to detect the site and use appropriate selectors
            domain = urlparse(url).netloc.lower()
            
            if 'amazon' in domain:
                return self._scrape_amazon(soup, url)
            elif 'ebay' in domain:
                return self._scrape_ebay(soup, url)
            else:
                return self._scrape_generic(soup, url)
                
        except Exception as e:
            raise Exception(f"Error scraping product from {url}: {str(e)}")
    
    def _scrape_amazon(self, soup, url):
        """Amazon-specific scraping logic"""
        product_data = {
            'url': url,
            'name': self._safe_extract(soup, '#productTitle'),
            'price': self._extract_amazon_price(soup),
            'description': self._safe_extract(soup, '#feature-bullets ul'),
            'availability': self._safe_extract(soup, '#availability span'),
            'rating': self._extract_amazon_rating(soup),
            'reviews_count': self._extract_amazon_reviews_count(soup),
            'brand': self._safe_extract(soup, 'a#bylineInfo'),
            'category': self._extract_amazon_category(soup)
        }
        return product_data
    
    def _scrape_ebay(self, soup, url):
        """eBay-specific scraping logic"""
        product_data = {
            'url': url,
            'name': self._safe_extract(soup, 'h1#x-title-label-lbl'),
            'price': self._safe_extract(soup, '.notranslate'),
            'description': self._safe_extract(soup, '#viTabs_0_is'),
            'availability': self._safe_extract(soup, '#qtySubTxt'),
            'rating': None,  # eBay doesn't have consistent ratings
            'reviews_count': None,
            'brand': self._safe_extract(soup, '[data-testid="ux-labels-values-brand"]'),
            'category': self._extract_ebay_category(soup)
        }
        return product_data
    
    def _scrape_generic(self, soup, url):
        """Generic scraping logic for unknown sites"""
        product_data = {
            'url': url,
            'name': self._extract_generic_name(soup),
            'price': self._extract_generic_price(soup),
            'description': self._extract_generic_description(soup),
            'availability': self._extract_generic_availability(soup),
            'rating': self._extract_generic_rating(soup),
            'reviews_count': None,
            'brand': self._extract_generic_brand(soup),
            'category': None
        }
        return product_data
    
    def _safe_extract(self, soup, selector):
        """Safely extract text from a CSS selector"""
        try:
            element = soup.select_one(selector)
            return element.get_text().strip() if element else None
        except:
            return None
    
    def _extract_amazon_price(self, soup):
        """Extract price from Amazon page"""
        price_selectors = [
            '.a-price-whole',
            '.a-offscreen',
            '#priceblock_dealprice',
            '#priceblock_ourprice',
            '.a-price .a-offscreen'
        ]
        
        for selector in price_selectors:
            price = self._safe_extract(soup, selector)
            if price:
                return price
        return None
    
    def _extract_amazon_rating(self, soup):
        """Extract rating from Amazon page"""
        rating_element = soup.select_one('[data-hook="average-star-rating"] .a-icon-alt')
        if rating_element:
            rating_text = rating_element.get_text()
            match = re.search(r'(\d+\.?\d*)', rating_text)
            if match:
                return float(match.group(1))
        return None
    
    def _extract_amazon_reviews_count(self, soup):
        """Extract reviews count from Amazon page"""
        reviews_element = soup.select_one('[data-hook="total-review-count"]')
        if reviews_element:
            reviews_text = reviews_element.get_text()
            match = re.search(r'([\d,]+)', reviews_text.replace(',', ''))
            if match:
                return int(match.group(1).replace(',', ''))
        return None
    
    def _extract_amazon_category(self, soup):
        """Extract category from Amazon breadcrumbs"""
        breadcrumbs = soup.select('#wayfinding-breadcrumbs_feature_div a')
        if breadcrumbs:
            return ' > '.join([crumb.get_text().strip() for crumb in breadcrumbs])
        return None
    
    def _extract_ebay_category(self, soup):
        """Extract category from eBay breadcrumbs"""
        breadcrumbs = soup.select('.seo-breadcrumb-text')
        if breadcrumbs:
            return ' > '.join([crumb.get_text().strip() for crumb in breadcrumbs])
        return None
    
    def _extract_generic_name(self, soup):
        """Extract product name using generic selectors"""
        name_selectors = [
            'h1',
            '.product-title',
            '.product-name',
            '[data-testid="product-title"]',
            '.title'
        ]
        
        for selector in name_selectors:
            name = self._safe_extract(soup, selector)
            if name and len(name) > 5:  # Reasonable length check
                return name
        return None
    
    def _extract_generic_price(self, soup):
        """Extract price using generic selectors and patterns"""
        price_selectors = [
            '.price',
            '.product-price',
            '[data-testid="price"]',
            '.cost',
            '.amount'
        ]
        
        for selector in price_selectors:
            price = self._safe_extract(soup, selector)
            if price and re.search(r'[\$£€¥]\d+', price):
                return price
        
        # Look for price patterns in text
        text = soup.get_text()
        price_match = re.search(r'[\$£€¥]\d+(?:\.\d{2})?', text)
        if price_match:
            return price_match.group()
        
        return None
    
    def _extract_generic_description(self, soup):
        """Extract description using generic selectors"""
        desc_selectors = [
            '.product-description',
            '.description',
            '[data-testid="description"]',
            '.product-details',
            '.summary'
        ]
        
        for selector in desc_selectors:
            desc = self._safe_extract(soup, selector)
            if desc and len(desc) > 20:
                return desc[:500]  # Limit length
        return None
    
    def _extract_generic_availability(self, soup):
        """Extract availability using generic patterns"""
        availability_patterns = [
            r'in stock',
            r'out of stock',
            r'available',
            r'unavailable',
            r'limited stock'
        ]
        
        text = soup.get_text().lower()
        for pattern in availability_patterns:
            if re.search(pattern, text):
                return pattern.replace('r', '').strip()
        return None
    
    def _extract_generic_rating(self, soup):
        """Extract rating using generic patterns"""
        rating_selectors = [
            '.rating',
            '.stars',
            '[data-testid="rating"]'
        ]
        
        for selector in rating_selectors:
            rating_element = soup.select_one(selector)
            if rating_element:
                rating_text = rating_element.get_text()
                match = re.search(r'(\d+\.?\d*)', rating_text)
                if match:
                    rating = float(match.group(1))
                    if 0 <= rating <= 5:  # Reasonable rating range
                        return rating
        return None
    
    def _extract_generic_brand(self, soup):
        """Extract brand using generic selectors"""
        brand_selectors = [
            '.brand',
            '.manufacturer',
            '[data-testid="brand"]',
            '.product-brand'
        ]
        
        for selector in brand_selectors:
            brand = self._safe_extract(soup, selector)
            if brand and len(brand) < 50:  # Reasonable brand name length
                return brand
        return None
