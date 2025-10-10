# Research: Professional Portfolio Website

**Feature**: Professional Portfolio Website  
**Phase**: 0 - Research & Technology Selection  
**Date**: 2025-10-07

## Purpose

Research Quarto capabilities, best practices for portfolio websites, and resolve any technical unknowns for implementing a professional portfolio site with split-layout hero, project showcase, and blog functionality.

## Research Tasks

### 1. Quarto Static Site Generation

**Question**: How does Quarto handle multi-page websites with navigation and custom layouts?

**Findings**:
- Quarto uses `_quarto.yml` for site-wide configuration including navigation menus
- Supports website projects with automatic navigation generation
- Can define custom layouts using HTML templates and CSS
- Built-in support for responsive design and mobile-friendly output
- Native support for code syntax highlighting in blog posts

**Decision**: Use Quarto's website project type with custom CSS for the minimalist design

**Rationale**: Quarto is specifically designed for this use case and provides all needed features out of the box without requiring additional frameworks

### 2. Content Organization Pattern

**Question**: What's the best way to organize projects and blog posts in Quarto for easy maintenance?

**Findings**:
- Quarto supports listing pages that automatically aggregate content from directories
- Individual .qmd files can include YAML frontmatter for metadata (title, date, tags, description)
- Listings can be filtered, sorted, and customized via configuration
- Projects and posts can be in separate directories (projects/, posts/)

**Decision**: Use directory-based organization with YAML frontmatter for metadata

**Rationale**: Aligns with constitution's modularity principle - each content item is a separate file with clear metadata

**Alternatives Considered**:
- Single file with all content: Rejected - poor maintainability and violates modularity principle
- External CMS: Rejected - adds unnecessary complexity and violates lean architecture principle

### 3. Custom Styling Approach

**Question**: How to implement the minimalist split-layout hero design within Quarto's framework?

**Findings**:
- Quarto allows custom CSS files referenced in `_quarto.yml`
- Can use CSS Grid or Flexbox for split layouts
- Quarto generates semantic HTML that can be styled with standard CSS
- Can add custom HTML divs in .qmd files using raw HTML blocks

**Decision**: Custom CSS file (styles/styles.css) with CSS Grid for hero layout

**Rationale**: CSS-only approach keeps code minimal, maintainable, and within <50 line constraint for any helper functions

**Alternatives Considered**:
- JavaScript framework: Rejected - unnecessary complexity for static content
- Quarto theme customization: Rejected - requires understanding Quarto's Sass variables, CSS more direct

### 4. Image Optimization Strategy

**Question**: What's the recommended approach for image optimization in Quarto projects?

**Findings**:
- Quarto doesn't have built-in image optimization
- Manual optimization needed before adding to assets/
- Recommended formats: WebP for photographs, PNG for screenshots with transparency
- Standard practice: multiple sizes for responsive images

**Decision**: Manual pre-optimization of images before adding to repository

**Rationale**: Simple, one-time process that maintains constitution's lean approach without build-time complexity

**Tools**:
- ImageMagick or similar for batch conversion/compression
- Target: <500KB per image, WebP format preferred

### 5. Deployment Target Selection

**Question**: Which static hosting platform works best with Quarto sites?

**Findings**:
- **GitHub Pages**: Free, built-in GitHub Actions for Quarto
- **Netlify**: Free tier, drag-and-drop or Git integration, better build control
- **Quarto Pub**: Quarto-specific, simplest deployment (quarto publish command)

**Decision**: Document all three options in quickstart.md, recommend GitHub Pages for Git integration

**Rationale**: GitHub Pages is free, integrates with existing workflow, and has excellent Quarto support

**Alternatives Considered**:
- Vercel: Good option but GitHub Pages simpler for static Quarto sites
- Custom server: Overkill for static content

### 6. Navigation Menu Pattern

**Question**: How to implement the sticky navigation menu that works across all pages?

**Findings**:
- Quarto's `_quarto.yml` navbar configuration handles site-wide navigation
- Built-in support for sticky headers via theme options
- Can customize with CSS for specific positioning/styling needs

**Decision**: Use Quarto's built-in navbar with custom CSS for minimal styling

**Rationale**: Leverages framework features, no custom code needed

### 7. Blog Post Features

**Question**: How to implement read time estimates, syntax highlighting, and related posts?

**Findings**:
- **Syntax highlighting**: Built-in via Quarto's code block rendering (multiple themes available)
- **Read time**: Can be calculated manually and added to frontmatter, or use simple JS snippet
- **Related posts**: Requires custom logic based on tags/categories (can be manual or automated)

**Decision**: 
- Syntax highlighting: Use Quarto's default (no additional setup)
- Read time: Manual calculation and frontmatter field
- Related posts: Manual curation via frontmatter (simpler, more control)

**Rationale**: Manual approach aligns with constitution's simplicity and manual testing principles

### 8. Performance Optimization

**Question**: How to ensure <3 second page load times?

**Findings**:
- Quarto generates optimized static HTML
- Main performance factors: image sizes, CSS complexity, external resources
- No JavaScript frameworks needed = faster loads
- Can use browser DevTools for performance auditing

**Decision**: 
- Optimize all images before adding (<500KB each)
- Minimal CSS (single file)
- No external fonts or heavy libraries
- Lazy loading for images (native HTML `loading="lazy"`)

**Rationale**: Prevention better than optimization - keep assets small from the start

### 9. Accessibility Implementation

**Question**: How to ensure WCAG 2.1 Level AA compliance?

**Findings**:
- Quarto generates semantic HTML automatically (good foundation)
- Key requirements: alt text, color contrast, keyboard navigation, heading hierarchy
- Testing tools: WAVE browser extension, axe DevTools, manual keyboard testing

**Decision**: 
- Add descriptive alt text to all images in .qmd files
- Verify color contrast manually (4.5:1 minimum)
- Test keyboard navigation for all interactive elements
- Use proper heading hierarchy in content files

**Rationale**: Manual process aligns with constitution, most checks done during content creation

## Summary

All technical unknowns resolved. Quarto provides native support for all required features. Implementation will use:
- Quarto website project with custom CSS
- Directory-based content organization (projects/, posts/)
- YAML frontmatter for metadata
- Manual image optimization
- GitHub Pages for hosting
- Built-in syntax highlighting
- Manual approach for read times and related posts
- Standard semantic HTML for accessibility

No complex code or frameworks needed - aligns perfectly with constitution's lean architecture and modularity principles.
