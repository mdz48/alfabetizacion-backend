/**
 * Generate a simple placeholder image when external placeholders fail
 * @param {HTMLImageElement} img - The image element that failed to load
 * @param {string} text - Text to display on the placeholder
 * @param {string} bgColor - Background color (hex or name)
 * @param {string} textColor - Text color (hex or name)
 */
function createPlaceholder(img, text, bgColor = '#cccccc', textColor = '#333333') {
    // Get dimensions from the image or use defaults
    const width = img.width || 100;
    const height = img.height || 100;
    
    // Create canvas element
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    
    // Get context and draw background
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, width, height);
    
    // Draw text
    ctx.fillStyle = textColor;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    // Scale font size based on canvas dimension
    const fontSize = Math.floor(Math.min(width, height) / 10);
    ctx.font = `bold ${fontSize}px Arial, sans-serif`;
    
    // Wrap text if needed
    const maxWidth = width * 0.8;
    const words = text.split(' ');
    const lines = [];
    let currentLine = words[0];
    
    for (let i = 1; i < words.length; i++) {
        const word = words[i];
        const testLine = currentLine + ' ' + word;
        const metrics = ctx.measureText(testLine);
        
        if (metrics.width > maxWidth) {
            lines.push(currentLine);
            currentLine = word;
        } else {
            currentLine = testLine;
        }
    }
    lines.push(currentLine);
    
    // Draw each line, positioning vertically
    const lineHeight = fontSize * 1.2;
    const totalHeight = lineHeight * lines.length;
    let y = (height - totalHeight) / 2 + lineHeight / 2;
    
    for (const line of lines) {
        ctx.fillText(line, width / 2, y);
        y += lineHeight;
    }
    
    // Convert to data URL and set as source
    img.src = canvas.toDataURL('image/png');
}

/**
 * Set a placeholder fallback for an image that might fail to load
 * @param {HTMLImageElement|string} imgElement - The image element or selector
 * @param {string} text - Text to display on the placeholder
 * @param {string} bgColor - Background color (hex or name)
 * @param {string} textColor - Text color (hex or name)
 */
function setPlaceholderFallback(imgElement, text, bgColor = '#007bff', textColor = '#ffffff') {
    const img = typeof imgElement === 'string' ? document.querySelector(imgElement) : imgElement;
    if (!img) return;
    
    img.onerror = function() {
        createPlaceholder(this, text, bgColor, textColor);
    };
}

// Intercept any jQuery image error handlers that try to use placeholder.com
if (typeof jQuery !== 'undefined') {
    jQuery.fn.originalOn = jQuery.fn.on;
    jQuery.fn.on = function(event, selector, data, callback) {
        if (event === 'error' && this.is('img')) {
            const originalCallback = typeof selector === 'function' ? selector : 
                                      typeof data === 'function' ? data : callback;
            
            const newCallback = function(e) {
                // Check if the original callback tries to set src to placeholder.com
                const originalAttr = jQuery.fn.attr;
                jQuery.fn.attr = function(attr, value) {
                    if (attr === 'src' && typeof value === 'string' && value.includes('placeholder.com')) {
                        // Extract text from the URL
                        const textMatch = value.match(/text=([^&]+)/);
                        const text = textMatch ? decodeURIComponent(textMatch[1]) : 'Image';
                        
                        // Instead of setting external placeholder, use our local one
                        createPlaceholder(this[0], text, '#007bff', '#ffffff');
                        return this;
                    }
                    return originalAttr.apply(this, arguments);
                };
                
                // Call original callback
                if (originalCallback) {
                    originalCallback.apply(this, arguments);
                }
                
                // Restore original jQuery attr method
                jQuery.fn.attr = originalAttr;
            };
            
            // Replace the callback with our interceptor
            if (typeof selector === 'function') {
                return jQuery.fn.originalOn.call(this, event, newCallback, data, callback);
            } else if (typeof data === 'function') {
                return jQuery.fn.originalOn.call(this, event, selector, newCallback, callback);
            } else {
                return jQuery.fn.originalOn.call(this, event, selector, data, newCallback);
            }
        }
        return jQuery.fn.originalOn.apply(this, arguments);
    };
}

// Add global handler for all images on page load
document.addEventListener('DOMContentLoaded', function() {
    // Find all images with onerror attributes that use placeholder.com
    const images = document.querySelectorAll('img[onerror*="placeholder.com"]');
    
    // Update their onerror handlers
    images.forEach(img => {
        // Extract text from original onerror, fallback to image alt
        const textMatch = img.getAttribute('onerror').match(/text=([^'&"]+)/);
        const placeholderText = textMatch ? textMatch[1] : (img.alt || 'Image');
        
        // Replace with our local placeholder generator
        img.setAttribute('onerror', `createPlaceholder(this, '${placeholderText}', '#007bff', '#ffffff')`);
    });
    
    // Also find any img tags with placeholder.com in the src
    const placeholderImages = document.querySelectorAll('img[src*="placeholder.com"]');
    placeholderImages.forEach(img => {
        const textMatch = img.getAttribute('src').match(/text=([^&]+)/);
        const placeholderText = textMatch ? decodeURIComponent(textMatch[1]) : (img.alt || 'Image');
        
        // Set up error handler to use our local placeholder
        img.onerror = function() {
            createPlaceholder(this, placeholderText, '#007bff', '#ffffff');
        };
        
        // Trigger error handler immediately if placeholder.com is already in the src
        if (img.complete && img.naturalHeight === 0) {
            img.onerror();
        }
    });
});

// Expose the setPlaceholderFallback function globally
window.setPlaceholderFallback = setPlaceholderFallback;
