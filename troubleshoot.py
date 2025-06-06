#!/usr/bin/env python3
"""
Troubleshooting script for the Web Scraper application.
Helps diagnose common issues and test functionality.
"""

import sys
import requests
import time
from scrapers.seo_scraper import SeoScraper
from scrapers.product_scraper import ProductScraper

def test_network_connectivity():
    """Test basic network connectivity"""
    print("🌐 Testing Network Connectivity")
    print("-" * 40)
    
    test_urls = [
        "https://httpbin.org/get",
        "https://example.com",
        "https://www.google.com"
    ]
    
    for url in test_urls:
        try:
            print(f"Testing {url}... ", end="")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print("✅ OK")
            else:
                print(f"❌ HTTP {response.status_code}")
        except requests.exceptions.Timeout:
            print("❌ Timeout")
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_seo_scraper():
    """Test SEO scraper functionality"""
    print("\n🔍 Testing SEO Scraper")
    print("-" * 40)
    
    test_urls = [
        "https://httpbin.org/html",
        "https://example.com"
    ]
    
    scraper = SeoScraper()
    
    for url in test_urls:
        try:
            print(f"\nAnalyzing {url}...")
            start_time = time.time()
            result = scraper.analyze_url(url)
            end_time = time.time()
            
            print(f"✅ Success in {end_time - start_time:.2f}s")
            print(f"   Title: {result.get('title', 'N/A')}")
            print(f"   Load Time: {result.get('load_time', 0)}s")
            print(f"   Word Count: {result.get('word_count', 0)}")
            print(f"   Mobile Friendly: {result.get('mobile_friendly', False)}")
            
        except Exception as e:
            print(f"❌ Failed: {e}")

def test_product_scraper():
    """Test product scraper functionality"""
    print("\n🛍️ Testing Product Scraper")
    print("-" * 40)
    
    test_urls = [
        "https://httpbin.org/html",  # Generic test
    ]
    
    scraper = ProductScraper()
    
    for url in test_urls:
        try:
            print(f"\nScraping {url}...")
            start_time = time.time()
            result = scraper.scrape_product(url)
            end_time = time.time()
            
            print(f"✅ Success in {end_time - start_time:.2f}s")
            print(f"   Name: {result.get('name', 'N/A')}")
            print(f"   Price: {result.get('price', 'N/A')}")
            print(f"   Brand: {result.get('brand', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Failed: {e}")

def test_flask_api():
    """Test Flask API endpoints"""
    print("\n🌐 Testing Flask API")
    print("-" * 40)
    
    base_url = "http://localhost:5000"
    
    # Test if Flask is running
    try:
        print("Testing Flask server... ", end="")
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Flask is running")
        else:
            print(f"❌ HTTP {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Flask server not running")
        print("   Please start the server with: python3 app.py")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test SEO API
    try:
        print("Testing SEO API... ", end="")
        data = {"url": "https://httpbin.org/html"}
        response = requests.post(f"{base_url}/api/analyze-seo", 
                               json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ SEO API working")
            else:
                print(f"❌ API Error: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Product API
    try:
        print("Testing Product API... ", end="")
        data = {"url": "https://httpbin.org/html"}
        response = requests.post(f"{base_url}/api/scrape-product", 
                               json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Product API working")
            else:
                print(f"❌ API Error: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n📦 Checking Dependencies")
    print("-" * 40)
    
    required_packages = [
        'flask',
        'requests',
        'beautifulsoup4',
        'tinydb',
        'pandas'
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Not installed")

def main():
    """Main troubleshooting function"""
    print("🔧 Web Scraper Troubleshooting Tool")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        
        if test_type == "network":
            test_network_connectivity()
        elif test_type == "seo":
            test_seo_scraper()
        elif test_type == "product":
            test_product_scraper()
        elif test_type == "api":
            test_flask_api()
        elif test_type == "deps":
            check_dependencies()
        else:
            print(f"❌ Unknown test type: {test_type}")
            print("Available tests: network, seo, product, api, deps")
    else:
        # Run all tests
        check_dependencies()
        test_network_connectivity()
        test_seo_scraper()
        test_product_scraper()
        test_flask_api()
    
    print("\n" + "=" * 50)
    print("🔧 Troubleshooting completed!")
    print("\nCommon solutions:")
    print("• If network tests fail: Check your internet connection")
    print("• If Flask API tests fail: Make sure Flask is running (python3 app.py)")
    print("• If scraping fails: Some sites block automated requests (normal)")
    print("• If dependencies fail: Run 'pip install -r requirements.txt'")

if __name__ == "__main__":
    main()
