
document.addEventListener('DOMContentLoaded', function() {
  // Theme Toggle
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const themeIcon = themeToggleBtn.querySelector('i');
  
  // Check for saved theme preference or use the default one
  const savedTheme = localStorage.getItem('theme') || 'light';
  
  // Apply the saved theme on page load
  if (savedTheme === 'dark') {
    document.body.classList.add('dark-mode');
    themeIcon.classList.remove('fa-moon');
    themeIcon.classList.add('fa-sun');
  }
  
  // Toggle theme when the button is clicked
  themeToggleBtn.addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    
    // Update the theme icon
    if (document.body.classList.contains('dark-mode')) {
      themeIcon.classList.remove('fa-moon');
      themeIcon.classList.add('fa-sun');
      localStorage.setItem('theme', 'dark');
    } else {
      themeIcon.classList.remove('fa-sun');
      themeIcon.classList.add('fa-moon');
      localStorage.setItem('theme', 'light');
    }
  });
  
  // Back to top button
  const backToTopBtn = document.getElementById('back-to-top-btn');
  
  // Show/hide back to top button based on scroll position
  window.addEventListener('scroll', function() {
    if (window.pageYOffset > 300) {
      backToTopBtn.style.opacity = '1';
    } else {
      backToTopBtn.style.opacity = '0';
    }
  });
  
  // Smooth scroll for table of contents links
  const tocLinks = document.querySelectorAll('.table-of-contents a');
  
  tocLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      const targetSection = document.querySelector(targetId);
      
      if (targetSection) {
        window.scrollTo({
          top: targetSection.offsetTop - 80,
          behavior: 'smooth'
        });
      }
    });
  });
  
  // Intersection Observer for scroll animations
  const sections = document.querySelectorAll('.article-section');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        
        // Highlight the corresponding TOC link
        const id = entry.target.getAttribute('id');
        document.querySelectorAll('.table-of-contents a').forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === '#' + id) {
            link.classList.add('active');
          }
        });
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '-100px 0px -100px 0px'
  });
  
  sections.forEach(section => {
    observer.observe(section);
  });
  
  // Add a class to style the active TOC link
  const style = document.createElement('style');
  style.innerHTML = `
    .table-of-contents a.active {
      color: var(--primary);
      font-weight: bold;
      transform: translateX(5px);
    }
    
    #back-to-top-btn {
      opacity: 0;
      transition: opacity 0.3s ease;
    }
  `;
  document.head.appendChild(style);
});

// Add a smooth reveal effect when the page loads
window.addEventListener('load', function() {
  document.body.classList.add('loaded');
  
  // Add a style for the loaded state
  const style = document.createElement('style');
  style.innerHTML = `
    body.loaded .hero, 
    body.loaded .table-of-contents {
      animation: fadeIn 0.8s ease-out forwards;
    }
  `;
  document.head.appendChild(style);
});
