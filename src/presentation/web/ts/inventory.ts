"""Real-time inventory display functionality."""

import { ProductSearch } from './search';

class InventoryDisplay {
    private searchService: ProductSearch;
    private productId: string;
    private inventoryElement: HTMLElement;
    private deliveryElement: HTMLElement;

    constructor(productId: string) {
        this.searchService = new ProductSearch();
        this.productId = productId;
        
        // Find elements in the DOM
        this.inventoryElement = document.getElementById('inventory-status') || document.createElement('div');
        this.deliveryElement = document.getElementById('delivery-estimate') || document.createElement('div');
        
        // Initialize inventory display
        this.initialize();
    }

    private initialize(): void {
        this.loadInventoryData();
        
        // Set up periodic updates (every 30 seconds)
        setInterval(() => {
            this.loadInventoryData();
        }, 30000);
    }

    private async loadInventoryData(): void {
        try {
            // Get inventory status
            const inventory = await this.searchService.getInventoryStatus(this.productId);
            
            // Get delivery estimate
            const deliveryEstimate = await this.searchService.getDeliveryEstimate(this.productId);

            // Update inventory display
            if (inventory) {
                this.updateInventoryDisplay(inventory);
            } else {
                this.inventoryElement.innerHTML = '<span class="out-of-stock">Inventory information unavailable</span>';
            }

            // Update delivery estimate display
            this.deliveryElement.textContent = deliveryEstimate || 'Delivery estimate unavailable';

        } catch (error) {
            console.error('Error loading inventory data:', error);
            this.inventoryElement.innerHTML = '<span class="error">Error loading inventory</span>';
            this.deliveryElement.textContent = 'Delivery estimate unavailable';
        }
    }

    private updateInventoryDisplay(inventory: {available_quantity: number, status: string}): void {
        const statusClass = this.getStatusClass(inventory.status);
        const statusText = this.getStatusText(inventory);
        
        this.inventoryElement.innerHTML = `
            <span class="inventory-status ${statusClass}">
                ${statusText}
            </span>
        `;
    }

    private getStatusClass(status: string): string {
        switch (status) {
            case 'in_stock': return 'in-stock';
            case 'pre_order': return 'pre-order';
            default: return 'out-of-stock';
        }
    }

    private getStatusText(inventory: {available_quantity: number, status: string}): string {
        switch (inventory.status) {
            case 'in_stock':
                return inventory.available_quantity === 1
                    ? '1 item in stock'
                    : `${inventory.available_quantity} items in stock`;
            case 'pre_order':
                return 'Available for pre-order';
            default:
                return 'Out of stock';
        }
    }
}

// Export for use in product detail pages
export { InventoryDisplay };
