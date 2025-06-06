import json
import csv
import io
from urllib.parse import urlparse
import re

def is_valid_url(url):
    """Validate if a string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def clean_url(url):
    """Clean and normalize URL"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url.strip()

def format_price(price_str):
    """Extract and format price from string"""
    if not price_str:
        return None
    
    # Remove extra whitespace and common currency symbols
    price_str = re.sub(r'[^\d.,\$£€¥]', '', price_str)
    
    # Extract numeric value
    match = re.search(r'[\d,]+\.?\d*', price_str)
    if match:
        return match.group().replace(',', '')
    
    return price_str

def export_to_csv(data, filename):
    """Export data to CSV format"""
    if not data:
        return None
    
    output = io.StringIO()
    
    # Get field names from first record
    fieldnames = data[0].keys() if isinstance(data[0], dict) else []
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in data:
        if isinstance(row, dict):
            writer.writerow(row)
    
    csv_content = output.getvalue()
    output.close()
    
    return csv_content

def export_to_json(data):
    """Export data to JSON format"""
    return json.dumps(data, indent=2, default=str)

def truncate_text(text, max_length=100):
    """Truncate text to specified length"""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."

def extract_domain(url):
    """Extract domain from URL"""
    try:
        return urlparse(url).netloc
    except:
        return url

def format_number(num):
    """Format number with commas"""
    if num is None:
        return "N/A"
    
    try:
        return f"{int(num):,}"
    except:
        return str(num)

def calculate_seo_score(analysis):
    """Calculate SEO score based on analysis data"""
    score = 0
    max_score = 100
    
    # Title (20 points)
    if analysis.get('title'):
        title_len = len(analysis['title'])
        if 30 <= title_len <= 60:
            score += 20
        elif title_len > 0:
            score += 10
    
    # Meta description (20 points)
    if analysis.get('meta_description'):
        desc_len = len(analysis['meta_description'])
        if 120 <= desc_len <= 160:
            score += 20
        elif desc_len > 0:
            score += 10
    
    # H1 tags (15 points)
    h1_tags = analysis.get('h1_tags', [])
    if len(h1_tags) == 1:
        score += 15
    elif len(h1_tags) > 0:
        score += 8
    
    # H2 tags (10 points)
    h2_tags = analysis.get('h2_tags', [])
    if len(h2_tags) >= 2:
        score += 10
    elif len(h2_tags) > 0:
        score += 5
    
    # Word count (10 points)
    word_count = analysis.get('word_count', 0)
    if word_count >= 300:
        score += 10
    elif word_count >= 100:
        score += 5
    
    # Load time (15 points)
    load_time = analysis.get('load_time', 0)
    if load_time <= 2:
        score += 15
    elif load_time <= 4:
        score += 10
    elif load_time <= 6:
        score += 5
    
    # Mobile friendly (10 points)
    if analysis.get('mobile_friendly'):
        score += 10
    
    return min(score, max_score)
