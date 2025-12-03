// Global utility functions and shared JavaScript code

// Testing Framework - Controls element behavior based on fail.json
let testConfig = null;

// Load test configuration
async function loadTestConfig() {
    try {
        const response = await fetch('/data/fail.json');
        testConfig = await response.json();
        console.log('Test configuration loaded:', testConfig);
        applyTestConfig();
    } catch (error) {
        console.log('No test configuration found or error loading:', error);
    }
}

// Apply test configuration to elements
function applyTestConfig() {
    if (!testConfig) return;
    
    Object.keys(testConfig).forEach(elementType => {
        const config = testConfig[elementType];
        const elements = getElementsByType(elementType);
        
        elements.forEach(element => {
            // Handle visibility
            if (config.visible === "false") {
                element.style.display = 'none';
            } else if (config.visible === "true") {
                const delay = parseInt(config.visiabledelay) || 0;
                if (delay > 0) {
                    element.style.display = 'none';
                    setTimeout(() => {
                        element.style.display = '';
                    }, delay * 1000);
                } else {
                    element.style.display = '';
                }
            }
            
            // Handle clickability
            if (config.clickable === "false") {
                element.style.pointerEvents = 'none';
                element.style.opacity = '0.5';
                element.style.cursor = 'not-allowed';
                element.disabled = true;
            } else if (config.clickable === "true") {
                element.style.pointerEvents = 'auto';
                element.style.opacity = '1';
                element.style.cursor = 'pointer';
                element.disabled = false;
            }
        });
    });
}

// Get elements by type for testing
function getElementsByType(type) {
    const selectors = {
        'addtocart': [
            'button[onclick*="addToCart"]',
            '.btn[onclick*="addToCart"]',
            'button:contains("Add to Cart")',
            '.add-to-cart-btn'
        ],
        'cancelorder': [
            'button[onclick*="cancelOrder"]',
            'button[id*="btn-cancel-order"]',
            'button:contains("Cancel Order")'
        ],
        'checkout': [
            'button[onclick*="checkout"]',
            'button:contains("Checkout")',
            '.checkout-btn',
            '#checkout-btn'
        ],
        'login': [
            'button[onclick*="login"]',
            'button:contains("Login")',
            '.login-btn',
            '#login-btn'
        ],
        'register': [
            'button[onclick*="register"]',
            'button:contains("Register")',
            '.register-btn',
            '#register-btn'
        ],
        'search': [
            'button[onclick*="search"]',
            'button:contains("Search")',
            '.search-btn',
            '#search-btn'
        ],
        'wishlist': [
            'button[onclick*="wishlist"]',
            'button:contains("Wishlist")',
            '.wishlist-btn',
            '#wishlist-btn'
        ],
        'like': [
            'button[onclick*="toggleLike"]',
            'button:contains("Like")',
            '.like-btn',
            '#like-btn',
            'button[id*="btn-like"]'
        ]
    };
    
    const elements = [];
    const typeSelectors = selectors[type] || [];
    
    typeSelectors.forEach(selector => {
        try {
            const found = document.querySelectorAll(selector);
            found.forEach(el => elements.push(el));
        } catch (e) {
            // Handle complex selectors that might not work with querySelector
            if (selector.includes(':contains')) {
                const text = selector.match(/:contains\("([^"]+)"\)/);
                if (text) {
                    const allElements = document.querySelectorAll('button, a, input[type="button"]');
                    allElements.forEach(el => {
                        if (el.textContent.includes(text[1])) {
                            elements.push(el);
                        }
                    });
                }
            }
        }
    });
    
    return elements;
}

// Reapply test config when DOM changes
function reapplyTestConfig() {
    if (testConfig) {
        setTimeout(applyTestConfig, 100);
    }
}

// Initialize testing framework
document.addEventListener('DOMContentLoaded', function() {
    loadTestConfig();
    
    // Watch for DOM changes and reapply config
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                reapplyTestConfig();
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});

// Export testing functions
window.loadTestConfig = loadTestConfig;
window.applyTestConfig = applyTestConfig;
window.getElementsByType = getElementsByType;

// Check if user is authenticated
function checkAuth() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (!token || !user) {
        // Redirect to login if not authenticated
        if (window.location.pathname !== '/web/login' && 
            window.location.pathname !== '/web/register' && 
            window.location.pathname !== '/' &&
            !window.location.pathname.startsWith('/web/products')) {
            showAlert('Please login to continue', 'error');
            setTimeout(() => {
                window.location.href = '/web/login';
            }, 1500);
            return false;
        }
        return false;
    }
    return true;
}

// Update navigation based on auth status
function updateNavigation() {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    const userMenu = document.getElementById('user-menu');
    const guestMenu = document.getElementById('guest-menu');
    const adminMenu = document.getElementById('admin-menu');
    
    if (token && user.email) {
        // User is logged in
        if (userMenu) userMenu.style.display = 'block';
        if (guestMenu) guestMenu.style.display = 'none';
        
        // Show admin menu if user is admin
        if (user.is_admin && adminMenu) {
            adminMenu.style.display = 'block';
        }
    } else {
        // User is not logged in
        if (userMenu) userMenu.style.display = 'none';
        if (guestMenu) guestMenu.style.display = 'block';
        if (adminMenu) adminMenu.style.display = 'none';
    }
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('liked_products'); // Clear liked products on logout
    showAlert('Logged out successfully', 'success');
    setTimeout(() => {
        window.location.href = '/';
    }, 1000);
}

// Update cart count in navigation
async function updateCartCount() {
    const token = localStorage.getItem('token');
    
    if (!token) {
        const cartBadge = document.getElementById('cart-count');
        if (cartBadge) cartBadge.textContent = '0';
        return;
    }
    
    try {
        const response = await fetch('/api/cart', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            const cartBadge = document.getElementById('cart-count');
            if (cartBadge) {
                cartBadge.textContent = result.count || 0;
            }
        }
    } catch (error) {
        console.error('Error updating cart count:', error);
    }
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container');
    
    if (!alertContainer) {
        console.warn('Alert container not found');
        return;
    }
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.id = `alert-${Date.now()}`;
    alert.innerHTML = `
        <span class="alert-message">${message}</span>
        <button class="alert-close" onclick="closeAlert('${alert.id}')">&times;</button>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        closeAlert(alert.id);
    }, 5000);
}

// Close specific alert
function closeAlert(alertId) {
    const alert = document.getElementById(alertId);
    if (alert) {
        alert.style.opacity = '0';
        setTimeout(() => {
            alert.remove();
        }, 300);
    }
}

// Format currency
function formatCurrency(amount) {
    return `$${parseFloat(amount).toFixed(2)}`;
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    updateNavigation();
    updateCartCount();
    updateNotificationCount();
    
    // Logout button handler
    const logoutBtn = document.getElementById('btn-logout');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
    
    // Close modal when clicking outside
    window.onclick = function(event) {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    };
});

// API Helper Functions
const API = {
    baseURL: '/api',
    
    async request(endpoint, options = {}) {
        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                ...options,
                headers
            });
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    get(endpoint) {
        return this.request(endpoint);
    },
    
    post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    
    delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE'
        });
    }
};

// Form validation helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('error');
            isValid = false;
        } else {
            input.classList.remove('error');
        }
    });
    
    return isValid;
}

// Email validation
function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// Phone validation
function isValidPhone(phone) {
    const regex = /^[\d\s\-\+\(\)]+$/;
    return regex.test(phone);
}

// Loading spinner
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="spinner"></div>';
    }
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '';
    }
}

// Smooth scroll to element
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showAlert('Failed to copy', 'error');
    });
}

// Export functions for use in other scripts
window.checkAuth = checkAuth;
window.updateNavigation = updateNavigation;
window.logout = logout;
window.updateCartCount = updateCartCount;
window.showAlert = showAlert;
window.closeAlert = closeAlert;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;
window.debounce = debounce;
window.API = API;
window.validateForm = validateForm;
window.isValidEmail = isValidEmail;
window.isValidPhone = isValidPhone;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.scrollToElement = scrollToElement;
window.copyToClipboard = copyToClipboard;

// Update notification count in navigation
function updateNotificationCount() {
    const token = localStorage.getItem('token');
    if (!token) {
        const notificationCount = document.getElementById('notification-count');
        if (notificationCount) {
            notificationCount.textContent = '0';
            notificationCount.style.display = 'none';
        }
        return;
    }

    fetch('/api/notifications', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const notificationCount = document.getElementById('notification-count');
            if (notificationCount) {
                const unreadCount = data.data.filter(n => !n.is_read).length;
                notificationCount.textContent = unreadCount;
                notificationCount.style.display = unreadCount > 0 ? 'inline' : 'none';
            }
        }
    })
    .catch(error => {
        console.error('Error updating notification count:', error);
    });
}

// Add to wishlist function
async function addToWishlist(productId) {
    if (!checkAuth()) return;

    try {
        const response = await fetch('/api/wishlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                product_id: productId
            })
        });

        const data = await response.json();

        if (data.success) {
            showAlert('Item added to wishlist', 'success');
        } else {
            showAlert(data.error || 'Failed to add item to wishlist', 'error');
        }
    } catch (error) {
        console.error('Error adding to wishlist:', error);
        showAlert('Error adding item to wishlist', 'error');
    }
}

// Debounce mechanism to prevent rapid clicking
const likeDebounce = new Map();

// Track liked products in localStorage to prevent multiple likes
function getLikedProducts() {
    const liked = localStorage.getItem('liked_products');
    return liked ? JSON.parse(liked) : [];
}

function addLikedProduct(productId) {
    const liked = getLikedProducts();
    if (!liked.includes(productId)) {
        liked.push(productId);
        localStorage.setItem('liked_products', JSON.stringify(liked));
    }
}

function isProductLiked(productId) {
    const liked = getLikedProducts();
    return liked.includes(productId);
}

// Toggle like function - users can only like once
async function toggleLike(productId) {
    console.log('toggleLike called for product:', productId);
    
    if (!checkAuth()) {
        console.log('User not authenticated');
        return;
    }
    
    // Check if already liked in localStorage
    if (isProductLiked(productId)) {
        console.log('Product already liked in localStorage');
        showAlert('You have already liked this product!', 'info');
        updateLikeButton(productId, true);
        return;
    }
    
    // Debounce: prevent rapid clicking
    const now = Date.now();
    const lastClick = likeDebounce.get(productId) || 0;
    if (now - lastClick < 1000) { // 1 second cooldown
        console.log('Debounce triggered');
        showAlert('Please wait before liking again', 'info');
        return;
    }
    likeDebounce.set(productId, now);
    
    const token = localStorage.getItem('token');
    const likeButton = document.getElementById(`btn-like-${productId}`);
    
    // Prevent multiple rapid clicks
    if (likeButton && likeButton.disabled) {
        return;
    }
    
    // Check if already liked (multiple checks)
    if (likeButton && likeButton.classList.contains('liked')) {
        console.log('Button already marked as liked');
        showAlert('You have already liked this product!', 'info');
        return;
    }
    
    // Additional check: if button is disabled and has liked class
    if (likeButton && likeButton.disabled && likeButton.classList.contains('liked')) {
        console.log('Button is disabled and already liked');
        showAlert('You have already liked this product!', 'info');
        return;
    }
    
    // Check with server if user has already liked this product
    try {
        const checkResponse = await fetch(`/api/products/${productId}/likes/check`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const checkResult = await checkResponse.json();
        
        if (checkResult.success && checkResult.liked) {
            console.log('Server confirms user already liked this product');
            showAlert('You have already liked this product!', 'info');
            updateLikeButton(productId, true);
            return;
        }
    } catch (checkError) {
        console.log('Could not check like status, proceeding with like attempt');
    }
    
    // Disable button during request to prevent multiple clicks
    if (likeButton) {
        likeButton.disabled = true;
        likeButton.innerHTML = '⏳ Liking...';
    }
    
    try {
        const response = await fetch('/api/products/likes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ product_id: productId })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('Product liked! ❤️', 'success');
            updateLikeButton(productId, true);
            addLikedProduct(productId); // Add to localStorage
            console.log('Product added to liked list:', productId);
        } else {
            if (result.error && (result.error.includes('already liked') || result.already_liked)) {
                showAlert('You have already liked this product!', 'info');
                updateLikeButton(productId, true);
                addLikedProduct(productId); // Add to localStorage even if server says already liked
            } else {
                showAlert(result.error || 'Failed to like product', 'error');
                // Re-enable button if error
                if (likeButton) {
                    likeButton.disabled = false;
                    likeButton.innerHTML = '🤍 Like <span id="like-count-' + productId + '">0</span>';
                }
            }
        }
    } catch (error) {
        showAlert('Error liking product', 'error');
        // Re-enable button if error
        if (likeButton) {
            likeButton.disabled = false;
            likeButton.innerHTML = '🤍 Like <span id="like-count-' + productId + '">0</span>';
        }
    }
}

// Update like button appearance
function updateLikeButton(productId, isLiked) {
    const likeButton = document.getElementById(`btn-like-${productId}`);
    const likeCount = document.getElementById(`like-count-${productId}`);
    
    if (likeButton) {
        if (isLiked) {
            likeButton.classList.add('liked');
            likeButton.innerHTML = '❤️ Liked';
            likeButton.disabled = true;
        } else {
            likeButton.classList.remove('liked');
            likeButton.innerHTML = '🤍 Like';
            likeButton.disabled = false;
        }
    }
    
    if (likeCount) {
        const currentCount = parseInt(likeCount.textContent) || 0;
        likeCount.textContent = isLiked ? currentCount + 1 : Math.max(0, currentCount - 1);
    }
}

// Validate coupon code
async function validateCoupon(code, amount) {
    const token = localStorage.getItem('token');
    if (!token) return null;

    try {
        const response = await fetch('/api/coupons/validate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                code: code,
                amount: amount
            })
        });

        const data = await response.json();
        return data.success ? data.data : null;
    } catch (error) {
        console.error('Error validating coupon:', error);
        return null;
    }
}

// Test like button functionality
function testLikeButton(productId) {
    console.log('Testing like button for product:', productId);
    const button = document.getElementById(`btn-like-${productId}`);
    if (button) {
        console.log('Button found:', button);
        console.log('Button disabled:', button.disabled);
        console.log('Button classes:', button.className);
        console.log('Button style:', button.style.cssText);
        console.log('Button onclick:', button.onclick);
    } else {
        console.log('Button not found for product:', productId);
    }
}

// Force enable like buttons (for debugging)
function forceEnableLikeButtons() {
    const likeButtons = document.querySelectorAll('.like-btn');
    likeButtons.forEach(button => {
        button.disabled = false;
        button.style.pointerEvents = 'auto';
        button.style.cursor = 'pointer';
        button.style.opacity = '1';
        console.log('Force enabled button:', button.id);
    });
    console.log(`Force enabled ${likeButtons.length} like buttons`);
}

// Test like validation system
async function testLikeValidation(productId) {
    console.log('Testing like validation for product:', productId);
    
    const token = localStorage.getItem('token');
    if (!token) {
        console.log('No token found - user not authenticated');
        return;
    }
    
    try {
        // Check current like status
        const checkResponse = await fetch(`/api/products/${productId}/likes/check`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const checkResult = await checkResponse.json();
        console.log('Current like status:', checkResult);
        
        // Try to like the product
        const likeResponse = await fetch('/api/products/likes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ product_id: productId })
        });
        const likeResult = await likeResponse.json();
        console.log('Like attempt result:', likeResult);
        
        // Update button state based on result
        if (likeResult.success) {
            updateLikeButton(productId, true);
            console.log('✅ Like successful - button updated');
        } else if (likeResult.already_liked) {
            updateLikeButton(productId, true);
            console.log('⚠️ Already liked - button updated');
        } else {
            console.log('❌ Like failed:', likeResult.error);
        }
        
    } catch (error) {
        console.error('Error testing like validation:', error);
    }
}

// Reset like button state (for testing)
function resetLikeButton(productId) {
    const likeButton = document.getElementById(`btn-like-${productId}`);
    if (likeButton) {
        likeButton.classList.remove('liked');
        likeButton.disabled = false;
        likeButton.innerHTML = '🤍 Like <span id="like-count-' + productId + '">0</span>';
        likeButton.style.pointerEvents = 'auto';
        likeButton.style.cursor = 'pointer';
        likeButton.style.opacity = '1';
        console.log('Reset like button for product:', productId);
    }
}

// Clear all liked products from localStorage (for testing)
function clearLikedProducts() {
    localStorage.removeItem('liked_products');
    console.log('Cleared all liked products from localStorage');
    
    // Reset all like buttons
    const likeButtons = document.querySelectorAll('.like-btn');
    likeButtons.forEach(button => {
        const productId = button.id.replace('btn-like-', '');
        resetLikeButton(productId);
    });
}

// Show current liked products
function showLikedProducts() {
    const liked = getLikedProducts();
    console.log('Currently liked products:', liked);
    return liked;
}

// Export new functions
window.updateNotificationCount = updateNotificationCount;
window.addToWishlist = addToWishlist;
window.toggleLike = toggleLike;
window.updateLikeButton = updateLikeButton;
window.testLikeButton = testLikeButton;
window.forceEnableLikeButtons = forceEnableLikeButtons;
window.testLikeValidation = testLikeValidation;
window.resetLikeButton = resetLikeButton;
window.clearLikedProducts = clearLikedProducts;
window.showLikedProducts = showLikedProducts;
window.validateCoupon = validateCoupon;