// ShoeStore - Responsive JavaScript Enhancements

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Mobile menu improvements
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            const isClickInside = navbarCollapse.contains(event.target) || navbarToggler.contains(event.target);
            if (!isClickInside && navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });

        // Close mobile menu when clicking on a link
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992) {
                    navbarToggler.click();
                }
            });
        });
    }

    // Responsive product grid/list view toggle
    const gridViewBtn = document.getElementById('grid-view');
    const listViewBtn = document.getElementById('list-view');
    const productsGrid = document.getElementById('products-grid');

    if (gridViewBtn && listViewBtn && productsGrid) {
        gridViewBtn.addEventListener('click', function() {
            productsGrid.classList.remove('list-view');
            productsGrid.classList.add('grid-view');
            gridViewBtn.classList.add('active');
            listViewBtn.classList.remove('active');
            localStorage.setItem('viewMode', 'grid');
        });

        listViewBtn.addEventListener('click', function() {
            productsGrid.classList.remove('grid-view');
            productsGrid.classList.add('list-view');
            listViewBtn.classList.add('active');
            gridViewBtn.classList.remove('active');
            localStorage.setItem('viewMode', 'list');
        });

        // Load saved view mode
        const savedViewMode = localStorage.getItem('viewMode') || 'grid';
        if (savedViewMode === 'list') {
            listViewBtn.click();
        } else {
            gridViewBtn.click();
        }
    }

    // Responsive search functionality
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(this.value);
            }, 500);
        });

        // Mobile search improvements
        if (window.innerWidth < 768) {
            searchInput.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });

            searchInput.addEventListener('blur', function() {
                this.parentElement.classList.remove('focused');
            });
        }
    }

    // Touch-friendly product card interactions
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        // Add touch feedback
        card.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.98)';
        });

        card.addEventListener('touchend', function() {
            this.style.transform = '';
        });

        // Lazy loading for images
        const images = card.querySelectorAll('img');
        images.forEach(img => {
            if ('IntersectionObserver' in window) {
                const imageObserver = new IntersectionObserver((entries, observer) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            img.src = img.dataset.src || img.src;
                            img.classList.remove('lazy');
                            imageObserver.unobserve(img);
                        }
                    });
                });
                imageObserver.observe(img);
            }
        });
    });

    // Responsive filter improvements
    const filterSections = document.querySelectorAll('.filter-section');
    filterSections.forEach(section => {
        const header = section.querySelector('h5');
        const content = section.querySelector('.list-group, .gender-filter, form, .search-bar');
        
        if (header && content && window.innerWidth < 768) {
            // Make filter sections collapsible on mobile
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                content.style.display = content.style.display === 'none' ? 'block' : 'none';
                this.classList.toggle('collapsed');
            });
        }
    });

    // Responsive pagination improvements
    const pagination = document.querySelector('.pagination');
    if (pagination && window.innerWidth < 576) {
        // Simplify pagination on mobile
        const pageItems = pagination.querySelectorAll('.page-item');
        pageItems.forEach((item, index) => {
            if (index > 2 && index < pageItems.length - 2) {
                item.style.display = 'none';
            }
        });
    }

    // Newsletter form improvements
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            if (email) {
                // Show success message
                showNotification('Thank you for subscribing!', 'success');
                this.reset();
            }
        });
    }

    // Wishlist functionality
    const wishlistBtns = document.querySelectorAll('.wishlist-btn');
    wishlistBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const icon = this.querySelector('i');
            if (icon.classList.contains('far')) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                icon.style.color = '#dc3545';
                showNotification('Added to wishlist!', 'success');
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                icon.style.color = '';
                showNotification('Removed from wishlist!', 'info');
            }
        });
    });

    // Responsive image gallery
    const categoryImages = document.querySelectorAll('.category-images-gallery img, .category-images-carousel img');
    categoryImages.forEach(img => {
        img.addEventListener('click', function() {
            openImageModal(this.src, this.alt);
        });
    });

    // Mobile-specific enhancements
    if (window.innerWidth < 768) {
        // Add pull-to-refresh functionality
        let startY = 0;
        let currentY = 0;
        let pullDistance = 0;
        const pullThreshold = 100;

        document.addEventListener('touchstart', function(e) {
            startY = e.touches[0].pageY;
        });

        document.addEventListener('touchmove', function(e) {
            currentY = e.touches[0].pageY;
            pullDistance = currentY - startY;
            
            if (pullDistance > 0 && window.scrollY === 0) {
                e.preventDefault();
                document.body.style.transform = `translateY(${Math.min(pullDistance * 0.3, pullThreshold)}px)`;
            }
        });

        document.addEventListener('touchend', function() {
            if (pullDistance > pullThreshold) {
                // Trigger refresh
                location.reload();
            }
            document.body.style.transform = '';
            pullDistance = 0;
        });

        // Improve mobile scrolling
        const scrollableElements = document.querySelectorAll('.container, .card-body');
        scrollableElements.forEach(element => {
            element.style.webkitOverflowScrolling = 'touch';
        });
    }

    // Performance optimizations
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            handleResize();
        }, 250);
    });

    // Accessibility improvements
    document.addEventListener('keydown', function(e) {
        // Escape key to close modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });
        }
    });

    // Initialize responsive features
    handleResize();
});

// Utility functions
function performSearch(query) {
    // Implement search functionality
    console.log('Searching for:', query);
    // You can implement AJAX search here
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

function openImageModal(src, alt) {
    // Create modal for image viewing
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${alt}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body text-center">
                    <img src="${src}" class="img-fluid" alt="${alt}">
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();
    
    modal.addEventListener('hidden.bs.modal', function() {
        modal.remove();
    });
}

function handleResize() {
    const isMobile = window.innerWidth < 768;
    const isTablet = window.innerWidth >= 768 && window.innerWidth < 992;
    const isDesktop = window.innerWidth >= 992;

    // Adjust layout based on screen size
    if (isMobile) {
        document.body.classList.add('mobile-view');
        document.body.classList.remove('tablet-view', 'desktop-view');
    } else if (isTablet) {
        document.body.classList.add('tablet-view');
        document.body.classList.remove('mobile-view', 'desktop-view');
    } else {
        document.body.classList.add('desktop-view');
        document.body.classList.remove('mobile-view', 'tablet-view');
    }

    // Adjust product grid columns
    const productsGrid = document.getElementById('products-grid');
    if (productsGrid) {
        if (isMobile) {
            productsGrid.style.gridTemplateColumns = 'repeat(1, 1fr)';
        } else if (isTablet) {
            productsGrid.style.gridTemplateColumns = 'repeat(2, 1fr)';
        } else {
            productsGrid.style.gridTemplateColumns = 'repeat(3, 1fr)';
        }
    }
}

// Add CSS for responsive enhancements
const responsiveCSS = `
    .mobile-view .product-card {
        margin-bottom: 1rem;
    }
    
    .mobile-view .filter-section {
        margin-bottom: 1rem;
    }
    
    .mobile-view .navbar-nav .nav-link {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .mobile-view .search-bar.focused {
        transform: scale(1.02);
        transition: transform 0.2s ease;
    }
    
    .tablet-view .product-card {
        margin-bottom: 1.5rem;
    }
    
    .desktop-view .product-card:hover {
        transform: translateY(-5px);
    }
    
    @media (max-width: 575.98px) {
        .container {
            padding-left: 10px;
            padding-right: 10px;
        }
        
        .btn {
            min-height: 44px;
        }
        
        .product-card .card-body {
            padding: 1rem;
        }
    }
`;

// Inject responsive CSS
const style = document.createElement('style');
style.textContent = responsiveCSS;
document.head.appendChild(style); 