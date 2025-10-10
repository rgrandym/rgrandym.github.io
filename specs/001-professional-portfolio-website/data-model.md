# Data Model: Professional Portfolio Website

**Feature**: Professional Portfolio Website  
**Phase**: 1 - Design  
**Date**: 2025-10-07

## Overview

This portfolio website is content-driven with no dynamic backend or database. All "data" exists as structured content in Quarto Markdown files (.qmd) with YAML frontmatter. This document describes the content structure and relationships.

## Content Entities

### Profile (Singleton)

**Location**: `index.qmd`, `about.qmd`  
**Purpose**: Represents the professional's identity and contact information

**Attributes**:

- `name` (string): Full professional name
- `title` (string): Professional title/role
- `tagline` (string): Brief professional tagline
- `bio` (array of strings): 2-3 paragraph biography
- `email` (string): Contact email address
- `linkedin_url` (string): LinkedIn profile URL
- `github_url` (string): GitHub profile URL
- `profile_image` (string): Path to professional photograph
- `resume_file` (string): Path to PDF resume/CV
- `skills` (array of strings): Key skills or technologies

**Validation Rules**:

- `email` must be valid email format
- `linkedin_url` and `github_url` must be valid URLs
- `profile_image` must reference existing file in assets/images/
- `resume_file` must reference existing PDF in assets/

**YAML Example**:

```yaml
---
name: "Rodrigo Grandy"
title: "Principal Scientist & Group Leader"
tagline: "Computational biology and immunology research"
profile_image: "assets/images/profile.jpg"
resume_file: "assets/CV_Rodrigo_Grandy.pdf"
email: "contact@example.com"
linkedin_url: "https://linkedin.com/in/example"
github_url: "https://github.com/rgrandym"
---
```

### Project

**Location**: Individual .qmd files in `projects/` directory  
**Purpose**: Represents a completed work item to showcase

**Attributes**:

- `title` (string): Project name
- `description_brief` (string): 1-2 sentence summary for cards
- `description_full` (markdown): Full project description
- `problem` (markdown): Problem statement/context
- `solution` (markdown): What was built/implemented
- `technologies` (array of strings): Technologies used (for tags)
- `outcomes` (markdown): Results, impact, or learnings
- `hero_image` (string): Path to main project image
- `screenshots` (array of strings): Paths to additional images
- `github_url` (string, optional): GitHub repository URL
- `demo_url` (string, optional): Live demo URL
- `date_completed` (date): Completion date (YYYY-MM-DD)
- `featured` (boolean): Whether to show on home page
- `categories` (array of strings): Project categories for filtering

**Validation Rules**:

- `title` is required and must be unique
- `description_brief` must be 100-200 characters
- `date_completed` must be valid ISO date format
- `hero_image` must reference existing file
- `technologies` must not be empty (minimum 1 tag)
- At least one of `github_url` or `demo_url` should be provided

**Relationships**:

- One project can be marked as `featured: true` for home page display
- Projects are listed on `projects.qmd` page
- Related to Profile via implicit "created by" relationship

**YAML Example**:

```yaml
---
title: "Immunology Development Analysis"
description_brief: "Computational analysis of immune system development patterns"
date_completed: 2024-12-15
technologies: ["Python", "R", "Bioconductor", "Machine Learning"]
categories: ["Bioinformatics", "Research"]
hero_image: "assets/images/immuno_dev.png"
screenshots: 
  - "assets/images/immuno_dev_chart1.png"
  - "assets/images/immuno_dev_chart2.png"
github_url: "https://github.com/rgrandym/immuno-dev"
featured: true
---

## Problem

[Markdown content describing the problem context]

## Solution

[Markdown content describing what was built]

## Outcomes

[Markdown content describing results and learnings]
```

### Blog Post

**Location**: Individual .qmd files in `posts/` directory  
**Purpose**: Represents a technical article or insight

**Attributes**:

- `title` (string): Post title
- `author` (string): Author name (usually profile name)
- `date` (date): Publication date (YYYY-MM-DD)
- `description` (string): Excerpt/summary for listings (2-3 sentences)
- `read_time` (integer): Estimated read time in minutes
- `categories` (array of strings): Post categories for filtering
- `tags` (array of strings): Topical tags
- `draft` (boolean): Whether post is published (default: false)
- `image` (string, optional): Featured image for the post
- `related_posts` (array of strings, optional): Filenames of related posts

**Validation Rules**:

- `title` is required and must be unique
- `date` must be valid ISO date format
- `description` must be 150-300 characters
- `read_time` must be positive integer
- `categories` must not be empty (minimum 1 category)
- If `draft: true`, post should not appear in production listings

**Relationships**:

- Posts are listed on `blog.qmd` page chronologically
- `related_posts` references other Blog Post entities by filename
- Related to Profile via `author` attribute

**YAML Example**:

```yaml
---
title: "Understanding Single-Cell RNA Sequencing Analysis"
author: "Rodrigo Grandy"
date: 2025-01-15
description: "A practical guide to analyzing single-cell RNA sequencing data using modern computational tools and best practices."
read_time: 8
categories: ["Tutorial", "Bioinformatics"]
tags: ["scRNA-seq", "Python", "Data Analysis"]
image: "assets/images/scrna-seq-workflow.png"
related_posts: ["2024-12-10-rna-seq-basics.qmd"]
draft: false
---

[Markdown content with code blocks]
```

### Navigation

**Location**: `_quarto.yml`  
**Purpose**: Defines site structure and menu items

**Attributes**:

- `menu_items` (array of objects): Navigation links
  - `text` (string): Display text
  - `href` (string): Target page path
- `logo` (string, optional): Site logo image
- `site_title` (string): Website title

**YAML Example** (in `_quarto.yml`):

```yaml
website:
  title: "Rodrigo Grandy"
  navbar:
    logo: "assets/logo.png"
    left:
      - text: "Home"
        href: "index.qmd"
      - text: "Projects"
        href: "projects.qmd"
      - text: "Blog"
        href: "blog.qmd"
      - text: "CV"
        href: "cv.qmd"
```

## Content Relationships

```text
Profile (1)
  |
  ├── creates --> Projects (many)
  |                  |
  |                  └── featured (0-1) --> displayed on Home
  |
  └── authors --> Blog Posts (many)
                     |
                     └── related_to --> other Blog Posts (many-to-many)

Navigation (1)
  |
  ├── links to --> Home (Profile)
  ├── links to --> Projects page (lists all Projects)
  └── links to --> Blog page (lists all Blog Posts)
```

## File Naming Conventions

### Projects

Format: `kebab-case-descriptive-name.qmd`

Examples:

- `immunology-development-analysis.qmd`
- `protein-structure-prediction.qmd`
- `data-visualization-toolkit.qmd`

### Blog Posts

Format: `YYYY-MM-DD-kebab-case-title.qmd`

Examples:

- `2025-01-15-understanding-scrna-seq.qmd`
- `2024-12-10-rna-seq-basics.qmd`
- `2025-02-20-python-best-practices.qmd`

## Content State Management

### Draft vs Published

Blog posts support draft status:

- `draft: false` (or omitted): Published, appears in listings
- `draft: true`: Hidden from production, visible during development

Projects do not have draft status - they are either present in the repository or not.

### Featured Content

Only projects can be featured:

- Maximum 1 project should have `featured: true`
- Featured project appears on home page
- If multiple projects marked featured, use most recent by `date_completed`

## Validation Strategy

Since this is a static site with no database, validation happens at different stages:

1. **Content Creation**: Manual review of YAML frontmatter syntax
2. **Build Time**: Quarto validates YAML syntax and file references
3. **Pre-Commit** (optional): Could add YAML linter for frontmatter validation
4. **Manual Testing**: Verify all links, images, and content render correctly

## Content Workflow

1. **Create**: Author writes content in .qmd file with proper frontmatter
2. **Review**: Manual review for accuracy, formatting, and metadata completeness
3. **Build**: Run `quarto render` to generate HTML
4. **Test**: Manual testing in browser (navigation, images, responsiveness)
5. **Deploy**: Push to Git, automatic deployment via hosting platform

## Notes

- No database or API layer - all content is file-based
- Content is version-controlled in Git alongside code
- Each content entity is completely self-contained in its file
- Relationships are expressed through frontmatter references
- This model aligns with constitution's modularity principle (separate files) and lean architecture (no complex state management)
