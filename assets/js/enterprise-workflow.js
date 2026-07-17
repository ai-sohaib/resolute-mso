/**
 * Enterprise Workflow Familiarity - Interactive Animations
 * Handles KPI counter animations, visibility-triggered animations, and interactive effects
 */

(function() {
  'use strict';

  // Configuration
  const config = {
    animationDuration: 2000, // 2 seconds for KPI counter
    observerOptions: {
      threshold: 0.3,
      rootMargin: '0px'
    }
  };

  /**
   * Animate number counters when they enter viewport
   */
  function animateCounter(element, target, duration) {
    const start = 0;
    const startTime = Date.now();

    // Extract number from target (handle %, hrs, etc.)
    const numericTarget = parseInt(target.replace(/[^\d]/g, ''), 10);
    const suffix = target.replace(/[\d]/g, '');

    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Easing function: easeOutQuart
      const eased = 1 - Math.pow(1 - progress, 4);
      const current = Math.floor(start + (numericTarget - start) * eased);

      element.textContent = current + suffix;

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    animate();
  }

  /**
   * Setup Intersection Observer for KPI animations
   */
  function setupKPIObserver() {
    const kpiItems = document.querySelectorAll('.kpi-number');
    
    if (!kpiItems.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !entry.target.dataset.animated) {
          entry.target.dataset.animated = 'true';
          const targetValue = entry.target.textContent;
          animateCounter(entry.target, targetValue, config.animationDuration);
        }
      });
    }, config.observerOptions);

    kpiItems.forEach(item => observer.observe(item));
  }

  /**
   * Setup workflow diagram connection line animation
   */
  function setupWorkflowDiagramAnimation() {
    const diagram = document.querySelector('.workflow-diagram');
    if (!diagram) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.animation = 'none';
          // Trigger reflow to restart animation
          void entry.target.offsetWidth;
          entry.target.style.animation = '';
        }
      });
    }, { threshold: 0.5 });

    observer.observe(diagram);
  }

  /**
   * Add hover effects to compatibility cards
   */
  function setupCardInteractions() {
    const cards = document.querySelectorAll('.ehr-card, .lis-card');
    
    cards.forEach(card => {
      // Add smooth transition on hover
      card.addEventListener('mouseenter', function() {
        this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
      });

      // Optional: Add ripple effect on click
      card.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        ripple.style.cssText = `
          position: absolute;
          width: 20px;
          height: 20px;
          background: rgba(0, 168, 132, 0.3);
          border-radius: 50%;
          left: ${x}px;
          top: ${y}px;
          pointer-events: none;
          animation: cardRipple 0.6s ease-out;
        `;

        this.style.position = 'relative';
        this.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
      });
    });
  }

  /**
   * Setup tab-like behavior for section tabs (EHR vs LIS)
   */
  function setupSectionTabs() {
    const sections = document.querySelectorAll('[data-section]');
    if (!sections.length) return;

    sections.forEach(section => {
      section.addEventListener('click', function() {
        const sectionType = this.dataset.section;
        
        // Smooth scroll to section
        const targetSection = document.querySelector(`.${sectionType}-cards-grid`);
        if (targetSection) {
          targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  /**
   * Parallax effect for background elements
   */
  function setupParallaxEffects() {
    const container = document.querySelector('.enterprise-workflow');
    if (!container) return;

    let ticking = false;
    let scrollY = 0;

    window.addEventListener('scroll', () => {
      scrollY = window.pageYOffset;
      
      if (!ticking) {
        window.requestAnimationFrame(() => {
          const offset = (scrollY * 0.5) % 100;
          container.style.backgroundPosition = `0 ${offset}px`;
          ticking = false;
        });
        
        ticking = true;
      }
    }, { passive: true });
  }

  /**
   * Add keyboard navigation support
   */
  function setupKeyboardNavigation() {
    const cards = document.querySelectorAll('.ehr-card, .lis-card');
    
    cards.forEach((card, index) => {
      card.setAttribute('tabindex', '0');
      
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          card.click();
        }
      });
    });
  }

  /**
   * Ensure accessibility with ARIA live regions
   */
  function setupAccessibility() {
    const kpiBar = document.querySelector('.kpi-trust-bar');
    if (kpiBar) {
      kpiBar.setAttribute('aria-label', 'Key performance indicators - animated on viewport entry');
      kpiBar.setAttribute('role', 'region');
    }

    const diagram = document.querySelector('.workflow-diagram');
    if (diagram) {
      diagram.setAttribute('aria-label', 'Enterprise workflow diagram showing system integration');
      diagram.setAttribute('role', 'img');
    }
  }

  /**
   * Handle reduced motion preferences
   */
  function handleReducedMotion() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      // Disable all animations
      const style = document.createElement('style');
      style.textContent = `
        * {
          animation: none !important;
          transition: none !important;
        }
      `;
      document.head.appendChild(style);
    }
  }

  /**
   * Initialize all interactive features
   */
  function init() {
    // Wait for DOM to be fully loaded
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initFeatures);
    } else {
      initFeatures();
    }
  }

  function initFeatures() {
    handleReducedMotion();
    setupKPIObserver();
    setupWorkflowDiagramAnimation();
    setupCardInteractions();
    setupSectionTabs();
    setupParallaxEffects();
    setupKeyboardNavigation();
    setupAccessibility();
  }

  // Initialize when script loads
  init();

  // Export for testing if needed
  if (typeof window !== 'undefined') {
    window.EnterpriseWorkflow = {
      animateCounter,
      setupKPIObserver,
      setupWorkflowDiagramAnimation
    };
  }
})();
