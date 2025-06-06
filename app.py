from flask import Flask, render_template, request, jsonify, make_response
from config import Config
from models.database import DatabaseManager
from scrapers.seo_scraper import SeoScraper
from scrapers.product_scraper import ProductScraper
from scrapers.site_crawler import SiteCrawler
from utils.helpers import (
    is_valid_url, clean_url, export_to_csv, export_to_json,
    calculate_seo_score, truncate_text, format_number
)
from utils.seo_analyzer import SeoIssueAnalyzer
import json
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    """Dashboard page"""
    # Get recent analyses
    recent_seo = DatabaseManager.get_recent_seo_analyses(5)
    recent_products = DatabaseManager.get_recent_products(5)

    # Get statistics
    stats = DatabaseManager.get_database_stats()

    return render_template('index.html',
                         recent_seo=recent_seo,
                         recent_products=recent_products,
                         total_seo=stats['total_seo_analyses'],
                         total_products=stats['total_products'],
                         total_crawl_sessions=stats['total_crawl_sessions'],
                         pending_jobs=stats['pending_jobs'])

@app.route('/seo-analysis')
def seo_analysis():
    """SEO analysis page"""
    analyses = DatabaseManager.get_all_seo_analyses()
    return render_template('seo_analysis.html', analyses=analyses)

@app.route('/product-research')
def product_research():
    """Product research page"""
    products = DatabaseManager.get_all_products()
    return render_template('product_research.html', products=products)

@app.route('/test')
def test_page():
    """Test page with working URLs"""
    return render_template('test.html')

@app.route('/site-crawler')
def site_crawler():
    """Site crawler page"""
    sessions = DatabaseManager.get_all_crawl_sessions()
    return render_template('site_crawler.html', sessions=sessions)

@app.route('/crawl-results/<session_id>')
def crawl_results(session_id):
    """View crawl results for a specific session"""
    session = DatabaseManager.get_crawl_session(session_id)
    if not session:
        return "Crawl session not found", 404

    results = DatabaseManager.get_crawl_results(session_id)
    summary = SeoIssueAnalyzer.generate_summary(results)

    return render_template('crawl_results.html',
                         session=session,
                         results=results,
                         summary=summary)

@app.route('/api/analyze-seo', methods=['POST'])
def analyze_seo():
    """API endpoint to analyze SEO of a URL"""
    try:
        data = request.get_json()
        url = data.get('url')
        respect_robots = data.get('respect_robots', app.config.get('RESPECT_ROBOTS_TXT', True))

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        url = clean_url(url)
        if not is_valid_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400

        # Create scrape job
        job = DatabaseManager.create_scrape_job('seo', url)
        DatabaseManager.update_scrape_job(job['id'], {'status': 'running'})

        try:
            # Perform SEO analysis
            print(f"Starting SEO analysis for: {url} (respect_robots: {respect_robots})")  # Debug logging
            scraper = SeoScraper(user_agent=app.config['USER_AGENT'],
                               timeout=app.config['REQUEST_TIMEOUT'],
                               respect_robots=respect_robots)
            analysis_data = scraper.analyze_url(url)
            print(f"SEO analysis completed successfully")  # Debug logging

            # Save to database
            seo_analysis = DatabaseManager.create_seo_analysis(analysis_data)

            # Update job status
            DatabaseManager.update_scrape_job(job['id'], {
                'status': 'completed',
                'result_id': seo_analysis['id'],
                'completed_at': datetime.now().isoformat()
            })

            # Calculate SEO score
            analysis_data['seo_score'] = calculate_seo_score(analysis_data)
            analysis_data['id'] = seo_analysis['id']

            return jsonify({
                'success': True,
                'data': analysis_data,
                'job_id': job['id']
            })

        except Exception as e:
            # Update job with error
            error_msg = str(e)
            print(f"SEO analysis failed: {error_msg}")  # Debug logging
            DatabaseManager.update_scrape_job(job['id'], {
                'status': 'failed',
                'error_message': error_msg,
                'completed_at': datetime.now().isoformat()
            })

            return jsonify({'error': error_msg}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scrape-product', methods=['POST'])
def scrape_product():
    """API endpoint to scrape product data"""
    try:
        data = request.get_json()
        url = data.get('url')
        respect_robots = data.get('respect_robots', app.config.get('RESPECT_ROBOTS_TXT', True))

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        url = clean_url(url)
        if not is_valid_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400

        # Create scrape job
        job = DatabaseManager.create_scrape_job('product', url)
        DatabaseManager.update_scrape_job(job['id'], {'status': 'running'})

        try:
            # Perform product scraping
            print(f"Starting product scraping for: {url} (respect_robots: {respect_robots})")  # Debug logging
            scraper = ProductScraper(user_agent=app.config['USER_AGENT'],
                                   timeout=app.config['REQUEST_TIMEOUT'],
                                   respect_robots=respect_robots)
            product_data = scraper.scrape_product(url)

            # Save to database
            product = DatabaseManager.create_product_data(product_data)

            # Update job status
            DatabaseManager.update_scrape_job(job['id'], {
                'status': 'completed',
                'result_id': product['id'],
                'completed_at': datetime.now().isoformat()
            })

            product_data['id'] = product['id']

            return jsonify({
                'success': True,
                'data': product_data,
                'job_id': job['id']
            })

        except Exception as e:
            # Update job with error
            DatabaseManager.update_scrape_job(job['id'], {
                'status': 'failed',
                'error_message': str(e),
                'completed_at': datetime.now().isoformat()
            })

            return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crawl-site', methods=['POST'])
def crawl_site():
    """API endpoint to crawl an entire site"""
    try:
        data = request.get_json()
        base_url = data.get('url')
        max_urls = data.get('max_urls', 50)
        max_depth = data.get('max_depth', 2)
        respect_robots = data.get('respect_robots', app.config.get('RESPECT_ROBOTS_TXT', True))

        if not base_url:
            return jsonify({'error': 'URL is required'}), 400

        base_url = clean_url(base_url)
        if not is_valid_url(base_url):
            return jsonify({'error': 'Invalid URL format'}), 400

        # Validate limits
        max_urls = min(max(int(max_urls), 1), 200)  # Limit between 1-200
        max_depth = min(max(int(max_depth), 1), 5)   # Limit between 1-5

        # Create crawl session
        session = DatabaseManager.create_crawl_session(
            base_url=base_url,
            max_urls=max_urls,
            max_depth=max_depth,
            respect_robots=respect_robots
        )

        try:
            # Update session status
            DatabaseManager.update_crawl_session(session['id'], {'status': 'running'})

            # Initialize crawler
            crawler = SiteCrawler(
                user_agent=app.config['USER_AGENT'],
                timeout=app.config['REQUEST_TIMEOUT'],
                respect_robots=respect_robots
            )

            # Crawl the site
            print(f"Starting crawl for {base_url}")
            discovered_urls = crawler.crawl_site(base_url, max_urls, max_depth)

            # Analyze each URL
            seo_scraper = SeoScraper(
                user_agent=app.config['USER_AGENT'],
                timeout=app.config['REQUEST_TIMEOUT'],
                respect_robots=respect_robots
            )

            total_issues = 0
            analyzed_count = 0

            for url in discovered_urls:
                try:
                    print(f"Analyzing URL: {url}")
                    seo_data = seo_scraper.analyze_url(url)

                    # Analyze issues
                    issues = SeoIssueAnalyzer.analyze_issues(seo_data)
                    total_issues += len(issues)

                    # Save result
                    DatabaseManager.create_crawl_result(
                        session_id=session['id'],
                        url=url,
                        seo_data=seo_data,
                        issues=issues
                    )

                    analyzed_count += 1

                except Exception as e:
                    print(f"Error analyzing {url}: {e}")
                    # Save error result
                    DatabaseManager.create_crawl_result(
                        session_id=session['id'],
                        url=url,
                        seo_data={'url': url, 'error': str(e)},
                        issues=[f"Analysis failed: {str(e)}"]
                    )

            # Update session with completion
            DatabaseManager.update_crawl_session(session['id'], {
                'status': 'completed',
                'total_urls_found': len(discovered_urls),
                'total_urls_analyzed': analyzed_count,
                'issues_found': total_issues,
                'completed_at': datetime.now().isoformat()
            })

            return jsonify({
                'success': True,
                'session_id': session['id'],
                'urls_found': len(discovered_urls),
                'urls_analyzed': analyzed_count,
                'total_issues': total_issues
            })

        except Exception as e:
            # Update session with error
            DatabaseManager.update_crawl_session(session['id'], {
                'status': 'failed',
                'error_message': str(e),
                'completed_at': datetime.now().isoformat()
            })

            return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/crawl-results/<session_id>')
def export_crawl_results(session_id):
    """Export crawl results as CSV or JSON"""
    format_type = request.args.get('format', 'csv')

    try:
        session = DatabaseManager.get_crawl_session(session_id)
        if not session:
            return jsonify({'error': 'Session not found'}), 404

        results = DatabaseManager.get_crawl_results(session_id)

        # Prepare data for export
        export_data = []
        for result in results:
            export_data.append({
                'url': result.get('url'),
                'title': result.get('title'),
                'meta_description': result.get('meta_description'),
                'h1_count': len(result.get('h1_tags', [])),
                'h2_count': len(result.get('h2_tags', [])),
                'word_count': result.get('word_count'),
                'load_time': result.get('load_time'),
                'mobile_friendly': result.get('mobile_friendly'),
                'issue_count': result.get('issue_count', 0),
                'issues': '; '.join(result.get('issues', [])),
                'analyzed_at': result.get('analyzed_at')
            })

        if format_type == 'csv':
            csv_content = export_to_csv(export_data, f'crawl_results_{session_id}.csv')
            response = make_response(csv_content)
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = f'attachment; filename=crawl_results_{session_id}.csv'
            return response
        else:
            json_content = export_to_json(export_data)
            response = make_response(json_content)
            response.headers['Content-Type'] = 'application/json'
            response.headers['Content-Disposition'] = f'attachment; filename=crawl_results_{session_id}.json'
            return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/<data_type>')
def export_data(data_type):
    """Export data as CSV or JSON"""
    format_type = request.args.get('format', 'csv')

    try:
        if data_type == 'seo':
            analyses = DatabaseManager.get_all_seo_analyses()
            data = []
            for analysis in analyses:
                data.append({
                    'id': analysis['id'],
                    'url': analysis['url'],
                    'title': analysis['title'],
                    'meta_description': analysis['meta_description'],
                    'word_count': analysis['word_count'],
                    'load_time': analysis['load_time'],
                    'mobile_friendly': analysis['mobile_friendly'],
                    'created_at': analysis.get('created_at', '')
                })
        elif data_type == 'products':
            products = DatabaseManager.get_all_products()
            data = []
            for product in products:
                data.append({
                    'id': product['id'],
                    'url': product['url'],
                    'name': product['name'],
                    'price': product['price'],
                    'description': truncate_text(product.get('description'), 200),
                    'availability': product['availability'],
                    'rating': product['rating'],
                    'reviews_count': product['reviews_count'],
                    'brand': product['brand'],
                    'category': product['category'],
                    'created_at': product.get('created_at', '')
                })
        else:
            return jsonify({'error': 'Invalid data type'}), 400
        
        if format_type == 'csv':
            csv_content = export_to_csv(data, f'{data_type}_export.csv')
            response = make_response(csv_content)
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = f'attachment; filename={data_type}_export.csv'
            return response
        else:
            json_content = export_to_json(data)
            response = make_response(json_content)
            response.headers['Content-Type'] = 'application/json'
            response.headers['Content-Disposition'] = f'attachment; filename={data_type}_export.json'
            return response
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Template filters
@app.template_filter('truncate_text')
def truncate_text_filter(text, length=100):
    return truncate_text(text, length)

@app.template_filter('format_number')
def format_number_filter(num):
    return format_number(num)

@app.template_filter('parse_json')
def parse_json_filter(data):
    """Parse JSON data - now handles both strings and already parsed data"""
    if isinstance(data, (list, dict)):
        return data
    try:
        return json.loads(data) if data else []
    except:
        return []

@app.template_filter('format_datetime')
def format_datetime_filter(dt):
    """Format datetime for display"""
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%d %H:%M')
    elif isinstance(dt, str):
        try:
            # Parse ISO format datetime string
            parsed_dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
            return parsed_dt.strftime('%Y-%m-%d %H:%M')
        except:
            return dt
    return str(dt) if dt else 'N/A'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
