# Frontend Project Structure with DDD Patterns
# Basic frontend structure for the furniture web shop

import os


def create_frontend_structure():
    """Create frontend project structure"""
    # Create directories
    directories = [
        "src/presentation/web/pages",
        "src/presentation/web/ts",
        "src/presentation/web/styles",
        "src/presentation/web/images",
        "src/presentation/web/components",
        "src/presentation/web/services",
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

    # Create basic HTML files
    pages = [
        "index.html",
        "catalog.html",
        "product.html",
        "basket.html",
        "checkout.html",
        "confirmation.html",
    ]

    for page in pages:
        page_path = f"src/presentation/web/pages/{page}"
        if not os.path.exists(page_path):
            with open(page_path, "w") as f:
                f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Designer Furniture Web Shop - {page.replace(".html", "").title()}</title>
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
        <h2>{page.replace(".html", "").title()} Page</h2>
        <p>Content for {page.replace(".html", "").title()} page will be added here.</p>
    </main>

    <footer>
        <p>&copy; 2025 Designer Furniture Web Shop. All rights reserved.</p>
    </footer>

    <script src="/ts/main.js" type="module"></script>
</body>
</html>""")
            print(f"✅ Created page: {page_path}")


if __name__ == "__main__":
    create_frontend_structure()
