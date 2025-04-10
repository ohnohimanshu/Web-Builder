"""
Template engine for rendering websites with dynamic content, enhanced styling, and animations.
"""
import json
import re
from django.utils.safestring import mark_safe
from django.utils.html import escape


def render_website(website, is_public=False):
    """
    Render a website based on its content and template.

    Args:
        website: The Website model instance
        is_public: Whether this is a public shared preview

    Returns:
        str: The rendered HTML content
    """
    content = website.content

    # If there's a template, use it, otherwise use a basic template
    if website.template and website.template.template_path:
        # In a real implementation, this would load the template file
        # For now, we'll use an enhanced template
        html = render_enhanced_template(content)
    else:
        html = render_enhanced_template(content)

    # Add preview controls if not a public preview
    if not is_public:
        html = add_preview_controls(html, website)

    return html


def render_enhanced_template(content):
    """
    Render website content using an enhanced HTML template with modern styling and animations.

    Args:
        content: The website content dictionary

    Returns:
        str: The rendered HTML content
    """
    # Enhanced HTML boilerplate with modern styling and animations
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{escape(content.get('title', 'Website Preview'))}</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.9.1/gsap.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.9.1/ScrollTrigger.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

            :root {{
                --primary-color: {content.get('theme', {}).get('primary_color', '#6366f1')};
                --secondary-color: {content.get('theme', {}).get('secondary_color', '#4f46e5')};
                --accent-color: {content.get('theme', {}).get('accent_color', '#8b5cf6')};
                --text-color: {content.get('theme', {}).get('text_color', '#334155')};
                --light-bg: {content.get('theme', {}).get('light_bg', '#f1f5f9')};
                --dark-bg: {content.get('theme', {}).get('dark_bg', '#1e293b')};
            }}

            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: 'Poppins', sans-serif;
                line-height: 1.7;
                color: var(--text-color);
                background-color: #fff;
                overflow-x: hidden;
            }}

            .container {{
                max-width: 1280px;
                margin: 0 auto;
                padding: 0 2rem;
                position: relative;
            }}

            header {{
                background-color: var(--dark-bg);
                background-image: linear-gradient(135deg, var(--dark-bg) 0%, var(--secondary-color) 100%);
                color: white;
                padding: 1.5rem 0;
                position: fixed;
                width: 100%;
                top: 0;
                z-index: 1000;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }}

            header.scrolled {{
                padding: 0.8rem 0;
                background-color: rgba(30, 41, 59, 0.95);
                backdrop-filter: blur(10px);
            }}

            nav {{
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}

            .logo {{
                font-size: 1.8rem;
                font-weight: 700;
                background: linear-gradient(to right, #fff, var(--accent-color));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                position: relative;
                overflow: hidden;
            }}

            .nav-links {{
                display: flex;
                gap: 2rem;
                align-items: center;
            }}

            .nav-links a {{
                color: white;
                text-decoration: none;
                font-weight: 500;
                transition: all 0.3s ease;
                position: relative;
            }}

            .nav-links a:after {{
                content: '';
                position: absolute;
                width: 0;
                height: 2px;
                bottom: -5px;
                left: 0;
                background-color: white;
                transition: width 0.3s ease;
            }}

            .nav-links a:hover:after {{
                width: 100%;
            }}

            .mobile-menu-btn {{
                display: none;
                background: none;
                border: none;
                color: white;
                font-size: 1.5rem;
                cursor: pointer;
            }}

            section {{
                padding: 6rem 0;
                overflow: hidden;
            }}

            section h2 {{
                font-size: 2.5rem;
                margin-bottom: 1.5rem;
                position: relative;
                display: inline-block;
            }}

            section h2:after {{
                content: '';
                position: absolute;
                bottom: -10px;
                left: 0;
                width: 80px;
                height: 4px;
                background: var(--primary-color);
                border-radius: 2px;
            }}

            section p.subtitle {{
                font-size: 1.2rem;
                margin-bottom: 3rem;
                color: var(--secondary-color);
                opacity: 0.8;
            }}

            .hero {{
                height: 100vh;
                display: flex;
                align-items: center;
                background-color: var(--light-bg);
                position: relative;
                overflow: hidden;
            }}

            .hero::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: 
                    radial-gradient(circle at 20% 30%, rgba(99, 102, 241, 0.15) 0%, transparent 30%),
                    radial-gradient(circle at 80% 70%, rgba(139, 92, 246, 0.15) 0%, transparent 30%);
                z-index: 0;
            }}

            .hero-content {{
                position: relative;
                z-index: 1;
                max-width: 650px;
            }}

            .hero h1 {{
                font-size: 4rem;
                font-weight: 700;
                line-height: 1.2;
                margin-bottom: 1.5rem;
                background: linear-gradient(to right, var(--primary-color), var(--accent-color));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}

            .hero p {{
                font-size: 1.5rem;
                margin-bottom: 2.5rem;
                color: var(--text-color);
            }}

            .btn {{
                display: inline-block;
                text-decoration: none;
                padding: 1rem 2.5rem;
                border-radius: 50px;
                font-weight: 600;
                font-size: 1rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
                z-index: 1;
            }}

            .btn-primary {{
                background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
                color: white;
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
            }}

            .btn-primary:hover {{
                transform: translateY(-3px);
                box-shadow: 0 10px 20px rgba(99, 102, 241, 0.4);
            }}

            .btn-primary::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
                z-index: -1;
                transition: opacity 0.3s ease;
                opacity: 0;
            }}

            .btn-primary:hover::before {{
                opacity: 1;
            }}

            .features {{
                background-color: white;
                position: relative;
            }}

            .features::before {{
                content: '';
                position: absolute;
                width: 300px;
                height: 300px;
                border-radius: 50%;
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
                top: -100px;
                right: -100px;
                z-index: 0;
            }}

            .feature-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                gap: 3rem;
                position: relative;
                z-index: 1;
            }}

            .feature-item {{
                background-color: white;
                padding: 2.5rem;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
                transition: all 0.3s ease;
                position: relative;
                z-index: 1;
                overflow: hidden;
            }}

            .feature-item::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
                z-index: -1;
                opacity: 0;
                transition: opacity 0.3s ease;
            }}

            .feature-item:hover {{
                transform: translateY(-10px);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            }}

            .feature-item:hover::before {{
                opacity: 0.05;
            }}

            .feature-item .feature-icon {{
                font-size: 2.5rem;
                margin-bottom: 1.5rem;
                color: var(--primary-color);
                background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}

            .feature-item h3 {{
                font-size: 1.5rem;
                margin-bottom: 1rem;
                position: relative;
                display: inline-block;
            }}

            .feature-item p {{
                color: #64748b;
            }}

            .about {{
                background-color: var(--light-bg);
                position: relative;
                overflow: hidden;
            }}

            .about-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 4rem;
                align-items: center;
            }}

            .about-content h2 {{
                margin-bottom: 2rem;
            }}

            .about-content p {{
                margin-bottom: 1.5rem;
                color: #64748b;
            }}

            .about-image {{
                position: relative;
                z-index: 1;
                height: 400px;
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            }}

            .about-image::before {{
                content: '';
                position: absolute;
                width: 100%;
                height: 100%;
                background-color: var(--dark-bg);
                opacity: 0.1;
                z-index: 1;
            }}

            .about-image img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
            }}

            .services {{
                background-color: white;
                position: relative;
            }}

            .services::after {{
                content: '';
                position: absolute;
                width: 300px;
                height: 300px;
                border-radius: 50%;
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
                bottom: -150px;
                left: -150px;
                z-index: 0;
            }}

            .service-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                gap: 3rem;
                position: relative;
                z-index: 1;
            }}

            .service-item {{
                position: relative;
                overflow: hidden;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
                transition: all 0.3s ease;
            }}

            .service-item:hover {{
                transform: translateY(-10px);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            }}

            .service-image {{
                height: 200px;
                overflow: hidden;
            }}

            .service-image img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                transition: transform 0.5s ease;
            }}

            .service-item:hover .service-image img {{
                transform: scale(1.1);
            }}

            .service-content {{
                padding: 2rem;
                background-color: white;
            }}

            .service-content h3 {{
                font-size: 1.5rem;
                margin-bottom: 1rem;
                color: var(--text-color);
            }}

            .service-content p {{
                color: #64748b;
                margin-bottom: 1.5rem;
            }}

            .service-link {{
                display: inline-flex;
                align-items: center;
                color: var(--primary-color);
                font-weight: 600;
                text-decoration: none;
                transition: all 0.3s ease;
            }}

            .service-link i {{
                margin-left: 0.5rem;
                transition: transform 0.3s ease;
            }}

            .service-link:hover {{
                color: var(--secondary-color);
            }}

            .service-link:hover i {{
                transform: translateX(5px);
            }}

            .testimonials {{
                background-color: var(--light-bg);
                position: relative;
                overflow: hidden;
            }}

            .testimonial-slider {{
                position: relative;
                overflow: hidden;
                padding: 2rem 0;
            }}

            .testimonial-item {{
                background-color: white;
                padding: 2.5rem;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
                transition: all 0.3s ease;
                margin-bottom: 2rem;
            }}

            .testimonial-text {{
                margin-bottom: 1.5rem;
                font-style: italic;
                color: #64748b;
                position: relative;
            }}

            .testimonial-text::before {{
                content: '"';
                font-size: 4rem;
                color: var(--primary-color);
                opacity: 0.1;
                position: absolute;
                top: -30px;
                left: -10px;
            }}

            .testimonial-author {{
                display: flex;
                align-items: center;
            }}

            .testimonial-avatar {{
                width: 60px;
                height: 60px;
                border-radius: 50%;
                overflow: hidden;
                margin-right: 1rem;
            }}

            .testimonial-avatar img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
            }}

            .testimonial-info h4 {{
                margin-bottom: 0.25rem;
                color: var(--text-color);
            }}

            .testimonial-info p {{
                color: #64748b;
                font-size: 0.875rem;
            }}

            .contact {{
                background-color: white;
                position: relative;
            }}

            .contact-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 4rem;
            }}

            .contact-info h3 {{
                margin-bottom: 1.5rem;
                color: var(--text-color);
            }}

            .contact-info p {{
                color: #64748b;
                margin-bottom: 1rem;
            }}

            .contact-info-item {{
                display: flex;
                align-items: center;
                margin-bottom: 1.5rem;
            }}

            .contact-icon {{
                width: 40px;
                height: 40px;
                background: var(--primary-color);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 1rem;
                color: white;
                font-size: 1rem;
            }}

            .contact-form {{
                background-color: white;
                padding: 2.5rem;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
            }}

            .form-group {{
                margin-bottom: 1.5rem;
            }}

            .form-control {{
                width: 100%;
                padding: 1rem;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                font-family: 'Poppins', sans-serif;
                transition: all 0.3s ease;
            }}

            .form-control:focus {{
                outline: none;
                border-color: var(--primary-color);
                box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
            }}

            .form-submit {{
                width: 100%;
                padding: 1rem;
                background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            }}

            .form-submit:hover {{
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
            }}

            footer {{
                background-color: var(--dark-bg);
                color: white;
                padding: 4rem 0 2rem;
            }}

            .footer-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 3rem;
                margin-bottom: 3rem;
            }}

            .footer-logo {{
                font-size: 1.5rem;
                font-weight: 700;
                margin-bottom: 1rem;
                background: linear-gradient(to right, #fff, var(--accent-color));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}

            .footer-about p {{
                color: #94a3b8;
                margin-bottom: 1.5rem;
            }}

            .social-links {{
                display: flex;
                gap: 1rem;
            }}

            .social-link {{
                width: 40px;
                height: 40px;
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                text-decoration: none;
                transition: all 0.3s ease;
            }}

            .social-link:hover {{
                background-color: var(--primary-color);
                transform: translateY(-3px);
            }}

            .footer-heading {{
                font-size: 1.2rem;
                margin-bottom: 1.5rem;
                position: relative;
                display: inline-block;
            }}

            .footer-heading::after {{
                content: '';
                position: absolute;
                bottom: -10px;
                left: 0;
                width: 40px;
                height: 2px;
                background: var(--primary-color);
            }}

            .footer-links {{
                list-style: none;
            }}

            .footer-links li {{
                margin-bottom: 0.75rem;
            }}

            .footer-links a {{
                color: #94a3b8;
                text-decoration: none;
                transition: all 0.3s ease;
                display: inline-flex;
                align-items: center;
            }}

            .footer-links a i {{
                margin-right: 0.5rem;
                font-size: 0.75rem;
                color: var(--primary-color);
            }}

            .footer-links a:hover {{
                color: white;
            }}

            .copyright {{
                text-align: center;
                padding-top: 2rem;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                color: #94a3b8;
            }}

            /* Animation Classes */
            .fade-in {{
                opacity: 0;
                transform: translateY(20px);
                transition: opacity 0.6s ease, transform 0.6s ease;
            }}

            .fade-in.active {{
                opacity: 1;
                transform: translateY(0);
            }}

            .slide-in-left {{
                opacity: 0;
                transform: translateX(-50px);
                transition: opacity 0.6s ease, transform 0.6s ease;
            }}

            .slide-in-right {{
                opacity: 0;
                transform: translateX(50px);
                transition: opacity 0.6s ease, transform 0.6s ease;
            }}

            .slide-in-left.active, .slide-in-right.active {{
                opacity: 1;
                transform: translateX(0);
            }}

            .scale-in {{
                opacity: 0;
                transform: scale(0.9);
                transition: opacity 0.6s ease, transform 0.6s ease;
            }}

            .scale-in.active {{
                opacity: 1;
                transform: scale(1);
            }}

            /* Responsive Design */
            @media (max-width: 992px) {{
                .container {{
                    padding: 0 1.5rem;
                }}

                .hero h1 {{
                    font-size: 3rem;
                }}

                .hero p {{
                    font-size: 1.2rem;
                }}

                .about-grid {{
                    grid-template-columns: 1fr;
                }}

                .about-image {{
                    height: 300px;
                    order: -1;
                }}
            }}

            @media (max-width: 768px) {{
                .nav-links {{
                    display: none;
                    position: absolute;
                    top: 100%;
                    left: 0;
                    width: 100%;
                    background-color: var(--dark-bg);
                    padding: 1rem 0;
                    flex-direction: column;
                    gap: 0;
                }}

                .nav-links.active {{
                    display: flex;
                }}

                .nav-links a {{
                    display: block;
                    padding: 0.75rem 2rem;
                }}

                .nav-links a:after {{
                    display: none;
                }}

                .mobile-menu-btn {{
                    display: block;
                }}

                .hero h1 {{
                    font-size: 2.5rem;
                }}

                .feature-grid, .service-grid {{
                    grid-template-columns: 1fr;
                }}

                section {{
                    padding: 4rem 0;
                }}
            }}

            /* Animation Utilities */
            .floating {{
                animation: floating 3s ease-in-out infinite;
            }}

            @keyframes floating {{
                0% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-20px); }}
                100% {{ transform: translateY(0px); }}
            }}

            .pulse {{
                animation: pulse 2s ease-in-out infinite;
            }}

           @keyframes pulse {{
                 0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
                100% {{ transform: scale(1); }}
            }}


        </style>
    </head>
    <body>
    """

    # Header with animated navigation
    header = content.get('header', {})
    nav_items = header.get('navigation', [])

    html += f"""
        <header id="main-header">
            <div class="container">
                <nav>
                    <div class="logo">{escape(header.get('title', content.get('title', 'Stylish Brand')))}</div>
                    <div class="nav-links" id="nav-links">
    """

    # Navigation items with icons
    nav_icons = ['home', 'gem', 'info-circle', 'cogs', 'comment', 'envelope']
    for i, item in enumerate(nav_items):
        icon = nav_icons[i % len(nav_icons)]
        html += f'<a href="{escape(item.get("url", "#"))}"><i class="fas fa-{icon}"></i> {escape(item.get("text", "Link"))}</a>'

    html += """
                    </div>
                    <button class="mobile-menu-btn" id="mobile-menu-btn">
                        <i class="fas fa-bars"></i>
                    </button>
                </nav>
            </div>
        </header>
    """

    # Hero section with animations
    hero = content.get('hero', {})
    if hero:
        html += f"""
            <section class="hero" id="home">
                <div class="container">
                    <div class="hero-content slide-in-left">
                        <h1 class="animate__animated animate__fadeInDown">{escape(hero.get('title', 'Cutting-Edge Digital Solutions'))}</h1>
                        <p class="animate__animated animate__fadeInUp" style="animation-delay: 0.2s;">{escape(hero.get('subtitle', 'Transform your digital presence with our innovative solutions'))}</p>
                        <a href="{escape(hero.get('button_url', '#'))}" class="btn btn-primary animate__animated animate__fadeInUp" style="animation-delay: 0.4s;">{escape(hero.get('button_text', 'Get Started'))}</a>
                    </div>
                </div>
            </section>
        """

    # Features section with icons and animations
    features = content.get('features', {})
    if features:
        feature_items = features.get('items', [])
        # Define feature icons
        feature_icons = [
            'rocket', 'cog', 'chart-line', 'clock', 'shield-alt', 'magic'
        ]

        html += f"""
            <section class="features" id="features">
                <div class="container">
                    <h2 class="fade-in">{escape(features.get('title', 'Our Innovative Features'))}</h2>
                    <p class="subtitle fade-in">{escape(features.get('subtitle', 'Discover what makes us different'))}</p>
                    <div class="feature-grid">
        """

        for i, item in enumerate(feature_items):
            delay = 0.1 * (i + 1)
            icon = feature_icons[i % len(feature_icons)]
            html += f"""
                <div class="feature-item fade-in" style="transition-delay: {delay}s;">
                    <div class="feature-icon">
                        <i class="fas fa-{icon}"></i>
                    </div>
                    <h3>{escape(item.get('title', 'Feature'))}</h3>
                    <p>{escape(item.get('description', 'Feature description'))}</p>
                </div>
            """

        html += """
                    </div>
                </div>
            </section>
        """

    # About section with image and animation
    about = content.get('about', {})
    if about:
        html += f"""
            <section class="about" id="about">
                <div class="container">
                    <div class="about-grid">
                        <div class="about-content slide-in-left">
                            <h2>{escape(about.get('title', 'About Us'))}</h2>
                            <p>{escape(about.get('content', 'We are a team of passionate designers and developers dedicated to creating exceptional digital experiences.'))}</p>
                            <a href="#contact" class="btn btn-primary">Learn More</a>
                        </div>
                        <div class="about-image slide-in-right">
                            <img src="/api/placeholder/600/400" alt="About Us" />
                        </div>
                    </div>
                </div>
            </section>
        """
        # Services section with cards and hover effects
    services = content.get('services', {})
    if services:
        service_items = services.get('items', [])
        html += f"""
            <section class="services" id="services">
                <div class="container">
                    <h2 class="fade-in">{escape(services.get('title', 'Our Premium Services'))}</h2>
                    <p class="subtitle fade-in">{escape(services.get('subtitle', 'Tailored solutions for your business'))}</p>
                    <div class="service-grid">
        """

        for i, item in enumerate(service_items):
            delay = 0.1 * (i + 1)
            html += f"""
                <div class="service-item fade-in" style="transition-delay: {delay}s;">
                    <div class="service-image">
                        <img src="/api/placeholder/600/400" alt="{escape(item.get('title', 'Service'))}" />
                    </div>
                    <div class="service-content">
                        <h3>{escape(item.get('title', 'Service'))}</h3>
                        <p>{escape(item.get('description', 'Service description'))}</p>
                        <a href="#contact" class="service-link">Learn More <i class="fas fa-arrow-right"></i></a>
                    </div>
                </div>
            """

        html += """
                    </div>
                </div>
            </section>
        """

    # Testimonials section with slider effect
    testimonials = content.get('testimonials', {})
    if testimonials:
        testimonial_items = testimonials.get('items', [])
        html += f"""
            <section class="testimonials" id="testimonials">
                <div class="container">
                    <h2 class="fade-in">{escape(testimonials.get('title', 'Client Testimonials'))}</h2>
                    <p class="subtitle fade-in">{escape(testimonials.get('subtitle', 'What our clients say about us'))}</p>
                    <div class="testimonial-slider">
        """

        for i, item in enumerate(testimonial_items):
            delay = 0.1 * (i + 1)
            html += f"""
                <div class="testimonial-item fade-in" style="transition-delay: {delay}s;">
                    <div class="testimonial-text">
                        {escape(item.get('quote', 'This company has transformed our business with their innovative solutions.'))}
                    </div>
                    <div class="testimonial-author">
                        <div class="testimonial-avatar">
                            <img src="/api/placeholder/120/120" alt="{escape(item.get('name', 'Client Name'))}" />
                        </div>
                        <div class="testimonial-info">
                            <h4>{escape(item.get('name', 'Client Name'))}</h4>
                            <p>{escape(item.get('title', 'Client Title'))}</p>
                        </div>
                    </div>
                </div>
            """

        html += """
                    </div>
                </div>
            </section>
        """

    # Contact section with animated form
    contact = content.get('contact', {})
    if contact:
        html += f"""
            <section class="contact" id="contact">
                <div class="container">
                    <h2 class="fade-in">{escape(contact.get('title', 'Get In Touch'))}</h2>
                    <p class="subtitle fade-in">{escape(contact.get('subtitle', 'Let\'s start a conversation'))}</p>
                    <div class="contact-grid">
                        <div class="contact-info slide-in-left">
                            <h3>Contact Information</h3>
                            <p>We're here to help with any questions you might have about our products or services.</p>

                            <div class="contact-info-item">
                                <div class="contact-icon">
                                    <i class="fas fa-envelope"></i>
                                </div>
                                <div>
                                    <h4>Email</h4>
                                    <p>{escape(contact.get('email', 'info@example.com'))}</p>
                                </div>
                            </div>

                            <div class="contact-info-item">
                                <div class="contact-icon">
                                    <i class="fas fa-phone"></i>
                                </div>
                                <div>
                                    <h4>Phone</h4>
                                    <p>{escape(contact.get('phone', '+1 234 567 890'))}</p>
                                </div>
                            </div>

                            <div class="contact-info-item">
                                <div class="contact-icon">
                                    <i class="fas fa-map-marker-alt"></i>
                                </div>
                                <div>
                                    <h4>Address</h4>
                                    <p>{escape(contact.get('address', '123 Street, City, Country'))}</p>
                                </div>
                            </div>
                        </div>

                        <div class="contact-form slide-in-right">
                            <h3>Send us a message</h3>
                            <div class="form-group">
                                <input type="text" class="form-control" placeholder="Your Name" required>
                            </div>
                            <div class="form-group">
                                <input type="email" class="form-control" placeholder="Your Email" required>
                            </div>
                            <div class="form-group">
                                <input type="text" class="form-control" placeholder="Subject">
                            </div>
                            <div class="form-group">
                                <textarea class="form-control" rows="5" placeholder="Your Message" required></textarea>
                            </div>
                            <button type="submit" class="form-submit">
                                <i class="fas fa-paper-plane"></i> Send Message
                            </button>
                            <p style="text-align: center; margin-top: 1rem; font-size: 0.875rem; color: #64748b;">
                                This is a preview. Contact form will be functional in the published website.
                            </p>
                        </div>
                    </div>
                </div>
            </section>
        """

    # Footer with social links
    footer = content.get('footer', {})
    html += f"""
        <footer>
            <div class="container">
                <div class="footer-grid">
                    <div class="footer-about">
                        <div class="footer-logo">{escape(header.get('title', content.get('title', 'Stylish Brand')))}</div>
                        <p>We create cutting-edge digital solutions that help businesses thrive in today's competitive landscape.</p>
                        <div class="social-links">
                            <a href="#" class="social-link"><i class="fab fa-facebook-f"></i></a>
                            <a href="#" class="social-link"><i class="fab fa-twitter"></i></a>
                            <a href="#" class="social-link"><i class="fab fa-instagram"></i></a>
                            <a href="#" class="social-link"><i class="fab fa-linkedin-in"></i></a>
                        </div>
                    </div>

                    <div class="footer-links-column">
                        <h3 class="footer-heading">Quick Links</h3>
                        <ul class="footer-links">
                            <li><a href="#home"><i class="fas fa-chevron-right"></i> Home</a></li>
                            <li><a href="#about"><i class="fas fa-chevron-right"></i> About</a></li>
                            <li><a href="#services"><i class="fas fa-chevron-right"></i> Services</a></li>
                            <li><a href="#testimonials"><i class="fas fa-chevron-right"></i> Testimonials</a></li>
                            <li><a href="#contact"><i class="fas fa-chevron-right"></i> Contact</a></li>
                        </ul>
                    </div>

                    <div class="footer-links-column">
                        <h3 class="footer-heading">Our Services</h3>
                        <ul class="footer-links">
                            <li><a href="#"><i class="fas fa-chevron-right"></i> Web Development</a></li>
                            <li><a href="#"><i class="fas fa-chevron-right"></i> Mobile Apps</a></li>
                            <li><a href="#"><i class="fas fa-chevron-right"></i> UI/UX Design</a></li>
                            <li><a href="#"><i class="fas fa-chevron-right"></i> Digital Marketing</a></li>
                            <li><a href="#"><i class="fas fa-chevron-right"></i> Consulting</a></li>
                        </ul>
                    </div>
                </div>

                <div class="copyright">
                    <p>{escape(footer.get('copyright', '© 2025 Stylish Brand. All rights reserved.'))}</p>
                </div>
            </div>
        </footer>
    """

    # Add JavaScript for animations and interactivity
    html += """
    <script>
        // Mobile menu toggle
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const navLinks = document.getElementById('nav-links');

        if (mobileMenuBtn) {
            mobileMenuBtn.addEventListener('click', () => {
                navLinks.classList.toggle('active');
                mobileMenuBtn.innerHTML = navLinks.classList.contains('active') 
                    ? '<i class="fas fa-times"></i>' 
                    : '<i class="fas fa-bars"></i>';
            });
        }

        // Header scroll effect
        const header = document.getElementById('main-header');
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });

        // Scroll reveal animations
        const fadeElems = document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right, .scale-in');

        const checkFade = () => {
            const triggerBottom = window.innerHeight * 0.8;

            fadeElems.forEach(elem => {
                const elemTop = elem.getBoundingClientRect().top;

                if (elemTop < triggerBottom) {
                    elem.classList.add('active');
                }
            });
        }

        // Initial check
        checkFade();

        // Check on scroll
        window.addEventListener('scroll', checkFade);

        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();

                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    window.scrollTo({
                        top: target.offsetTop - 80,
                        behavior: 'smooth'
                    });

                    // Close mobile menu if open
                    navLinks.classList.remove('active');
                    mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
                }
            });
        });

        // Add GSAP animations for enhanced effects
        gsap.registerPlugin(ScrollTrigger);

        // Hero section parallax effect
        gsap.to(".hero", {
            backgroundPosition: "50% 0%",
            ease: "none",
            scrollTrigger: {
                trigger: ".hero",
                start: "top top",
                end: "bottom top",
                scrub: true
            }
        });

        // Animate feature items on scroll
        gsap.utils.toArray('.feature-item').forEach((item, i) => {
            gsap.from(item, {
                y: 50,
                opacity: 0,
                duration: 0.8,
                ease: "power3.out",
                scrollTrigger: {
                    trigger: item,
                    start: "top 80%",
                    toggleActions: "play none none none"
                },
                delay: i * 0.1
            });
        });

        // Animate service items with stagger
        gsap.from(".service-item", {
            opacity: 0,
            y: 30,
            stagger: 0.2,
            duration: 0.8,
            ease: "power3.out",
            scrollTrigger: {
                trigger: ".service-grid",
                start: "top 80%"
            }
        });

        // Floating animation for certain elements
        gsap.to(".hero-content", {
            y: 15,
            duration: 2,
            repeat: -1,
            yoyo: true,
            ease: "sine.inOut"
        });
    </script>
    """

    html += """
    </body>
    </html>
    """

    return html


def add_preview_controls(html, website):
    """
    Add modern, animated preview controls panel to the rendered HTML.

    Args:
        html: The rendered HTML content
        website: The Website model instance

    Returns:
        str: HTML with preview controls
    """
    # Create the controls HTML with improved styling and animations
    controls = """
    <div id="preview-controls" style="
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(17, 24, 39, 0.95));
        backdrop-filter: blur(10px);
        color: white;
        padding: 15px 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 9999;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        animation: slideUp 0.5s ease forwards;
    ">
        <div style="display: flex; align-items: center;">
            <div style="
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #6366f1, #8b5cf6);
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 15px;
                box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
            ">
                <i class="fas fa-eye" style="font-size: 18px;"></i>
            </div>
            <div>
                <span style="display: block; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.7;">Preview Mode</span>
                <span style="font-weight: 600; font-size: 16px;">""" + escape(
        website.title) + """</span>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <button onclick="handleEdit()" 
               style="
                  display: flex;
                  align-items: center;
                  color: white;
                  border: none;
                  background: rgba(255, 255, 255, 0.1);
                  padding: 8px 15px;
                  border-radius: 8px;
                  font-weight: 500;
                  font-size: 14px;
                  transition: all 0.3s ease;
                  cursor: pointer;
               "
               class="preview-control-btn"
               onmouseover="this.style.background='rgba(255, 255, 255, 0.2)'"
               onmouseout="this.style.background='rgba(255, 255, 255, 0.1)'">
               <i class="fas fa-edit" style="margin-right: 8px;"></i> Edit
            </button>
            <button onclick="handleUpdate()" 
               style="
                  display: flex;
                  align-items: center;
                  color: white;
                  border: none;
                  background: linear-gradient(135deg, #6366f1, #8b5cf6);
                  padding: 8px 15px;
                  border-radius: 8px;
                  font-weight: 500;
                  font-size: 14px;
                  transition: all 0.3s ease;
                  box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
                  cursor: pointer;
               "
               class="preview-control-btn" 
               onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 15px rgba(99, 102, 241, 0.4)'"
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 10px rgba(99, 102, 241, 0.3)'">
               <i class="fas fa-pen" style="margin-right: 8px;"></i> Update Content
            </button>
            <button onclick="handleRegenerate('/api/generator/regenerate/""" + str(
            website.generation_request.id if website.generation_request else 0
        ) + """/about/')" 
               style="
                  display: flex;
                  align-items: center;
                  color: white;
                  text-decoration: none;
                  background: rgba(255, 255, 255, 0.1);
                  padding: 8px 15px;
                  border-radius: 8px;
                  font-weight: 500;
                  font-size: 14px;
                  transition: all 0.3s ease;
               "
               class="preview-control-link"
               onmouseover="this.style.background='rgba(255, 255, 255, 0.2)'"
               onmouseout="this.style.background='rgba(255, 255, 255, 0.1)'"
               target="_blank">
               <i class="fas fa-sync-alt" style="margin-right: 8px;"></i> Regenerate
            </a>
            <button id="hide-controls-btn" 
                    style="
                        background: none;
                        border: none;
                        color: white;
                        opacity: 0.5;
                        cursor: pointer;
                        font-size: 16px;
                        margin-left: 10px;
                        transition: all 0.3s ease;
                    "
                    onmouseover="this.style.opacity='1'"
                    onmouseout="this.style.opacity='0.5'">
                <i class="fas fa-chevron-down"></i>
            </button>
        </div>
    </div>

    <div id="show-controls-btn" style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border-radius: 50%;
        display: none;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        z-index: 9998;
        transition: all 0.3s ease;
    "
    onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 20px rgba(99, 102, 241, 0.5)'"
    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(99, 102, 241, 0.4)'">
        <i class="fas fa-eye"></i>
    </div>

    <script>
        // Add Font Awesome
        if (!document.querySelector('link[href*="font-awesome"]')) {
            const fontAwesome = document.createElement('link');
            fontAwesome.rel = 'stylesheet';
            fontAwesome.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css';
            document.head.appendChild(fontAwesome);
        }

        // Handle controls visibility
        const previewControls = document.getElementById('preview-controls');
        const hideControlsBtn = document.getElementById('hide-controls-btn');
        const showControlsBtn = document.getElementById('show-controls-btn');

        hideControlsBtn.addEventListener('click', () => {
            previewControls.style.animation = 'slideDown 0.5s ease forwards';
            setTimeout(() => {
                previewControls.style.display = 'none';
                showControlsBtn.style.display = 'flex';
                showControlsBtn.style.animation = 'fadeIn 0.3s ease forwards';
            }, 500);
        });

        showControlsBtn.addEventListener('click', () => {
            showControlsBtn.style.animation = 'fadeOut 0.3s ease forwards';
            setTimeout(() => {
                showControlsBtn.style.display = 'none';
                previewControls.style.display = 'flex';
                previewControls.style.animation = 'slideUp 0.5s ease forwards';
            }, 300);
        });

        // Add animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideUp {
                from { transform: translateY(100%); }
                to { transform: translateY(0); }
            }

            @keyframes slideDown {
                from { transform: translateY(0); }
                to { transform: translateY(100%); }
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: scale(0.9); }
                to { opacity: 1; transform: scale(1); }
            }

            @keyframes fadeOut {
                from { opacity: 1; transform: scale(1); }
                to { opacity: 0; transform: scale(0.9); }
            }
        `;
        document.head.appendChild(style);

        // Handle button actions
     
        function handleRegenerate(url) {
    const token = localStorage.getItem('access_token');
    fetch(url, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/login/';
                return;
            }
            throw new Error('Failed to regenerate content');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Failed to regenerate content');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while regenerating content');
    });
}

function handleEdit() {
    const websiteId = '""" + str(website.id) + """';
    const token = localStorage.getItem('access_token');
    window.location.href = `/api/websites/${websiteId}/edit/`;
}

function handleUpdate() {
    const websiteId = '${website.id}';
    const token = localStorage.getItem('access_token');
    fetch(`/api/websites/${websiteId}/content/`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            content: document.getElementById('website-content').value
        })
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/login/';
                return;
            }
            throw new Error('Failed to update content');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Failed to update content');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating content');
    });
}

     

    

        // Handle authentication token from localStorage
        const token = localStorage.getItem('access_token');
    </script>
    """

    # Insert controls before closing body tag
    html = html.replace('</body>', controls + '</body>')

    return html




