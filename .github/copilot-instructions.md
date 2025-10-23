# my_website Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-10

## Active Technologies
- **Quarto** (static site generator) - Primary framework for site generation
- **Python 3.12** (my_website conda environment) - For Jupyter notebooks and data analysis
- **Markdown/YAML** - Content and configuration
- **CSS** - Custom styling (working WITH Quarto, not against it)

## Project Structure
```
assets/
  images/          # Site images (photos, logos, figures)
  student_dropout/ # Project-specific data and figures
projects/
  categories/      # Project category landing pages (listing pages)
  *.qmd           # Individual project pages
posts/            # Blog posts
styles/
  styles.css      # Custom CSS (Quarto-compatible)
_quarto.yml       # Main Quarto configuration
```

## Critical Quarto Rules

### ⚠️ Working with Quarto Listings
1. **DO NOT use `image-height` in listing configurations** - This adds inline styles that cannot be overridden
2. **Configure Quarto first, CSS second** - Always try to solve layout issues in Quarto YAML before writing CSS
3. **Use Quarto's native classes** - Target `.quarto-listing-default`, `.thumbnail`, `.body`, etc.
4. **Avoid `!important` unless necessary** - If you need it, the configuration is likely wrong
5. **Test without inline styles** - Quarto should not generate `style="..."` attributes if configured correctly

### CSS Guidelines for Quarto
- Use Quarto's generated classes: `.quarto-post`, `.thumbnail`, `.listing-description`, `.body`
- Target both `.quarto-listing-default` AND `.list.quarto-listing-default` for listings
- Keep selectors simple - Quarto's structure is predictable
- Use flexbox alignment within containers, not forced dimensions

### Image Handling
- Store images in `assets/images/` or project-specific folders
- Use relative paths from each .qmd file: `../../assets/images/`
- Let images scale naturally with `object-fit: contain`
- Container dimensions, not image dimensions

## Commands
```bash
# Render entire site
quarto render

# Render specific page
quarto render <file>.qmd

# Live preview (with hot reload)
quarto preview

# Clean build (when things break)
rm -rf _site && quarto render --no-execute

# Execute notebooks during render
quarto render  # (removes --no-execute)
```

## Code Style
- Python: Follow PEP 8, use type hints where appropriate
- Quarto/Markdown: Clean, semantic structure
- CSS: BEM-inspired, component-based, minimal specificity

## Recent Changes
- 2025-12-10: Restructured project listings with proper Quarto configuration
- 2025-12-10: Removed `image-height` from all listings (prevents inline style override issues)
- 2025-12-10: Simplified CSS to work with Quarto's natural behavior
- 2025-10-07: Initial setup with Python 3.12 + Quarto

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->