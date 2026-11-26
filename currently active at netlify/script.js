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
    if (menuBtn) menuBtn.setAttribute('aria-expanded', 'true');
  }
  
  // Function to close menu
  function closeMenu() {
    sidebar.classList.remove('active');
    overlay.style.display = 'none';
    document.body.style.overflow = ''; // Allow scrolling
    if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');
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
    if (event.key === 'Escape' && sidebar && sidebar.classList.contains('active')) {
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


/* ------------------------------------------------------------------
   Shared helper for the "particle" button effects.
   - Mouse: particles spawn while hovering (same as before).
   - Touch/pen: a short burst on tap, so nothing keeps spawning after
     a finger leaves (touch screens have no real "mouseleave").
------------------------------------------------------------------- */
function attachParticleEffect(btn, spawn, intervalMs, touchBurst) {
  let timer = null;
  const stop = () => {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  };

  btn.addEventListener('pointerenter', (e) => {
    if (e.pointerType !== 'mouse') return;
    spawn();
    stop();
    timer = setInterval(spawn, intervalMs);
  });

  btn.addEventListener('pointerleave', stop);

  btn.addEventListener('pointerdown', (e) => {
    if (e.pointerType === 'mouse' || !touchBurst) return;
    for (let i = 0; i < touchBurst; i++) {
      setTimeout(spawn, i * 120);
    }
  });
}


// 🎵 Musical Chair button
(function () {
  const btn = document.getElementById('musicalChairBtn');
  if (!btn) return;
  const notesContainer = btn.querySelector('.notes-container');
  const noteChars = ['🎵', '🎶', '🎼'];

  function spawnNote() {
    const note = document.createElement('span');
    note.className = 'note';
    note.textContent = noteChars[Math.floor(Math.random() * noteChars.length)];
    note.style.left = (10 + Math.random() * 80) + '%';
    note.style.setProperty('--drift', (Math.random() * 40 - 20) + 'px');
    note.style.animationDuration = (1.2 + Math.random() * 0.6) + 's';
    notesContainer.appendChild(note);
    setTimeout(() => note.remove(), 2000);
  }

  attachParticleEffect(btn, spawnNote, 350, 4);
})();


// 🎄 Christmas games button
(function () {
  const button = document.getElementById('icy-btn');
  if (!button) return;

  function createSnowflake() {
    const snowflake = document.createElement('div');
    snowflake.className = 'icy-snowflake';
    snowflake.innerHTML = '❄';

    const buttonRect = button.getBoundingClientRect();
    const startX = Math.random() * Math.max(buttonRect.width - 20, 0);
    snowflake.style.left = startX + 'px';
    snowflake.style.top = '0px';

    const duration = Math.random() * 2 + 2;
    snowflake.style.animationDuration = duration + 's';

    const size = Math.random() * 8 + 8;
    snowflake.style.fontSize = size + 'px';

    button.appendChild(snowflake);

    setTimeout(() => {
      snowflake.remove();
    }, duration * 1000);
  }

  attachParticleEffect(button, createSnowflake, 100, 8);

  button.addEventListener('click', () => {
    window.open('https://santatracker.google.com/', '_blank', 'noopener');
  });
})();


// 🎮 Friend Group Games button
(function () {
  const button = document.getElementById('friend-games-btn');
  if (!button) return;

  const particles = ['🎲', '🎯', '🃏', '❓', '😂', '🔥', '⭐', '🎮', '🏆', '👀'];

  function createParticle() {
    const particle = document.createElement('span');

    particle.className = 'fgb-particle';
    particle.textContent = particles[Math.floor(Math.random() * particles.length)];

    particle.style.left = (Math.random() * 85 + 7) + '%';
    particle.style.bottom = (Math.random() * 10 + 15) + 'px';
    particle.style.setProperty('--drift', (Math.random() * 100 - 50) + 'px');
    particle.style.setProperty('--rotation', (Math.random() * 80 - 40) + 'deg');
    particle.style.animationDuration = (Math.random() * 0.8 + 1.4) + 's';

    button.appendChild(particle);

    setTimeout(() => {
      particle.remove();
    }, 2200);
  }

  // Hover effect for mouse users (taps already get the click burst below)
  attachParticleEffect(button, createParticle, 180, 0);

  button.addEventListener('click', () => {
    // Small click burst
    for (let i = 0; i < 6; i++) {
      setTimeout(createParticle, i * 45);
    }

    // Open the friend-group game hub (opened immediately so phones don't block the popup)
    window.open('FriendGroupGames.html', '_blank');
  });
})();