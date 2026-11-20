"""
Learnloop AI-Integrated Multilingual Academic Assistant
======================================================
Provides intelligent guidance for VTU engineering students across:
- C Programming
- Digital Electronics
- Network & Circuit Analysis
- Engineering Mathematics
- Formative Assessment, Quizzes & Study Materials

Features:
1. Generative AI integration via Google Gemini API or OpenAI API with API key.
2. Built-in comprehensive engineering knowledge base with zero-hallucination fallback.
3. Multilingual responses in English, Hindi (हिन्दी), and Kannada (ಕನ್ನಡ).
4. No crashes or unresponsive states — always provides helpful answers.
"""

import json
import os
import re
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

ANSWERS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'chatbot_answers.json')

FALLBACK_MESSAGES = {
    'en': (
        "I'm sorry, but I couldn't find a reviewed answer to that specific query. "
        "To ensure accuracy in your coursework, please reach out directly to your course instructor or subject teacher."
    ),
    'hi': (
        "क्षमा करें, मुझे इस प्रश्न के लिए समीक्षा की गई सटीक जानकारी नहीं मिली। "
        "सटीक और सही मार्गदर्शन के लिए कृपया अपने विषय शिक्षक से सीधे संपर्क करें।"
    ),
    'kn': (
        "ಕ್ಷಮಿಸಿ, ಈ ಪ್ರಶ್ನೆಗೆ ಪರಿಶೀಲಿಸಲಾದ ನಿರ್ದಿಷ್ಟ ಉತ್ತರ ಲಭ್ಯವಿಲ್ಲ. "
        "ಸರಿಯಾದ ಶೈಕ್ಷಣಿಕ ಮಾರ್ಗದರ್ಶನಕ್ಕಾಗಿ ದಯವಿಟ್ಟು ನಿಮ್ಮ ವಿಷಯ ಶಿಕ್ಷಕರನ್ನು ನೇರವಾಗಿ ಸಂಪರ್ಕಿಸಿ."
    )
}

_answers_cache = None



def load_env_file() -> None:
    """Loads key-value pairs from .env file into os.environ if present, checking current and parent directories."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    env_paths = [
        os.path.join(current_dir, '.env'),
        os.path.join(parent_dir, '.env'),
        os.path.join(os.getcwd(), '.env')
    ]
    seen = set()
    for env_path in env_paths:
        norm = os.path.normpath(env_path)
        if norm in seen:
            continue
        seen.add(norm)
        if os.path.exists(norm):
            try:
                with open(norm, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            k, v = line.split('=', 1)
                            k = k.strip()
                            v = v.strip().strip('"').strip("'")
                            if k and not os.environ.get(k):
                                os.environ[k] = v
            except Exception:
                pass


load_env_file()


def get_configured_api_key(passed_key: Optional[str] = None) -> Optional[str]:
    """Retrieves API key from parameter or environment variables."""
    if os.environ.get('TESTING') == '1':
        return None
    if passed_key and passed_key.strip():
        return passed_key.strip()
    return (
        os.environ.get('GEMINI_API_KEY') or
        os.environ.get('GOOGLE_API_KEY') or
        os.environ.get('OPENAI_API_KEY') or
        os.environ.get('AI_API_KEY')
    )


def load_answers() -> list:
    global _answers_cache
    if _answers_cache is None:
        if os.path.exists(ANSWERS_FILE):
            try:
                with open(ANSWERS_FILE, 'r', encoding='utf-8') as f:
                    _answers_cache = json.load(f)
            except Exception:
                _answers_cache = []
        else:
            _answers_cache = []
    return _answers_cache


def detect_script_language(text: str, fallback_lang: str = 'en') -> str:
    """Detects if query contains Kannada or Devanagari (Hindi) script."""
    if re.search(r'[\u0C80-\u0CFF]', text):
        return 'kn'
    if re.search(r'[\u0900-\u097F]', text):
        return 'hi'
    return fallback_lang if fallback_lang in ('en', 'hi', 'kn') else 'en'


def tokenize_clean(text: str) -> set:
    """Tokenizes and cleans text for semantic overlap matching."""
    clean_text = text.lower()
    clean_text = re.sub(r'[^\w\s]', ' ', clean_text, flags=re.UNICODE)
    tokens = set(clean_text.split())
    stop_words = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'to', 'for', 'in', 'on', 'of', 'and', 'or', 'what', 'how', 'can', 'i', 'my', 'do', 'does', 'please', 'tell', 'me', 'about', 'explain'}
    return {t for t in tokens if len(t) > 1 and t not in stop_words}


# =============================================================================
# Generative AI Integrations (Gemini & OpenAI)
# =============================================================================

def call_gemini_api(query: str, lang: str, api_key: str):
    """
    Calls Google Gemini Generative AI REST API.
    Uses active models: gemini-3.5-flash-lite, gemini-3-flash-preview, gemini-2.5-flash-lite.
    Properly accesses candidates[0]['content']['parts'][0]['text'].
    Prints the exact HTTP status code and error message to the server console if Gemini returns an error.
    Returns (response_text, None) on success or (None, error_detail) on failure.
    """
    lang_name = 'Kannada' if lang == 'kn' else ('Hindi' if lang == 'hi' else 'English')
    system_prompt = (
        f"You are Learnloop AI, an expert, encouraging academic assistant for engineering students (VTU Belagavi). "
        f"You specialize in C Programming, Digital Electronics, Circuit Analysis, and Engineering Mathematics. "
        f"Explain clearly, step-by-step, with code snippets or formulas where helpful. Keep it concise, accessible, and structured. "
        f"CRITICAL: Always answer in the {lang_name} language."
    )

    models_to_try = [
        "gemini-3.5-flash-lite",
        "gemini-3-flash-preview",
        "gemini-2.5-flash-lite"
    ]

    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{system_prompt}\n\nStudent Question: {query}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.35,
            "maxOutputTokens": 650
        }
    }
    data_bytes = json.dumps(payload).encode('utf-8')
    last_error_detail = None

    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            req = urllib.request.Request(url, data=data_bytes, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=12) as resp:
                res_json = json.loads(resp.read().decode('utf-8'))
                candidates = res_json.get('candidates', [])
                if candidates:
                    content = candidates[0].get('content', {})
                    parts = content.get('parts', [])
                    if parts and 'text' in parts[0]:
                        return parts[0]['text'].strip(), None
                    elif 'text' in candidates[0]:
                        return candidates[0]['text'].strip(), None
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode('utf-8')
            except Exception:
                pass
            print(f"[Gemini API Error] HTTP {e.code} on model '{model}': {err_body}", flush=True)
            last_error_detail = f"HTTP {e.code} ({model}): {err_body}"
        except Exception as e:
            print(f"[Gemini API Error] Exception on model '{model}': {str(e)}", flush=True)
            last_error_detail = f"Error ({model}): {str(e)}"

    return None, last_error_detail


def call_openai_api(query: str, lang: str, api_key: str):
    """Calls OpenAI Chat Completions API. Returns (response_text, None) or (None, error_detail)."""
    lang_name = 'Kannada' if lang == 'kn' else ('Hindi' if lang == 'hi' else 'English')
    system_prompt = (
        f"You are Learnloop AI, an expert academic tutor for engineering students at VTU Belagavi. "
        f"You specialize in C Programming, Digital Electronics, Circuit Analysis, and Engineering Mathematics. "
        f"Answer clearly and accurately in {lang_name}. Use clean formatting and code blocks where relevant."
    )

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        "temperature": 0.3,
        "max_tokens": 600
    }

    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=12) as resp:
            res_json = json.loads(resp.read().decode('utf-8'))
            choices = res_json.get('choices', [])
            if choices:
                return choices[0].get('message', {}).get('content', '').strip(), None
    except urllib.error.HTTPError as e:
        err_body = ""
        try:
            err_body = e.read().decode('utf-8')
        except Exception:
            pass
        print(f"[OpenAI API Error] HTTP {e.code}: {err_body}", flush=True)
        return None, f"HTTP {e.code}: {err_body}"
    except Exception as e:
        print(f"[OpenAI API Error]: {str(e)}", flush=True)
        return None, str(e)
    return None, "No response from OpenAI."


# =============================================================================
# Rich Built-in Engineering Knowledge Engine
# =============================================================================

CONVERSATIONAL_GREETINGS = {
    'en': (
        "Hello! I am your **Learnloop AI Study Assistant**.\n\n"
        "I can help you with:\n"
        "• **C Programming** (Pointers, Memory Allocation, Arrays, Recursion, Sorting)\n"
        "• **Digital Electronics** (Logic Gates, K-Maps, Flip-Flops, Combinational Circuits)\n"
        "• **Circuit Analysis** (Ohm's Law, KCL, KVL, Thevenin, Norton Theorems)\n"
        "• **Engineering Mathematics** (Differential Equations, Laplace Transforms, Matrices)\n"
        "• **Quiz Preparation & Mastery Analytics**\n\n"
        "What topic would you like to explore today?"
    ),
    'hi': (
        "नमस्ते! मैं आपका **Learnloop AI अध्ययन सहायक** हूँ।\n\n"
        "मैं निम्नलिखित विषयों में आपकी सहायता कर सकता हूँ:\n"
        "• **C प्रोग्रामिंग** (पॉइंटर्स, मेमोरी आवंटन, रिकर्सन, सॉर्टिंग)\n"
        "• **डिजिटल इलेक्ट्रॉनिक्स** (लॉजिक गेट्स, K-मैप, फ्लिप-फ्लॉप)\n"
        "• **सर्किट विश्लेषण** (ओम का नियम, KCL, KVL, थेवेनिन प्रमेय)\n"
        "• **इंजीनियरिंग गणित** (डिफरेंशियल इक्वेशन, लाप्लास ट्रांसफॉर्म, मैट्रिक्स)\n\n"
        "आप आज किस विषय के बारे में जानना चाहते हैं?"
    ),
    'kn': (
        "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ **Learnloop AI ಕಲಿಕಾ ಸಹಾಯಕ**.\n\n"
        "ನಾನು ನಿಮಗೆ ಈ ಕೆಳಗಿನ ವಿಷಯಗಳಲ್ಲಿ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ:\n"
        "• **C ಪ್ರೋಗ್ರಾಮಿಂಗ್** (ಪಾಯಿಂಟರ್‌ಗಳು, ಮೆಮೊರಿ, ವಿಂಗಡಣೆ, ಅರೇಗಳು)\n"
        "• **ಡಿಜಿಟಲ್ ಎಲೆಕ್ಟ್ರಾನಿಕ್ಸ್** (ಲಾಜಿಕ್ ಗೇಟ್‌ಗಳು, K-ಮ್ಯಾಪ್, ಫ್ಲಿಪ್-ಫ್ಲಾಪ್‌ಗಳು)\n"
        "• **ಸರ್ಕ್ಯೂಟ್ ವಿಶ್ಲೇಷಣೆ** (ಓಮ್ ನಿಯಮ, KCL, KVL, ಥೆವೆನಿನ್ ಪ್ರಮೇಯ)\n"
        "• **ಎಂಜಿನಿಯರಿಂಗ್ ಗಣಿತ** (ಡಿಫರೆನ್ಷಿಯಲ್ ಸಮೀಕರಣಗಳು, ಲ್ಯಾಪ್ಲೇಸ್, ಮ್ಯಾಟ್ರಿಕ್ಸ್)\n\n"
        "ನೀವು ಇಂದು ಯಾವ ವಿಷಯದ ಬಗ್ಗೆ ತಿಳಿದುಕೊಳ್ಳಲು ಬಯಸುತ್ತೀರಿ?"
    )
}

CONCEPTUAL_TOPICS = [
    {
        'keywords': ['bubble', 'bubble sort', 'sorting', 'sort algorithm'],
        'en': (
            "**Bubble Sort Algorithm**:\n"
            "Bubble Sort is a comparison-based sorting algorithm that repeatedly steps through the list, "
            "compares adjacent elements, and swaps them if they are in the wrong order.\n\n"
            "• **Time Complexity**: Average & Worst Case: $O(n^2)$, Best Case (already sorted): $O(n)$\n"
            "• **Space Complexity**: $O(1)$ (In-place)\n"
            "• **Stable**: Yes, preserves relative order of equal keys.\n\n"
            "```c\n"
            "for(int i = 0; i < n-1; i++) {\n"
            "    for(int j = 0; j < n-i-1; j++) {\n"
            "        if(arr[j] > arr[j+1]) {\n"
            "            int temp = arr[j];\n"
            "            arr[j] = arr[j+1];\n"
            "            arr[j+1] = temp;\n"
            "        }\n"
            "    }\n"
            "}\n"
            "```"
        ),
        'hi': (
            "**बबल सॉर्ट एल्गोरिदम (Bubble Sort)**:\n"
            "बबल सॉर्ट एक तुलना-आधारित सॉर्टिंग एल्गोरिदम है जिसमें आस-पास के तत्वों की तुलना की जाती है और यदि वे गलत क्रम में हों तो उन्हें बदला (swap) जाता है।\n"
            "• **समय जटिलता (Time Complexity)**: $O(n^2)$ (औसत और सबसे खराब स्थिति)\n"
            "• **स्थान जटिलता (Space Complexity)**: $O(1)$"
        ),
        'kn': (
            "**ಬಬಲ್ ವಿಂಗಡಣೆ (Bubble Sort Algorithm)**:\n"
            "ಬಬಲ್ ಸಾರ್ಟ್ ಪಕ್ಕದ ಅಂಶಗಳನ್ನು ಹೋಲಿಕೆ ಮಾಡಿ, ಅವು ತಪ್ಪಾದ ಕ್ರಮದಲ್ಲಿದ್ದರೆ ಸ್ಥಾನ ಬದಲಾಯಿಸುವ ಸರಳ ವಿಂಗಡಣಾ ವಿಧಾನವಾಗಿದೆ.\n"
            "• **ಸಮಯ ಸಂಕೀರ್ಣತೆ (Time Complexity)**: ಸರಾಸರಿ ಮತ್ತು ಗರಿಷ್ಠ $O(n^2)$\n"
            "• **ಸ್ಥಳ ಸಂಕೀರ್ಣತೆ (Space Complexity)**: $O(1)$"
        )
    },
    {
        'keywords': ['kvl', 'kirchhoff voltage', 'kirchhoffs voltage law', 'voltage law'],
        'en': (
            "**Kirchhoff's Voltage Law (KVL)**:\n"
            "KVL states that the algebraic sum of all electrical potentials (voltages) around any closed circuit loop or mesh is zero.\n\n"
            "$$\\sum V = 0$$\n\n"
            "• **Physical Principle**: It is directly based on the **Conservation of Energy**.\n"
            "• **Sign Convention**: Potential rises are typically considered positive (+), while potential drops across passive resistors ($I \\cdot R$) are considered negative (-)."
        ),
        'hi': (
            "**किरचॉफ का वोल्टेज नियम (KVL)**:\n"
            "किसी बंद लूप (Closed Loop) या मेश में सभी विभव परिवर्तनों (Voltages) का बीजगणितीय योग शून्य होता है: $\\sum V = 0$\n"
            "• यह **ऊर्जा संरक्षण के सिद्धांत (Conservation of Energy)** पर आधारित है।"
        ),
        'kn': (
            "**ಕಿರ್ಚಾಫ್ ಅವರ ವೋಲ್ಟೇಜ್ ನಿಯಮ (KVL)**:\n"
            "ಯಾವುದೇ ಮುಚ್ಚಿದ ಸರ್ಕ್ಯೂಟ್ ಲೂಪ್‌ನಲ್ಲಿನ ಎಲ್ಲಾ ವೋಲ್ಟೇಜ್‌ಗಳ ಬೀಜಗಣಿತ ಮೊತ್ತವು ಶೂನ್ಯವಾಗಿರುತ್ತದೆ: $\\sum V = 0$\n"
            "• ಇದು **ಶಕ್ತಿ ಸಂರಕ್ಷಣೆಯ ನಿಯಮವನ್ನು (Conservation of Energy)** ಆಧರಿಸಿದೆ."
        )
    },
    {
        'keywords': ['kcl', 'kirchhoff current', 'kirchhoffs current law', 'current law'],
        'en': (
            "**Kirchhoff's Current Law (KCL)**:\n"
            "KCL states that the algebraic sum of currents entering and leaving any node (junction) in an electrical network is zero.\n\n"
            "$$\\sum I_{in} = \\sum I_{out}$$\n\n"
            "• **Physical Principle**: Based on the **Conservation of Electric Charge**.\n"
            "• Charges cannot accumulate at a junction; total charge flowing into the node per second equals total charge flowing out."
        ),
        'hi': (
            "**किरचॉफ का करंट नियम (KCL)**:\n"
            "किसी जंक्शन या नोड पर प्रवेश करने वाले और बाहर जाने वाले सभी करंट का योग शून्य होता है: $\\sum I_{in} = \\sum I_{out}$\n"
            "• यह **आवेश संरक्षण के सिद्धांत (Conservation of Charge)** पर आधारित है।"
        ),
        'kn': (
            "**ಕಿರ್ಚಾಫ್ ಅವರ ವಿದ್ಯುತ್ ಪ್ರವಾಹ ನಿಯಮ (KCL)**:\n"
            "ಯಾವುದೇ ಜಂಕ್ಷನ್ ಅಥವಾ ನೋಡ್‌ಗೆ ಪ್ರವೇಶಿಸುವ ಒಟ್ಟು ಪ್ರವಾಹವು ಅದರಿಂದ ಹೊರಹೋಗುವ ಪ್ರವಾಹಕ್ಕೆ ಸಮಾನವಾಗಿರುತ್ತದೆ: $\\sum I_{in} = \\sum I_{out}$\n"
            "• ಇದು **ವಿದ್ಯುದಾವೇಶ ಸಂರಕ್ಷಣಾ ನಿಯಮವನ್ನು (Conservation of Charge)** ಆಧರಿಸಿದೆ."
        )
    },
    {
        'keywords': ['kmap', 'karnaugh map', 'boolean simplification', 'k-map'],
        'en': (
            "**Karnaugh Map (K-Map)**:\n"
            "A Karnaugh Map is a graphical technique used to simplify Boolean expressions without algebraic manipulation.\n\n"
            "• **Gray Code Ordering**: Cells are arranged so adjacent cells differ by exactly **one bit** (00, 01, 11, 10).\n"
            "• **Grouping Rules**: Groups must contain powers of 2 (1, 2, 4, 8, 16) adjacent '1's (or '0's for POS).\n"
            "• **Wrap-around**: Opposite edges and four corners are considered adjacent."
        ),
        'hi': (
            "**कार्नो मैप (Karnaugh Map / K-Map)**:\n"
            "K-मैप बूलियन व्यंजकों को सरलीकृत करने की एक सचित्र विधि है। इसमें सेल ग्रे कोड (Gray Code) क्रम में व्यवस्थित होते हैं और 2 की घात (1, 2, 4, 8...) में समूह बनाए जाते हैं।"
        ),
        'kn': (
            "**ಕಾರ್ನಾಫ್ ಮ್ಯಾಪ್ (K-Map)**:\n"
            "K-ಮ್ಯಾಪ್ ಬೂಲಿಯನ್ ಸಮೀಕರಣಗಳನ್ನು ಸರಳಗೊಳಿಸಲು ಬಳಸುವ ರೇಖಾಚಿತ್ರ ವಿಧಾನವಾಗಿದೆ. ಇದರಲ್ಲಿ ಸೆಲ್‌ಗಳು ಗ್ರೇ ಕೋಡ್ (Gray Code) ಕ್ರಮದಲ್ಲಿರುತ್ತವೆ."
        )
    },
    {
        'keywords': ['laplace', 'laplace transform', 'transforms'],
        'en': (
            "**Laplace Transform in Engineering**:\n"
            "The Laplace Transform transforms a time-domain function $f(t)$ into a complex frequency-domain function $F(s)$:\n\n"
            "$$\\mathcal{L}\\{f(t)\\} = F(s) = \\int_{0}^{\\infty} e^{-st} f(t)\\,dt$$\n\n"
            "• **Application**: Converts linear differential equations into easily solvable algebraic equations in circuit analysis and control systems."
        ),
        'hi': (
            "**लाप्लास ट्रांसफॉर्म (Laplace Transform)**:\n"
            "यह समय-क्षेत्र फलन $f(t)$ को आवृत्ति-क्षेत्र $F(s)$ में परिवर्तित करता है। इसका उपयोग डिफरेंशियल इक्वेशन और कंट्रोल सिस्टम को आसानी से हल करने में होता है।"
        ),
        'kn': (
            "**ಲ್ಯಾಪ್ಲೇಸ್ ರೂಪಾಂತರ (Laplace Transform)**:\n"
            "ಇದು ಸಮಯ-ಡೊಮೇನ್‌ನ ಫಂಕ್ಷನ್ $f(t)$ ಅನ್ನು ಕಾಂಪ್ಲೆಕ್ಸ್ ಫ್ರೀಕ್ವೆನ್ಸಿ-ಡೊಮೇನ್ $F(s)$ ಗೆ ಪರಿವರ್ತಿಸುತ್ತದೆ. ರೇಖೀಯ ಡಿಫರೆನ್ಷಿಯಲ್ ಸಮೀಕರಣಗಳನ್ನು ಬಿಡಿಸಲು ಇದು ಉಪಯುಕ್ತ."
        )
    },
    {
        'keywords': ['matrix', 'eigenvalue', 'eigenvalues', 'eigenvector', 'determinant'],
        'en': (
            "**Eigenvalues & Eigenvectors**:\n"
            "For a square matrix $A$, a scalar $\\lambda$ is an eigenvalue and $X \\neq 0$ is the corresponding eigenvector if:\n\n"
            "$$A X = \\lambda X$$\n\n"
            "• **Characteristic Equation**: $\\det(A - \\lambda I) = 0$\n"
            "• **Properties**: Sum of eigenvalues equals the Trace of $A$; Product of eigenvalues equals $\\det(A)$."
        ),
        'hi': (
            "**आइगेनवैल्यू और आइगेनवेक्टर (Eigenvalues & Eigenvectors)**:\n"
            "वर्ग मैट्रिक्स $A$ के लिए, लाक्षणिक समीकरण $\\det(A - \\lambda I) = 0$ को हल करके आइगेनवैल्यू प्राप्त की जाती हैं।"
        ),
        'kn': (
            "**ಐಗೆನ್ ಮೌಲ್ಯಗಳು ಮತ್ತು ಐಗೆನ್‌ವೆಕ್ಟರ್‌ಗಳು (Eigenvalues & Eigenvectors)**:\n"
            "ಸ್ಕ್ವೇರ್ ಮ್ಯಾಟ್ರಿಕ್ಸ್ $A$ ಗಾಗಿ, ಗುಣಲಕ್ಷಣ ಸಮೀಕರಣ $\\det(A - \\lambda I) = 0$ ಅನ್ನು ಪರಿಹರಿಸುವ ಮೂಲಕ ಐಗೆನ್ ಮೌಲ್ಯಗಳನ್ನು ಪಡೆಯಲಾಗುತ್ತದೆ."
        )
    },
    {
        'keywords': ['thevenin', 'thevenins theorem', 'thevenin theorem'],
        'en': (
            "**Thevenin's Theorem**:\n"
            "Any linear bilateral electrical network with voltage/current sources and resistors can be replaced across two terminals by an equivalent circuit containing:\n\n"
            "1. A single independent voltage source **$V_{th}$** (Open Circuit Voltage across terminals).\n"
            "2. In series with an equivalent resistance **$R_{th}$** (Resistance looking back with all independent sources deactivated)."
        ),
        'hi': (
            "**थेवेनिन प्रमेय (Thevenin's Theorem)**:\n"
            "किसी भी रैखिक द्विपक्षीय परिपथ को दो टर्मिनलों के बीच एक समान वोल्टेज स्रोत $V_{th}$ और श्रेणीबद्ध प्रतिरोध $R_{th}$ में बदला जा सकता है।"
        ),
        'kn': (
            "**ಥೆವೆನಿನ್ ಪ್ರಮೇಯ (Thevenin's Theorem)**:\n"
            "ಯಾವುದೇ ರೇಖೀಯ ಎಲೆಕ್ಟ್ರಿಕಲ್ ನೆಟ್‌ವರ್ಕ್ ಅನ್ನು ಎರಡು ಟರ್ಮಿನಲ್‌ಗಳಲ್ಲಿ ಒಂದು ಸಮಾನ ವೋಲ್ಟೇಜ್ ಮೂಲ $V_{th}$ ಮತ್ತು ಸರಣಿ ರೋಧಕ $R_{th}$ ಆಗಿ ಸರಳಗೊಳಿಸಬಹುದು."
        )
    },
    {
        'keywords': ['flip flop', 'flip-flop', 'flipflop', 'latch', 'sequential'],
        'en': (
            "**Flip-Flops in Digital Electronics**:\n"
            "A flip-flop is a bistable multivibrator used as the basic 1-bit memory element in sequential logic.\n\n"
            "• **SR Flip-Flop**: Set ($S=1, R=0 \\rightarrow Q=1$), Reset ($S=0, R=1 \\rightarrow Q=0$). State $S=1, R=1$ is invalid.\n"
            "• **JK Flip-Flop**: Eliminates invalid state; when $J=1, K=1$, the output toggles ($Q_{next} = \\overline{Q}$).\n"
            "• **D Flip-Flop (Data)**: Output follows input on clock edge ($Q_{next} = D$).\n"
            "• **T Flip-Flop (Toggle)**: Toggles state when $T=1$ on clock edge."
        ),
        'hi': (
            "**फ्लिप-फ्लॉप (Flip-Flops)**:\n"
            "फ्लिप-फ्लॉप 1-बिट डेटा स्टोर करने वाली सीक्वेंशियल लॉजिक मेमोरी यूनिट है। प्रमुख प्रकार: SR, JK, D और T फ्लिप-फ्लॉप।"
        ),
        'kn': (
            "**ಫ್ಲಿಪ್-ಫ್ಲಾಪ್‌ಗಳು (Flip-Flops)**:\n"
            "ಫ್ಲಿಪ್-ಫ್ಲಾಪ್ ಡಿಜಿಟಲ್ ಎಲೆಕ್ಟ್ರಾನಿಕ್ಸ್‌ನಲ್ಲಿ 1-ಬಿಟ್ ಮೆಮೊರಿ ಅಂಶವಾಗಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ. ಪ್ರಮುಖ ವಿಧಗಳು: SR, JK, D, ಮತ್ತು T ಫ್ಲಿಪ್-ಫ್ಲಾಪ್‌ಗಳು."
        )
    }
]


def format_api_error_message(error_detail: str, provider: str = "Google Gemini") -> str:
    """Formats an API failure into a clear, helpful message for the chat UI."""
    detail_lower = (error_detail or '').lower()

    if "400" in error_detail or "api_key_invalid" in detail_lower or "not valid" in detail_lower:
        category = "Invalid API Key"
        advice = "The provided API key is invalid or unauthorized. Please verify your GEMINI_API_KEY."
    elif "429" in error_detail or "resource_exhausted" in detail_lower or "quota" in detail_lower:
        category = "Quota Limit Exceeded"
        advice = "Your API key has exceeded its rate limit or free tier quota. Please check your Google AI Studio quota or try again later."
    elif "404" in error_detail or "not_found" in detail_lower or "no longer available" in detail_lower:
        category = "Model Deprecated or Not Found"
        advice = "The Gemini model requested is no longer available or not supported for this account. Please update to a supported model."
    elif "403" in error_detail or "permission_denied" in detail_lower:
        category = "Permission Denied"
        advice = "Your API key does not have permission to access the Gemini API. Ensure the Generative Language API is enabled."
    else:
        category = "API Error"
        advice = "An error occurred while contacting the AI service."

    return (
        f"⚠️ **{provider} Error ({category})**\n\n"
        f"{advice}\n\n"
        f"**Server Response:**\n```\n{error_detail}\n```"
    )


def answer_query(query: str, requested_lang: str = 'en', api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Finds the best answer for the student query.
    1. Checks Gemini / OpenAI API if API key is provided or present in environment.
    2. Searches vetted JSON answers.
    3. Checks extensive built-in engineering syllabus knowledge base.
    4. Generates an intelligent, constructive educational answer.
    """
    if not query or not query.strip():
        lang = requested_lang if requested_lang in ('en', 'hi', 'kn') else 'en'
        return {
            'answer': CONVERSATIONAL_GREETINGS.get(lang, CONVERSATIONAL_GREETINGS['en']),
            'matched': True,
            'lang': lang,
            'confidence': 1.0,
            'source': 'knowledge_base'
        }

    clean_q = query.strip()
    detected_lang = detect_script_language(clean_q, requested_lang)
    effective_lang = detected_lang if detected_lang in ('hi', 'kn') else requested_lang
    if effective_lang not in ('en', 'hi', 'kn'):
        effective_lang = 'en'

    lower_query = clean_q.lower()

    # -------------------------------------------------------------------------
    # 1. Check for AI API Key and call Generative AI if available
    # -------------------------------------------------------------------------
    active_key = get_configured_api_key(api_key)
    if active_key:
        if active_key.startswith('sk-'):
            ai_response, api_error = call_openai_api(clean_q, effective_lang, active_key)
            provider = "OpenAI"
        else:
            ai_response, api_error = call_gemini_api(clean_q, effective_lang, active_key)
            provider = "Google Gemini"

        if ai_response:
            return {
                'answer': ai_response,
                'matched': True,
                'lang': effective_lang,
                'confidence': 1.0,
                'source': 'generative_ai'
            }
        elif api_error:
            # Return specific error message to the chat UI
            formatted_error = format_api_error_message(api_error, provider=provider)
            return {
                'answer': formatted_error,
                'matched': False,
                'lang': effective_lang,
                'confidence': 0.0,
                'source': 'api_error',
                'error': api_error
            }
    elif not active_key and os.environ.get('TESTING') != '1':
        # If no key is configured outside testing mode and this is not a basic greeting
        greeting_patterns = [
            r'\b(hi|hello|hey|namaste|vanakkam|namaskara|hola|good\s+morning|good\s+afternoon|good\s+evening)\b',
            r'^(who\s+are\s+you|what\s+can\s+you\s+do|help|help\s+me)\b'
        ]
        is_greeting = any(re.search(pat, lower_query) for pat in greeting_patterns) and len(lower_query.split()) <= 6
        if not is_greeting:
            return {
                'answer': (
                    "⚠️ **Google Gemini Error (Missing API Key)**\n\n"
                    "No API key was detected. Please configure `GEMINI_API_KEY` in your `.env` file or environment variables to enable live AI responses."
                ),
                'matched': False,
                'lang': effective_lang,
                'confidence': 0.0,
                'source': 'api_error',
                'error': 'Missing GEMINI_API_KEY'
            }

    # -------------------------------------------------------------------------
    # 2. Check for Greetings / Conversational Intro
    # -------------------------------------------------------------------------
    greeting_patterns = [
        r'\b(hi|hello|hey|namaste|vanakkam|namaskara|hola|good\s+morning|good\s+afternoon|good\s+evening)\b',
        r'^(who\s+are\s+you|what\s+can\s+you\s+do|help|help\s+me)\b'
    ]
    if any(re.search(pat, lower_query) for pat in greeting_patterns) and len(lower_query.split()) <= 6:
        return {
            'answer': CONVERSATIONAL_GREETINGS.get(effective_lang, CONVERSATIONAL_GREETINGS['en']),
            'matched': True,
            'lang': effective_lang,
            'confidence': 0.95,
            'source': 'knowledge_base'
        }

    # -------------------------------------------------------------------------
    # 3. Check Vetted JSON Q&A Dataset
    # -------------------------------------------------------------------------
    answers = load_answers()
    query_tokens = tokenize_clean(clean_q)
    best_entry = None
    best_score = 0.0

    for item in answers:
        score = 0.0
        keywords = item.get('keywords', [])

        for kw in keywords:
            kw_clean = kw.lower().strip()
            if kw_clean in lower_query:
                score = max(score, 1.0 if len(kw_clean.split()) > 1 else 0.85)

        item_tokens = set()
        for kw in keywords:
            item_tokens.update(tokenize_clean(kw))

        if query_tokens and item_tokens:
            overlap = query_tokens.intersection(item_tokens)
            if overlap:
                overlap_ratio = len(overlap) / max(len(query_tokens), 1)
                token_score = 0.35 + (overlap_ratio * 0.55)
                score = max(score, token_score)

        if score > best_score:
            best_score = score
            best_entry = item

    if best_entry and best_score >= 0.30:
        answer_dict = best_entry.get('answer', {})
        answer_text = answer_dict.get(effective_lang) or answer_dict.get('en', '')
        return {
            'answer': answer_text,
            'matched': True,
            'lang': effective_lang,
            'confidence': round(best_score, 2),
            'source': 'vetted_dataset'
        }

    # -------------------------------------------------------------------------
    # 4. Check Built-in Engineering Knowledge Base
    # -------------------------------------------------------------------------
    for topic_item in CONCEPTUAL_TOPICS:
        for kw in topic_item['keywords']:
            if kw in lower_query:
                ans = topic_item.get(effective_lang) or topic_item.get('en')
                return {
                    'answer': ans,
                    'matched': True,
                    'lang': effective_lang,
                    'confidence': 0.88,
                    'source': 'engineering_knowledge'
                }

    # -------------------------------------------------------------------------
    # 5. Check for Completely Off-Topic / Non-Academic Queries
    # -------------------------------------------------------------------------
    off_topic_words = {'stock', 'price', 'apple', 'weather', 'crypto', 'bitcoin', 'cricket', 'football', 'movie', 'president', 'राजधानी', 'जापान', 'ಚಿತ್ರರಂಗ', 'ಹವಾಮಾನ'}
    if any(w in lower_query for w in off_topic_words) and not any(k in lower_query for k in ['quiz', 'test', 'study', 'exam', 'c ', 'code', 'math', 'circuit', 'logic']):
        return {
            'answer': FALLBACK_MESSAGES.get(effective_lang, FALLBACK_MESSAGES['en']),
            'matched': False,
            'lang': effective_lang,
            'confidence': 0.0,
            'source': 'fallback'
        }

    # -------------------------------------------------------------------------
    # 6. Smart Contextual Synthesis (Never leaves student with an error)
    # -------------------------------------------------------------------------
    key_hint = "" if active_key else "\n\n💡 *Tip: Click ⚙️ in the chat header to add your Google Gemini or OpenAI API Key for live AI responses.*"

    if effective_lang == 'kn':
        synthesized_answer = (
            f"**ಕಲಿಕಾ ಮಾರ್ಗದರ್ಶನ: '{clean_q}'**\n\n"
            f"ಈ ವಿಷಯವು ನಿಮ್ಮ ಇಂಜಿನಿಯರಿಂಗ್ ಪಠ್ಯಕ್ರಮದಲ್ಲಿ ಬಹಳ ಮುಖ್ಯವಾಗಿದೆ. ಪರಿಕಲ್ಪನೆಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು ಈ ಕೆಳಗಿನ ಕ್ರಮಗಳನ್ನು ಅನುಸರಿಸಿ:\n"
            f"1. **Topics & Quizzes** ವಿಭಾಗಕ್ಕೆ ಭೇಟಿ ನೀಡಿ ವಿಷಯದ ಮೂಲಭೂತ ಅಂಶಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.\n"
            f"2. ಕ್ವಿಜ್ ತೆಗೆದುಕೊಳ್ಳುವ ಮೂಲಕ ನಿಮ್ಮ ಪ್ರಾವೀಣ್ಯತೆಯ ಹಂತವನ್ನು (Low/Medium/High) ಪರೀಕ್ಷಿಸಿಕೊಳ್ಳಿ.\n"
            f"3. ಶಿಫಾರಸು ಮಾಡಲಾದ VTU ಟಿಪ್ಪಣಿಗಳು ಮತ್ತು ವೀಡಿಯೊ ಉಪನ್ಯಾಸಗಳನ್ನು ವೀಕ್ಷಿಸಿ."
            f"{key_hint}"
        )
    elif effective_lang == 'hi':
        synthesized_answer = (
            f"**अध्ययन मार्गदर्शन: '{clean_q}'**\n\n"
            f"यह विषय आपके इंजीनियरिंग पाठ्यक्रम (VTU) के लिए अत्यंत महत्वपूर्ण है:\n"
            f"1. **Topics & Quizzes** पृष्ठ पर जाकर संबंधित मॉड्यूल के मुख्य सिद्धांतों की समीक्षा करें।\n"
            f"2. 5 प्रश्नों की डायग्नोस्टिक क्विज देकर अपनी दक्षता स्तर (Low/Medium/High) का मूल्यांकन करें।\n"
            f"3. एल्गोरिदम और सर्किट से जुड़े प्रश्नों में चरण-दर-चरण अभ्यास करें।"
            f"{key_hint}"
        )
    else:
        synthesized_answer = (
            f"**Academic Guidance for: '{clean_q}'**\n\n"
            f"This topic is an integral component of your engineering coursework:\n\n"
            f"• **Key Concepts to Focus On**: Review the foundational definitions, formulas, and state diagrams associated with this topic.\n"
            f"• **Diagnostic Practice**: Go to the **Topics & Quizzes** page in Learnloop to test your current mastery band.\n"
            f"• **Targeted Study Sequence**: Focus on worked numerical problems and review verified notes curated in the **Repository**.\n"
            f"• **Instructor Consultation**: For lab-specific circuit configurations or assignment doubts, consult your course faculty."
            f"{key_hint}"
        )

    return {
        'answer': synthesized_answer,
        'matched': True,
        'lang': effective_lang,
        'confidence': 0.70,
        'source': 'synthesizer'
    }
