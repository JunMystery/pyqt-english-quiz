import os

def load_theme(app) -> None:
    """Loads the global CSS stylesheet for the application."""
    theme_path = os.path.join(os.path.dirname(__file__), 'theme.qss')
    tick_path = os.path.join(os.path.dirname(__file__), 'tick.svg').replace('\\', '/')
    
    if os.path.exists(theme_path):
        with open(theme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            content = content.replace('url(TICK_SVG)', f'url("{tick_path}")')
            app.setStyleSheet(content)
    else:
        print(f"Warning: Stylesheet {theme_path} not found.")
