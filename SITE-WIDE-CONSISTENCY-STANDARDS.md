# Resolute MSO - Site-Wide Consistency Standards

## Design System Foundation

### Color System

**Primary Palette**
```
--navy: #073456          (Primary text, headings)
--midnight: #0b4c6f      (Dark accents)
--ink: #07253f           (Body text)
--teal: #00a884          (Primary CTA, emphasis)
--cyan: #1877f2          (Secondary CTA, features)
--emerald: #11b981       (Success states)
--soft: #f6fbff          (Light backgrounds)
--line: #d9edf5          (Borders)
--muted: #527086         (Secondary text)
--white: #fff            (White)
```

**Usage Guidelines**
- Primary Actions: teal (#00a884)
- Secondary Actions: cyan (#1877f2)
- Text Hierarchy: navy (headings) → ink (body) → muted (secondary)
- Backgrounds: soft (#f6fbff) for light sections
- Borders: line (#d9edf5) for all dividers

---

## Spacing System

**Consistent Units** (Base 8px grid)
```
Minimal:  4px, 8px
Small:    12px, 16px
Medium:   20px, 24px
Large:    32px, 40px
Huge:     48px, 56px, 64px
Section:  88px (padding top/bottom)
```

**Application Rules**
- Padding inside cards: 20px, 28px, 32px
- Margin between sections: 48px, 56px, 72px
- Gap in grids: 16px (default), 24px (spacious)
- Container padding: 40px (horizontal)

---

## Typography

**Font Stack**
```
Heading: 'Poppins', Inter, 'Segoe UI', Arial, sans-serif
Body:    Inter, 'Segoe UI', Roboto, Arial, sans-serif
Weight:  400 (regular), 600 (semibold), 700 (bold), 900 (extra-bold)
```

**Scale**
- H1: 2.5rem (40px) - Page title
- H2: 2rem (32px) - Section headline
- H3: 1.3rem (20px) - Card title
- Body: 1rem (16px) - Default text
- Small: 0.95rem (15px) - Secondary text
- Label: 0.8rem (12px) - Tags, badges

**Line Height**
- Headings: 1.2
- Body: 1.6
- Compact: 1.4

---

## Border Radius System

**Consistent Values**
```
Small:   8px    (buttons, small elements)
Medium:  12px   (form inputs, small cards)
Large:   16px   (medium components)
XLarge:  20px   (cards, panels)
XXLarge: 24px   (large containers)
Round:   999px  (pills, badges)
```

**Application**
- Buttons: 14px
- Form inputs: 12px
- Cards: 20px
- Large containers: 24px
- Badges/pills: 999px

---

## Shadow System

**Shadow Tiers**
```
Light:    0 8px 20px rgba(7, 52, 86, 0.08)
Medium:   0 12px 32px rgba(7, 52, 86, 0.12)
Standard: 0 16px 45px rgba(7, 52, 86, 0.08)
Strong:   0 24px 64px rgba(7, 52, 86, 0.24)
Glow:     0 24px 62px rgba(0, 168, 132, 0.18)
```

**Usage**
- Hover state: use one tier stronger
- Floating elements: Strong
- Cards: Standard
- Subtle backgrounds: Light

---

## Animation & Motion

**Transition Timing**
```
Fast:     200ms
Standard: 250ms
Slow:     300-500ms
Default:  cubic-bezier(0.4, 0, 0.2, 1) [ease-out-quart]
```

**Animation Rules**
- All transitions use cubic-bezier(0.4, 0, 0.2, 1) by default
- Hover states: 200-250ms
- Page transitions: 300-500ms
- Entrance animations: 0.6s with stagger
- Respect `prefers-reduced-motion` media query

**Common Animations**
```javascript
// Fade in on scroll
animation: fadeIn 0.6s ease-out forwards;

// Slide up on scroll
animation: slideUp 0.6s ease-out forwards;

// Hover lift
transform: translateY(-8px); /* 250ms transition */

// Stagger children
animation-delay: calc(50ms * var(--index));
```

---

## Button Styles

**Primary Button (CTA)**
- Background: linear-gradient(135deg, #00a884, #1877f2)
- Color: white
- Border-radius: 14px
- Padding: 14px 28px
- Font-weight: 600
- Box-shadow: 0 16px 38px rgba(24, 119, 242, 0.18)
- Hover: transform translateY(-2px), stronger shadow

**Secondary Button**
- Background: transparent
- Border: 1px solid #d8edf5
- Color: #00a884
- Border-radius: 14px
- Padding: 12px 24px
- Hover: background #ecfff9

**Ghost Button (Light)**
- Background: transparent
- Color: #007c70
- Border: 1px solid #bdeee3
- Hover: background #ecfff9

---

## Card Components

**Standard Card**
```css
background: #fff;
border: 1px solid #d8edf5;
border-radius: 20px;
padding: 28px;
box-shadow: 0 12px 32px rgba(7, 52, 86, 0.08);
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

**Card Hover**
```css
transform: translateY(-8px);
border-color: #00a884;
box-shadow: 0 20px 56px rgba(0, 168, 132, 0.18);
```

**Card Variants**
- Info Card: background gradient, no shadow
- Featured Card: top accent border (4px)
- Minimal Card: no border, light background

---

## Grid & Layout

**Responsive Breakpoints**
```
Mobile:       480px and down
Tablet:       481px to 768px
Desktop:      769px to 1200px
Wide:         1201px and up
Container:    max 1180px width, 40px horizontal padding
```

**Grid Patterns**
- 1-column: Mobile (480px and down)
- 2-column: Tablet (600px and up)
- 3-column: Desktop (768px and up)
- 4-column: Wide (1000px and up)

**Gap Values**
- Mobile: 12px, 16px
- Tablet: 16px, 20px
- Desktop: 20px, 24px, 28px

---

## Navigation & Header

**Header Specification**
- Position: sticky top
- Height: 76px (min-height)
- Background: rgba(255, 255, 255, 0.97) with backdrop-filter blur(18px)
- Border-bottom: 1px solid rgba(215, 231, 246, 0.9)
- Box-shadow: 0 10px 32px rgba(7, 52, 86, 0.08)

**Navigation Links**
- Hover background: #eafbf8
- Hover color: #007c70
- Font-size: 0.95rem
- Transition: 200ms

**Mobile Menu Button**
- Always consistent color & styling
- Hamburger icon consistency
- Transition timing: 250ms

---

## Forms & Inputs

**Input Field**
```css
background: #fff;
border: 1px solid #d8edf5;
border-radius: 12px;
padding: 14px 16px;
font-size: 1rem;
font-family: inherit;
transition: all 200ms ease;
```

**Input Focus**
```css
border-color: #00a884;
box-shadow: 0 0 0 3px rgba(0, 168, 132, 0.1);
```

**Input Hover**
```css
border-color: #00a884;
box-shadow: 0 8px 20px rgba(7, 52, 86, 0.12);
```

---

## Icons

**Sizing System**
```
Extra Small:  16px (16x16) - inline text
Small:        20px (20x20) - small badges
Standard:     24px (24x24) - default (1.25rem in CSS)
Medium:       32px (32x32) - medium components
Large:        40px (40x40) - hero elements
Extra Large:  56px (56x56) - section icons
```

**SVG Properties**
```css
stroke: currentColor;
stroke-width: 2;
fill: none;
stroke-linecap: round;
stroke-linejoin: round;
```

**Color Usage**
- Primary: inherit from --teal
- Secondary: inherit from --cyan
- Neutral: inherit from --muted
- Change on hover using CSS color property

---

## Section Structure

**Standard Section**
```html
<section class="section">
  <div class="container">
    <!-- Content -->
  </div>
</section>
```

**Section Variants**
- `.section`: default white, padding 88px 0
- `.section-soft`: light gradient background
- `.section-dark`: enterprise gradient
- `.section-soft-dark`: subtle dark background

**Spacing**
- Top padding: 88px
- Bottom padding: 88px
- Between elements: 24px, 32px, 48px

---

## Component Consistency Checklist

### Before Shipping Any Page Component:

✅ **Color**
- Text uses navy, ink, or muted
- Links use teal or cyan
- Accents match primary palette

✅ **Spacing**
- All padding/margin from spacing system
- Consistent gaps in grids
- 88px section padding

✅ **Typography**
- Font stack is consistent
- Weight values: 400, 600, 700, 900 only
- Line-height matches scale

✅ **Shadows**
- Uses shadow tier system
- Consistent hover elevation

✅ **Border Radius**
- Uses radius system (8px, 12px, 16px, 20px, 24px, 999px)
- No arbitrary values

✅ **Animation**
- Uses 200-250ms standard timing
- Uses cubic-bezier(0.4, 0, 0.2, 1)
- Respects prefers-reduced-motion

✅ **Responsive**
- Breakpoints: 480px, 768px, 1000px, 1200px
- Mobile-first approach
- Touch targets: 44px minimum

✅ **Accessibility**
- Semantic HTML
- ARIA labels where needed
- Color not only distinguisher
- Focus states visible

---

## CSS File Organization

**Global Styles**
```
/assets/css/styles.css          - Base styles, CSS variables
/assets/css/free-audit-modal.css - Modal component
```

**Page-Specific Styles**
```
/assets/css/pagespeed-home.css           - Homepage critical CSS
/assets/css/enterprise-product-hero.css  - Product hero component
/assets/css/enterprise-workflow.css      - Workflow section (NEW)
```

**Theme & Polish**
```
/assets/css/resolute-minimal-theme.css   - Theme overrides
/assets/css/medcare-footer.css           - Footer styling
```

---

## Implementation Examples

### Card with Hover
```css
.card {
  background: #fff;
  border: 1px solid #d8edf5;
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0 12px 32px rgba(7, 52, 86, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
  transform: translateY(-8px);
  border-color: #00a884;
  box-shadow: 0 20px 56px rgba(0, 168, 132, 0.18);
}
```

### Responsive Grid
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

@media (max-width: 768px) {
  .grid {
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
  }
}
```

### Animation on Scroll
```css
.animated-element {
  opacity: 0;
  animation: fadeIn 0.6s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile Safari 14+

**CSS Features Used**
- CSS Grid
- Flexbox
- CSS Custom Properties
- backdrop-filter
- transform/animation
- nth-child

---

## Performance Considerations

- Reduce animations with `prefers-reduced-motion`
- Use `defer` for non-critical scripts
- Lazy-load images
- Minimize critical CSS
- Use CSS variables for theming
- Avoid layout thrashing in animations

---

## Migration Guide

### For Existing Pages:

1. **Replace custom colors** with CSS variables from color system
2. **Update spacing** to nearest standard value
3. **Standardize shadows** using shadow tier system
4. **Align border-radius** to system values
5. **Use standard button styles**
6. **Apply consistent typography scale**
7. **Ensure responsive breakpoints** match system
8. **Add animation timing** with standard values
9. **Test accessibility** with WCAG guidelines
10. **Verify mobile hamburger** styling consistency

---

## Maintenance

**CSS File Size Targets**
- Global: < 50KB gzipped
- Per-page: < 30KB gzipped
- Unused CSS removal quarterly

**Update Process**
- Version all component CSS files (e.g., ?v=20260716)
- Test across all pages before deployment
- Document breaking changes in this guide
- Maintain backward compatibility where possible

---

## Contact & Questions

For component requests or design system updates:
- Check this guide first
- Review existing implementations
- Follow established patterns
- Test across all devices before shipping

