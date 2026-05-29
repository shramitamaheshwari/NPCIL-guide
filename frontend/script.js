// ── NAVBAR SCROLL EFFECT ──
const navbar = document.getElementById('navbar');
const backToTop = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
  if (window.scrollY > 60) {
    navbar.classList.add('scrolled');
    backToTop.classList.add('visible');
  } else {
    navbar.classList.remove('scrolled');
    backToTop.classList.remove('visible');
  }

  // Active nav link highlight
  const sections = document.querySelectorAll('section[id], div[id]');
  let current = '';
  sections.forEach(sec => {
    const top = sec.offsetTop - 100;
    if (window.scrollY >= top) current = sec.getAttribute('id');
  });
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === '#' + current) link.classList.add('active');
  });
});

// ── HAMBURGER MENU ──
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');

hamburger.addEventListener('click', () => {
  navLinks.classList.toggle('open');
});

// Close nav on link click (mobile)
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', () => navLinks.classList.remove('open'));
});

// ── HERO PARTICLES ──
function createParticles() {
  const container = document.getElementById('particles');
  if (!container) return;
  for (let i = 0; i < 40; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    p.style.cssText = `
      left: ${Math.random() * 100}%;
      top: ${40 + Math.random() * 60}%;
      --dur: ${3 + Math.random() * 5}s;
      --delay: ${Math.random() * 6}s;
      opacity: 0;
    `;
    container.appendChild(p);
  }
}
createParticles();

// ── INTERSECTION OBSERVER — ANIMATIONS ──
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.timeline-item, .apply-step').forEach(el => observer.observe(el));

// ── SITE FILTER ──
const filterBtns = document.querySelectorAll('.filter-btn');
const siteCards = document.querySelectorAll('.site-card');

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;
    siteCards.forEach(card => {
      if (filter === 'all' || card.dataset.type === filter) {
        card.classList.remove('hidden');
        card.style.animation = 'none';
        card.offsetHeight; // reflow
        card.style.animation = 'fadeInCard 0.4s ease forwards';
      } else {
        card.classList.add('hidden');
      }
    });
  });
});

// ── JOB TABS ──
const jobTabs = document.querySelectorAll('.job-tab');
const jobPanels = document.querySelectorAll('.job-panel');

jobTabs.forEach(tab => {
  tab.addEventListener('click', () => {
    jobTabs.forEach(t => t.classList.remove('active'));
    jobPanels.forEach(p => p.classList.remove('active'));
    tab.classList.add('active');
    const target = document.getElementById('tab-' + tab.dataset.tab);
    if (target) target.classList.add('active');
  });
});

// ── FAQ ACCORDION ──
document.querySelectorAll('.faq-item').forEach(item => {
  const btn = item.querySelector('.faq-q');
  btn.addEventListener('click', () => {
    const isOpen = item.classList.contains('open');
    // Close all
    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
    // Open clicked if it was closed
    if (!isOpen) item.classList.add('open');
  });
});

// ── ANIMATED COUNTER (hero stats) ──
function animateCounter(el, target, duration = 1800) {
  const isDecimal = String(target).includes('.');
  let start = 0;
  const step = (timestamp) => {
    if (!start) start = timestamp;
    const progress = Math.min((timestamp - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const value = Math.floor(eased * target);
    el.textContent = value.toLocaleString('en-IN');
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = target.toLocaleString('en-IN');
  };
  requestAnimationFrame(step);
}

const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const nums = entry.target.querySelectorAll('.hstat-num');
      const targets = [25, 8880, 7, 1987];
      nums.forEach((el, i) => animateCounter(el, targets[i]));
      statsObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) statsObserver.observe(heroStats);

// ── SMOOTH ANCHOR SCROLL ──
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const offset = 72;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// ── CARD FADE IN ANIMATION (CSS keyframe injection) ──
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeInCard {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
  }
`;
document.head.appendChild(style);

fetch("http://127.0.0.1:8000/jobs")
  .then(res => res.json())
  .then(data => {

    const container = document.getElementById("jobs-container");

    data.forEach(job => {

      const card = document.createElement("div");

      card.classList.add("live-job-card");

      card.innerHTML = `

  <div class="job-top">

    <div class="job-badge ${job.status === "Open" ? "open" : "closed"}">
      ${job.status}
    </div>

    <h4>${job.title}</h4>

  </div>

  <div class="job-details">

    <p>📅 Start Date: ${job.start_date}</p>

    <p>⏳ Last Date: ${job.last_date}</p>

  </div>

  <a href="${job.link}" target="_blank" class="job-btn">
    View Notification
  </a>

`;

      container.appendChild(card);

    });

  })
  .catch(error => {
    console.error("Error fetching jobs:", error);
  });