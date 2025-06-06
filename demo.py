#!/usr/bin/env python3
"""
Demo script for the Web Scraper application.
Shows how to use the scrapers programmatically.
"""

import sys
import time
from scrapers.seo_scraper import SeoScraper
from scrapers.product_scraper import ProductScraper
from models.database import DatabaseManager
from utils.helpers import calculate_seo_score

def demo_seo_analysis():
    """Demonstrate SEO analysis functionality"""
    print("🔍 SEO Analysis Demo")
    print("=" * 50)
    
    # Test URLs
    test_urls = [
        "https://example.com",
        "https://httpbin.org/html",
        "https://www.python.org"
    ]
    
    scraper = SeoScraper(respect_robots=False)  # Ignore robots.txt for demo

    for url in test_urls:
        print(f"\n📊 Analyzing: {url}")
        try:
            # Perform analysis
            analysis = scraper.analyze_url(url)
            
            # Calculate SEO score
            seo_score = calculate_seo_score(analysis)
            
            # Save to database
            saved_analysis = DatabaseManager.create_seo_analysis(analysis)
            
            # Display results
            print(f"   ✅ Title: {analysis.get('title', 'N/A')}")
            print(f"   📝 Meta Description: {len(analysis.get('meta_description', '') or '')} chars")
            print(f"   🏷️  H1 Tags: {len(analysis.get('h1_tags', []))}")
            print(f"   📱 Mobile Friendly: {analysis.get('mobile_friendly', False)}")
            print(f"   ⏱️  Load Time: {analysis.get('load_time', 0)}s")
            print(f"   📊 SEO Score: {seo_score}/100")
            print(f"   💾 Saved with ID: {saved_analysis['id']}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)  # Be respectful with requests

def demo_product_scraping():
    """Demonstrate product scraping functionality"""
    print("\n\n🛍️ Product Scraping Demo")
    print("=" * 50)
    
    # Test URLs (these might not work due to anti-bot measures)
    test_urls = [
        "https://example.com",  # Will use generic scraper
    ]
    
    scraper = ProductScraper(respect_robots=False)  # Ignore robots.txt for demo

    for url in test_urls:
        print(f"\n🛒 Scraping: {url}")
        try:
            # Perform scraping
            product_data = scraper.scrape_product(url)
            
            # Save to database
            saved_product = DatabaseManager.create_product_data(product_data)
            
            # Display results
            print(f"   ✅ Name: {product_data.get('name', 'N/A')}")
            print(f"   💰 Price: {product_data.get('price', 'N/A')}")
            print(f"   🏷️  Brand: {product_data.get('brand', 'N/A')}")
            print(f"   ⭐ Rating: {product_data.get('rating', 'N/A')}")
            print(f"   📦 Availability: {product_data.get('availability', 'N/A')}")
            print(f"   💾 Saved with ID: {saved_product['id']}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)  # Be respectful with requests

def demo_database_operations():
    """Demonstrate database operations"""
    print("\n\n💾 Database Operations Demo")
    print("=" * 50)
    
    # Get statistics
    stats = DatabaseManager.get_database_stats()
    print(f"\n📊 Database Statistics:")
    print(f"   • SEO Analyses: {stats['total_seo_analyses']}")
    print(f"   • Products: {stats['total_products']}")
    print(f"   • Pending Jobs: {stats['pending_jobs']}")
    print(f"   • Database Size: {stats['database_size']} bytes")
    
    # Show recent data
    print(f"\n📋 Recent SEO Analyses:")
    recent_seo = DatabaseManager.get_recent_seo_analyses(3)
    for i, analysis in enumerate(recent_seo, 1):
        print(f"   {i}. {analysis.get('title', 'No title')} - {analysis.get('url', '')}")
    
    print(f"\n📋 Recent Products:")
    recent_products = DatabaseManager.get_recent_products(3)
    for i, product in enumerate(recent_products, 1):
        print(f"   {i}. {product.get('name', 'Unknown')} - {product.get('url', '')}")
    
    # Create backup
    print(f"\n💾 Creating backup...")
    backup_path = DatabaseManager.backup_database()
    print(f"   ✅ Backup created: {backup_path}")

def main():
    """Main demo function"""
    print("🚀 Web Scraper Demo")
    print("This demo shows the capabilities of the web scraper application.")
    print("The Flask app should be running at http://localhost:5000")
    print("\n" + "=" * 60)
    
    if len(sys.argv) > 1:
        demo_type = sys.argv[1].lower()
        
        if demo_type == "seo":
            demo_seo_analysis()
        elif demo_type == "product":
            demo_product_scraping()
        elif demo_type == "database":
            demo_database_operations()
        else:
            print(f"❌ Unknown demo type: {demo_type}")
            print("Available demos: seo, product, database")
    else:
        # Run all demos
        demo_seo_analysis()
        demo_product_scraping()
        demo_database_operations()
    
    print("\n" + "=" * 60)
    print("✨ Demo completed!")
    print("Visit http://localhost:5000 to see the web interface.")
    print("Check scraper_data.json to see the stored data.")

if __name__ == "__main__":
    main()
