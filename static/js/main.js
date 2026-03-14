/**
 * LoanAI – Frontend Interactivity
 */

// ─── Form validation & submission ────────────────────────
const form = document.getElementById('loanForm');
const submitBtn = document.getElementById('submitBtn');
const spinner = document.getElementById('spinner');

if (form) {
  form.addEventListener('submit', function (e) {
    const requiredFields = form.querySelectorAll('[required]');
    let valid = true;

    requiredFields.forEach(field => {
      field.classList.remove('invalid');
      if (!field.value || field.value.trim() === '') {
        field.classList.add('invalid');
        valid = false;
        // Shake animation
        field.style.animation = 'none';
        requestAnimationFrame(() => {
          field.style.animation = 'shake 0.4s ease';
        });
      }
    });

    if (!valid) {
      e.preventDefault();
      showToast('⚠️ Please fill in all required fields.');
      return;
    }

    // Show loading state
    if (submitBtn) {
      const btnText = submitBtn.querySelector('.btn-text');
      const btnArr  = submitBtn.querySelector('.btn-arrow');
      if (btnText) btnText.textContent = 'Predicting…';
      if (spinner)  spinner.classList.remove('hidden');
      if (btnArr)   btnArr.textContent = '⏳';
      submitBtn.disabled = true;
      submitBtn.style.opacity = '0.8';
    }
  });
}

// ─── Input focus effects ──────────────────────────────────
document.querySelectorAll('.form-input, .form-select').forEach(el => {
  el.addEventListener('focus', () => {
    const group = el.closest('.form-group');
    if (group) group.classList.add('focused');
  });
  el.addEventListener('blur', () => {
    const group = el.closest('.form-group');
    if (group) group.classList.remove('focused');
    el.classList.remove('invalid');
  });
});

// ─── Toast notification ───────────────────────────────────
function showToast(msg) {
  let existing = document.querySelector('.toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = msg;
  document.body.appendChild(toast);

  // Inject toast styles dynamically if needed
  if (!document.getElementById('toast-style')) {
    const style = document.createElement('style');
    style.id = 'toast-style';
    style.textContent = `
      .toast {
        position: fixed; bottom: 2rem; left: 50%; transform: translateX(-50%);
        background: rgba(239,68,68,0.95); color: #fff; backdrop-filter: blur(10px);
        padding: 0.75rem 1.5rem; border-radius: 9999px;
        font-size: 0.875rem; font-weight: 600; z-index: 9999;
        box-shadow: 0 4px 24px rgba(0,0,0,0.4);
        animation: slideUp 0.3s ease, fadeOut 0.4s ease 2.8s forwards;
      }
      @keyframes slideUp {
        from { opacity: 0; transform: translateX(-50%) translateY(20px); }
        to   { opacity: 1; transform: translateX(-50%) translateY(0); }
      }
      @keyframes fadeOut {
        to   { opacity: 0; transform: translateX(-50%) translateY(10px); }
      }
      .form-input.invalid, .form-select.invalid {
        border-color: rgba(239,68,68,0.6) !important;
        box-shadow: 0 0 0 3px rgba(239,68,68,0.2) !important;
      }
      @keyframes shake {
        0%,100%{ transform: translateX(0); }
        20%    { transform: translateX(-6px); }
        40%    { transform: translateX(6px); }
        60%    { transform: translateX(-4px); }
        80%    { transform: translateX(4px); }
      }
    `;
    document.head.appendChild(style);
  }

  setTimeout(() => toast.remove(), 3300);
}

// ─── Scroll-in animation for cards ───────────────────────
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity    = '1';
      entry.target.style.transform  = 'translateY(0)';
    }
  });
}, { threshold: 0.08 });

document.querySelectorAll('.form-card, .stat-card, .model-card').forEach(el => {
  el.style.opacity   = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.55s ease, transform 0.55s ease';
  observer.observe(el);
});

// ─── Number input: format on blur ────────────────────────
document.querySelectorAll('input[type="number"]').forEach(input => {
  input.addEventListener('wheel', e => e.preventDefault()); // prevent scroll change
});

console.log('%c🏦 LoanAI', 'font-size:20px;font-weight:bold;color:#3b82f6;');
console.log('%cPowered by Python · Scikit-learn · Flask', 'color:#64748b;font-size:12px;');
