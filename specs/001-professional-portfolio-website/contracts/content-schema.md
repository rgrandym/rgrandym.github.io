# Content Schema Contract

**Feature**: Professional Portfolio Website  
**Purpose**: Define the YAML frontmatter contracts for all content types  
**Date**: 2025-10-07

## Overview

This document defines the "contracts" for content in the portfolio website. Since this is a static site, there are no API endpoints. Instead, the contracts define the required and optional YAML frontmatter fields for each content type.

## Project Content Contract

**File Location**: `projects/*.qmd`  
**Content Type**: Project showcase page

### Required Fields

```yaml
title: string              # Project name (unique)
description_brief: string  # 100-200 char summary for cards
date_completed: date       # ISO format YYYY-MM-DD
technologies: [string]     # Array of technology tags (minimum 1)
hero_image: string         # Path to main image (must exist)
```

### Optional Fields

```yaml
categories: [string]       # Project categories for filtering
screenshots: [string]      # Array of image paths
github_url: string         # GitHub repository URL
demo_url: string          # Live demo URL
featured: boolean         # Show on home page (default: false)
```

### Content Sections (Markdown)

After frontmatter, the .qmd file should contain:

- `## Problem`: Context and problem statement
- `## Solution`: What was built
- `## Technologies`: Detailed technology discussion (optional)
- `## Outcomes`: Results, impact, learnings

### Example

```yaml
---
title: "Immunology Development Analysis"
description_brief: "Computational analysis of immune system development using machine learning"
date_completed: 2024-12-15
technologies: ["Python", "R", "Bioconductor", "Machine Learning"]
categories: ["Bioinformatics", "Research"]
hero_image: "assets/images/immuno_dev.png"
screenshots: 
  - "assets/images/immuno_dev_chart1.png"
github_url: "https://github.com/rgrandym/immuno-dev"
featured: true
---

## Problem

[Content here]

## Solution

[Content here]

## Outcomes

[Content here]
```

### Validation Rules

- `title` must be unique across all projects
- `description_brief` length: 100-200 characters
- `date_completed` must be valid ISO date (YYYY-MM-DD)
- `technologies` array must have at least 1 item
- `hero_image` path must reference existing file in repository
- If `featured: true`, only one project should have this flag
- At least one of `github_url` or `demo_url` should be present

---

## Blog Post Content Contract

**File Location**: `posts/*.qmd`  
**Naming Convention**: `YYYY-MM-DD-post-title.qmd`  
**Content Type**: Blog article

### Required Fields

```yaml
title: string         # Post title (unique)
author: string        # Author name
date: date           # Publication date ISO format YYYY-MM-DD
description: string  # 150-300 char excerpt for listings
read_time: integer   # Estimated minutes to read
categories: [string] # Array of categories (minimum 1)
```

### Optional Fields

```yaml
tags: [string]           # Topical tags
draft: boolean          # Draft status (default: false)
image: string           # Featured image path
related_posts: [string] # Array of related post filenames
```

### Content Sections (Markdown)

Free-form markdown content with:

- Headings (##, ###) for structure
- Code blocks with language specification
- Images, links, lists as needed

### Example

```yaml
---
title: "Understanding Single-Cell RNA Sequencing Analysis"
author: "Rodrigo Grandy"
date: 2025-01-15
description: "A practical guide to analyzing single-cell RNA sequencing data using modern computational tools and best practices for bioinformatics research."
read_time: 8
categories: ["Tutorial", "Bioinformatics"]
tags: ["scRNA-seq", "Python", "Data Analysis"]
image: "assets/images/scrna-seq-workflow.png"
related_posts: ["2024-12-10-rna-seq-basics.qmd"]
draft: false
---

[Markdown content with code examples]
```

### Validation Rules

- `title` must be unique across all blog posts
- `date` must be valid ISO date (YYYY-MM-DD)
- Filename must match format: `YYYY-MM-DD-title.qmd` where YYYY-MM-DD matches `date` field
- `description` length: 150-300 characters
- `read_time` must be positive integer (1-60 reasonable range)
- `categories` array must have at least 1 item
- If `draft: true`, post won't appear in production listings
- `related_posts` filenames must reference existing post files

---

## Profile Content Contract

**File Location**: `index.qmd`, `about.qmd`  
**Content Type**: Profile information (singleton)

### Required Fields

```yaml
title: string         # Page title
name: string          # Professional name
professional_title: string  # Role/title
tagline: string       # Brief tagline
profile_image: string # Path to photo
```

### Optional Fields

```yaml
email: string         # Contact email
linkedin_url: string  # LinkedIn profile URL
github_url: string    # GitHub profile URL
resume_file: string   # Path to PDF resume
skills: [string]      # Array of key skills
```

### Content Sections (Markdown)

- Hero section with name, title, tagline, CTA
- About section with 2-3 paragraphs of biography
- Contact links section
- Featured project section (on home page only)

### Example

```yaml
---
title: "Home"
name: "Rodrigo Grandy"
professional_title: "Principal Scientist & Group Leader"
tagline: "Computational biology and immunology research"
profile_image: "assets/images/profile.jpg"
resume_file: "assets/CV_Rodrigo_Grandy.pdf"
email: "r.grandy@example.com"
linkedin_url: "https://linkedin.com/in/rgrandy"
github_url: "https://github.com/rgrandym"
skills: ["Python", "R", "Bioinformatics", "Machine Learning"]
---

[Markdown content for hero and about sections]
```

### Validation Rules

- `email` must be valid email format
- `linkedin_url` and `github_url` must be valid URLs
- `profile_image` must reference existing file
- `resume_file` must reference existing PDF file

---

## Site Configuration Contract

**File Location**: `_quarto.yml`  
**Content Type**: Site-wide configuration

### Required Fields

```yaml
website:
  title: string              # Site title
  navbar:
    left: [NavItem]         # Array of navigation items

project:
  type: website
  output-dir: _site
```

### NavItem Structure

```yaml
- text: string    # Display text
  href: string    # Target page path
```

### Optional Fields

```yaml
website:
  navbar:
    logo: string           # Path to logo image
    background: string     # Navbar background color
  page-footer: string      # Footer content
  
format:
  html:
    theme: string          # Theme name or custom CSS
    css: [string]          # Array of CSS file paths
    toc: boolean           # Table of contents
```

### Example

```yaml
project:
  type: website
  output-dir: _site

website:
  title: "Rodrigo Grandy"
  navbar:
    logo: "assets/logo.png"
    background: "#F5F5F0"
    left:
      - text: "Home"
        href: "index.qmd"
      - text: "Projects"
        href: "projects.qmd"
      - text: "Blog"
        href: "blog.qmd"
      - text: "CV"
        href: "cv.qmd"

format:
  html:
    theme: cosmo
    css: styles/styles.css
    toc: false
```

---

## Listing Page Contract

**File Location**: `projects.qmd`, `blog.qmd`  
**Content Type**: Aggregation page for content listings

### Required Fields

```yaml
title: string         # Page title
listing:
  contents: string    # Directory path to list (e.g., "projects")
  type: string        # Layout type (grid, default, table)
```

### Optional Fields

```yaml
listing:
  sort: string        # Sort field (date, title)
  sort-ui: boolean    # Show sort controls
  filter-ui: boolean  # Show filter controls
  categories: boolean # Show category filter
  fields: [string]    # Fields to display in listing
```

### Example - Projects Page

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

Browse my portfolio of completed projects in computational biology and bioinformatics.
```

### Example - Blog Page

```yaml
---
title: "Blog"
listing:
  contents: posts
  type: default
  sort: "date desc"
  filter-ui: true
  categories: true
  fields: [date, title, description, reading-time, categories]
---

Technical articles and insights on bioinformatics, data analysis, and scientific computing.
```

---

## Contract Validation Process

Since these are file-based contracts (not API contracts), validation happens at:

1. **Development Time**: Editor/IDE YAML syntax checking
2. **Build Time**: Quarto validates YAML and file references
3. **Manual Review**: Check content against contract before commit
4. **Browser Testing**: Verify rendered output matches expectations

## Error Handling

**Invalid YAML**: Quarto build will fail with syntax error  
**Missing Required Field**: Quarto build will fail or use defaults  
**Invalid File Reference**: Broken image or link in rendered output  
**Validation Failure**: Documented in this contract, enforced manually

## Notes

- These contracts define the "API" between content files and the Quarto rendering engine
- Following these contracts ensures consistent content structure
- All contracts are declarative (YAML + Markdown) - no code required
- Aligns with constitution's lean architecture (no complex validation logic)
- Content creators can reference this document as the source of truth
