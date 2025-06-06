from tinydb import TinyDB, Query
from datetime import datetime
import os
import uuid
import json

# Custom datetime serializer for TinyDB
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Initialize TinyDB with custom serialization
db_path = os.path.join(os.getcwd(), 'scraper_data.json')
db = TinyDB(db_path)

# Define tables
seo_table = db.table('seo_analysis')
product_table = db.table('product_data')
job_table = db.table('scrape_jobs')
crawl_session_table = db.table('crawl_sessions')
crawl_result_table = db.table('crawl_results')

class DatabaseManager:
    """Database manager for TinyDB operations"""

    @staticmethod
    def generate_id():
        """Generate a unique ID"""
        return str(uuid.uuid4())

    # SEO Analysis methods
    @staticmethod
    def create_seo_analysis(data):
        """Create a new SEO analysis record"""
        record = {
            'id': DatabaseManager.generate_id(),
            'url': data.get('url'),
            'title': data.get('title'),
            'meta_description': data.get('meta_description'),
            'h1_tags': data.get('h1_tags', []),
            'h2_tags': data.get('h2_tags', []),
            'keywords': data.get('keywords', {}),
            'word_count': data.get('word_count'),
            'load_time': data.get('load_time'),
            'mobile_friendly': data.get('mobile_friendly', False),
            'created_at': datetime.now().isoformat()
        }
        seo_table.insert(record)
        return record

    @staticmethod
    def get_all_seo_analyses():
        """Get all SEO analyses, sorted by creation date (newest first)"""
        analyses = seo_table.all()
        return sorted(analyses, key=lambda x: x.get('created_at', ''), reverse=True)

    @staticmethod
    def get_recent_seo_analyses(limit=5):
        """Get recent SEO analyses"""
        analyses = DatabaseManager.get_all_seo_analyses()
        return analyses[:limit]

    @staticmethod
    def count_seo_analyses():
        """Count total SEO analyses"""
        return len(seo_table)

    # Product Data methods
    @staticmethod
    def create_product_data(data):
        """Create a new product data record"""
        record = {
            'id': DatabaseManager.generate_id(),
            'url': data.get('url'),
            'name': data.get('name'),
            'price': data.get('price'),
            'description': data.get('description'),
            'availability': data.get('availability'),
            'rating': data.get('rating'),
            'reviews_count': data.get('reviews_count'),
            'brand': data.get('brand'),
            'category': data.get('category'),
            'created_at': datetime.now().isoformat()
        }
        product_table.insert(record)
        return record

    @staticmethod
    def get_all_products():
        """Get all products, sorted by creation date (newest first)"""
        products = product_table.all()
        return sorted(products, key=lambda x: x.get('created_at', ''), reverse=True)

    @staticmethod
    def get_recent_products(limit=5):
        """Get recent products"""
        products = DatabaseManager.get_all_products()
        return products[:limit]

    @staticmethod
    def count_products():
        """Count total products"""
        return len(product_table)

    # Scrape Job methods
    @staticmethod
    def create_scrape_job(job_type, url):
        """Create a new scrape job"""
        record = {
            'id': DatabaseManager.generate_id(),
            'job_type': job_type,
            'url': url,
            'status': 'pending',
            'result_id': None,
            'error_message': None,
            'created_at': datetime.now().isoformat(),
            'completed_at': None
        }
        job_table.insert(record)
        return record

    @staticmethod
    def update_scrape_job(job_id, updates):
        """Update a scrape job"""
        Job = Query()
        job_table.update(updates, Job.id == job_id)

    @staticmethod
    def get_scrape_job(job_id):
        """Get a scrape job by ID"""
        Job = Query()
        return job_table.get(Job.id == job_id)

    @staticmethod
    def count_pending_jobs():
        """Count pending jobs"""
        Job = Query()
        return len(job_table.search(Job.status == 'pending'))

    # Utility methods
    @staticmethod
    def backup_database(backup_path=None):
        """Create a backup of the database"""
        if backup_path is None:
            backup_path = f'scraper_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

        import shutil
        shutil.copy2(db_path, backup_path)
        return backup_path

    # Crawl Session methods
    @staticmethod
    def create_crawl_session(base_url, max_urls=100, max_depth=3, respect_robots=True):
        """Create a new crawl session"""
        record = {
            'id': DatabaseManager.generate_id(),
            'base_url': base_url,
            'max_urls': max_urls,
            'max_depth': max_depth,
            'respect_robots': respect_robots,
            'status': 'pending',
            'total_urls_found': 0,
            'total_urls_analyzed': 0,
            'issues_found': 0,
            'started_at': datetime.now().isoformat(),
            'completed_at': None,
            'error_message': None
        }
        crawl_session_table.insert(record)
        return record

    @staticmethod
    def update_crawl_session(session_id, updates):
        """Update a crawl session"""
        Session = Query()
        crawl_session_table.update(updates, Session.id == session_id)

    @staticmethod
    def get_crawl_session(session_id):
        """Get a crawl session by ID"""
        Session = Query()
        return crawl_session_table.get(Session.id == session_id)

    @staticmethod
    def get_all_crawl_sessions():
        """Get all crawl sessions, sorted by creation date (newest first)"""
        sessions = crawl_session_table.all()
        return sorted(sessions, key=lambda x: x.get('started_at', ''), reverse=True)

    @staticmethod
    def create_crawl_result(session_id, url, seo_data, issues):
        """Create a crawl result for a specific URL"""
        record = {
            'id': DatabaseManager.generate_id(),
            'session_id': session_id,
            'url': url,
            'title': seo_data.get('title'),
            'meta_description': seo_data.get('meta_description'),
            'h1_tags': seo_data.get('h1_tags', []),
            'h2_tags': seo_data.get('h2_tags', []),
            'word_count': seo_data.get('word_count'),
            'load_time': seo_data.get('load_time'),
            'mobile_friendly': seo_data.get('mobile_friendly', False),
            'robots_txt_status': seo_data.get('robots_txt_status'),
            'issues': issues,  # List of issue descriptions
            'issue_count': len(issues),
            'analyzed_at': datetime.now().isoformat()
        }
        crawl_result_table.insert(record)
        return record

    @staticmethod
    def get_crawl_results(session_id):
        """Get all crawl results for a session"""
        Result = Query()
        results = crawl_result_table.search(Result.session_id == session_id)
        return sorted(results, key=lambda x: x.get('analyzed_at', ''))

    @staticmethod
    def count_crawl_sessions():
        """Count total crawl sessions"""
        return len(crawl_session_table)

    @staticmethod
    def get_database_stats():
        """Get database statistics"""
        return {
            'total_seo_analyses': DatabaseManager.count_seo_analyses(),
            'total_products': DatabaseManager.count_products(),
            'total_crawl_sessions': DatabaseManager.count_crawl_sessions(),
            'pending_jobs': DatabaseManager.count_pending_jobs(),
            'database_size': os.path.getsize(db_path) if os.path.exists(db_path) else 0
        }
