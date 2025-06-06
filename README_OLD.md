# Web Scraper - SEO & Product Research Tool

A powerful Flask-based web application for SEO analysis and product research using web scraping techniques. Built with Python, Flask, and Tailwind CSS.

## Features

### 🔍 SEO Analysis
- **Meta Tag Analysis**: Extract and analyze title tags, meta descriptions
- **Header Structure**: Analyze H1, H2 heading tags
- **Performance Metrics**: Measure page load times
- **Mobile Responsiveness**: Check viewport meta tags
- **Keyword Analysis**: Extract and count keyword frequency
- **Link Analysis**: Count internal and external links
- **SEO Scoring**: Calculate overall SEO score
- **Robots.txt Compliance**: Option to respect or ignore robots.txt

### 🕷️ Site Crawler
- **Intelligent URL Discovery**: Finds URLs via sitemaps and link crawling
- **Batch SEO Analysis**: Analyze multiple pages automatically
- **Issue Detection**: Identifies 15+ types of SEO problems
- **Systemic Analysis**: Highlights patterns and common issues across sites
- **Detailed Reporting**: Comprehensive results with filtering and export
- **Respectful Crawling**: Built-in delays and rate limiting

### 🛍️ Product Research
- **Multi-Platform Support**: Amazon, eBay, and generic e-commerce sites
- **Product Details**: Name, price, description, availability
- **Review Data**: Ratings and review counts
- **Brand Information**: Extract brand and category data
- **Price Tracking**: Monitor product prices over time
- **Robots.txt Compliance**: Option to respect or ignore robots.txt

### 📊 Data Management
- **TinyDB Storage**: Lightweight, JSON-based local database
- **Export Options**: CSV and JSON export formats
- **Historical Data**: Track analysis and scraping history
- **Dashboard**: Overview of recent activities and statistics
- **Job Tracking**: Monitor scraping job status
- **Easy Backup**: Simple database backup and restore utilities

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+ (for Tailwind CSS)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd web-scraper
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node.js dependencies**
   ```bash
   npm install
   ```

5. **Build Tailwind CSS**
   ```bash
   npm run build-css
   ```

6. **Set up environment variables** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

7. **Initialize database**
   ```bash
   python app.py
   # TinyDB database file will be created automatically
   ```

## Usage

### Running the Application

1. **Start the Flask development server**
   ```bash
   python app.py
   ```

2. **Start Tailwind CSS watcher** (in another terminal)
   ```bash
   npm run build-css
   ```

3. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

### SEO Analysis

1. Navigate to the SEO Analysis page
2. Enter a website URL (e.g., `https://example.com`)
3. Click "Analyze" to start the analysis
4. View results including:
   - SEO score
   - Page title and meta description
   - Header tags (H1, H2)
   - Word count and load time
   - Mobile-friendly status

### Product Research

1. Navigate to the Product Research page
2. Enter a product URL from supported sites:
   - Amazon: `https://amazon.com/dp/PRODUCT_ID`
   - eBay: `https://ebay.com/itm/ITEM_ID`
   - Other e-commerce sites
3. Click "Scrape" to extract product data
4. View extracted information:
   - Product name and description
   - Price and availability
   - Brand and category
   - Ratings and reviews

## API Endpoints

### SEO Analysis
```
POST /api/analyze-seo
Content-Type: application/json

{
  "url": "https://example.com"
}
```

### Product Scraping
```
POST /api/scrape-product
Content-Type: application/json

{
  "url": "https://amazon.com/dp/PRODUCT_ID"
}
```

### Data Export
```
GET /api/export/seo?format=csv
GET /api/export/products?format=json
```

## Database Management

The application uses TinyDB, a lightweight JSON-based database perfect for local usage. Your data is stored in a human-readable `scraper_data.json` file.

### Backup and Restore

Use the included backup utility:

```bash
# Create a backup
python backup_database.py backup

# List available backups
python backup_database.py list

# Restore from backup
python backup_database.py restore scraper_backup_20241205_143022.json
```

### Database Location

- **Database file**: `scraper_data.json` (created automatically)
- **Backup files**: `scraper_backup_YYYYMMDD_HHMMSS.json`

### Advantages of TinyDB

- **Human readable**: JSON format, easy to inspect and edit
- **No setup required**: No database server installation needed
- **Lightweight**: Perfect for local development and small to medium datasets
- **Easy backup**: Simple file copy for backup and restore
- **Cross-platform**: Works on any system with Python

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
REQUEST_TIMEOUT=30
MAX_RETRIES=3
REQUESTS_PER_SECOND=1
RESPECT_ROBOTS_TXT=true
```

### Customization

- **User Agent**: Modify `USER_AGENT` in `config.py`
- **Timeout Settings**: Adjust `REQUEST_TIMEOUT` and `MAX_RETRIES`
- **Rate Limiting**: Configure `REQUESTS_PER_SECOND`
- **Robots.txt**: Set `RESPECT_ROBOTS_TXT=false` to ignore robots.txt globally
- **Styling**: Customize Tailwind CSS in `tailwind.config.js`

### Robots.txt Compliance

The scraper includes built-in robots.txt compliance:

- **Default Behavior**: Respects robots.txt by default
- **Per-Request Override**: Use the "Ignore robots.txt" checkbox in the UI
- **Global Setting**: Set `RESPECT_ROBOTS_TXT=false` in `.env` to ignore globally
- **API Control**: Send `"respect_robots": false` in API requests

**Ethical Usage**:
- Always respect website terms of service
- Use robots.txt override responsibly and only for legitimate research
- Consider rate limiting and be respectful of server resources

## Project Structure

```
web-scraper/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── package.json          # Node.js dependencies
├── tailwind.config.js    # Tailwind CSS configuration
├── models/
│   └── database.py       # Database models
├── scrapers/
│   ├── seo_scraper.py    # SEO analysis logic
│   └── product_scraper.py # Product scraping logic
├── static/
│   ├── css/              # CSS files
│   └── js/               # JavaScript files
├── templates/            # HTML templates
└── utils/
    └── helpers.py        # Utility functions
```

## Technologies Used

- **Backend**: Python, Flask, TinyDB
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Scraping**: BeautifulSoup, Requests, Selenium
- **Database**: TinyDB (JSON-based, local storage)
- **Build Tools**: Node.js, npm

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and research purposes. Please respect website terms of service and robots.txt files. Use responsibly and consider implementing rate limiting and proper error handling for production use.

## Support

For issues and questions, please open an issue on the GitHub repository.
