# Frontend Routing and Page Structure
# Basic routing implementation for the furniture web shop

class FrontendRouter:
    """Frontend routing service"""
    
    def __init__(self):
        self.routes = {
            '/': 'index.html',
            '/catalog': 'catalog.html',
            '/product': 'product.html',
            '/basket': 'basket.html',
            '/checkout': 'checkout.html',
            '/confirmation': 'confirmation.html'
        }
        
    def navigate(self, path: str) -> str:
        """Navigate to a specific route"""
        return self.routes.get(path, 'index.html')
        
    def get_all_routes(self) -> dict:
        """Get all available routes"""
        return self.routes

# Basic frontend layout
class FrontendLayout:
    """Frontend layout service"""
    
    def __init__(self):
        self.layout = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <link rel="stylesheet" href="/styles/main.css">
        </head>
        <body>
            <header>
                <h1>Designer Furniture Web Shop</h1>
                <nav>
                    <a href="/">Home</a>
                    <a href="/catalog.html">Catalog</a>
                    <a href="/basket.html">Basket</a>
                </nav>
            </header>
            
            <main>
                {content}
            </main>
            
            <footer>
                <p>&copy; 2025 Designer Furniture Web Shop. All rights reserved.</p>
            </footer>
            
            <script src="/ts/main.js" type="module"></script>
        </body>
        </html>
        """
        
    def render(self, title: str, content: str) -> str:
        """Render layout with content"""
        return self.layout.replace('{title}', title).replace('{content}', content)