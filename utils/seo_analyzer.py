"""
SEO Issue Analyzer
Identifies common SEO problems in crawled pages
"""

import re
from collections import Counter

class SeoIssueAnalyzer:
    """Analyzes SEO data and identifies issues"""
    
    @staticmethod
    def analyze_issues(seo_data):
        """
        Analyze SEO data and return list of issues
        
        Args:
            seo_data: Dictionary containing SEO analysis results
            
        Returns:
            List of issue descriptions
        """
        issues = []
        
        # Title issues
        title_issues = SeoIssueAnalyzer._analyze_title(seo_data.get('title'))
        issues.extend(title_issues)
        
        # Meta description issues
        meta_issues = SeoIssueAnalyzer._analyze_meta_description(seo_data.get('meta_description'))
        issues.extend(meta_issues)
        
        # Header issues
        header_issues = SeoIssueAnalyzer._analyze_headers(
            seo_data.get('h1_tags', []), 
            seo_data.get('h2_tags', [])
        )
        issues.extend(header_issues)
        
        # Performance issues
        performance_issues = SeoIssueAnalyzer._analyze_performance(seo_data.get('load_time'))
        issues.extend(performance_issues)
        
        # Mobile issues
        mobile_issues = SeoIssueAnalyzer._analyze_mobile(seo_data.get('mobile_friendly'))
        issues.extend(mobile_issues)
        
        # Content issues
        content_issues = SeoIssueAnalyzer._analyze_content(seo_data.get('word_count'))
        issues.extend(content_issues)
        
        # Image issues
        image_issues = SeoIssueAnalyzer._analyze_images(seo_data.get('images_without_alt', []))
        issues.extend(image_issues)
        
        return issues
    
    @staticmethod
    def _analyze_title(title):
        """Analyze title tag issues"""
        issues = []
        
        if not title:
            issues.append("Missing title tag")
        elif not title.strip():
            issues.append("Empty title tag")
        else:
            title_length = len(title)
            if title_length < 30:
                issues.append(f"Title too short ({title_length} chars) - should be 30-60 characters")
            elif title_length > 60:
                issues.append(f"Title too long ({title_length} chars) - should be 30-60 characters")
            
            # Check for common title issues
            if title.lower() == 'untitled':
                issues.append("Generic 'Untitled' title")
            elif title.lower().startswith('welcome to'):
                issues.append("Generic 'Welcome to' title")
            elif '|' not in title and '-' not in title and ':' not in title:
                issues.append("Title lacks brand/site name separator")
        
        return issues
    
    @staticmethod
    def _analyze_meta_description(meta_description):
        """Analyze meta description issues"""
        issues = []
        
        if not meta_description:
            issues.append("Missing meta description")
        elif not meta_description.strip():
            issues.append("Empty meta description")
        else:
            desc_length = len(meta_description)
            if desc_length < 120:
                issues.append(f"Meta description too short ({desc_length} chars) - should be 120-160 characters")
            elif desc_length > 160:
                issues.append(f"Meta description too long ({desc_length} chars) - should be 120-160 characters")
            
            # Check for duplicate content
            if meta_description.lower().strip() == meta_description.lower().strip():
                # This is a placeholder for duplicate detection across pages
                pass
        
        return issues
    
    @staticmethod
    def _analyze_headers(h1_tags, h2_tags):
        """Analyze header tag issues"""
        issues = []
        
        # H1 analysis
        if not h1_tags:
            issues.append("Missing H1 tag")
        elif len(h1_tags) > 1:
            issues.append(f"Multiple H1 tags ({len(h1_tags)}) - should have only one")
        else:
            h1_text = h1_tags[0].strip()
            if not h1_text:
                issues.append("Empty H1 tag")
            elif len(h1_text) < 20:
                issues.append(f"H1 too short ({len(h1_text)} chars)")
            elif len(h1_text) > 70:
                issues.append(f"H1 too long ({len(h1_text)} chars)")
        
        # H2 analysis
        if not h2_tags:
            issues.append("No H2 tags found - consider adding subheadings")
        elif len(h2_tags) > 10:
            issues.append(f"Too many H2 tags ({len(h2_tags)}) - consider restructuring content")
        
        return issues
    
    @staticmethod
    def _analyze_performance(load_time):
        """Analyze performance issues"""
        issues = []
        
        if load_time is None:
            return issues
        
        if load_time > 3:
            issues.append(f"Slow page load time ({load_time:.1f}s) - should be under 3 seconds")
        elif load_time > 2:
            issues.append(f"Page load time could be improved ({load_time:.1f}s)")
        
        return issues
    
    @staticmethod
    def _analyze_mobile(mobile_friendly):
        """Analyze mobile friendliness issues"""
        issues = []
        
        if not mobile_friendly:
            issues.append("Not mobile-friendly - missing viewport meta tag")
        
        return issues
    
    @staticmethod
    def _analyze_content(word_count):
        """Analyze content issues"""
        issues = []
        
        if word_count is None:
            return issues
        
        if word_count < 300:
            issues.append(f"Low content volume ({word_count} words) - consider adding more content")
        elif word_count > 3000:
            issues.append(f"Very long content ({word_count} words) - consider breaking into multiple pages")
        
        return issues
    
    @staticmethod
    def _analyze_images(images_without_alt):
        """Analyze image accessibility issues"""
        issues = []
        
        if images_without_alt:
            count = len(images_without_alt)
            if count == 1:
                issues.append("1 image missing alt text")
            else:
                issues.append(f"{count} images missing alt text")
        
        return issues
    
    @staticmethod
    def categorize_issue(issue_text):
        """Categorize an issue by type"""
        issue_lower = issue_text.lower()
        
        if 'title' in issue_lower:
            return 'title'
        elif 'meta description' in issue_lower:
            return 'meta_description'
        elif 'h1' in issue_lower or 'h2' in issue_lower or 'heading' in issue_lower:
            return 'headers'
        elif 'load time' in issue_lower or 'slow' in issue_lower:
            return 'performance'
        elif 'mobile' in issue_lower:
            return 'mobile'
        elif 'content' in issue_lower or 'word' in issue_lower:
            return 'content'
        elif 'image' in issue_lower or 'alt' in issue_lower:
            return 'images'
        else:
            return 'other'
    
    @staticmethod
    def get_issue_severity(issue_text):
        """Get severity level of an issue"""
        issue_lower = issue_text.lower()
        
        # Critical issues
        if any(keyword in issue_lower for keyword in ['missing title', 'missing h1', 'empty title']):
            return 'critical'
        
        # High priority issues
        elif any(keyword in issue_lower for keyword in ['missing meta description', 'not mobile-friendly', 'slow page load']):
            return 'high'
        
        # Medium priority issues
        elif any(keyword in issue_lower for keyword in ['too short', 'too long', 'multiple h1']):
            return 'medium'
        
        # Low priority issues
        else:
            return 'low'
    
    @staticmethod
    def generate_summary(all_results):
        """Generate a summary of issues across all crawled pages"""
        total_pages = len(all_results)
        total_issues = sum(len(result.get('issues', [])) for result in all_results)
        
        # Count issues by category
        issue_categories = Counter()
        issue_severities = Counter()
        
        for result in all_results:
            for issue in result.get('issues', []):
                category = SeoIssueAnalyzer.categorize_issue(issue)
                severity = SeoIssueAnalyzer.get_issue_severity(issue)
                issue_categories[category] += 1
                issue_severities[severity] += 1
        
        # Find most common issues
        all_issues = []
        for result in all_results:
            all_issues.extend(result.get('issues', []))
        
        common_issues = Counter(all_issues).most_common(10)
        
        # Calculate percentages
        pages_with_issues = len([r for r in all_results if r.get('issues')])
        issue_percentage = (pages_with_issues / total_pages * 100) if total_pages > 0 else 0
        
        return {
            'total_pages': total_pages,
            'total_issues': total_issues,
            'pages_with_issues': pages_with_issues,
            'issue_percentage': round(issue_percentage, 1),
            'avg_issues_per_page': round(total_issues / total_pages, 1) if total_pages > 0 else 0,
            'issue_categories': dict(issue_categories),
            'issue_severities': dict(issue_severities),
            'common_issues': common_issues
        }
