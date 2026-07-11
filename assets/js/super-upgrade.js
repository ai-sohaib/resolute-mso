(function(){
  "use strict";
  var tiltSelectors = [".card",".service-card",".visual-panel",".photo-panel",".impact-panel",".snapshot-item",".line-card",".contact-card",".blog-card",".resource-card",".specialty-card",".outcome-card",".outcome-table",".roi-card",".chart-card",".outcome-visual",".cta-slab"];
  var prefersReduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function clamp(n,min,max){ return Math.max(min, Math.min(max, n)); }
  function setPointerVars(el, event){
    var rect = el.getBoundingClientRect();
    var x = event.clientX - rect.left;
    var y = event.clientY - rect.top;
    var mx = clamp(x / rect.width * 100, 0, 100);
    var my = clamp(y / rect.height * 100, 0, 100);
    el.style.setProperty("--mx", mx + "%");
    el.style.setProperty("--my", my + "%");
    if(!prefersReduced){
      var ry = ((x / rect.width) - .5) * 6;
      var rx = -(((y / rect.height) - .5) * 6);
      el.style.setProperty("--rx", clamp(rx,-5,5) + "deg");
      el.style.setProperty("--ry", clamp(ry,-5,5) + "deg");
    }
  }
  tiltSelectors.forEach(function(sel){
    Array.prototype.slice.call(document.querySelectorAll(sel)).forEach(function(el){
      el.addEventListener("pointermove", function(e){ setPointerVars(el,e); }, {passive:true});
      el.addEventListener("pointerleave", function(){ el.style.removeProperty("--rx"); el.style.removeProperty("--ry"); }, {passive:true});
    });
  });
  Array.prototype.slice.call(document.querySelectorAll(".btn")).forEach(function(el){
    el.classList.add("magnetic-cta");
    el.addEventListener("pointermove", function(e){ setPointerVars(el,e); }, {passive:true});
  });
  function animateCount(el){
    var target = parseFloat(el.getAttribute("data-count-to") || "0");
    var suffix = el.getAttribute("data-count-suffix") || "";
    var prefix = el.getAttribute("data-count-prefix") || "";
    var start = 0;
    var duration = 1100;
    var begin = performance.now();
    function tick(now){
      var p = Math.min(1, (now-begin)/duration);
      var eased = 1 - Math.pow(1-p, 3);
      var val = Math.round((start + (target-start)*eased) * 10) / 10;
      el.textContent = prefix + val + suffix;
      if(p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  if("IntersectionObserver" in window){
    var observer = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){
          Array.prototype.slice.call(entry.target.querySelectorAll("[data-count-to]")).forEach(animateCount);
          observer.unobserve(entry.target);
        }
      });
    }, {threshold:.22});
    Array.prototype.slice.call(document.querySelectorAll(".provider-outcomes,.comparison-strip")).forEach(function(el){observer.observe(el);});
  } else {
    Array.prototype.slice.call(document.querySelectorAll("[data-count-to]")).forEach(animateCount);
  }
  // Smooth section highlight from internal nav clicks
  Array.prototype.slice.call(document.querySelectorAll('a[href^="#"]')).forEach(function(a){
    a.addEventListener('click', function(){
      var target = document.querySelector(a.getAttribute('href'));
      if(!target) return;
      target.classList.add('glow-line');
      window.setTimeout(function(){ target.classList.remove('glow-line'); }, 1500);
    });
  });
})();
