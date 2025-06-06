# 🕷️ Web Scraper & SEO Crawler

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A powerful, open-source web scraping and SEO analysis tool with comprehensive site crawling capabilities. Perfect for SEO professionals, developers, and researchers who need detailed website analysis and competitive research tools.

![Web Scraper Dashboard](https://via.placeholder.com/800x400/3B82F6/FFFFFF?text=Web+Scraper+Dashboard)

## ✨ Features

### 🔍 **SEO Analysis**
- **Complete SEO Audits** - Meta tags, headers, performance, mobile-friendliness
- **Issue Detection** - Identifies 15+ types of SEO problems with severity levels
- **Performance Metrics** - Page load times, content analysis, keyword density
- **Mobile Optimization** - Viewport and responsive design checks

### 🕷️ **Site Crawler**
- **Intelligent Discovery** - Finds URLs via sitemaps and link crawling
- **Batch Analysis** - Analyze entire websites (up to 200 pages)
- **Systemic Issues** - Identify patterns and common problems across sites
- **Detailed Reporting** - Comprehensive results with filtering and export

### 🛍️ **Product Research**
- **Multi-Platform Support** - Amazon, eBay, and generic e-commerce sites
- **Product Details** - Names, prices, descriptions, availability, reviews
- **Price Tracking** - Monitor product prices over time
- **Brand Analysis** - Extract brand and category information

### 🤖 **Robots.txt Compliance**
- **Ethical by Default** - Respects robots.txt automatically
- **Research Override** - Option to ignore for legitimate research
- **Transparent Reporting** - Clear status on compliance for each request

### 📊 **Data Management**
- **TinyDB Storage** - Lightweight, JSON-based local database
- **Export Options** - CSV and JSON export formats
- **Historical Tracking** - Monitor analysis history and trends
- **Dashboard** - Beautiful overview with statistics and recent activity

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 14+ (for Tailwind CSS)

### Installation

```bash
# Clone the repository
git clone https://github.com/websitebutlers/web-scraper-crawler.git
cd web-scraper-crawler

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
npm install

# Build CSS
npm run build-css

# Run the application
python app.py
```

Open your browser and navigate to `http://localhost:5000`

## 📖 Usage

### SEO Analysis
1. Navigate to **SEO Analysis**
2. Enter a website URL
3. Click **"Analyze"** to get comprehensive SEO insights
4. View detailed results including performance metrics and recommendations

### Site Crawler
1. Go to **Site Crawler**
2. Enter a website URL
3. Configure crawl settings (max URLs, depth)
4. Start crawl to analyze entire websites
5. View systemic issues and export results

### Product Research
1. Visit **Product Research**
2. Enter product URLs from Amazon, eBay, or other e-commerce sites
3. Extract detailed product information including prices and reviews

## 🔧 API Usage

### SEO Analysis
```bash
curl -X POST http://localhost:5000/api/analyze-seo \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Site Crawling
```bash
curl -X POST http://localhost:5000/api/crawl-site \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "max_urls": 50,
    "max_depth": 2,
    "respect_robots": true
  }'
```

### Product Scraping
```bash
curl -X POST http://localhost:5000/api/scrape-product \
  -H "Content-Type: application/json" \
  -d '{"url": "https://amazon.com/dp/PRODUCT_ID"}'
```

## ⚙️ Configuration

Create a `.env` file for custom settings:

```env
SECRET_KEY=your-secret-key-here
REQUEST_TIMEOUT=30
MAX_RETRIES=3
REQUESTS_PER_SECOND=1
RESPECT_ROBOTS_TXT=true
```

## 📁 Project Structure

```
web-scraper-crawler/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── package.json             # Node.js dependencies
├── models/
│   └── database.py          # Database models and management
├── scrapers/
│   ├── seo_scraper.py       # SEO analysis engine
│   ├── product_scraper.py   # Product scraping logic
│   └── site_crawler.py      # Site crawling engine
├── utils/
│   ├── helpers.py           # Utility functions
│   └── seo_analyzer.py      # SEO issue detection
├── templates/               # HTML templates
└── static/                  # CSS, JS, and assets
```

## 🛡️ Ethical Usage

This tool is designed for legitimate research and analysis:

- ✅ **Respects robots.txt by default**
- ✅ **Built-in rate limiting**
- ✅ **Transparent compliance reporting**
- ✅ **Educational and research focused**

**Please use responsibly:**
- Always check website terms of service
- Use robots.txt override only for legitimate research
- Implement appropriate delays between requests
- Respect server resources and bandwidth

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/) and [Tailwind CSS](https://tailwindcss.com/)
- Uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- Database powered by [TinyDB](https://tinydb.readthedocs.io/)

## 📞 Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/websitebutlers/web-scraper-crawler/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/websitebutlers/web-scraper-crawler/discussions)
- 📖 **Documentation**: Check our [Wiki](https://github.com/websitebutlers/web-scraper-crawler/wiki)

---

**Made with ❤️ for the SEO and web development community**
