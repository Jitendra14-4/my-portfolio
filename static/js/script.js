/**
 * ==============================================================================
 * Jitendra Kumar Jena — Developer Portfolio Interactive Script
 * Features:
 * 1. Theme Manager (Dark/Light Mode with localStorage persistence)
 * 2. Constellation Particle Canvas Background (Subtle interactive physics)
 * 3. Typewriter Hero Animation
 * 4. Animated Counters & Skill Progress Bars (IntersectionObserver)
 * 5. ScrollSpy & Sticky Navbar Styling
 * 6. Skills & Projects Filtering + Real-Time Search
 * 7. Project Details Lightbox Modal
 * 8. Asynchronous Contact Form Submission (Fetch API to POST /api/contact)
 * 9. Live SQLite Database Submissions Inspector Modal
 * 10. Copy-to-Clipboard & Back-to-Top Handlers
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
  initThemeManager();
  initParticleCanvas();
  initTypewriter();
  initScrollAnimations();
  initNavbarScrollSpy();
  initSkillsFilter();
  initProjectsFilter();
  initProjectModal();
  initContactForm();
  initSubmissionsInspector();
  initClipboardAndUtils();
});

/* ==============================================================================
   1. Theme Manager (Dark / Light Mode)
   ============================================================================== */
function initThemeManager() {
  const toggleBtn = document.getElementById('themeToggleBtn');
  const toggleIcon = document.getElementById('themeToggleIcon');
  const toggleBtnMobile = document.getElementById('themeToggleBtnMobile');
  const toggleIconMobile = document.getElementById('themeToggleIconMobile');

  // Load saved theme preference or default to futuristic dark mode
  const savedTheme = localStorage.getItem('theme') || 'dark';
  applyTheme(savedTheme);

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);

    const isLight = theme === 'light';
    const iconClass = isLight ? 'bi bi-moon-stars-fill' : 'bi bi-sun-fill';
    const btnTitle = isLight ? 'Switch to Dark Mode' : 'Switch to Light Mode';

    if (toggleIcon) toggleIcon.className = iconClass;
    if (toggleBtn) toggleBtn.setAttribute('title', btnTitle);
    if (toggleIconMobile) toggleIconMobile.className = iconClass;
    if (toggleBtnMobile) toggleBtnMobile.setAttribute('title', btnTitle);
  }

  function handleThemeToggle() {
    const active = document.documentElement.getAttribute('data-theme') || 'dark';
    const nextTheme = active === 'dark' ? 'light' : 'dark';
    applyTheme(nextTheme);
  }

  if (toggleBtn) toggleBtn.addEventListener('click', handleThemeToggle);
  if (toggleBtnMobile) toggleBtnMobile.addEventListener('click', handleThemeToggle);
}

/* ==============================================================================
   2. Constellation Particle Canvas Background
   ============================================================================== */
function initParticleCanvas() {
  const canvas = document.getElementById('particles-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  let particles = [];
  const particleCount = Math.min(Math.floor(window.innerWidth / 25), 55);
  const maxDistance = 130;

  let mouse = { x: null, y: null, radius: 120 };

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    createParticles();
  });

  window.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
  });

  window.addEventListener('mouseleave', () => {
    mouse.x = null;
    mouse.y = null;
  });

  class Particle {
    constructor() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.7;
      this.vy = (Math.random() - 0.5) * 0.7;
      this.radius = Math.random() * 1.8 + 1;
      this.color = Math.random() > 0.5 ? 'rgba(56, 189, 248, ' : 'rgba(168, 85, 247, ';
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;

      if (this.x < 0 || this.x > width) this.vx *= -1;
      if (this.y < 0 || this.y > height) this.vy *= -1;

      // Mouse repulsion
      if (mouse.x !== null && mouse.y !== null) {
        const dx = mouse.x - this.x;
        const dy = mouse.y - this.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < mouse.radius) {
          const force = (mouse.radius - dist) / mouse.radius;
          this.x -= (dx / dist) * force * 2;
          this.y -= (dy / dist) * force * 2;
        }
      }
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = this.color + '0.7)';
      ctx.fill();
    }
  }

  function createParticles() {
    particles = [];
    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }
  }

  function connectParticles() {
    for (let a = 0; a < particles.length; a++) {
      for (let b = a + 1; b < particles.length; b++) {
        const dx = particles[a].x - particles[b].x;
        const dy = particles[a].y - particles[b].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < maxDistance) {
          const opacity = (1 - dist / maxDistance) * 0.22;
          ctx.beginPath();
          ctx.strokeStyle = `rgba(56, 189, 248, ${opacity})`;
          ctx.lineWidth = 0.8;
          ctx.moveTo(particles[a].x, particles[a].y);
          ctx.lineTo(particles[b].x, particles[b].y);
          ctx.stroke();
        }
      }
    }
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);
    particles.forEach((p) => {
      p.update();
      p.draw();
    });
    connectParticles();
    requestAnimationFrame(animate);
  }

  createParticles();
  animate();
}

/* ==============================================================================
   3. Typewriter Hero Animation
   ============================================================================== */
function initTypewriter() {
  const target = document.getElementById('typewriterText');
  if (!target) return;

  const roles = [
    'Python Full Stack Developer',
    'AI & Data Science Enthusiast',
    'Flask & Django Specialist',
    'Machine Learning & NLP Builder',
    'QA & System Testing Engineer'
  ];

  let roleIdx = 0;
  let charIdx = 0;
  let isDeleting = false;
  const typeSpeed = 85;
  const deleteSpeed = 40;
  const pauseTime = 1800;

  function tick() {
    const current = roles[roleIdx];

    if (isDeleting) {
      target.textContent = current.substring(0, charIdx - 1);
      charIdx--;
    } else {
      target.textContent = current.substring(0, charIdx + 1);
      charIdx++;
    }

    if (!isDeleting && charIdx === current.length) {
      setTimeout(() => {
        isDeleting = true;
        tick();
      }, pauseTime);
      return;
    } else if (isDeleting && charIdx === 0) {
      isDeleting = false;
      roleIdx = (roleIdx + 1) % roles.length;
      setTimeout(tick, 300);
      return;
    }

    setTimeout(tick, isDeleting ? deleteSpeed : typeSpeed);
  }

  tick();
}

/* ==============================================================================
   4. Scroll Animations (Counters, Progress Bars, Reveal Items)
   ============================================================================== */
function initScrollAnimations() {
  // 1. Reveal Elements on Scroll
  const revealItems = document.querySelectorAll('.reveal-item');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
      }
    });
  }, { threshold: 0.1 });

  revealItems.forEach((el) => revealObserver.observe(el));

  // 2. Animated Numerical Counters
  const counterElements = document.querySelectorAll('.stat-number');
  let countersStarted = false;

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && !countersStarted) {
        countersStarted = true;
        counterElements.forEach((counter) => {
          const target = parseInt(counter.getAttribute('data-target'), 10) || 0;
          animateNumber(counter, target, 1600);
        });
      }
    });
  }, { threshold: 0.4 });

  if (counterElements.length > 0) {
    counterObserver.observe(counterElements[0]);
  }

  function animateNumber(elem, target, duration) {
    let startTime = null;
    function update(timestamp) {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      // Easing out cubic
      const easeOut = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(easeOut * target);
      elem.textContent = current;
      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        elem.textContent = target;
      }
    }
    requestAnimationFrame(update);
  }

  // 3. Animated Progress Bars in About section
  const progressBars = document.querySelectorAll('.progress-bar-gradient');
  const progressObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        progressBars.forEach((bar) => {
          const val = bar.getAttribute('data-progress') || 0;
          bar.style.width = val + '%';
        });
      }
    });
  }, { threshold: 0.3 });

  if (progressBars.length > 0) {
    progressObserver.observe(progressBars[0]);
  }
}

/* ==============================================================================
   5. Navbar ScrollSpy & Sticky Shadow
   ============================================================================== */
function initNavbarScrollSpy() {
  const navbar = document.getElementById('mainNavbar');
  const navLinks = document.querySelectorAll('.nav-link-custom');
  const sections = document.querySelectorAll('section[id]');

  window.addEventListener('scroll', () => {
    const scrollPos = window.scrollY + 120;

    // Sticky styling
    if (window.scrollY > 40) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }

    // ScrollSpy active link tracking
    sections.forEach((sec) => {
      const top = sec.offsetTop;
      const height = sec.offsetHeight;
      const id = sec.getAttribute('id');

      if (scrollPos >= top && scrollPos < top + height) {
        navLinks.forEach((link) => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
          }
        });
      }
    });
  });

  // Mobile nav auto-collapse upon clicking any anchor link
  navLinks.forEach((link) => {
    link.addEventListener('click', () => {
      const navCollapse = document.getElementById('portfolioNavContent');
      if (navCollapse && navCollapse.classList.contains('show')) {
        const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
        if (bsCollapse) bsCollapse.hide();
      }
    });
  });
}

/* ==============================================================================
   6. Skills Category Filtering
   ============================================================================== */
function initSkillsFilter() {
  const filterBtns = document.querySelectorAll('.skill-filter-btn');
  const skillCards = document.querySelectorAll('.skill-grid-card');

  if (!filterBtns.length || !skillCards.length) return;

  filterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      filterBtns.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-skill-filter');

      skillCards.forEach((card) => {
        const cat = card.getAttribute('data-skill-category');
        if (filter === 'all' || cat === filter) {
          card.style.display = 'block';
          card.classList.add('animate-fadeIn');
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/* ==============================================================================
   7. Projects Filtering & Real-Time Search
   ============================================================================== */
function initProjectsFilter() {
  const filterBtns = document.querySelectorAll('.project-filter-btn');
  const projectCards = document.querySelectorAll('.project-item-card');
  const searchInput = document.getElementById('projectSearchInput');
  const clearBtn = document.getElementById('clearSearchBtn');
  const noProjectsMsg = document.getElementById('noProjectsFound');
  const resetBtn = document.getElementById('resetProjectFilterBtn');

  if (!projectCards.length) return;

  let activeCategory = 'all';
  let searchQuery = '';

  filterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      filterBtns.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      activeCategory = btn.getAttribute('data-filter') || 'all';
      applyFilters();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.toLowerCase().trim();
      if (clearBtn) {
        clearBtn.style.display = searchQuery ? 'block' : 'none';
      }
      applyFilters();
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      if (searchInput) {
        searchInput.value = '';
        searchQuery = '';
        clearBtn.style.display = 'none';
        applyFilters();
      }
    });
  }

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      activeCategory = 'all';
      searchQuery = '';
      if (searchInput) searchInput.value = '';
      if (clearBtn) clearBtn.style.display = 'none';
      filterBtns.forEach((b) => {
        if (b.getAttribute('data-filter') === 'all') b.classList.add('active');
        else b.classList.remove('active');
      });
      applyFilters();
    });
  }

  function applyFilters() {
    let visibleCount = 0;

    projectCards.forEach((card) => {
      const category = (card.getAttribute('data-category') || '').toLowerCase();
      const title = (card.getAttribute('data-title') || '').toLowerCase();
      const tech = (card.getAttribute('data-tech') || '').toLowerCase();

      const matchesCat = activeCategory === 'all' || category === activeCategory;
      const matchesSearch =
        !searchQuery ||
        title.includes(searchQuery) ||
        tech.includes(searchQuery) ||
        category.includes(searchQuery);

      if (matchesCat && matchesSearch) {
        card.style.display = 'block';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    if (noProjectsMsg) {
      noProjectsMsg.style.display = visibleCount === 0 ? 'block' : 'none';
    }
  }
}

/* ==============================================================================
   8. Project Details Lightbox Modal
   ============================================================================== */
function initProjectModal() {
  const modalEl = document.getElementById('projectDetailsModal');
  if (!modalEl) return;

  const modalTitle = document.getElementById('projectModalTitle');
  const modalCat = document.getElementById('projectModalCategory');
  const modalImg = document.getElementById('projectModalImage');
  const modalDesc = document.getElementById('projectModalDescription');
  const modalTech = document.getElementById('projectModalTech');
  const modalGithub = document.getElementById('projectModalGithub');
  const modalDemo = document.getElementById('projectModalDemo');

  document.querySelectorAll('.open-project-modal-btn').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();

      const title = btn.getAttribute('data-title') || 'Project Overview';
      const category = btn.getAttribute('data-category') || 'Software';
      const desc = btn.getAttribute('data-desc') || '';
      const tech = btn.getAttribute('data-tech') || '';
      const image = btn.getAttribute('data-image') || '';
      const github = btn.getAttribute('data-github') || '';
      const demo = btn.getAttribute('data-demo') || '';

      if (modalTitle) modalTitle.textContent = title;
      if (modalCat) modalCat.textContent = category;
      if (modalDesc) modalDesc.textContent = desc;
      if (modalImg) modalImg.src = image;

      if (modalTech) {
        modalTech.innerHTML = '';
        tech.split(',').forEach((t) => {
          if (t.trim()) {
            const span = document.createElement('span');
            span.className = 'tech-pill';
            span.textContent = t.trim();
            modalTech.appendChild(span);
          }
        });
      }

      if (modalGithub) {
        if (github && github !== '#') {
          modalGithub.href = github;
          modalGithub.style.display = 'inline-flex';
        } else {
          modalGithub.style.display = 'none';
        }
      }

      if (modalDemo) {
        if (demo && demo !== '#') {
          modalDemo.href = demo;
          modalDemo.style.display = 'inline-flex';
        } else {
          modalDemo.style.display = 'none';
        }
      }

      const bsModal = bootstrap.Modal.getOrCreateInstance(modalEl);
      bsModal.show();
    });
  });
}

/* ==============================================================================
   9. Asynchronous Contact Form Submission (Fetch API to POST /api/contact)
   ============================================================================== */
function initContactForm() {
  const form = document.getElementById('contactForm');
  if (!form) return;

  const nameInput = document.getElementById('formName');
  const emailInput = document.getElementById('formEmail');
  const phoneInput = document.getElementById('formPhone');
  const subjectInput = document.getElementById('formSubject');
  const messageInput = document.getElementById('formMessage');
  const honeypotInput = document.getElementById('formWebsite');

  const charCounter = document.getElementById('charCounter');
  const submitBtn = document.getElementById('submitContactBtn');
  const submitSpinner = document.getElementById('btnSubmitSpinner');
  const submitIcon = document.getElementById('btnSubmitIcon');
  const submitText = document.getElementById('btnSubmitText');

  const alertSuccess = document.getElementById('contactFormAlertSuccess');
  const alertError = document.getElementById('contactFormAlertError');
  const successMsg = document.getElementById('contactSuccessMsg');
  const errorMsg = document.getElementById('contactErrorMsg');
  const submissionIdBadge = document.getElementById('submissionIdBadge');

  // Live Character Counter
  if (messageInput && charCounter) {
    messageInput.addEventListener('input', () => {
      const len = messageInput.value.length;
      charCounter.textContent = `${len} / 4000`;
      if (len > 3800) {
        charCounter.classList.add('text-danger');
      } else {
        charCounter.classList.remove('text-danger');
      }
    });
  }

  // Real-time input validation markers
  [nameInput, emailInput, subjectInput, messageInput].forEach((inp) => {
    if (!inp) return;
    inp.addEventListener('blur', () => validateField(inp));
    inp.addEventListener('input', () => {
      if (inp.classList.contains('is-invalid')) {
        validateField(inp);
      }
    });
  });

  function validateField(input) {
    if (!input.checkValidity()) {
      input.classList.add('is-invalid');
      input.classList.remove('is-valid');
      return false;
    } else {
      input.classList.remove('is-invalid');
      input.classList.add('is-valid');
      return true;
    }
  }

  // Form Submit Handler
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Reset alert banners
    alertSuccess.style.display = 'none';
    alertError.style.display = 'none';

    // Client-side validation check
    const isNameValid = validateField(nameInput);
    const isEmailValid = validateField(emailInput);
    const isSubjectValid = validateField(subjectInput);
    const isMessageValid = validateField(messageInput);

    if (!isNameValid || !isEmailValid || !isSubjectValid || !isMessageValid) {
      errorMsg.textContent = 'Please fill out all required fields marked with an asterisk (*).';
      alertError.style.display = 'block';
      return;
    }

    // Set UI loading state
    setButtonLoading(true);

    const payload = {
      name: nameInput.value.trim(),
      email: emailInput.value.trim(),
      phone: phoneInput ? phoneInput.value.trim() : '',
      subject: subjectInput.value.trim(),
      message: messageInput.value.trim(),
      website: honeypotInput ? honeypotInput.value.trim() : ''
    };

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      const result = await response.json();

      if (response.ok && result.status === 'success') {
        // Success presentation
        successMsg.textContent = result.message || 'Your message has been safely saved in the database!';
        if (submissionIdBadge) {
          submissionIdBadge.textContent = `Submission Ref: ${result.submission_id || 'CNT-RECORDED'}`;
        }
        alertSuccess.style.display = 'block';

        // Clear inputs and validation classes
        form.reset();
        if (charCounter) charCounter.textContent = '0 / 4000';
        [nameInput, emailInput, phoneInput, subjectInput, messageInput].forEach((inp) => {
          if (inp) {
            inp.classList.remove('is-valid');
            inp.classList.remove('is-invalid');
          }
        });

        // Smooth scroll to notification if needed
        alertSuccess.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      } else {
        // Error handling
        const errors = result.errors ? result.errors.join(' ') : result.message;
        errorMsg.textContent = errors || 'Failed to submit form. Please check your fields and try again.';
        alertError.style.display = 'block';
      }
    } catch (err) {
      console.error('Contact Form Fetch Error:', err);
      errorMsg.textContent = 'Unable to reach the backend server. Please verify your connection or email jitendrax144@gmail.com directly.';
      alertError.style.display = 'block';
    } finally {
      setButtonLoading(false);
    }
  });

  function setButtonLoading(isLoading) {
    if (isLoading) {
      submitBtn.disabled = true;
      submitSpinner.style.display = 'inline-block';
      submitIcon.style.display = 'none';
      submitText.textContent = 'Saving to SQLite Database...';
    } else {
      submitBtn.disabled = false;
      submitSpinner.style.display = 'none';
      submitIcon.style.display = 'inline-block';
      submitText.textContent = 'Send Message via API';
    }
  }
}

/* ==============================================================================
   10. SQLite Database Submissions Inspector Modal (Step 8 Verification)
   ============================================================================== */
function initSubmissionsInspector() {
  const inspectBtn = document.getElementById('viewSubmissionsBtn');
  const modalEl = document.getElementById('submissionsModal');
  const refreshBtn = document.getElementById('refreshSubmissionsBtn');
  const loadingEl = document.getElementById('submissionsLoading');
  const listContainer = document.getElementById('submissionsListContainer');
  const listEl = document.getElementById('submissionsList');
  const totalCountEl = document.getElementById('submissionTotalCount');

  if (!inspectBtn || !modalEl) return;

  inspectBtn.addEventListener('click', () => {
    const bsModal = bootstrap.Modal.getOrCreateInstance(modalEl);
    bsModal.show();
    loadSubmissions();
  });

  if (refreshBtn) {
    refreshBtn.addEventListener('click', loadSubmissions);
  }

  async function loadSubmissions() {
    loadingEl.style.display = 'block';
    listContainer.style.display = 'none';
    listEl.innerHTML = '';

    try {
      const res = await fetch('/api/contacts?limit=50');
      const data = await res.json();

      if (res.ok && data.status === 'success') {
        const contacts = data.contacts || [];
        totalCountEl.textContent = contacts.length;

        if (contacts.length === 0) {
          listEl.innerHTML = `
            <div class="text-center py-4 text-muted-custom">
              <i class="bi bi-inbox fs-2 mb-2"></i>
              <p>No contact messages stored in database yet. Try submitting the contact form!</p>
            </div>
          `;
        } else {
          contacts.forEach((c) => {
            const item = document.createElement('div');
            item.className = 'submission-item-card';
            item.innerHTML = `
              <div class="d-flex justify-content-between align-items-center mb-1 flex-wrap gap-2">
                <span class="badge bg-primary bg-opacity-25 text-primary font-monospace">${escapeHtml(c.id)}</span>
                <span class="small text-muted-custom"><i class="bi bi-clock me-1"></i>${escapeHtml(c.created_at)}</span>
              </div>
              <h5 class="h6 fw-bold text-light mb-1">${escapeHtml(c.subject)}</h5>
              <div class="small text-muted-custom mb-2">
                <strong>From:</strong> ${escapeHtml(c.name)} &lt;${escapeHtml(c.email)}&gt;
                ${c.phone ? ` | <strong>Phone:</strong> ${escapeHtml(c.phone)}` : ''}
              </div>
              <p class="small text-light mb-0 bg-dark p-2 rounded-2 font-monospace" style="border: 1px solid rgba(255,255,255,0.05);">${escapeHtml(c.message)}</p>
            `;
            listEl.appendChild(item);
          });
        }
      } else {
        listEl.innerHTML = `<div class="text-danger">Failed to load contacts: ${data.message}</div>`;
      }
    } catch (err) {
      console.error(err);
      listEl.innerHTML = `<div class="text-danger">Error querying database API.</div>`;
    } finally {
      loadingEl.style.display = 'none';
      listContainer.style.display = 'block';
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
}

/* ==============================================================================
   11. Clipboard, Back-to-Top & Year Stamp
   ============================================================================== */
function initClipboardAndUtils() {
  // 1. Current Year in Footer
  const yearEl = document.getElementById('currentYear');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  // 2. Back to Top Button
  const backToTopBtn = document.getElementById('backToTopBtn');
  if (backToTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 350) {
        backToTopBtn.classList.add('show');
      } else {
        backToTopBtn.classList.remove('show');
      }
    });

    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // 3. One-Click Copy to Clipboard for Email and Phone
  document.querySelectorAll('.btn-copy-clip').forEach((btn) => {
    btn.addEventListener('click', () => {
      const textToCopy = btn.getAttribute('data-copy');
      if (textToCopy) {
        navigator.clipboard.writeText(textToCopy).then(() => {
          const originalIcon = btn.innerHTML;
          btn.innerHTML = '<i class="bi bi-check-lg text-success"></i>';
          btn.classList.add('border-success');
          setTimeout(() => {
            btn.innerHTML = originalIcon;
            btn.classList.remove('border-success');
          }, 2000);
        });
      }
    });
  });
}
