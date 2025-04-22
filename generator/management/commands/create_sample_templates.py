from django.core.management.base import BaseCommand
from generator.models import WebsiteTemplate

class Command(BaseCommand):
    help = 'Creates sample website templates'

    def handle(self, *args, **kwargs):
        # Blog Template
        blog_template = WebsiteTemplate.objects.create(
            name='Modern Blog',
            description='A clean and modern blog template with a focus on readability and content presentation.',
            template_type='blog',
            html_structure='''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ blog_title }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light">
        <div class="container">
            <a class="navbar-brand" href="#">{{ blog_title }}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="#home">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="#about">About</a></li>
                    <li class="nav-item"><a class="nav-link" href="#blog">Blog</a></li>
                    <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <header class="hero">
        <div class="container">
            <h1>{{ blog_title }}</h1>
            <p>{{ blog_description }}</p>
        </div>
    </header>

    <main class="container my-5">
        <div class="row">
            <div class="col-lg-8">
                <!-- Blog posts will go here -->
            </div>
            <div class="col-lg-4">
                <!-- Sidebar will go here -->
            </div>
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 {{ blog_title }}. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
            ''',
            css_structure='''
body {
    font-family: 'Segoe UI', sans-serif;
    line-height: 1.6;
}

.navbar {
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.hero {
    background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
    color: white;
    padding: 100px 0;
    text-align: center;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.footer {
    background: #f8f9fa;
    padding: 20px 0;
    text-align: center;
    margin-top: 50px;
}
            ''',
            features={
                'responsive': True,
                'customizable_colors': True,
                'blog_features': ['categories', 'tags', 'comments'],
                'seo_optimized': True
            }
        )
        self.stdout.write(self.style.SUCCESS('Created Blog template'))

        # Portfolio Template
        portfolio_template = WebsiteTemplate.objects.create(
            name='Creative Portfolio',
            description='A stunning portfolio template for creative professionals and artists.',
            template_type='portfolio',
            html_structure='''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ portfolio_name }} - Portfolio</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="#">{{ portfolio_name }}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="#work">Work</a></li>
                    <li class="nav-item"><a class="nav-link" href="#about">About</a></li>
                    <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <header class="hero">
        <div class="container">
            <h1>{{ portfolio_name }}</h1>
            <p>{{ portfolio_tagline }}</p>
        </div>
    </header>

    <main class="container my-5">
        <section id="work" class="portfolio-grid">
            <!-- Portfolio items will go here -->
        </section>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 {{ portfolio_name }}. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
            ''',
            css_structure='''
body {
    font-family: 'Segoe UI', sans-serif;
    background: #f8f9fa;
}

.navbar {
    background: #000;
    padding: 20px 0;
}

.hero {
    background: #000;
    color: white;
    padding: 150px 0;
    text-align: center;
}

.hero h1 {
    font-size: 4rem;
    font-weight: bold;
    margin-bottom: 1rem;
}

.portfolio-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 30px;
    padding: 50px 0;
}

.footer {
    background: #000;
    color: white;
    padding: 30px 0;
    text-align: center;
}
            ''',
            features={
                'responsive': True,
                'gallery_layout': True,
                'project_showcase': True,
                'contact_form': True
            }
        )
        self.stdout.write(self.style.SUCCESS('Created Portfolio template'))

        # Business Template
        business_template = WebsiteTemplate.objects.create(
            name='Professional Business',
            description='A professional template for businesses and corporate websites.',
            template_type='business',
            html_structure='''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ business_name }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light">
        <div class="container">
            <a class="navbar-brand" href="#">{{ business_name }}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="#services">Services</a></li>
                    <li class="nav-item"><a class="nav-link" href="#about">About</a></li>
                    <li class="nav-item"><a class="nav-link" href="#team">Team</a></li>
                    <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <header class="hero">
        <div class="container">
            <h1>{{ business_name }}</h1>
            <p>{{ business_tagline }}</p>
            <a href="#contact" class="btn btn-primary btn-lg">Get Started</a>
        </div>
    </header>

    <main>
        <section id="services" class="py-5">
            <div class="container">
                <!-- Services will go here -->
            </div>
        </section>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 {{ business_name }}. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
            ''',
            css_structure='''
body {
    font-family: 'Segoe UI', sans-serif;
}

.navbar {
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.hero {
    background: linear-gradient(135deg, #0061ff 0%, #60efff 100%);
    color: white;
    padding: 120px 0;
    text-align: center;
}

.hero h1 {
    font-size: 3.5rem;
    margin-bottom: 1rem;
}

.btn-primary {
    background: #0061ff;
    border: none;
    padding: 12px 30px;
}

.footer {
    background: #f8f9fa;
    padding: 30px 0;
    text-align: center;
}
            ''',
            features={
                'responsive': True,
                'service_showcase': True,
                'team_section': True,
                'contact_form': True
            }
        )
        self.stdout.write(self.style.SUCCESS('Created Business template'))

        # E-commerce Template
        ecommerce_template = WebsiteTemplate.objects.create(
            name='Modern E-commerce',
            description='A feature-rich e-commerce template for online stores.',
            template_type='ecommerce',
            html_structure='''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ store_name }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light">
        <div class="container">
            <a class="navbar-brand" href="#">{{ store_name }}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item"><a class="nav-link" href="#shop">Shop</a></li>
                    <li class="nav-item"><a class="nav-link" href="#categories">Categories</a></li>
                    <li class="nav-item"><a class="nav-link" href="#deals">Deals</a></li>
                </ul>
                <ul class="navbar-nav">
                    <li class="nav-item"><a class="nav-link" href="#cart">Cart (0)</a></li>
                    <li class="nav-item"><a class="nav-link" href="#account">Account</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <header class="hero">
        <div class="container">
            <h1>Welcome to {{ store_name }}</h1>
            <p>{{ store_tagline }}</p>
            <a href="#shop" class="btn btn-primary btn-lg">Shop Now</a>
        </div>
    </header>

    <main class="container my-5">
        <section id="featured" class="product-grid">
            <!-- Products will go here -->
        </section>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 {{ store_name }}. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
            ''',
            css_structure='''
body {
    font-family: 'Segoe UI', sans-serif;
}

.navbar {
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.hero {
    background: linear-gradient(135deg, #ff6b6b 0%, #ff9f43 100%);
    color: white;
    padding: 100px 0;
    text-align: center;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 30px;
    padding: 50px 0;
}

.footer {
    background: #f8f9fa;
    padding: 30px 0;
    text-align: center;
}
            ''',
            features={
                'responsive': True,
                'shopping_cart': True,
                'product_catalog': True,
                'secure_checkout': True
            }
        )
        self.stdout.write(self.style.SUCCESS('Created E-commerce template')) 