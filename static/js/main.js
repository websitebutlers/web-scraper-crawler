// Main JavaScript functionality
class WebScraperApp {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.initTooltips();
    }
    
    bindEvents() {
        // SEO Analysis form
        const seoForm = document.getElementById('seo-form');
        if (seoForm) {
            seoForm.addEventListener('submit', this.handleSeoAnalysis.bind(this));
        }
        
        // Product scraping form
        const productForm = document.getElementById('product-form');
        if (productForm) {
            productForm.addEventListener('submit', this.handleProductScraping.bind(this));
        }
        
        // Export buttons
        document.querySelectorAll('[data-export]').forEach(btn => {
            btn.addEventListener('click', this.handleExport.bind(this));
        });
        
        // Delete buttons
        document.querySelectorAll('[data-delete]').forEach(btn => {
            btn.addEventListener('click', this.handleDelete.bind(this));
        });
    }
    
    async handleSeoAnalysis(e) {
        e.preventDefault();
        
        const form = e.target;
        const url = form.querySelector('input[name="url"]').value;
        const ignoreRobots = form.querySelector('input[name="ignore_robots"]').checked;
        const submitBtn = form.querySelector('button[type="submit"]');
        const resultsDiv = document.getElementById('seo-results');
        
        if (!url) {
            this.showAlert('Please enter a URL', 'error');
            return;
        }

        // Basic URL validation and cleanup
        url = url.trim();
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
            url = 'https://' + url;
        }

        // Update the input field with the cleaned URL
        form.querySelector('input[name="url"]').value = url;
        
        // Show loading state
        this.setLoadingState(submitBtn, true);
        resultsDiv.innerHTML = '<div class="text-center py-8"><div class="loading-spinner mx-auto"></div><p class="mt-2 text-gray-600">Analyzing URL...</p></div>';
        
        try {
            const response = await fetch('/api/analyze-seo', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: url,
                    respect_robots: !ignoreRobots
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displaySeoResults(data.data);
                this.showAlert('SEO analysis completed successfully!', 'success');
                form.reset();
            } else {
                throw new Error(data.error || 'Analysis failed');
            }
            
        } catch (error) {
            console.error('Error:', error);
            let errorMessage = 'Analysis failed. Please try again.';
            if (error.message) {
                errorMessage = error.message;
            }
            this.showAlert(errorMessage, 'error');
            resultsDiv.innerHTML = `
                <div class="text-center py-8">
                    <div class="text-red-600 mb-2">❌ Analysis Failed</div>
                    <div class="text-sm text-gray-600">${errorMessage}</div>
                    <div class="text-xs text-gray-500 mt-2">
                        Common causes: Network issues, blocked by website, invalid URL
                    </div>
                </div>
            `;
        } finally {
            this.setLoadingState(submitBtn, false);
        }
    }
    
    async handleProductScraping(e) {
        e.preventDefault();
        
        const form = e.target;
        const url = form.querySelector('input[name="url"]').value;
        const ignoreRobots = form.querySelector('input[name="ignore_robots"]').checked;
        const submitBtn = form.querySelector('button[type="submit"]');
        const resultsDiv = document.getElementById('product-results');
        
        if (!url) {
            this.showAlert('Please enter a URL', 'error');
            return;
        }

        // Basic URL validation and cleanup
        url = url.trim();
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
            url = 'https://' + url;
        }

        // Update the input field with the cleaned URL
        form.querySelector('input[name="url"]').value = url;
        
        // Show loading state
        this.setLoadingState(submitBtn, true);
        resultsDiv.innerHTML = '<div class="text-center py-8"><div class="loading-spinner mx-auto"></div><p class="mt-2 text-gray-600">Scraping product data...</p></div>';
        
        try {
            const response = await fetch('/api/scrape-product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: url,
                    respect_robots: !ignoreRobots
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayProductResults(data.data);
                this.showAlert('Product data scraped successfully!', 'success');
                form.reset();
            } else {
                throw new Error(data.error || 'Scraping failed');
            }
            
        } catch (error) {
            console.error('Error:', error);
            let errorMessage = 'Scraping failed. Please try again.';
            if (error.message) {
                errorMessage = error.message;
            }
            this.showAlert(errorMessage, 'error');
            resultsDiv.innerHTML = `
                <div class="text-center py-8">
                    <div class="text-red-600 mb-2">❌ Scraping Failed</div>
                    <div class="text-sm text-gray-600">${errorMessage}</div>
                    <div class="text-xs text-gray-500 mt-2">
                        Common causes: Site blocks bots, invalid URL, network issues
                    </div>
                </div>
            `;
        } finally {
            this.setLoadingState(submitBtn, false);
        }
    }
    
    displaySeoResults(data) {
        const resultsDiv = document.getElementById('seo-results');
        
        const html = `
            <div class="card fade-in">
                <h3 class="text-lg font-semibold mb-4">SEO Analysis Results</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                    <div class="stat-card">
                        <div class="text-2xl font-bold">${data.seo_score || 0}/100</div>
                        <div class="text-sm opacity-90">SEO Score</div>
                    </div>
                    <div class="stat-card">
                        <div class="text-2xl font-bold">${data.word_count || 0}</div>
                        <div class="text-sm opacity-90">Words</div>
                    </div>
                    <div class="stat-card">
                        <div class="text-2xl font-bold">${data.load_time || 0}s</div>
                        <div class="text-sm opacity-90">Load Time</div>
                    </div>
                </div>
                
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Title</label>
                        <p class="text-gray-900">${data.title || 'No title found'}</p>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Meta Description</label>
                        <p class="text-gray-900">${data.meta_description || 'No meta description found'}</p>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">H1 Tags (${data.h1_tags?.length || 0})</label>
                        <ul class="list-disc list-inside text-gray-900">
                            ${(data.h1_tags || []).map(tag => `<li>${tag}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Mobile Friendly</label>
                        <span class="badge ${data.mobile_friendly ? 'badge-success' : 'badge-error'}">
                            ${data.mobile_friendly ? 'Yes' : 'No'}
                        </span>
                    </div>
                </div>
            </div>
        `;
        
        resultsDiv.innerHTML = html;
    }
    
    displayProductResults(data) {
        const resultsDiv = document.getElementById('product-results');
        
        const html = `
            <div class="card fade-in">
                <h3 class="text-lg font-semibold mb-4">Product Data</h3>
                
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Product Name</label>
                        <p class="text-gray-900 font-medium">${data.name || 'Not found'}</p>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Price</label>
                            <p class="text-gray-900 text-lg font-semibold text-green-600">${data.price || 'Not found'}</p>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Availability</label>
                            <span class="badge ${data.availability ? 'badge-success' : 'badge-warning'}">
                                ${data.availability || 'Unknown'}
                            </span>
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Brand</label>
                            <p class="text-gray-900">${data.brand || 'Not found'}</p>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Rating</label>
                            <p class="text-gray-900">${data.rating ? `${data.rating}/5` : 'Not found'}</p>
                        </div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
                        <p class="text-gray-900 text-sm">${data.description || 'No description found'}</p>
                    </div>
                </div>
            </div>
        `;
        
        resultsDiv.innerHTML = html;
    }
    
    handleExport(e) {
        const dataType = e.target.dataset.export;
        const format = e.target.dataset.format || 'csv';
        
        window.open(`/api/export/${dataType}?format=${format}`, '_blank');
    }
    
    setLoadingState(button, loading) {
        if (loading) {
            button.disabled = true;
            button.innerHTML = '<div class="loading-spinner mr-2"></div>Processing...';
        } else {
            button.disabled = false;
            button.innerHTML = button.dataset.originalText || 'Submit';
        }
    }
    
    showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
            type === 'success' ? 'bg-green-500 text-white' :
            type === 'error' ? 'bg-red-500 text-white' :
            'bg-blue-500 text-white'
        }`;
        alertDiv.textContent = message;
        
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
    
    initTooltips() {
        // Simple tooltip implementation
        document.querySelectorAll('[data-tooltip]').forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                const tooltip = document.createElement('div');
                tooltip.className = 'absolute bg-gray-800 text-white text-sm rounded px-2 py-1 z-50';
                tooltip.textContent = e.target.dataset.tooltip;
                document.body.appendChild(tooltip);
                
                const rect = e.target.getBoundingClientRect();
                tooltip.style.left = rect.left + 'px';
                tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
                
                e.target._tooltip = tooltip;
            });
            
            element.addEventListener('mouseleave', (e) => {
                if (e.target._tooltip) {
                    e.target._tooltip.remove();
                    delete e.target._tooltip;
                }
            });
        });
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WebScraperApp();
});
