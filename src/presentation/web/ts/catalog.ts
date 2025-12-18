"""Product catalog display functionality."""

import { ProductSearch } from './search';

interface ProductCardData {
    id: string;
    name: string;
    price: number;
    thumbnail: string;
    availability: string;
    availableQuantity?: number;
    deliveryEstimate?: string;
}

class ProductCatalog {
    private searchService: ProductSearch;
    private productsContainer: HTMLElement;

    constructor() {
        this.searchService = new ProductSearch();
        this.productsContainer = document.getElementById('products-grid') || document.body;
        
        // Initialize the catalog
        this.initialize();
    }

    private initialize(): void {
        // Load all products initially
        this.loadProducts();
        
        // Set up event listeners
        this.setupEventListeners();
    }

    private setupEventListeners(): void {
        const searchButton = document.getElementById('search-button');
        const searchInput = document.getElementById('search-input') as HTMLInputElement;
        const categoryFilter = document.getElementById('category-filter') as HTMLSelectElement;

        searchButton?.addEventListener('click', () => {
            this.handleSearch();
        });

        searchInput?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.handleSearch();
            }
        });

        categoryFilter?.addEventListener('change', () => {
            this.handleSearch();
        });
    }

    private handleSearch(): void {
        const searchInput = document.getElementById('search-input') as HTMLInputElement;
        const categoryFilter = document.getElementById('category-filter') as HTMLSelectElement;

        const searchTerm = searchInput?.value || '';
        const category = categoryFilter?.value || '';

        this.loadProducts(searchTerm, category);
    }

    private async loadProducts(searchTerm: string = '', category: string = ''): void {
        try {
            // Show loading state
            this.productsContainer.innerHTML = '<div class="loading">Loading products...</div>';

            // Fetch products
            const products = await this.searchService.searchProducts(searchTerm, category || undefined);

            if (products.length === 0) {
                this.productsContainer.innerHTML = '<div class="no-results">No products found.</div>';
                return;
            }

            // Create product cards
            const productCards = await Promise.all(
                products.map(async (product) => {
                    const inventory = await this.searchService.getInventoryStatus(product.id);
                    const deliveryEstimate = await this.searchService.getDeliveryEstimate(product.id);

                    return this.createProductCard({
                        id: product.id,
                        name: product.name,
                        price: product.price,
                        thumbnail: product.thumbnail || 'https://via.placeholder.com/300',
                        availability: inventory?.status || 'out_of_stock',
                        availableQuantity: inventory?.available_quantity,
                        deliveryEstimate: deliveryEstimate
                    });
                })
            );

            // Display product cards
            this.productsContainer.innerHTML = '';
            productCards.forEach(card => {
                this.productsContainer.appendChild(card);
            });

        } catch (error) {
            console.error('Error loading products:', error);
            this.productsContainer.innerHTML = '<div class="error">Error loading products. Please try again.</div>';
        }
    }

    private createProductCard(product: ProductCardData): HTMLElement {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.dataset.productId = product.id;

        const availabilityClass = this.getAvailabilityClass(product.availability);

        card.innerHTML = `
            <div class="product-image">
                <img src="${product.thumbnail}" alt="${product.name}">
            </div>
            <div class="product-info">
                <h3>${product.name}</h3>
                <p class="price">$${product.price.toFixed(2)}</p>
                <p class="availability ${availabilityClass}">
                    ${this.getAvailabilityText(product)}
                </p>
                ${product.deliveryEstimate ? `
                    <p class="delivery-estimate">Delivery: ${product.deliveryEstimate}</p>
                ` : ''}
                <button class="view-details" data-product-id="${product.id}">View Details</button>
            </div>
        `;

        // Add click handler for view details button
        const viewDetailsButton = card.querySelector('.view-details');
        if (viewDetailsButton) {
            viewDetailsButton.addEventListener('click', () => {
                window.location.href = `/product.html?id=${product.id}`;
            });
        }

        return card;
    }

    private getAvailabilityClass(availability: string): string {
        switch (availability) {
            case 'in_stock': return 'in-stock';
            case 'pre_order': return 'pre-order';
            default: return 'out-of-stock';
        }
    }

    private getAvailabilityText(product: ProductCardData): string {
        switch (product.availability) {
            case 'in_stock':
                return product.availableQuantity !== undefined 
                    ? `${product.availableQuantity} in stock` 
                    : 'In stock';
            case 'pre_order':
                return 'Available for pre-order';
            default:
                return 'Out of stock';
        }
    }
}

// Initialize the catalog when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ProductCatalog();
});
