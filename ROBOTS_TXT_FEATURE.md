# 🤖 Robots.txt Compliance Feature

Your web scraper now includes comprehensive robots.txt compliance functionality, giving you full control over how the scraper respects website crawling policies.

## ✅ **What's Been Added**

### 🔧 **Core Functionality**
- **Automatic robots.txt checking** for all scraping requests
- **Per-request override** via UI checkboxes
- **Global configuration** via environment variables
- **API parameter support** for programmatic control
- **Detailed status reporting** in analysis results

### 🎛️ **Control Options**

#### **1. UI Controls**
- **Checkbox on all forms**: "Ignore robots.txt (for research purposes)"
- **Dashboard forms**: Both SEO and Product scraping forms
- **Dedicated pages**: SEO Analysis and Product Research pages
- **Test page**: Global setting for all test buttons

#### **2. API Parameters**
```json
{
  "url": "https://example.com",
  "respect_robots": false
}
```

#### **3. Environment Configuration**
```env
RESPECT_ROBOTS_TXT=false  # Ignore robots.txt globally
```

#### **4. Programmatic Control**
```python
# SEO Scraper
scraper = SeoScraper(respect_robots=False)

# Product Scraper  
scraper = ProductScraper(respect_robots=False)
```

## 🚀 **How It Works**

### **Default Behavior (Respects robots.txt)**
1. Scraper fetches `/robots.txt` from target domain
2. Parses robots.txt rules for the user agent
3. Checks if the specific URL is allowed
4. **Blocks request** if robots.txt disallows it
5. **Proceeds** if allowed or if robots.txt is not found

### **When Ignoring robots.txt**
1. Skips robots.txt checking entirely
2. Proceeds directly to scraping
3. Reports "Robots.txt checking disabled" in results

## 📊 **Status Reporting**

The scraper now includes robots.txt status in all analysis results:

```json
{
  "robots_txt_status": "Allowed by robots.txt",
  "respect_robots": true
}
```

**Possible status messages:**
- `"Allowed by robots.txt"` - URL is permitted
- `"Blocked by robots.txt (https://site.com/robots.txt)"` - URL is blocked
- `"Could not read robots.txt: [error]"` - robots.txt not accessible (allows by default)
- `"Robots.txt checking disabled"` - Checking was bypassed

## 🎯 **Use Cases**

### **Research & Analysis**
- **Academic research** - Bypass restrictions for legitimate research
- **SEO auditing** - Analyze sites that block crawlers
- **Competitive analysis** - Research competitor sites
- **Security testing** - Test your own sites

### **Respectful Scraping**
- **Default compliance** - Respect website policies by default
- **Selective override** - Ignore only when necessary
- **Transparent operation** - Clear status reporting

## ⚖️ **Ethical Guidelines**

### **When to Ignore robots.txt**
✅ **Appropriate uses:**
- Analyzing your own websites
- Academic or research purposes
- SEO auditing with permission
- Testing and development
- Competitive analysis (limited scope)

### **When to Respect robots.txt**
✅ **Always respect when:**
- Scraping third-party sites at scale
- Commercial data collection
- Automated monitoring systems
- Public-facing tools

### **Best Practices**
- **Start with compliance** - Always try respecting robots.txt first
- **Use sparingly** - Only ignore when necessary for your research
- **Be respectful** - Implement delays and rate limiting
- **Check terms of service** - robots.txt is just one consideration
- **Consider alternatives** - Look for official APIs first

## 🛠️ **Technical Implementation**

### **Robots.txt Parser**
- Uses Python's built-in `urllib.robotparser`
- Handles standard robots.txt syntax
- Supports user-agent specific rules
- Graceful fallback if robots.txt is unavailable

### **Error Handling**
- **Network errors** - Assumes allowed if robots.txt unreachable
- **Parse errors** - Assumes allowed if robots.txt malformed
- **Timeout errors** - Assumes allowed if robots.txt times out

### **Performance**
- **Caching** - robots.txt is fetched once per domain per session
- **Timeout** - Quick timeout for robots.txt requests
- **Fallback** - Fast fallback to allow if robots.txt unavailable

## 🧪 **Testing**

### **Test the Feature**
1. Visit `/test` page in your web scraper
2. Check "Ignore robots.txt for all tests"
3. Test with sites that have robots.txt restrictions
4. Compare results with and without the checkbox

### **API Testing**
```bash
# Respect robots.txt
curl -X POST http://localhost:5000/api/analyze-seo \
  -H "Content-Type: application/json" \
  -d '{"url": "https://amazon.com", "respect_robots": true}'

# Ignore robots.txt  
curl -X POST http://localhost:5000/api/analyze-seo \
  -H "Content-Type: application/json" \
  -d '{"url": "https://amazon.com", "respect_robots": false}'
```

## 📝 **Configuration Examples**

### **Respect robots.txt by default (recommended)**
```env
RESPECT_ROBOTS_TXT=true
```

### **Ignore robots.txt globally (research mode)**
```env
RESPECT_ROBOTS_TXT=false
```

### **Mixed approach (programmatic control)**
```python
# Respect for general scraping
general_scraper = SeoScraper(respect_robots=True)

# Ignore for research
research_scraper = SeoScraper(respect_robots=False)
```

## 🎉 **Benefits**

### **For Researchers**
- **Unrestricted analysis** when needed
- **Transparent compliance** when appropriate
- **Flexible control** per request or globally

### **For Developers**
- **Ethical defaults** - Respects robots.txt by default
- **Easy override** - Simple checkbox or API parameter
- **Clear reporting** - Always know the robots.txt status

### **For Site Owners**
- **Respectful scraping** - Honors your robots.txt by default
- **Research exception** - Allows legitimate research when needed
- **Transparent operation** - Clear about when robots.txt is ignored

---

**Your web scraper now provides the perfect balance between ethical compliance and research flexibility!** 🚀

Use the robots.txt override responsibly and always consider the website owner's intentions and terms of service.
