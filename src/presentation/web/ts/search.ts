"""Product search functionality."""

interface Product {
    id: string;
    name: string;
    description: string;
    price: number;
    category: string;
    thumbnail: string;
    availability: string;
}

class ProductSearch {
    private apiBaseUrl: string;

    constructor(apiBaseUrl: string = "http://localhost:8000/api/v1") {
        this.apiBaseUrl = apiBaseUrl;
    }

    async searchProducts(searchTerm: string, category?: string): Promise<Product[]> {
        let url = `${this.apiBaseUrl}/catalog/products?`;
        const params = new URLSearchParams();
        
        if (searchTerm) {
            params.append('search', searchTerm);
        }
        
        if (category) {
            params.append('category', category);
        }
        
        url += params.toString();

        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Error searching products:", error);
            return [];
        }
    }

    async getProductById(productId: string): Promise<Product | null> {
        try {
            const response = await fetch(`${this.apiBaseUrl}/catalog/products/${productId}`);
            if (!response.ok) {
                if (response.status === 404) {
                    return null;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Error fetching product:", error);
            return null;
        }
    }

    async getInventoryStatus(productId: string): Promise<{available_quantity: number, status: string} | null> {
        try {
            const response = await fetch(`${this.apiBaseUrl}/inventory/${productId}`);
            if (!response.ok) {
                if (response.status === 404) {
                    return null;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const inventory = await response.json();
            return {
                available_quantity: inventory.available_quantity,
                status: inventory.status
            };
        } catch (error) {
            console.error("Error fetching inventory:", error);
            return null;
        }
    }

    async getDeliveryEstimate(productId: string): Promise<string> {
        try {
            const response = await fetch(`${this.apiBaseUrl}/inventory/${productId}/delivery-estimate`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data.delivery_estimate;
        } catch (error) {
            console.error("Error fetching delivery estimate:", error);
            return "Delivery estimate unavailable";
        }
    }
}

// Export for use in other modules
export { ProductSearch };
