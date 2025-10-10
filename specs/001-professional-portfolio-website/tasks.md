# Tasks: Professional Portfolio Website

**Feature**: Professional Portfolio Website  
**Input**: Design documents from `/specs/001-professional-portfolio-website/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Per project constitution, NO automated test tasks will be created. All testing is manual.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Static website structure - all files at repository root:

- `_quarto.yml` - Site configuration
- `index.qmd` - Home page
- `projects.qmd` - Projects listing
- `blog.qmd` - Blog listing
- `projects/*.qmd` - Individual project pages
- `posts/*.qmd` - Individual blog posts
- `assets/` - Images, resume, static files
- `styles/styles.css` - Custom CSS

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure needed by all user stories

- [X] T001 Activate my_website conda environment and verify Python 3.12
- [X] T002 Install Quarto (system install, not via conda - download from quarto.org)
- [X] T003 [P] Create directory structure: projects/, posts/, assets/images/, styles/
- [X] T004 [P] Create .gitignore to exclude _site/, .quarto/, and other generated files
- [X] T005 Update environment.yml to document any additional dependencies

**Checkpoint**: ✅ Project structure ready - user story implementation can begin

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Create _quarto.yml with basic website configuration (title, navbar structure, output-dir)
- [X] T007 Configure _quarto.yml navbar with navigation items: Home, Projects, Blog
- [X] T008 Create styles/styles.css with base styles (colors, typography, CSS variables)
- [X] T009 Add hero section split layout styles to styles/styles.css (60/40 grid layout)
- [X] T010 Add responsive breakpoints to styles/styles.css for mobile (<768px)

**Checkpoint**: ✅ Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Professional Profile Discovery (Priority: P1) 🎯 MVP

**Goal**: Visitor can learn about the professional's background, expertise, and contact them

**Independent Test**: Navigate to home page and verify profile info, contact links, and resume are visible and functional

### Implementation for User Story 1

- [X] T011 [P] [US1] Create index.qmd with YAML frontmatter (name, title, tagline, profile_image, resume_file, email, linkedin_url, github_url)
- [X] T012 [P] [US1] Add hero section to index.qmd with name, title, tagline, CTA button, and profile image
- [X] T013 [P] [US1] Add about section to index.qmd with 2-3 paragraph bio content
- [X] T014 [P] [US1] Add contact links section to index.qmd (email, LinkedIn, GitHub) with target="_blank" for external links
- [X] T015 [P] [US1] Add resume download link to index.qmd
- [X] T016 [P] [US1] Add placeholder profile image to assets/images/profile.jpg (or use actual photo)
- [X] T017 [P] [US1] Add resume PDF to assets/CV_Rodrigo_Grandy.pdf (or placeholder)
- [X] T018 [US1] Style hero section in styles/styles.css (grid layout, typography, spacing)
- [X] T019 [US1] Style about section in styles/styles.css (background color, padding, typography)
- [X] T020 [US1] Style contact links in styles/styles.css (button/link appearance)
- [X] T021 [US1] Add mobile responsive styles for hero and about sections (<768px breakpoint)
- [X] T022 [US1] Verify all content displays correctly: Run `quarto preview` and check home page
- [ ] T023 [US1] Test contact links open correctly (email, LinkedIn, GitHub in new tabs)
- [ ] T024 [US1] Test resume downloads successfully
- [ ] T025 [US1] Test mobile responsiveness at 320px, 768px, 1024px widths
- [ ] T026 [US1] Verify color contrast meets 4.5:1 ratio using browser DevTools
- [ ] T027 [US1] Test keyboard navigation works for all links and buttons

**Checkpoint**: ✅ User Story 1 IMPLEMENTED - Manual testing required before marking complete

---

## Phase 4: User Story 2 - Project Portfolio Exploration (Priority: P2)

**Goal**: Visitor can browse and explore professional work examples

**Independent Test**: Navigate to projects page, view project cards, click into individual projects, verify all details and navigation work

### Implementation for User Story 2

- [X] T028 [P] [US2] Create projects.qmd with YAML frontmatter for listing configuration (contents: projects, type: grid, sort, filter-ui, categories)
- [X] T029 [P] [US2] Add introductory content to projects.qmd page
- [X] T030 [P] [US2] Create first project file projects/project-1.qmd with complete YAML frontmatter (title, description_brief, date_completed, technologies, categories, hero_image, github_url)
- [X] T031 [P] [US2] Add Problem, Solution, Technologies, and Outcomes sections to projects/project-1.qmd
- [X] T032 [P] [US2] Create second project file projects/project-2.qmd with complete YAML and content
- [X] T033 [P] [US2] Create third project file projects/project-3.qmd with complete YAML and content
- [X] T034 [P] [US2] Add project images to assets/images/ (hero images and screenshots for 3 projects)
- [X] T035 [P] [US2] Mark one project as featured: true in its YAML frontmatter
- [X] T036 [US2] Add featured project section to index.qmd (below about section)
- [X] T037 [US2] Style featured project section in styles/styles.css (card layout, image, text)
- [X] T038 [US2] Style project cards in styles/styles.css (grid layout, card design, hover effects)
- [X] T039 [US2] Style individual project pages in styles/styles.css (hero image, content sections, back button)
- [X] T040 [US2] Add mobile responsive styles for project cards and pages
- [X] T041 [US2] Add "Back to Projects" navigation link to project template
- [X] T042 [US2] Verify projects page displays grid of 3 projects: Run `quarto preview`
- [ ] T043 [US2] Test clicking project cards navigates to individual project pages
- [ ] T044 [US2] Test featured project displays correctly on home page
- [ ] T045 [US2] Test "Back to Projects" navigation works
- [ ] T046 [US2] Test project filtering by technology/category (if implemented)
- [ ] T047 [US2] Test GitHub/demo links open in new tabs
- [ ] T048 [US2] Test all project images load with alt text
- [ ] T049 [US2] Test mobile responsiveness of project cards and pages

**Checkpoint**: ✅ User Story 2 IMPLEMENTED - Manual testing required before marking complete

---

## Phase 5: User Story 3 - Technical Content Reading (Priority: P3)

**Goal**: Visitor can read technical blog posts and explore topics

**Independent Test**: Navigate to blog page, view post previews, click into posts, verify formatting and navigation work

### Implementation for User Story 3

- [X] T050 [P] [US3] Create blog.qmd with YAML frontmatter for listing configuration (contents: posts, type: default, sort: date desc, filter-ui, categories)
- [X] T051 [P] [US3] Add introductory content to blog.qmd page
- [X] T052 [P] [US3] Create first blog post posts/2025-01-15-first-post.qmd with complete YAML frontmatter (title, author, date, description, read_time, categories, tags)
- [X] T053 [P] [US3] Add content to first blog post with markdown, code blocks, and syntax highlighting examples
- [X] T054 [P] [US3] Create second blog post posts/2025-02-20-second-post.qmd with YAML and content (optional - can launch with 1 post)
- [X] T055 [P] [US3] Add blog post featured image to assets/images/ (optional)
- [X] T056 [US3] Style blog post previews in styles/styles.css (list layout, meta info, excerpts)
- [X] T057 [US3] Style individual blog post pages in styles/styles.css (typography, code blocks, back button)
- [X] T058 [US3] Add mobile responsive styles for blog listing and posts
- [X] T059 [US3] Add "Back to Blog" navigation link to post template
- [X] T060 [US3] Verify blog page displays post listing: Run `quarto preview`
- [ ] T061 [US3] Test clicking post preview navigates to full post
- [ ] T062 [US3] Test code syntax highlighting renders correctly
- [ ] T063 [US3] Test "Back to Blog" navigation works
- [ ] T064 [US3] Test blog post filtering by categories/tags (if implemented)
- [ ] T065 [US3] Test read time displays correctly
- [ ] T066 [US3] Test mobile responsiveness of blog pages

**Checkpoint**: ✅ User Story 3 IMPLEMENTED - Manual testing required before marking complete

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final touches, optimization, and deployment preparation

- [ ] T067 [P] Optimize all images: compress to <500KB each, convert to WebP if possible
- [ ] T068 [P] Add descriptive alt text to all images across all pages
- [ ] T069 [P] Verify all page titles are descriptive and unique in YAML frontmatter
- [ ] T070 [P] Add meta descriptions to all main pages (_quarto.yml or page frontmatter)
- [ ] T071 [P] Add favicon/logo to assets/ and configure in _quarto.yml (optional)
- [ ] T072 Verify semantic HTML structure: proper heading hierarchy (h1 → h2 → h3)
- [ ] T073 Run full site build: `quarto render` and verify no errors
- [ ] T074 Test all internal links work (home ↔ projects ↔ blog)
- [ ] T075 Test all external links open in new tabs
- [ ] T076 Test keyboard navigation works across entire site
- [ ] T077 Measure page load times with browser DevTools (target <3 seconds)
- [ ] T078 Test site on multiple browsers (Chrome, Firefox, Safari)
- [ ] T079 Test site at various viewport widths (320px, 768px, 1024px, 1920px)
- [ ] T080 Run accessibility audit with WAVE browser extension or axe DevTools
- [ ] T081 Fix any accessibility violations identified
- [ ] T082 Review and update .gitignore to exclude _site/ and build artifacts
- [ ] T083 Commit all source files (.qmd, .yml, .css, assets) to Git
- [ ] T084 Choose deployment platform (GitHub Pages, Netlify, or Quarto Pub)
- [ ] T085 Configure deployment (see quickstart.md for platform-specific steps)
- [ ] T086 Deploy site and verify production deployment works
- [ ] T087 Test production site: all pages, links, images, downloads
- [ ] T088 Share site with 3-5 peers for feedback
- [ ] T089 Address feedback and iterate if needed

**Checkpoint**: Site complete, polished, and deployed. Ready for launch! 🚀

---

## Task Dependencies & Execution Strategy

### Critical Path (Must Complete in Order)

```text
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
Phase 3 (User Story 1 - MVP) ← FIRST COMPLETE, INDEPENDENTLY TESTABLE
    ↓
Phase 4 (User Story 2)       ← SECOND COMPLETE, INDEPENDENTLY TESTABLE
    ↓
Phase 5 (User Story 3)       ← THIRD COMPLETE, INDEPENDENTLY TESTABLE
    ↓
Phase 6 (Polish & Deploy)
```

### User Story Independence

- **US1 (Profile)**: Can be completed and deployed standalone - this is the MVP
- **US2 (Projects)**: Independent of US3, depends only on US1 for home page integration
- **US3 (Blog)**: Independent of US2, can be skipped at launch if needed

### Parallel Execution Opportunities

#### Phase 1 (Setup)
- T003, T004, T005 can run in parallel (different directories/files)

#### Phase 2 (Foundational)
- T006-T007 must be sequential (same file: _quarto.yml)
- T008-T010 must be sequential (same file: styles.css)

#### Phase 3 (User Story 1)
- T011-T017 can run in parallel (different files/assets)
- T018-T021 must be sequential (same file: styles.css)
- T022-T027 must be sequential (testing/verification)

#### Phase 4 (User Story 2)
- T028-T034 can run in parallel (different files/assets)
- T037-T040 must be sequential (same file: styles.css)
- T042-T049 must be sequential (testing/verification)

#### Phase 5 (User Story 3)
- T050-T055 can run in parallel (different files/assets)
- T056-T058 must be sequential (same file: styles.css)
- T060-T066 must be sequential (testing/verification)

#### Phase 6 (Polish)
- T067-T071 can run in parallel (different files/content)
- T072-T089 generally sequential (testing, deployment)

### Implementation Strategy

**Recommended MVP Approach** (Minimum Viable Product):

1. Complete Phase 1 (Setup) + Phase 2 (Foundational) → Site infrastructure ready
2. Complete Phase 3 (User Story 1) → **MVP COMPLETE** - Deploy and share!
3. Add Phase 4 (User Story 2) → Enhanced portfolio with project showcase
4. Add Phase 5 (User Story 3) → Full-featured site with blog
5. Polish with Phase 6 → Production-ready, optimized site

**Incremental Delivery Benefits**:
- Ship MVP faster (just US1)
- Get early feedback on design and content
- Validate deployment process with minimal content
- Add projects and blog incrementally based on content availability

### Constitution Compliance Notes

- ✅ All work in my_website conda environment (T001)
- ✅ No automated tests (manual testing only per constitution)
- ✅ Modular structure (separate .qmd files per content item)
- ✅ No code >50 lines needed (Quarto is declarative configuration)
- ✅ Task-focused (no extraneous tasks)

---

## Task Summary

**Total Tasks**: 89

**By Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 5 tasks
- Phase 3 (US1 - Profile): 17 tasks
- Phase 4 (US2 - Projects): 22 tasks
- Phase 5 (US3 - Blog): 17 tasks
- Phase 6 (Polish): 23 tasks

**By User Story**:
- User Story 1 (Profile): 17 tasks → MVP deliverable
- User Story 2 (Projects): 22 tasks → Enhanced portfolio
- User Story 3 (Blog): 17 tasks → Full-featured site

**Parallel Opportunities**: 23 tasks marked [P] can run in parallel within their phase

**Testing Strategy**: Manual testing integrated into each user story phase (no automated tests per constitution)

**MVP Scope**: Phases 1-3 (27 tasks) deliver a functional portfolio with profile and contact information

---

## Next Steps

1. Start with Phase 1 (Setup) to prepare the development environment
2. Complete Phase 2 (Foundational) to establish site infrastructure
3. Focus on Phase 3 (User Story 1) for MVP - this delivers immediate value
4. Preview frequently with `quarto preview` during development
5. Test each phase completion against the independent test criteria
6. Deploy MVP after Phase 3 for early feedback
7. Add Phases 4-5 incrementally as content becomes available
8. Polish and optimize in Phase 6 before final launch

Reference: See `/specs/001-professional-portfolio-website/quickstart.md` for detailed development workflow and commands.
