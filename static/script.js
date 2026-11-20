/**
 * Learnloop Client JavaScript
 * Handles:
 * - AI-Integrated Multilingual Chatbot Drawer (EN, HI, KN) with API Key support
 * - Quiz interactive feedback & stepper navigation
 * - UI micro-interactions & Demo Auto-fills
 */

// ============================================================================
// 1. Multilingual Chatbot Drawer Controller & AI Integration
// ============================================================================
let chatLanguage = 'en';
let isChatOpen = false;

const GREETINGS = {
  en: "Hello! I am your **Learnloop AI Study Assistant**.\n\nI can help you master concepts in C Programming, Digital Electronics, Circuit Analysis, and Engineering Mathematics, or navigate your quizzes and recommendations.\n\nWhat would you like to learn today?",
  hi: "नमस्ते! मैं आपका **Learnloop AI अध्ययन सहायक** हूँ।\n\nमैं C प्रोग्रामिंग, डिजिटल इलेक्ट्रॉनिक्स, सर्किट विश्लेषण और इंजीनियरिंग गणित के प्रश्नों में आपकी सहायता कर सकता हूँ।\n\nआप क्या सीखना चाहते हैं?",
  kn: "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ **Learnloop AI ಕಲಿಕಾ ಸಹಾಯಕ**.\n\nನಾನು C ಪ್ರೋಗ್ರಾಮಿಂಗ್, ಡಿಜಿಟಲ್ ಎಲೆಕ್ಟ್ರಾನಿಕ್ಸ್, ಸರ್ಕ್ಯೂಟ್ ಮತ್ತು ಎಂಜಿನಿಯರಿಂಗ್ ಗಣಿತದ ಪರಿಕಲ್ಪನೆಗಳಲ್ಲಿ ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ.\n\nನೀವು ಇಂದು ಯಾವ ವಿಷಯದ ಬಗ್ಗೆ ತಿಳಿದುಕೊಳ್ಳಲು ಬಯಸುತ್ತೀರಿ?"
};

const PLACEHOLDERS = {
  en: "Ask any engineering question (e.g. What is KVL?)...",
  hi: "कोई भी प्रश्न पूछें (उदा. KVL क्या है?)...",
  kn: "ಪ್ರಶ್ನೆ ಕೇಳಿ (ಉದಾ. KVL ಎಂದರೇನು?)..."
};

const DISCLAIMERS = {
  en: "AI-assisted study guidance for engineering topics.",
  hi: "इंजीनियरिंग विषयों के लिए AI-आधारित अध्ययन मार्गदर्शन।",
  kn: "ಎಂಜಿನಿಯರಿಂಗ್ ವಿಷಯಗಳಿಗೆ AI-ಆಧಾರಿತ ಕಲಿಕಾ ಮಾರ್ಗದರ್ಶನ."
};

function toggleChatDrawer() {
  const drawer = document.getElementById('chat-drawer');
  const iconOpen = document.getElementById('chat-icon-open');
  const iconClose = document.getElementById('chat-icon-close');

  if (!drawer) return;

  isChatOpen = !isChatOpen;
  if (isChatOpen) {
    drawer.classList.remove('hidden-drawer');
    if (iconOpen) iconOpen.classList.add('hidden');
    if (iconClose) iconClose.classList.remove('hidden');

    // If chat is empty, insert initial greeting
    const messagesContainer = document.getElementById('chat-messages');
    if (messagesContainer && messagesContainer.children.length === 0) {
      appendChatMessage('assistant', GREETINGS[chatLanguage]);
    }

    const input = document.getElementById('chat-input');
    if (input) setTimeout(() => input.focus(), 150);
  } else {
    drawer.classList.add('hidden-drawer');
    if (iconOpen) iconOpen.classList.remove('hidden');
    if (iconClose) iconClose.classList.add('hidden');
  }
}

function setChatLanguage(lang) {
  if (!['en', 'hi', 'kn'].includes(lang)) return;
  chatLanguage = lang;

  // Update button active styles
  ['en', 'hi', 'kn'].forEach(l => {
    const btn = document.getElementById(`btn-lang-${l}`);
    if (btn) {
      if (l === lang) {
        btn.className = "px-2.5 py-1 rounded-md transition-all bg-white text-[#10222c] shadow-sm font-bold";
      } else {
        btn.className = "px-2.5 py-1 rounded-md transition-all text-gray-600 hover:text-black font-medium";
      }
    }
  });

  // Update placeholder and disclaimer
  const input = document.getElementById('chat-input');
  if (input) input.placeholder = PLACEHOLDERS[lang] || PLACEHOLDERS.en;

  const disclaimer = document.getElementById('chat-disclaimer-text');
  if (disclaimer) disclaimer.innerText = DISCLAIMERS[lang] || DISCLAIMERS.en;

  // Add system note in stream about language change
  appendChatMessage('system', `Language set to ${lang === 'hi' ? 'हिन्दी' : (lang === 'kn' ? 'ಕನ್ನಡ' : 'English')}`);
}

// ----------------------------------------------------------------------------
// Clean Markdown Formatter for Chat Messages
// ----------------------------------------------------------------------------
function formatMarkdown(text) {
  if (!text) return '';
  let safe = text
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  // Code blocks: ```c ... ```
  safe = safe.replace(/```([a-zA-Z0-9_-]*)\n?([\s\S]*?)```/g, (match, lang, code) => {
    return `<pre class="bg-[#10222c] text-emerald-300 p-2.5 rounded-xl my-2 overflow-x-auto text-[11px] font-mono leading-relaxed border border-[#213947] whitespace-pre"><code>${code.trim()}</code></pre>`;
  });

  // Inline code: `code`
  safe = safe.replace(/`([^`]+)`/g, '<code class="bg-[#ede6da] text-[#10222c] px-1 py-0.5 rounded font-mono text-[11px] mx-0.5">$1</code>');

  // Bold: **text**
  safe = safe.replace(/\*\*([^*]+)\*\*/g, '<strong class="font-bold text-[#10222c]">$1</strong>');

  // Math expressions: $formula$
  safe = safe.replace(/\$([^$]+)\$/g, '<span class="font-mono bg-white/70 px-1 rounded text-[#1a6b5f] font-semibold mx-0.5">$1</span>');

  // Bullet points
  safe = safe.replace(/^[•\-\*]\s+(.+)$/gm, '<li class="ml-3.5 list-disc my-0.5">$1</li>');

  // Newlines to <br> to preserve line breaks cleanly
  safe = safe.replace(/\n/g, '<br>');

  return safe;
}

function appendChatMessage(sender, text) {
  const container = document.getElementById('chat-messages');
  if (!container) return;

  const msgDiv = document.createElement('div');
  msgDiv.className = 'fade-in flex flex-col ' + (sender === 'user' ? 'items-end' : 'items-start');

  const bubble = document.createElement('div');
  if (sender === 'user') {
    bubble.className = 'chat-bubble chat-bubble-user max-w-[85%] bg-[#10222c] text-white p-3.5 rounded-2xl rounded-tr-sm text-xs sm:text-sm leading-relaxed shadow-sm whitespace-pre-wrap break-words';
    bubble.innerText = text;
  } else if (sender === 'assistant') {
    bubble.className = 'chat-bubble chat-bubble-assistant max-w-[85%] bg-[#f6f3ed] border border-[#e2dacd] text-[#1d2b33] p-3.5 rounded-2xl rounded-tl-sm text-xs sm:text-sm leading-relaxed shadow-sm whitespace-pre-wrap break-words font-sans';
    bubble.innerHTML = formatMarkdown(text);
  } else {
    // system note
    bubble.className = 'text-[10.5px] italic text-gray-500 py-1 text-center w-full font-mono';
    bubble.innerText = text;
  }

  msgDiv.appendChild(bubble);
  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;
}

async function handleChatSubmit(event) {
  event.preventDefault();
  const input = document.getElementById('chat-input');
  if (!input) return;

  const query = input.value.trim();
  if (!query) return;

  // Clear input
  input.value = '';

  // Render user bubble
  appendChatMessage('user', query);

  // Render temporary animated typing indicator
  const container = document.getElementById('chat-messages');
  const typingDiv = document.createElement('div');
  typingDiv.id = 'chat-typing-indicator';
  typingDiv.className = 'fade-in flex items-center gap-2 p-3 bg-[#f6f3ed] border border-[#e2dacd] rounded-2xl rounded-tl-sm text-xs text-gray-500 max-w-[85%]';
  typingDiv.innerHTML = `
    <span class="flex items-center gap-1 text-[#1a6b5f]">
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
    </span>
    <span class="italic">Analyzing query with Learnloop AI...</span>
  `;
  container.appendChild(typingDiv);
  container.scrollTop = container.scrollHeight;

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: query,
        lang: chatLanguage
      })
    });

    const data = await res.json();
    typingDiv.remove();

    appendChatMessage('assistant', data.answer);
  } catch (err) {
    typingDiv.remove();
    appendChatMessage('assistant', "Network connection error: Unable to reach the assistant. Please try again shortly.");
  }
}

// ----------------------------------------------------------------------------
// Global Demo Account Auto-Fill Helper
// ----------------------------------------------------------------------------
function fillDemo(email, pass, chipId) {
  const emailField = document.getElementById('email');
  const passField = document.getElementById('password');
  if (emailField) emailField.value = email;
  if (passField) passField.value = pass;

  // Visual feedback for selected chip
  document.querySelectorAll('.demo-chip').forEach(c => {
    c.classList.remove('ring-2', 'ring-[#1a6b5f]', 'bg-emerald-50');
  });
  if (chipId) {
    const activeChip = document.getElementById(chipId);
    if (activeChip) {
      activeChip.classList.add('ring-2', 'ring-[#1a6b5f]', 'bg-emerald-50');
    }
  }

  // Flash border highlight on fields
  if (emailField && passField) {
    emailField.classList.add('ring-2', 'ring-emerald-400');
    passField.classList.add('ring-2', 'ring-emerald-400');
    setTimeout(() => {
      emailField.classList.remove('ring-2', 'ring-emerald-400');
      passField.classList.remove('ring-2', 'ring-emerald-400');
    }, 600);
  }
}

// ----------------------------------------------------------------------------
// Global Password Visibility Toggle
// ----------------------------------------------------------------------------
function togglePasswordVisibility() {
  const passInput = document.getElementById('password');
  const eyeShow = document.getElementById('eye-icon-show');
  const eyeHide = document.getElementById('eye-icon-hide');
  if (!passInput) return;

  if (passInput.type === 'password') {
    passInput.type = 'text';
    if (eyeShow) eyeShow.classList.add('hidden');
    if (eyeHide) eyeHide.classList.remove('hidden');
  } else {
    passInput.type = 'password';
    if (eyeShow) eyeShow.classList.remove('hidden');
    if (eyeHide) eyeHide.classList.add('hidden');
  }
}

// ----------------------------------------------------------------------------
// Global Website Multilingual Switcher (Smooth Client & Server i18n)
// ----------------------------------------------------------------------------
let currentTranslations = {};

async function loadTranslations(lang) {
  try {
    const res = await fetch(`/api/translations/${lang}`);
    if (res.ok) {
      currentTranslations = await res.json();
      return currentTranslations;
    }
  } catch (err) {
    console.warn('Could not load translations:', err);
  }
  return null;
}

function applyTranslations(dict) {
  if (!dict) return;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        if (el.placeholder) el.placeholder = dict[key];
      } else {
        el.textContent = dict[key];
      }
    }
  });
  const htmlEl = document.querySelector('html');
  if (htmlEl) htmlEl.setAttribute('lang', dict['lang'] || 'en');
}

function switchLanguage(lang) {
  if (!['en', 'hi', 'kn'].includes(lang)) return;

  // 1. Immediately set cookie and localStorage so every navigation and click carries the chosen language
  document.cookie = `learnloop_lang=${lang};path=/;max-age=2592000;SameSite=Lax`;
  try {
    localStorage.setItem('learnloop_lang', lang);
  } catch (e) { }

  // 2. Navigate via /set_language to immediately render ALL page contents in the chosen language in 1 click
  window.location.href = `/set_language/${lang}`;
}

// ----------------------------------------------------------------------------
// Initialize on DOM load
// ----------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  }

  const savedLang = getCookie('learnloop_lang') || localStorage.getItem('learnloop_lang') || (document.body && document.body.getAttribute('data-user-lang')) || 'en';

  if (['en', 'hi', 'kn'].includes(savedLang)) {
    // 1. Highlight navbar language buttons accurately
    document.querySelectorAll('.lang-btn').forEach(btn => {
      if (btn.getAttribute('data-lang') === savedLang) {
        btn.className = "lang-btn px-2.5 py-1 rounded-lg transition-all font-semibold bg-[#e8a33d] text-[#10222c] shadow-sm";
      } else {
        btn.className = "lang-btn px-2.5 py-1 rounded-lg transition-all font-semibold text-gray-300 hover:text-white hover:bg-white/10";
      }
    });

    // 2. Set Chatbot language
    if (typeof setChatLanguage === 'function') {
      setChatLanguage(savedLang);
    }

    // 3. Translate all elements marked with data-i18n on the current page
    loadTranslations(savedLang).then(dict => {
      if (dict) applyTranslations(dict);
    });
  }

  // Initialize AI badge state
  updateAiBadge(!!getUserApiKey());

  // Trigger subtle shake animation on error alerts
  const errorAlerts = document.querySelectorAll('[role="alert"].bg-red-50');
  errorAlerts.forEach(alert => {
    alert.classList.add('animate-shake');
  });
});
