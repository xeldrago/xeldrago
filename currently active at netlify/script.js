// Wait for the DOM to fully load
document.addEventListener('DOMContentLoaded', function() {
  // Get DOM elements
  const menuBtn = document.getElementById('menuBtn');
  const closeMenuBtn = document.getElementById('closeMenu');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('menuOverlay');
  const scrollToContentBtn = document.getElementById('scrollToContent');
  const alternateNetflixBtn = document.getElementById('alternateNetflix');
  const demoElement = document.getElementById('demo');
  const currentYearElement = document.querySelectorAll('.copyright #currentYear');
  
  // Set current year in footer
  currentYearElement.forEach(element => {
    if (element) {
      element.textContent = new Date().getFullYear();
    }
  });
  
  // Function to open menu
  function openMenu() {
    sidebar.classList.add('active');
    overlay.style.display = 'block';
    document.body.style.overflow = 'hidden'; // Prevent scrolling
  }
  
  // Function to close menu
  function closeMenu() {
    sidebar.classList.remove('active');
    overlay.style.display = 'none';
    document.body.style.overflow = ''; // Allow scrolling
  }
  
  // Add event listeners for menu
  if (menuBtn) {
    menuBtn.addEventListener('click', openMenu);
  }
  
  if (closeMenuBtn) {
    closeMenuBtn.addEventListener('click', closeMenu);
  }
  
  if (overlay) {
    overlay.addEventListener('click', closeMenu);
  }
  
  // Close menu when ESC key is pressed
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && sidebar.classList.contains('active')) {
      closeMenu();
    }
  });
  
  // Scroll to content section
  if (scrollToContentBtn) {
    scrollToContentBtn.addEventListener('click', function() {
      const contentSection = document.getElementById('content');
      if (contentSection) {
        contentSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }
  
  // Update demo text when Netflix alternative is clicked
  if (alternateNetflixBtn) {
    alternateNetflixBtn.addEventListener('click', function() {
      if (demoElement) {
        demoElement.innerHTML = "search on google: 'myflixer'";
      }
    });
  }
});
