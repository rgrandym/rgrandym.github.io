# Quickstart Guide: Professional Portfolio Website

**Feature**: Professional Portfolio Website  
**Date**: 2025-10-07  
**Prerequisites**: Quarto installed, my_website conda environment created

## Overview

This guide walks through setting up and developing the professional portfolio website using Quarto. It covers environment setup, project initialization, content creation, local development, and deployment.

## Environment Setup

### 1. Activate Conda Environment

```bash
conda activate my_website
```

### 2. Install Quarto

Quarto is not available via conda, so install using the official installer:

**macOS**:

```bash
# Download and install from https://quarto.org/docs/get-started/
# Or using Homebrew:
brew install quarto
```

Verify installation:

```bash
quarto --version
```

### 3. Install Supporting Tools (Optional)

```bash
# Image optimization (if needed)
conda install imagemagick

# Or via pip if not in conda
pip install pillow
```

## Project Initialization

### 1. Initialize Quarto Website

The basic structure already exists, but to initialize a new Quarto website from scratch:

```bash
quarto create-project portfolio --type website
cd portfolio
```

### 2. Verify Project Structure

```bash
tree -L 2
```

Expected structure:

```text
my_website/
├── _quarto.yml
├── index.qmd
├── about.qmd
├── projects.qmd
├── blog.qmd
├── projects/
├── posts/
├── assets/
│   └── images/
├── styles/
│   └── styles.css
└── environment.yml
```

## Configuration

### 1. Edit `_quarto.yml`

Basic configuration:

```yaml
project:
  type: website
  output-dir: _site

website:
  title: "Your Name"
  navbar:
    background: "#F5F5F0"
    left:
      - text: "Home"
        href: "index.qmd"
      - text: "Projects"
        href: "projects.qmd"
      - text: "Blog"
        href: "blog.qmd"

format:
  html:
    theme: cosmo
    css: styles/styles.css
    toc: false
    link-external-newwindow: true
```

### 2. Create Custom Styles

Create `styles/styles.css` for the minimalist design:

```css
/* Hero section split layout */
.hero {
  display: grid;
  grid-template-columns: 60% 40%;
  min-height: 100vh;
  gap: 2rem;
}

/* Typography */
h1 {
  font-size: 4rem;
  font-weight: 300;
  line-height: 1.2;
}

/* Colors */
:root {
  --background: #F5F5F0;
  --text: #2C2C2C;
  --accent: #2C2C2C;
}

body {
  background-color: var(--background);
  color: var(--text);
}
```

## Content Creation

### 1. Create Home Page (`index.qmd`)

```yaml
---
title: "Home"
name: "Your Name"
professional_title: "Your Title"
profile_image: "assets/images/profile.jpg"
---

::: {.hero}
::: {.hero-content}
# Your Name

**Your Professional Title**

Brief description of who you are and what you do.

[View Projects](projects.qmd){.btn .btn-primary}
:::

::: {.hero-image}
![](assets/images/profile.jpg)
:::
:::

## About

2-3 paragraphs about your background, expertise, and current work.

**Contact**: [Email](mailto:your@email.com) | [LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/yourusername)
```

### 2. Create a Project (`projects/project-name.qmd`)

```yaml
---
title: "Project Title"
description_brief: "Short description for project cards"
date_completed: 2024-12-15
technologies: ["Python", "R", "Tool"]
categories: ["Category1", "Category2"]
hero_image: "assets/images/project-hero.png"
github_url: "https://github.com/user/repo"
featured: true
---

## Problem

Describe the context and problem you were solving.

## Solution

Explain what you built and how it works.

## Technologies

Detail the technologies used and why.

## Outcomes

Share results, learnings, and impact.
```

### 3. Create Projects Listing (`projects.qmd`)

```yaml
---
title: "Projects"
listing:
  contents: projects
  type: grid
  sort: "date desc"
  filter-ui: true
  categories: true
  fields: [image, title, description, categories, date]
---

Browse my portfolio of projects.
```

### 4. Create a Blog Post (`posts/2025-01-15-post-title.qmd`)

```yaml
---
title: "Blog Post Title"
author: "Your Name"
date: 2025-01-15
description: "Brief excerpt about the post content for listings."
read_time: 5
categories: ["Tutorial"]
tags: ["Python", "Data Science"]
---

Write your blog post content here with markdown.

## Section Heading

Content with code blocks:

```python
def example():
    return "Hello, World!"
```
```

### 5. Create Blog Listing (`blog.qmd`)

```yaml
---
title: "Blog"
listing:
  contents: posts
  type: default
  sort: "date desc"
  filter-ui: true
  categories: true
---

Technical articles and insights.
```

## Asset Management

### 1. Add Images

```bash
# Place images in assets/images/
cp ~/path/to/profile.jpg assets/images/
cp ~/path/to/project-screenshot.png assets/images/
```

### 2. Optimize Images

```bash
# Resize and compress (keep under 500KB)
convert profile.jpg -resize 1920x -quality 85 assets/images/profile.jpg
```

### 3. Add Resume

```bash
cp ~/path/to/resume.pdf assets/CV_Your_Name.pdf
```

## Local Development

### 1. Preview Site

```bash
quarto preview
```

This starts a local server at `http://localhost:4200` with live reload.

### 2. Build Site

```bash
quarto render
```

Output goes to `_site/` directory.

### 3. Check Build

```bash
# Open in browser
open _site/index.html
```

## Testing Checklist

Manual testing tasks:

- [ ] All navigation links work
- [ ] Images load correctly
- [ ] External links open in new tabs
- [ ] Mobile responsive (test at 320px, 768px, 1024px widths)
- [ ] All project cards display correctly
- [ ] Blog posts render with syntax highlighting
- [ ] Resume/CV downloads correctly
- [ ] Contact links work (email, LinkedIn, GitHub)
- [ ] Page load times < 3 seconds (check DevTools)
- [ ] Color contrast meets 4.5:1 ratio
- [ ] Keyboard navigation works
- [ ] No console errors in browser

## Deployment Options

### Option 1: GitHub Pages

1. Create `.github/workflows/quarto-publish.yml`:

```yaml
name: Quarto Publish

on:
  push:
    branches: [main]

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: quarto-dev/quarto-actions/setup@v2
      - run: quarto render
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./_site
```

2. Enable GitHub Pages in repository settings (source: gh-pages branch)

### Option 2: Netlify

1. Connect repository to Netlify
2. Build command: `quarto render`
3. Publish directory: `_site`
4. Deploy

### Option 3: Quarto Pub

```bash
quarto publish quarto-pub
```

Follow prompts to authenticate and publish.

## Development Workflow

### Adding New Content

1. Create new .qmd file in appropriate directory
2. Add YAML frontmatter (see contracts/content-schema.md)
3. Write markdown content
4. Preview locally: `quarto preview`
5. Review in browser
6. Commit and push

### Updating Existing Content

1. Edit .qmd file
2. Quarto auto-rebuilds (if preview running)
3. Review changes
4. Commit and push

### Adding New Features

1. Update `_quarto.yml` if needed (navigation, config)
2. Modify `styles/styles.css` for styling
3. Test locally
4. Commit and push

## Troubleshooting

### Quarto Not Found

```bash
# Check installation
which quarto

# If not installed, install via:
# macOS: brew install quarto
# Or download from https://quarto.org
```

### Images Not Loading

- Verify file path in frontmatter matches actual location
- Check file exists: `ls assets/images/filename.jpg`
- Rebuild: `quarto render`

### Links Broken

- Use relative paths: `projects.qmd` not `/projects.qmd`
- Check for typos in href attributes
- Verify target files exist

### CSS Not Applied

- Check `_quarto.yml` includes `css: styles/styles.css`
- Clear browser cache
- Check for CSS syntax errors
- Rebuild: `quarto render`

### Preview Server Won't Start

```bash
# Kill existing process
pkill quarto

# Restart preview
quarto preview
```

## Performance Optimization

### Image Optimization

```bash
# Batch optimize all images
for img in assets/images/*.{jpg,png}; do
    convert "$img" -resize 1920x -quality 85 "$img"
done
```

### Lazy Loading

Add to images in markdown:

```markdown
![Alt text](image.jpg){loading="lazy"}
```

### Minimize CSS

Keep `styles/styles.css` under 200 lines, focus on essential styles.

## Accessibility Checklist

- [ ] All images have descriptive alt text
- [ ] Heading hierarchy is logical (h1 → h2 → h3)
- [ ] Color contrast > 4.5:1 (use browser DevTools)
- [ ] Links have descriptive text (not "click here")
- [ ] Keyboard navigation works for all interactive elements
- [ ] ARIA labels added where needed

## Next Steps

1. Complete content for at least 3 projects
2. Write 1-2 blog posts
3. Optimize all images
4. Test on multiple devices/browsers
5. Run accessibility audit (WAVE extension)
6. Deploy to hosting platform
7. Test production deployment
8. Share with peers for feedback

## Reference Documentation

- [Quarto Websites](https://quarto.org/docs/websites/)
- [Quarto Publishing](https://quarto.org/docs/publishing/)
- [Markdown Basics](https://quarto.org/docs/authoring/markdown-basics.html)
- [YAML Options](https://quarto.org/docs/reference/formats/html.html)
- Content contracts: See `contracts/content-schema.md`
- Data model: See `data-model.md`

## Constitution Compliance

This development workflow complies with the project constitution:

- ✅ Uses `my_website` conda environment
- ✅ Installs dependencies via conda first (Quarto via system, optional tools via conda)
- ✅ Maintains lean architecture (no functions >50 lines needed)
- ✅ Manual testing only (checklist-based)
- ✅ Modular content (separate files per project/post)
- ✅ Task-focused (guide covers only necessary development tasks)
