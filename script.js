// Scroll-triggered reveal for cards/sections
const revealEls = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
            setTimeout(() => entry.target.classList.add('is-visible'), i * 80);
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.15 });
revealEls.forEach(el => observer.observe(el));

// Stagger the service/team cards within their own grid
document.querySelectorAll('.service-grid .reveal, .team-grid .reveal').forEach((el, i) => {
    el.style.transitionDelay = (i * 0.1) + 's';
});

// Shrink header on scroll
const header = document.getElementById('site-header');
window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 40);
});

// Button ripple effect
document.querySelectorAll('.btn-ripple').forEach(btn => {
    btn.addEventListener('click', function (e) {
        const rect = this.getBoundingClientRect();
        const ripple = document.createElement('span');
        const size = Math.max(rect.width, rect.height);
        ripple.className = 'ripple';
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
        ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
        this.appendChild(ripple);
        ripple.addEventListener('animationend', () => ripple.remove());
    });
});


// Login
// ---------- Auth Modal ----------
const authOverlay = document.getElementById('authOverlay');
const loginBtn = document.getElementById('loginBtn');
const modalClose = document.getElementById('modalClose');
const authTabs = document.querySelectorAll('.auth-tab');
const authForms = document.querySelectorAll('.auth-form');

function openModal() {
    authOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    authOverlay.classList.remove('active');
    document.body.style.overflow = '';
}

loginBtn.addEventListener('click', openModal);
modalClose.addEventListener('click', closeModal);

authOverlay.addEventListener('click', (e) => {
    if (e.target === authOverlay) closeModal();
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && authOverlay.classList.contains('active')) closeModal();
});

authTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        authTabs.forEach(t => t.classList.remove('active'));
        authForms.forEach(f => f.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(tab.dataset.tab + 'Form').classList.add('active');
    });
});

// Login Form Submission
// Login Form Submission
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const emailInput = loginForm.querySelector('input[type="email"]');
        const passwordInput = loginForm.querySelector('input[type="password"]');
        
        if (!emailInput || !passwordInput) {
            console.error("Could not find email or password inputs inside loginForm");
            return;
        }

        const email = emailInput.value;
        const password = passwordInput.value;

        try {
            const response = await fetch('http://127.0.0.1:5000/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const result = await response.json();
            alert(result.message);
            if (response.ok) closeModal();
        } catch (error) {
            alert('Could not connect to the Python server!');
        }
    });
}

// Signup Form Submission
const signupForm = document.getElementById('signupForm');
if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const emailInput = signupForm.querySelector('input[type="email"]');
        const passwordInput = signupForm.querySelector('input[type="password"]');
        
        if (!emailInput || !passwordInput) {
            console.error("Could not find email or password inputs inside signupForm");
            return;
        }

        const email = emailInput.value;
        const password = passwordInput.value;

        try {
            const response = await fetch('http://127.0.0.1:5000/api/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const result = await response.json();
            alert(result.message);
            if (response.ok) closeModal();
        } catch (error) {
            alert('Could not connect to the Python server!');
        }
    });
}

// ---------- Google Identity Services ----------
window.onload = function () {
    google.accounts.id.initialize({
        client_id: "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com",
        callback: handleCredentialResponse
    });

    document.getElementById('googleLoginBtn').addEventListener('click', () => {
        google.accounts.id.prompt((notification) => {
            if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
                console.log("Prompt skipped or blocked, handling alternative flow if needed.");
            }
        });
    });
};

function handleCredentialResponse(response) {
    console.log("Verified Google JWT Token:", response.credential);
    closeModal();
    alert("Successfully authenticated with Google!");
}