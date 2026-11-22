"""
Complete Trilingual Engineering Study Notes (VTU Syllabus Aligned)
==================================================================
Covers all 14 topics across:
1. C Programming
2. Digital Electronics
3. Engineering Mathematics
4. Basic Circuit Analysis

Each topic is structured into 4 essential pedagogical sections:
1. Detailed Concept Explanation (Step-by-step intuitive explanation)
2. Key Rules, Syntax & Formulas (Equations, truth tables, rules, syntax)
3. Annotated Example (Commented code or step-by-step numerical)
4. Quiz & VTU Exam Quick-Check Points (Direct traps, edge cases, formulas)

Provided with complete natural translations in English, Kannada, and Hindi.
"""

COMPLETE_STUDY_NOTES = {
    # =========================================================================
    # SUBJECT 1: C PROGRAMMING
    # =========================================================================
    "Arrays in C": {
        "title": "Comprehensive Study Notes: Arrays in C",
        "title_kn": "ಸಮಗ್ರ ಅಧ್ಯಯನ ಟಿಪ್ಪಣಿಗಳು: ಸಿ ಭಾಷೆಯಲ್ಲಿ ಅರೇಗಳು (Arrays in C)",
        "title_hi": "विस्तृत अध्ययन नोट्स: सी में एरे (Arrays in C)",
        "desc": "Master 1D & 2D array memory layout, 0-based indexing, pointer equivalences, and VTU exam problem-solving.",
        "desc_kn": "ಅರೇ ಮೆಮೊರಿ ವಿನ್ಯಾಸ, 0-ಆಧಾರಿತ ಇಂಡೆಕ್ಸಿಂಗ್, ಪಾಯಿಂಟರ್ ಸಮಾನತೆ ಮತ್ತು ಪರೀಕ್ಷಾ ಲೆಕ್ಕಾಚಾರಗಳನ್ನು ಕಲಿಯಿರಿ.",
        "desc_hi": "1D और 2D एरे मेमोरी लेआउट, शून्य-आधारित इंडेक्सिंग, पॉइंटर समानता और परीक्षा प्रश्नों को समझें।",
        "content_en": """## 1. Detailed Concept Explanation
An **Array** in C is a contiguous, fixed-size collection of elements of the same data type stored sequentially in memory. 

### Why Arrays Matter:
- **Contiguous Allocation:** All elements are stored in adjacent memory locations without gaps.
- **Constant-Time Direct Access:** Any element `arr[i]` can be accessed immediately in **O(1)** time using its index:
  $$\\text{Address of } arr[i] = \\text{Base Address} + i \\times \\text{sizeof}(\\text{datatype})$$
- **Zero-Based Indexing:** The first element is always located at index `0`, and the last valid element in an array of size `N` is at index `N - 1`.
- **Decay to Pointer:** In expressions, the name of an array (e.g., `arr`) automatically decays to a constant pointer pointing to its first element (`&arr[0]`).
- **No Automatic Bounds Checking:** C does **not** check array boundaries at compile time or runtime. Accessing `arr[N]` compiles but invokes **Undefined Behavior (UB)**, risking segmentation faults or data corruption.

---

## 2. Key Rules, Syntax & Formulas

### Essential Declarations & Initializations:
```c
int a[5] = {10, 20, 30, 40, 50}; // Fully initialized
int b[5] = {1, 2};               // Partial: b[0]=1, b[1]=2, remaining b[2..4] = 0
int c[]  = {1, 2, 3};            // Auto-sized: compiler sets size to 3
int mat[2][3] = {{1, 2, 3}, {4, 5, 6}}; // 2D array: Row-Major Order in memory
```

### Critical Formulas for VTU Quizzes:
- **Number of Elements in Array:**
  $$\\text{Length} = \\frac{\\text{sizeof}(arr)}{\\text{sizeof}(arr[0])}$$
- **1D Element Address:**
  $$\\text{Loc}(arr[i]) = \\text{Base} + (i - \\text{LowerBound}) \\times w$$
- **2D Element Address (Row-Major Order):**
  $$\\text{Loc}(mat[i][j]) = \\text{Base} + [i \\times C + j] \\times w$$
  *(where $C$ is the total number of columns and $w = \\text{sizeof}(\\text{datatype})$).*
- **Array-Pointer Identity:**
  $$arr[i] \\equiv *(arr + i) \\equiv *(i + arr) \\equiv i[arr]$$

---

## 3. Annotated Example
```c
#include <stdio.h>

int main() {
    int scores[5] = {88, 92, 79, 95, 84};
    int n = sizeof(scores) / sizeof(scores[0]); // n = 5
    int sum = 0;

    // Traverse elements using pointer arithmetic and indexing
    for (int i = 0; i < n; i++) {
        sum += *(scores + i); // Identical to sum += scores[i]
    }

    float average = (float)sum / n;
    printf("Total Sum = %d, Class Average = %.2f\\n", sum, average);

    // Demonstration of base address equivalence:
    printf("Base: %p == %p\\n", (void*)scores, (void*)&scores[0]);
    return 0;
}
```

---

## 4. Quiz & VTU Exam Quick-Check Points
- [x] **0-Indexing Trap:** In `int arr[10];`, valid indices are strictly `0` to `9`. `arr[10]` is an off-by-one illegal memory access.
- [x] **Uninitialized Locals:** Local arrays declared without values contain **garbage values**, while global/static arrays auto-initialize to zero.
- [x] **2D Array Parameter Rule:** When passing a 2D array to a function, the **column dimension must always be specified** (e.g., `void func(int mat[][4], int rows);`). The row dimension can be omitted.
- [x] **`sizeof` inside Functions:** When an array is passed to a function, it decays to a pointer. Calling `sizeof(arr)` inside the function yields the **pointer size (4 or 8 bytes)**, NOT the total array size!""",
        "content_kn": """## 1. ಪರಿಕಲ್ಪನೆಯ ವಿವರವಾದ ವಿವರಣೆ (Concept Explanation)
C ಪ್ರೋಗ್ರಾಮಿಂಗ್‌ನಲ್ಲಿ **ಅರೇ (Array)** ಎಂಬುದು ಒಂದೇ ಡೇಟಾ ಪ್ರಕಾರದ (Data Type) ಅಂಶಗಳನ್ನು ಮೆಮೊರಿಯಲ್ಲಿ ನಿರಂತರವಾಗಿ (Contiguously) ಸಂಗ್ರಹಿಸುವ ಒಂದು ಮೂಲ ರಚನೆಯಾಗಿದೆ.

### ಅರೇಗಳ ಪ್ರಮುಖ ಲಕ್ಷಣಗಳು:
- **ನಿರಂತರ ಮೆಮೊರಿ ಹಂಚಿಕೆ (Contiguous Allocation):** ಎಲ್ಲಾ ಅಂಶಗಳು ಒಂದರ ಪಕ್ಕದಲ್ಲಿ ಒಂದರಂತೆ ಮೆಮೊರಿಯಲ್ಲಿ ಶೇಖರವಾಗುತ್ತವೆ.
- **ತ್ವರಿತ ಪ್ರವೇಶ (Direct O(1) Access):** ಯಾವುದೇ ಅಂಶವನ್ನು ಅದರ ಇಂಡೆಕ್ಸ್ ಬಳಸಿ ತಕ್ಷಣವೇ ಪಡೆಯಬಹುದು:
  $$\\text{ವಿಳಾಸ} = \\text{ಮೂಲ ವಿಳಾಸ (Base)} + i \\times \\text{sizeof}(\\text{ಡೇಟಾ ಪ್ರಕಾರ})$$
- **ಶೂನ್ಯ-ಆಧಾರಿತ ಇಂಡೆಕ್ಸಿಂಗ್ (Zero-Based):** ಮೊದಲ ಅಂಶವು ಯಾವಾಗಲೂ ಇಂಡೆಕ್ಸ್ `0` ನಲ್ಲಿದ್ದರೆ, `N` ಗಾತ್ರದ ಅರೇಯ ಕೊನೆಯ ಅಂಶವು `N - 1` ನಲ್ಲಿದೆ.
- **ಪಾಯಿಂಟರ್‌ಗೆ ರೂಪಾಂತರ (Decay to Pointer):** ಅಭಿವ್ಯಕ್ತಿಗಳಲ್ಲಿ (Expressions), ಅರೇಯ ಹೆಸರೇ ಅದರ ಮೊದಲ ಅಂಶದ ಮೆಮೊರಿ ವಿಳಾಸವನ್ನು (`&arr[0]`) ಸೂಚಿಸುತ್ತದೆ.
- **ಬೌಂಡರಿ ತಪಾಸಣೆ ಇಲ್ಲದಿರುವುದು:** C ಕಂಪೈಲರ್ ಅರೇ ಮಿತಿಗಳನ್ನು ಪರೀಕ್ಷಿಸುವುದಿಲ್ಲ. `arr[N]` ಪ್ರವೇಶಿಸಿದರೆ ಅನಿರೀಕ್ಷಿತ ದೋಷ (Undefined Behavior) ಉಂಟಾಗುತ್ತದೆ.

---

## 2. ಪ್ರಮುಖ ನಿಯಮಗಳು, ಸಿಂಟ್ಯಾಕ್ಸ್ ಮತ್ತು ಸೂತ್ರಗಳು

### ಘೋಷಣೆ ಮತ್ತು ಪ್ರಾರಂಭೀಕರಣ:
```c
int a[5] = {10, 20, 30, 40, 50}; // ಪೂರ್ಣ ಪ್ರಾರಂಭೀಕರಣ
int b[5] = {1, 2};               // b[0]=1, b[1]=2, ಉಳಿದವು ಸ್ವಯಂಚಾಲಿತವಾಗಿ 0 ಆಗುತ್ತವೆ
int c[]  = {1, 2, 3};            // ಗಾತ್ರವನ್ನು ಕಂಪೈಲರ್ 3 ಎಂದು ನಿರ್ಧರಿಸುತ್ತದೆ
int mat[2][3] = {{1, 2, 3}, {4, 5, 6}}; // 2D ಅರೇ (Row-Major Order)
```

### VTU ಪರೀಕ್ಷಾ ಸೂತ್ರಗಳು:
- **ಅರೇಯಲ್ಲಿನ ಅಂಶಗಳ ಸಂಖ್ಯೆ:**
  $$\\text{ಅಂಶಗಳ ಸಂಖ್ಯೆ} = \\frac{\\text{sizeof}(arr)}{\\text{sizeof}(arr[0])}$$
- **2D ಅರೇ ಅಂಶದ ವಿಳಾಸ (Row-Major):**
  $$\\text{Loc}(mat[i][j]) = \\text{Base} + [i \\times C + j] \\times w$$
  *(ಇಲ್ಲಿ $C$ ಒಟ್ಟು ಕಾಲಮ್‌ಗಳ ಸಂಖ್ಯೆ ಮತ್ತು $w$ ಒಂದು ಅಂಶದ ಬೈಟ್‌ಗಳ ಗಾತ್ರ).*
- **ಪಾಯಿಂಟರ್ ಸಮಾನತೆ:**
  $$arr[i] \\equiv *(arr + i) \\equiv *(i + arr) \\equiv i[arr]$$

---

## 3. ವಿವರಿಸಿದ ಉದಾಹರಣೆ (Annotated Example)
```c
#include <stdio.h>

int main() {
    int ಅಂಕಗಳು[5] = {88, 92, 79, 95, 84};
    int n = sizeof(ಅಂಕಗಳು) / sizeof(ಅಂಕಗಳು[0]); // n = 5
    int ಮೊತ್ತ = 0;

    for (int i = 0; i < n; i++) {
        ಮೊತ್ತ += *(ಅಂಕಗಳು + i); // ಅಂಕಗಳು[i] ಗೆ ಸಮಾನ
    }

    float ಸರಾಸರಿ = (float)ಮೊತ್ತ / n;
    printf("ಒಟ್ಟು ಮೊತ್ತ = %d, ಸರಾಸರಿ = %.2f\\n", ಮೊತ್ತ, ಸರಾಸರಿ);
    return 0;
}
```

---

## 4. ರಸಪ್ರಶ್ನೆ & VTU ಪರೀಕ್ಷಾ ತ್ವರಿತ ಪರಿಶೀಲನಾ ಪಾಯಿಂಟ್‌ಗಳು
- [x] **0-ಇಂಡೆಕ್ಸ್ ಎಚ್ಚರಿಕೆ:** `int arr[10];` ನಲ್ಲಿ ಮಾನ್ಯ ಇಂಡೆಕ್ಸ್‌ಗಳು `0` ರಿಂದ `9` ವರೆಗೆ ಮಾತ್ರ. `arr[10]` ಬಳಸಿದರೆ ಮೆಮೊರಿ ದೋಷ ಬರುತ್ತದೆ.
- [x] **ಪ್ರಾರಂಭಿಸದ ಲೋಕಲ್ ಅರೇಗಳು:** ಇವುಗಳಲ್ಲಿ **ಗಾರ್ಬೇಜ್ ಮೌಲ್ಯಗಳು (Garbage values)** ಇರುತ್ತವೆ.
- [x] **2D ಅರೇ ನಿಯಮ:** ಫಂಕ್ಷನ್‌ಗೆ 2D ಅರೇ ರವಾನಿಸುವಾಗ **ಕಾಲಮ್ ಗಾತ್ರವನ್ನು ನಮೂದಿಸುವುದು ಕಡ್ಡಾಯ** (ಉದಾ: `void f(int m[][4]);`).
- [x] **ಫಂಕ್ಷನ್‌ನಲ್ಲಿ `sizeof`:** ಫಂಕ್ಷನ್‌ಗೆ ರವಾನಿಸಿದಾಗ ಅರೇಯು ಪಾಯಿಂಟರ್ ಆಗಿ ಬದಲಾಗುವುದರಿಂದ `sizeof(arr)` ಕೇವಲ ಪಾಯಿಂಟರ್ ಗಾತ್ರವನ್ನು (4 ಅಥವಾ 8 ಬೈಟ್) ನೀಡುತ್ತದೆ.""",
        "content_hi": """## 1. अवधारणा का विस्तृत विवरण (Concept Explanation)
C प्रोग्रामिंग में **एरे (Array)** एक ही डेटा प्रकार के तत्वों का क्रमिक और सन्निहित (Contiguous) मेमोरी संग्रह है।

### एरे के मुख्य सिद्धांत:
- **सन्निहित आवंटन (Contiguous Allocation):** सभी तत्व मेमोरी में बिना किसी अंतराल के एक के बाद एक संग्रहीत होते हैं।
- **त्वरित पहुंच (Direct Access O(1)):** किसी भी तत्व को उसके इंडेक्स का उपयोग करके सीधे पढ़ा जा सकता है:
  $$\\text{तत्व का पता} = \\text{आधार पता (Base Address)} + i \\times \\text{sizeof}(\\text{डेटा प्रकार})$$
- **शून्य-आधारित इंडेक्सिंग:** पहला तत्व इंडेक्स `0` पर और $N$ आकार का अंतिम तत्व इंडेक्स $N-1$ पर होता है।
- **पॉइंटर में रूपांतरण:** एक्सप्रेशन में एरे का नाम उसके पहले तत्व के पते (`&arr[0]`) को दर्शाता है।
- **बाउंड्स चेकिंग का अभाव:** C रनटाइम पर एरे बाउंड्स चेक नहीं करता। `arr[N]` तक पहुंचना अपरिभाषित व्यवहार (Undefined Behavior) उत्पन्न करता है।

---

## 2. प्रमुख नियम, सिंटैक्स और सूत्र

### घोषणा और प्रारंभीकरण:
```c
int a[5] = {10, 20, 30, 40, 50}; // पूर्ण प्रारंभीकरण
int b[5] = {1, 2};               // आंशिक: b[0]=1, b[1]=2, शेष 0 होंगे
int c[]  = {1, 2, 3};            // आकार स्वतः 3 निर्धारित होगा
int mat[2][3] = {{1, 2, 3}, {4, 5, 6}}; // 2D एरे (Row-Major Order)
```

### महत्वपूर्ण परीक्षा सूत्र:
- **एरे की लंबाई:**
  $$\\text{तत्वों की संख्या} = \\frac{\\text{sizeof}(arr)}{\\text{sizeof}(arr[0])}$$
- **2D एरे पता सूत्र (Row-Major):**
  $$\\text{Loc}(mat[i][j]) = \\text{Base} + [i \\times C + j] \\times w$$
  *(जहाँ $C$ कॉलम की संख्या और $w$ डेटा प्रकार का आकार है)*
- **पॉइंटर समानता:**
  $$arr[i] \\equiv *(arr + i) \\equiv *(i + arr) \\equiv i[arr]$$

---

## 3. उदाहरण (Annotated Example)
```c
#include <stdio.h>

int main() {
    int अंक[5] = {88, 92, 79, 95, 84};
    int n = sizeof(अंक) / sizeof(अंक[0]); // n = 5
    int कुल = 0;

    for (int i = 0; i < n; i++) {
        कुल += *(अंक + i); // अंक[i] के समान
    }

    float औसत = (float)कुल / n;
    printf("कुल योग = %d, औसत = %.2f\\n", कुल, औसत);
    return 0;
}
```

---

## 4. क्विज और VTU परीक्षा त्वरित चेकपॉइंट
- [x] **शून्य इंडेक्सिंग:** `int arr[10];` में केवल `0` से `9` इंडेक्स मान्य हैं। `arr[10]` अमान्य है।
- [x] **अनारंभीकृत तत्व:** लोकल एरे में **कचरा मान (Garbage values)** होते हैं, जबकि ग्लोबल एरे स्वतः शून्य होते हैं।
- [x] **2D एरे फलन पैरामीटर:** 2D एरे को फंक्शन में भेजते समय **कॉलम की संख्या निर्दिष्ट करना अनिवार्य है** (`void func(int mat[][4]);`)।
- [x] **फंक्शन में `sizeof`:** फंक्शन के अंदर `sizeof(arr)` केवल पॉइंटर का आकार (4 या 8 बाइट) देता है, पूरा एरे आकार नहीं।"""
    },

    "Pointers and Memory": {
        "title": "Comprehensive Study Notes: Pointers and Memory in C",
        "title_kn": "ಸಮಗ್ರ ಅಧ್ಯಯನ ಟಿಪ್ಪಣಿಗಳು: ಸಿ ಭಾಷೆಯಲ್ಲಿ ಪಾಯಿಂಟರ್‌ಗಳು ಮತ್ತು ಮೆಮೊರಿ",
        "title_hi": "विस्तृत अध्ययन नोट्स: सी में पॉइंटर्स और मेमोरी प्रबंधन",
        "desc": "Master memory addresses, dereferencing (*), address-of (&), pointer arithmetic, void pointers, and dynamic memory allocation.",
        "desc_kn": "ಮೆಮೊರಿ ವಿಳಾಸಗಳು, ಡೀರಫರೆನ್ಸಿಂಗ್, ಪಾಯಿಂಟರ್ ಗಣಿತ ಮತ್ತು ಡೈನಾಮಿಕ್ ಮೆಮೊರಿ ನಿರ್ವಹಣೆಯನ್ನು ಕಲಿಯಿರಿ.",
        "desc_hi": "मेमोरी पते, डिरेफरेंसिंग (*), पॉइंटर अंकगणित और डायनेमिक मेमोरी आवंटन (malloc/free) को समझें।",
        "content_en": """## 1. Detailed Concept Explanation
A **Pointer** in C is a variable that stores the memory address of another variable. Rather than holding direct data, it points to the memory location where that data resides.

### Fundamental Operators:
- **Address-Of Operator (`&`):** Retrieves the raw hexadecimal memory address of any variable (e.g., `&val`).
- **Dereference / Indirection Operator (`*`):** Accesses or modifies the value residing at the address stored in the pointer (e.g., `*ptr = 100`).

### Pointer Arithmetic Mechanics:
When you perform arithmetic on a pointer (`ptr + 1`), the compiler does **not** simply increment by 1 single byte. It scales by the size of the referenced type:
$$\\text{New Address} = \\text{Current Address} + k \\times \\text{sizeof}(*ptr)$$
For instance, if `int *p = 1000;`, then `p + 1` evaluates to `1004` on a 32-bit/64-bit platform where `sizeof(int) == 4`.

### Dynamic Memory Allocation:
- `malloc(size)`: Allocates uninitialized heap memory containing arbitrary garbage values.
- `calloc(n, size)`: Allocates and initializes all allocated bytes to **zero**.
- `realloc(ptr, new_size)`: Resizes an existing heap block while preserving existing data.
- `free(ptr)`: Releases allocated heap memory back to the operating system to prevent **Memory Leaks**.

---

## 2. Key Rules, Syntax & Formulas
```c
int x = 42;
int *p = &x;     // p stores address of x
int **pp = &p;   // pp is a double pointer storing address of pointer p

// Void (Generic) Pointer:
void *v = &x;
int val = *(int*)v; // Must explicitly typecast before dereferencing void pointer!

// Dynamic Allocation Pattern:
int *arr = (int*)malloc(10 * sizeof(int));
if (arr == NULL) { /* Handle allocation failure */ }
free(arr);
arr = NULL; // Prevent Dangling Pointer
```

### Essential Pointer Identities:
- `&(*p) == p` (The address of a dereferenced pointer is the pointer itself).
- `*(&x) == x` (Dereferencing the address of a variable yields the variable value).
- `p[i] == *(p + i)`.

---

## 3. Annotated Example
```c
#include <stdio.h>
#include <stdlib.h>

void swap(int *a, int *b) {
    int temp = *a; // Retrieve value at address a
    *a = *b;       // Put value of b into address a
    *b = temp;     // Put temp into address b
}

int main() {
    int num1 = 15, num2 = 30;
    printf("Before Swap: %d, %d\\n", num1, num2);

    // Pass addresses to function (Pass by Reference simulation)
    swap(&num1, &num2);
    printf("After Swap: %d, %d\\n", num1, num2);

    // Dynamic heap array demonstration
    int *dynamic_arr = (int*)calloc(3, sizeof(int)); // All 3 elements = 0
    dynamic_arr[0] = 100;
    printf("Heap element: %d\\n", dynamic_arr[0]);

    free(dynamic_arr); // Deallocate
    dynamic_arr = NULL;
    return 0;
}
```

---

## 4. Quiz & VTU Exam Quick-Check Points
- [x] **Dangling Pointer:** A pointer pointing to deallocated memory after `free(p);`. Always assign `p = NULL;` immediately after freeing.
- [x] **Memory Leak:** Occurs when heap memory allocated via `malloc/calloc` is lost without calling `free()`.
- [x] **Void Pointer Dereference:** You **cannot** directly dereference a `void*` (`*v` causes compile error). You must cast it first: `*(int*)v`.
- [x] **Pointer Size:** On a 64-bit machine, **all pointer types** (`char*`, `int*`, `double*`, `void*`) have the exact same size: **8 bytes** (or 4 bytes on 32-bit architecture).
- [x] **Increment Precedence:** `*p++` retrieves `*p` first, then increments the pointer address. `(*p)++` increments the value stored at the address.""",
        "content_kn": """## 1. ಪರಿಕಲ್ಪನೆಯ ವಿವರವಾದ ವಿವರಣೆ
C ಪ್ರೋಗ್ರಾಮಿಂಗ್‌ನಲ್ಲಿ **ಪಾಯಿಂಟರ್ (Pointer)** ಎಂಬುದು ಇನ್ನೊಂದು ವೇರಿಯೇಬಲ್‌ನ ಮೆಮೊರಿ ವಿಳಾಸವನ್ನು (Memory Address) ಸಂಗ್ರಹಿಸುವ ಒಂದು ವಿಶೇಷ ವೇರಿಯೇಬಲ್ ಆಗಿದೆ.

### ಮೂಲ ಆಪರೇಟರ್‌ಗಳು:
- **ವಿಳಾಸ ಪಡೆಯುವ ಆಪರೇಟರ್ (`&`):** ಯಾವುದೇ ವೇರಿಯೇಬಲ್‌ನ ಮೆಮೊರಿ ವಿಳಾಸವನ್ನು ಹಿಂತಿರುಗಿಸುತ್ತದೆ (ಉದಾ: `&x`).
- **ಡೀರಫರೆನ್ಸ್ ಆಪರೇಟರ್ (`*`):** ಪಾಯಿಂಟರ್ ಸಂಗ್ರಹಿಸಿರುವ ವಿಳಾಸದಲ್ಲಿರುವ ನೈಜ ಮೌಲ್ಯವನ್ನು ಪಡೆಯಲು ಅಥವಾ ಬದಲಾಯಿಸಲು ಬಳಸಲಾಗುತ್ತದೆ (ಉದಾ: `*p = 50`).

### ಪಾಯಿಂಟರ್ ಗಣಿತ (Pointer Arithmetic):
ಪಾಯಿಂಟರ್ ಅನ್ನು ಇನ್‌ಕ್ರಿಮೆಂಟ್ ಮಾಡಿದಾಗ (`ptr + 1`), ಅದು ಕೇವಲ 1 ಬೈಟ್ ಹೆಚ್ಚಾಗುವುದಿಲ್ಲ. ಅದು ಆ ಡೇಟಾ ಪ್ರಕಾರದ ಗಾತ್ರದಷ್ಟು ಹೆಚ್ಚಾಗುತ್ತದೆ:
$$\\text{ಹೊಸ ವಿಳಾಸ} = \\text{ಪ್ರಸ್ತುತ ವಿಳಾಸ} + k \\times \\text{sizeof}(*ptr)$$
ಉದಾಹರಣೆಗೆ, `int *p = 2000;` ಆಗಿದ್ದರೆ, `p + 1` ಮೌಲ್ಯವು `2004` ಆಗುತ್ತದೆ (ಏಕೆಂದರೆ int = 4 ಬೈಟ್‌ಗಳು).

### ಡೈನಾಮಿಕ್ ಮೆಮೊರಿ ನಿರ್ವಹಣೆ:
- `malloc(ಗಾತ್ರ)`: ಮೆಮೊರಿ ಹಂಚಿಕೆ ಮಾಡುತ್ತದೆ (ಗಾರ್ಬೇಜ್ ಮೌಲ್ಯಗಳನ್ನು ಹೊಂದಿರುತ್ತದೆ).
- `calloc(n, ಗಾತ್ರ)`: ಮೆಮೊರಿ ಹಂಚಿಕೆ ಮಾಡಿ ಎಲ್ಲಾ ಬೈಟ್‌ಗಳನ್ನು **ಶೂನ್ಯಕ್ಕೆ (0)** ಹೊಂದಿಸುತ್ತದೆ.
- `free(ptr)`: ಹಂಚಿಕೆಯಾದ ಮೆಮೊರಿಯನ್ನು ಬಿಡುಗಡೆ ಮಾಡಿ ಮೆಮೊರಿ ಸೋರಿಕೆಯನ್ನು (Memory Leak) ತಡೆಯುತ್ತದೆ.

---

## 2. ಪ್ರಮುಖ ನಿಯಮಗಳು, ಸಿಂಟ್ಯಾಕ್ಸ್ ಮತ್ತು ಸೂತ್ರಗಳು
```c
int a = 10;
int *p = &a;    // p ಪಾಯಿಂಟರ್ a ಯ ವಿಳಾಸವನ್ನು ಹೊಂದಿದೆ
int **pp = &p;  // ಡಬಲ್ ಪಾಯಿಂಟರ್

// Void ಪಾಯಿಂಟರ್ (ಸಾಮಾನ್ಯ ಪಾಯಿಂಟರ್):
void *v = &a;
int val = *(int*)v; // ಡೀರಫರೆನ್ಸ್ ಮಾಡುವ ಮುನ್ನ ಟೈಪ್‌ಕಾಸ್ಟ್ ಕಡ್ಡಾಯ!
```

---

## 3. ವಿವರಿಸಿದ ಉದಾಹರಣೆ
```c
#include <stdio.h>

void swap(int *x, int *y) {
    int ತಾತ್ಕಾಲಿಕ = *x;
    *x = *y;
    *y = ತಾತ್ಕಾಲಿಕ;
}

int main() {
    int p = 5, q = 10;
    swap(&p, &q); // ವಿಳಾಸಗಳನ್ನು ರವಾನಿಸಲಾಗುತ್ತಿದೆ
    printf("p = %d, q = %d\\n", p, q); // p=10, q=5
    return 0;
}
```

---

## 4. ರಸಪ್ರಶ್ನೆ & VTU ಪರೀಕ್ಷಾ ತ್ವರಿತ ಪರಿಶೀಲನಾ ಪಾಯಿಂಟ್‌ಗಳು
- [x] **ಡ್ಯಾಂಗ್ಲಿಂಗ್ ಪಾಯಿಂಟರ್ (Dangling Pointer):** `free(p);` ನಂತರ ಮೆಮೊರಿ ಬಿಡುಗಡೆಯಾದರೂ ಪಾಯಿಂಟರ್ ಅದೇ ವಿಳಾಸಕ್ಕೆ ತೋರಿಸುತ್ತಿದ್ದರೆ ಅದನ್ನು ಡ್ಯಾಂಗ್ಲಿಂಗ್ ಪಾಯಿಂಟರ್ ಎನ್ನುತ್ತಾರೆ.
- [x] **ಮೆಮೊರಿ ಸೋರಿಕೆ (Memory Leak):** ಹಂಚಿಕೆಯಾದ ಮೆಮೊರಿಯನ್ನು `free()` ಮಾಡದಿದ್ದಾಗ ಮೆಮೊರಿ ವ್ಯರ್ಥವಾಗುತ್ತದೆ.
- [x] **ಪಾಯಿಂಟರ್ ಗಾತ್ರ:** 64-ಬಿಟ್ ಸಿಸ್ಟಮ್‌ನಲ್ಲಿ ಎಲ್ಲಾ ಪಾಯಿಂಟರ್‌ಗಳ ಗಾತ್ರ **8 ಬೈಟ್** ಆಗಿರುತ್ತದೆ (`char*` ಅಥವಾ `double*` ಎಲ್ಲವೂ ಒಂದೇ ಗಾತ್ರ).
- [x] **`*p++` vs `(*p)++`:** `*p++` ಪಾಯಿಂಟರ್ ವಿಳಾಸವನ್ನು ಹೆಚ್ಚಿಸುತ್ತದೆ; `(*p)++` ವಿಳಾಸದಲ್ಲಿರುವ ಮೌಲ್ಯವನ್ನು ಹೆಚ್ಚಿಸುತ್ತದೆ.""",
        "content_hi": """## 1. अवधारणा का विस्तृत विवरण
C में **पॉइंटर (Pointer)** एक ऐसा चर (variable) है जो किसी अन्य चर का मेमोरी पता (Memory Address) संग्रहीत करता है।

### प्राथमिक ऑपरेटर्स:
- **पता ऑपरेटर (`&`):** किसी चर का हेक्साडेसिमल मेमोरी पता प्राप्त करता है (जैसे `&x`)।
- **डिरेफरेंस ऑपरेटर (`*`):** उस पते पर संग्रहीत वास्तविक मान तक पहुंचता है या उसे बदलता है (जैसे `*p = 50`)।

### पॉइंटर अंकगणित:
जब पॉइंटर में 1 जोड़ा जाता है (`p + 1`), तो वह 1 बाइट नहीं बल्कि डेटा प्रकार के आकार के बराबर आगे बढ़ता है:
$$\\text{नया पता} = \\text{वर्तमान पता} + k \\times \\text{sizeof}(*ptr)$$
यदि `int *p = 1000` है, तो `p + 1` का मान `1004` होगा (क्योंकि int = 4 बाइट्स)।

---

## 2. नियम, सिंटैक्स और सूत्र
```c
int a = 25;
int *p = &a;     // साधारण पॉइंटर
int **pp = &p;   // डबल पॉइंटर

void *v = &a;    // जेनेरिक पॉइंटर
int val = *(int*)v; // डिरेफरेंस करने से पहले टाइपकास्ट आवश्यक है!
```

---

## 3. उदाहरण
```c
#include <stdio.h>

void अदला_बदली(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    int x = 20, y = 40;
    अदला_बदली(&x, &y);
    printf("x = %d, y = %d\\n", x, y);
    return 0;
}
```

---

## 4. क्विज और VTU परीक्षा चेकपॉइंट
- [x] **डैंगलिंग पॉइंटर:** `free(p)` के बाद यदि पॉइंटर को `NULL` नहीं किया गया, तो वह अमान्य मेमोरी को इंगित करता है।
- [x] **मेमोरी लीक:** `malloc` से आवंटित मेमोरी को `free()` न करने पर मेमोरी लीक होती है।
- [x] **पॉइंटर का आकार:** 64-बिट कंप्यूटर पर सभी पॉइंटर्स का आकार समान रूप से **8 बाइट्स** होता है।
- [x] **`*p++` बनाम `(*p)++`:** `*p++` पता बदलता है; `(*p)++` पते पर मौजूद डेटा का मान बढ़ाता है।"""
    },

    "Functions and Recursion": {
        "title": "Comprehensive Study Notes: Functions and Recursion in C",
        "title_kn": "ಸಮಗ್ರ ಅಧ್ಯಯನ ಟಿಪ್ಪಣಿಗಳು: ಸಿ ಭಾಷೆಯಲ್ಲಿ ಫಂಕ್ಷನ್‌ಗಳು ಮತ್ತು ರಿಕರ್ಶನ್",
        "title_hi": "विस्तृत अध्ययन नोट्स: सी में फंक्शन और रिकर्सन",
        "desc": "Master modular programming, pass-by-value vs pass-by-reference, call stack mechanics, recursive base conditions, and preventing stack overflow.",
        "desc_kn": "ಫಂಕ್ಷನ್ ಮೂಲಗಳು, ಕಾಲ್ ಸ್ಟ್ಯಾಕ್, ರಿಕರ್ಶನ್ ಬೇಸ್ ಕಂಡೀಶನ್ ಮತ್ತು ಸ್ಟ್ಯಾಕ್ ಓವರ್‌ಫ್ಲೋ ತಡೆಗಟ್ಟುವಿಕೆಯನ್ನು ಕಲಿಯಿರಿ.",
        "desc_hi": "फंक्शन प्रोटोटाइप, कॉल स्टैक, रिकर्सिव बेस कंडीशन और स्टैक ओवरफ्लो से बचाव को समझें।",
        "content_en": """## 1. Detailed Concept Explanation
A **Function** in C is a self-contained block of code designed to perform a specific task, promoting modularity, code reuse, and testability.

### Call By Value vs. Call By Reference:
- **Call by Value:** In standard C, function arguments are passed by value. The function receives a **copy** of the variable. Changes inside the function do **not** affect the caller's original variable.
- **Call by Reference (Pointer Simulation):** By passing memory addresses (`&var`) into pointer parameters (`int *param`), the function can directly dereference and modify the original variables.

### Recursion Mechanics:
**Recursion** occurs when a function calls itself directly or indirectly to solve a smaller instance of the same problem.
- **The Call Stack:** Each recursive call pushes an **Activation Record (Stack Frame)** onto the program execution stack, preserving local variables and the return address.
- **Base Case (Termination Condition):** The anchor condition that stops further recursive calls.
- **Recursive Step:** Moves the problem state closer to the base case.
- **Stack Overflow:** Missing or unreachable base conditions cause infinite recursive calls, exhausting allocated stack space and crashing with a segmentation fault.

---

## 2. Key Rules, Syntax & Formulas
```c
// 1. Prototype Declaration:
int compute_factorial(int n);

// 2. Recursive Implementation:
int compute_factorial(int n) {
    if (n <= 1) return 1;          // Base condition
    return n * compute_factorial(n - 1); // Recursive step
}
```

### Recurrence Relations for VTU Algorithms:
- Factorial: $T(n) = T(n-1) + O(1) \\implies O(n)$ time, $O(n)$ stack space.
- Binary Search: $T(n) = T(n/2) + O(1) \\implies O(\\log_2 n)$ time.
- Fibonacci (Naive): $T(n) = T(n-1) + T(n-2) + O(1) \\implies O(2^n)$ exponential time.

---

## 3. Annotated Example
```c
#include <stdio.h>

// Step-by-step Fibonacci with recursion:
int fibonacci(int n) {
    // Base Cases:
    if (n == 0) return 0;
    if (n == 1) return 1;
    // Recursive Case:
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
    int term = 6;
    printf("Fibonacci term %d = %d\\n", term, fibonacci(term)); // Output: 8
    return 0;
}
```

---

## 4. Quiz & VTU Exam Quick-Check Points
- [x] **Base Case Requirement:** Without a base condition, recursion runs indefinitely until a **Stack Overflow (Segmentation Fault)** occurs.
- [x] **Default Return Type:** In legacy C, functions declared without an explicit return type default to `int`.
- [x] **Scope of Locals:** Variables declared inside a function are allocated on the stack and automatically destroyed when the function returns.
- [x] **Recursion vs Iteration:** Recursion incurs higher overhead due to stack frame allocation and function call overhead, but provides clean mathematical formulations (e.g., Tree traversals, Tower of Hanoi).""",
        "content_kn": """## 1. ಪರಿಕಲ್ಪನೆಯ ವಿವರವಾದ ವಿವರಣೆ
C ಭಾಷೆಯಲ್ಲಿ **ಫಂಕ್ಷನ್ (Function)** ಎಂಬುದು ನಿರ್ದಿಷ್ಟ ಕೆಲಸವನ್ನು ನಿರ್ವಹಿಸುವ ಕೋಡ್‌ನ ಸ್ವತಂತ್ರ ಭಾಗವಾಗಿದೆ.

### ಕಾಲ್ ಬೈ ವ್ಯಾಲ್ಯೂ vs ಕಾಲ್ ಬೈ ರೆಫರೆನ್ಸ್:
- **ಕಾಲ್ ಬೈ ವ್ಯಾಲ್ಯೂ (Call by Value):** ಮೌಲ್ಯದ ನಕಲನ್ನು (Copy) ಫಂಕ್ಷನ್‌ಗೆ ಕಳುಹಿಸಲಾಗುತ್ತದೆ. ಮೂಲ ವೇರಿಯೇಬಲ್ ಬದಲಾಗುವುದಿಲ್ಲ.
- **ಕಾಲ್ ಬೈ ರೆಫರೆನ್ಸ್ (Call by Reference):** ವಿಳಾಸವನ್ನು (`&var`) ಕಳುಹಿಸಿ ಪಾಯಿಂಟರ್ ಮೂಲಕ ಮೂಲ ಮೌಲ್ಯವನ್ನು ಬದಲಾಯಿಸಲಾಗುತ್ತದೆ.

### ರಿಕರ್ಶನ್ (Recursion):
ಒಂದು ಫಂಕ್ಷನ್ ತನ್ನನ್ನೇ ತಾನು ಮತ್ತೆ ಮತ್ತೆ ಕರೆಯುವುದನ್ನು **ರಿಕರ್ಶನ್** ಎನ್ನುತ್ತಾರೆ.
- **ಬೇಸ್ ಕಂಡೀಶನ್ (Base Condition):** ರಿಕರ್ಶನ್ ನಿಲ್ಲಲು ಅಗತ್ಯವಿರುವ ಮೂಲ ಷರತ್ತು.
- **ಸ್ಟ್ಯಾಕ್ ಓವರ್‌ಫ್ಲೋ (Stack Overflow):** ಬೇಸ್ ಕಂಡೀಶನ್ ಇಲ್ಲದಿದ್ದರೆ ಸ್ಟ್ಯಾಕ್ ಮೆಮೊರಿ ತುಂಬಿ ಪ್ರೋಗ್ರಾಂ ಕ್ರ್ಯಾಶ್ ಆಗುತ್ತದೆ.

---

## 2. ಪ್ರಮುಖ ನಿಯಮಗಳು ಮತ್ತು ಉದಾಹರಣೆ
```c
int factorial(int n) {
    if (n <= 1) return 1; // ಬೇಸ್ ಕಂಡೀಶನ್
    return n * factorial(n - 1); // ರಿಕರ್ಶನ್
}
```

---

## 3. ರಸಪ್ರಶ್ನೆ & VTU ಪರೀಕ್ಷಾ ತ್ವರಿತ ಪರಿಶೀಲನಾ ಪಾಯಿಂಟ್‌ಗಳು
- [x] **ಬೇಸ್ ಕಂಡೀಶನ್ ಕಡ್ಡಾಯ:** ಬೇಸ್ ಕಂಡೀಶನ್ ಇಲ್ಲದಿದ್ದರೆ **ಸ್ಟ್ಯಾಕ್ ಓವರ್‌ಫ್ಲೋ** ಉಂಟಾಗುತ್ತದೆ.
- [x] **ಲೋಕಲ್ ವೇರಿಯೇಬಲ್‌ಗಳು:** ಫಂಕ್ಷನ್ ಮುಗಿದ ತಕ್ಷಣ ಅದರಲ್ಲಿರುವ ಲೋಕಲ್ ವೇರಿಯೇಬಲ್‌ಗಳು ಮೆಮೊರಿಯಿಂದ ಅಳಿಸಿಹೋಗುತ್ತವೆ.""",
        "content_hi": """## 1. अवधारणा का विस्तृत विवरण
C में **फंक्शन** कोड का एक मॉड्यूलर ब्लॉक है जो किसी विशिष्ट कार्य को निष्पादित करता है।

### रिकर्सन (Recursion):
जब कोई फंक्शन स्वयं को बार-बार कॉल करता है, तो उसे **रिकर्सन** कहा जाता है।
- **बेस कंडीशन (Base Condition):** वह शर्त जो रिकर्सन को समाप्त करती है। इसके बिना फंक्शन अनंत लूप में चला जाता है और **स्टैक ओवरफ्लो** हो जाता है।

---

## 2. मुख्य नियम और कोड
```c
int फैक्टोरियल(int n) {
    if (n <= 1) return 1; // बेस कंडीशन
    return n * फैक्टोरियल(n - 1); // रिकर्सिव कॉल
}
```

---

## 3. क्विज और VTU परीक्षा चेकपॉइंट
- [x] **बेस कंडीशन:** प्रत्येक रिकर्सिव फंक्शन में बेस कंडीशन अनिवार्य है।
- [x] **कॉल बाय वैल्यू:** डिफ़ॉल्ट रूप से C में आर्गुमेंट्स कॉपी होकर पास होते हैं।"""
    },

    "Control Flow and Loops": {
        "title": "Comprehensive Study Notes: Control Flow and Loops in C",
        "title_kn": "ಸಮಗ್ರ ಅಧ್ಯಯನ ಟಿಪ್ಪಣಿಗಳು: ಸಿ ಭಾಷೆಯಲ್ಲಿ ಕಂಟ್ರೋಲ್ ಫ್ಲೋ ಮತ್ತು ಲೂಪ್‌ಗಳು",
        "title_hi": "विस्तृत अध्ययन नोट्स: सी में कंट्रोल फ्लो और लूप्स",
        "desc": "Master conditional branching (if-else, switch-case), looping constructs (for, while, do-while), and jump statements (break, continue, goto).",
        "desc_kn": "ಷರತ್ತುಬದ್ಧ ತೀರ್ಮಾನಗಳು, ಲೂಪ್‌ಗಳು ಮತ್ತು ಬ್ರೇಕ್/ಕಂಟಿನ್ಯೂ ನಿಯಮಗಳನ್ನು ಕಲಿಯಿರಿ.",
        "desc_hi": "कंडीशनल स्टेटमेंट्स (if-else, switch) और लूप्स (for, while, do-while) को समझें।",
        "content_en": """## 1. Detailed Concept Explanation
Control flow statements determine the execution order of instructions in a C program based on runtime conditions.

### Selection Statements:
- `if-else`: Evaluates Boolean expressions. Any non-zero numeric value is treated as **TRUE** in C; exactly `0` is **FALSE**.
- `switch`: Multi-way decision structure testing an integral or character expression against fixed `case` constants.
  - **Fallthrough:** Omitting a `break;` statement causes execution to cascade into subsequent cases regardless of their condition.

### Iteration Statements (Loops):
- `while`: Entry-controlled loop. Evaluates condition before executing the loop body (0 or more executions).
- `for`: Compact entry-controlled loop grouping initialization, condition, and increment/decrement.
- `do-while`: **Exit-controlled loop**. Executes the body **at least once** before evaluating the condition.

---

## 2. Key Rules, Syntax & Formulas
```c
// do-while executes at least 1 time:
int count = 10;
do {
    printf("%d\\n", count); // Executes once even though condition is false!
} while (count < 5);

// switch with fallthrough:
switch (val) {
    case 1: printf("One "); break;
    case 2: printf("Two "); // Fallthrough to case 3!
    case 3: printf("Three "); break;
    default: printf("Other");
}
```

---

## 3. Annotated Example
```c
#include <stdio.h>

int main() {
    // Demonstration of break vs continue:
    for (int i = 1; i <= 6; i++) {
        if (i == 3) continue; // Skip printing 3, continue next iteration
        if (i == 5) break;    // Terminate loop entirely at 5
        printf("%d ", i);
    }
    // Output: 1 2 4
    printf("\\n");
    return 0;
}
```

---

## 4. Quiz & VTU Exam Quick-Check Points
- [x] **`do-while` Semicolon:** The `do { ... } while(cond);` statement **must end with a semicolon**.
- [x] **`switch` Limitations:** Cases can only use integer or char constants (no floating-point values or strings).
- [x] **`continue` in `for` vs `while`:** In a `for` loop, `continue` jumps to the increment step (`i++`). In a `while` loop, it jumps straight to the condition check.""",
        "content_kn": """## 1. ಪರಿಕಲ್ಪನೆಯ ವಿವರವಾದ ವಿವರಣೆ
C ಭಾಷೆಯಲ್ಲಿ **ಕಂಟ್ರೋಲ್ ಫ್ಲೋ (Control Flow)** ಪ್ರೋಗ್ರಾಂ ಚಾಲನೆಯಾಗುವ ದಿಕ್ಕನ್ನು ನಿರ್ಧರಿಸುತ್ತದೆ.

### ಲೂಪ್‌ಗಳ ವಿಧಗಳು:
- `for` ಮತ್ತು `while`: ಎಂಟ್ರಿ-ಕಂಟ್ರೋಲ್ಡ್ ಲೂಪ್‌ಗಳು (ಷರತ್ತು ನಿಜವಾಗಿದ್ದರೆ ಮಾತ್ರ ಒಳಗಡೆ ಹೋಗುತ್ತದೆ).
- `do-while`: ಎಕ್ಸಿಟ್-ಕಂಟ್ರೋಲ್ಡ್ ಲೂಪ್ (ಷರತ್ತು ಸುಳ್ಳಾಗಿದ್ದರೂ **ಕನಿಷ್ಠ ಒಂದು ಬಾರಿ** ಚಾಲನೆಯಾಗುತ್ತದೆ).

---

## 2. ರಸಪ್ರಶ್ನೆ & VTU ಪರೀಕ್ಷಾ ತ್ವರಿತ ಪರಿಶೀಲನಾ ಪಾಯಿಂಟ್‌ಗಳು
- [x] **`do-while` ನಿಯಮ:** `do-while` ಕೊನೆಯಲ್ಲಿ ಸೆಮಿಕೋಲನ್ (`;`) ಹಾಕುವುದು ಕಡ್ಡಾಯ.
- [x] **`break` vs `continue`:** `break` ಲೂಪ್‌ನಿಂದ ಸಂಪೂರ್ಣವಾಗಿ ಹೊರಬರುತ್ತದೆ; `continue` ಪ್ರಸ್ತುತ ಪುನರಾವರ್ತನೆಯನ್ನು ಬಿಟ್ಟು ಮುಂದಿನದಕ್ಕೆ ಹೋಗುತ್ತದೆ.""",
        "content_hi": """## 1. अवधारणा का विस्तृत विवरण
कंट्रोल फ्लो स्टेटमेंट्स प्रोग्राम के निष्पादन क्रम को नियंत्रित करते हैं।

### लूप्स के प्रकार:
- `while`: एंट्री-कंट्रोल्ड लूप (शर्त पहले जांची जाती है)।
- `do-while`: एग्जिट-कंट्रोल्ड लूप (शर्त गलत होने पर भी **कम से कम एक बार** चलता है)।

---

## 2. क्विज और VTU परीक्षा चेकपॉइंट
- [x] **`do-while` सेमीकोलन:** `while(cond);` के अंत में सेमीकोलन लगाना अनिवार्य है।
- [x] **`switch` में फ्लोट्स अमान्य:** स्विच केस में केवल पूर्णांक (int) और कैरेक्टर मान्य हैं।"""
    },

    # =========================================================================
    # SUBJECT 2: DIGITAL ELECTRONICS
    # =========================================================================
    "Number Systems & Codes": {
        "title": "Comprehensive Study Notes: Number Systems & Codes",
        "title_kn": "ಸಮಗ್ರ ಅಧ್ಯಯನ ಟಿಪ್ಪಣಿಗಳು: ಸಂಖ್ಯಾ ಪದ್ಧತಿಗಳು ಮತ್ತು ಕೋಡ್‌ಗಳು",
        "title_hi": "विस्तृत अध्ययन नोट्स: संख्या पद्धतियाँ और कोड्स",
        "desc": "Master Binary, Octal, Hexadecimal conversions, 1's and 2's complement representation, BCD, Gray code, and alphanumeric codes.",
        "desc_kn": "ಬೈನರಿ, ಹೆಕ್ಸಾಡೆಸಿಮಲ್, 2's ಕಾಂಪ್ಲಿಮೆಂಟ್, BCD ಮತ್ತು ಗ್ರೇ ಕೋಡ್ ಪರಿವರ್ತನೆಗಳನ್ನು ಕಲಿಯಿರಿ.",
        "desc_hi": "बाइनरी, हेक्साडेसिमल, 1's और 2's पूरक, BCD और ग्रे कोड को विस्तार से समझें।",
        "content_en": """## 1. Detailed Concept Explanation
Digital computers represent all data using discrete numeric radices.

### Core Bases:
- **Binary (Base 2):** Digits `{0, 1}`.
- **Octal (Base 8):** Digits `{0-7}` (Each octal digit maps to 3 binary bits).
- **Decimal (Base 10):** Digits `{0-9}`.
- **Hexadecimal (Base 16):** Digits `{0-9, A, B, C, D, E, F}` (Each hex digit maps to 4 binary bits).

### Signed Number Representation:
- **1's Complement:** Invert all bits ($0 \\to 1, 1 \\to 0$).
- **2's Complement:** Add 1 to the 1's complement ($2\\text{'s Comp} = 1\\text{'s Comp} + 1$).
  - Range for $n$-bit signed 2's complement integer:
    $$-2^{n-1} \\text{ to } +2^{n-1} - 1$$
  - Crucial advantage: Unique representation of zero (`00000000`), unlike signed-magnitude or 1's complement which have $+0$ and $-0$.

### Specialized Codes:
- **BCD (Binary Coded Decimal / 8421):** Each decimal digit (0-9) is encoded into 4 bits. Invalid BCD states: `1010` to `1111` (10 to 15).
- **Gray Code (Reflected Binary):** **Unit-distance code** where consecutive values differ by only **one single bit**, preventing intermediate switching errors in mechanical encoders.

---

## 2. Key Rules, Syntax & Formulas
- **Binary to Gray Conversion:**
  $$G_n = B_n \\quad \\text{and} \\quad G_i = B_{i+1} \\oplus B_i$$
- **Gray to Binary Conversion:**
  $$B_n = G_n \\quad \\text{and} \\quad B_i = B_{i+1} \\oplus G_i$$
- **Decimal to Hex Conversion:** Group binary bits into sets of 4 from the binary point outwards.

---

## 3. Annotated Example
Convert Decimal `25` to Binary, Hex, and 2's Complement (-25 in 8 bits):
1. **Decimal 25 to Binary:**
   $$25 = 16 + 8 + 1 = 00011001_2$$
2. **Hexadecimal:**
   $$0001_2 = 1_{16}, \\quad 1001_2 = 9_{16} \\implies 19_{16}$$
3. **Negative (-25) in 8-bit 2's Complement:**
   - $+25 = 00011001$
   - 1's Complement = $11100110$
   - Add $1$: $11100110 + 1 = 11100111_2$

---

## 4. Quiz & VTU Exam Quick-Check Points
- [x] **8-bit 2's Complement Range:** Exactly **$-128$ to $+127$**.
- [x] **Gray Code Characteristic:** Only **1 bit changes** between adjacent states (used in K-maps and rotary encoders).
- [x] **Invalid BCD:** Any 4-bit nibble greater than 9 (`1010` through `1111`) is **invalid BCD**.""",
        "content_kn": """## 1. ಪರಿಕಲ್ಪನೆಯ ವಿವರವಾದ ವಿವರಣೆ
ಡಿಜಿಟಲ್ ಎಲೆಕ್ಟ್ರಾನಿಕ್ಸ್‌ನಲ್ಲಿ ವಿವಿಧ ಸಂಖ್ಯಾ ಪದ್ಧತಿಗಳನ್ನು ಬಳಸಲಾಗುತ್ತದೆ: ಬೈನರಿ (ಆಧಾರ 2), ಆಕ್ಟಲ್ (ಆಧಾರ 8), ದಶಮಾಂಶ (ಆಧಾರ 10), ಮತ್ತು ಹೆಕ್ಸಾಡೆಸಿಮಲ್ (ಆಧಾರ 16).

### 2's ಕಾಂಪ್ಲಿಮೆಂಟ್ (2's Complement):
- 1's ಕಾಂಪ್ಲಿಮೆಂಟ್ = ಬಿಟ್‌ಗಳನ್ನು ತಿರುಗಿಸುವುದು ($0 \\to 1, 1 \\to 0$).
- 2's ಕಾಂಪ್ಲಿಮೆಂಟ್ = 1's ಕಾಂಪ್ಲಿಮೆಂಟ್ + 1.
- 8-ಬಿಟ್ ಸಂಖ್ಯೆಯ ಶ್ರೇಣಿ: **$-128$ ರಿಂದ $+127$**.

---

## 2. ರಸಪ್ರಶ್ನೆ & VTU ಪರೀಕ್ಷಾ ತ್ವರಿತ ಪರಿಶೀಲನಾ ಪಾಯಿಂಟ್‌ಗಳು
- [x] **ಗ್ರೇ ಕೋಡ್ (Gray Code):** ಪ್ರತಿ ಸತತ ಸಂಖ್ಯೆಗಳ ನಡುವೆ ಕೇವಲ **ಒಂದು ಬಿಟ್ ಮಾತ್ರ ಬದಲಾಗುತ್ತದೆ**.
- [x] **ಅಸಿಂಧು BCD:** 9 ಕ್ಕಿಂತ ಹೆಚ್ಚಿನ ಸಂಖ್ಯೆಗಳು (`1010` ರಿಂದ `1111`) ಅಸಿಂಧು BCD ಕೋಡ್‌ಗಳಾಗಿವೆ.""",
        "content_hi": """## 1. अवधारणा का विस्तृत विवरण
डिजिटल इलेक्ट्रॉनिक्स में बाइनरी (Base 2), ऑक्टल (Base 8), दशमलव (Base 10) और हेक्साडेसिमल (Base 16) मुख्य संख्या प्रणालियाँ हैं।

### 2's पूरक (2's Complement):
- 1's पूरक में 1 जोड़ने पर 2's पूरक प्राप्त होता है।
- 8-बिट हस्ताक्षरित संख्या की सीमा: **$-128$ से $+127$**।

---

## 2. क्विज और VTU परीक्षा चेकपॉइंट
- [x] **ग्रे कोड:** इसमें दो लगातार मानों के बीच केवल **एक बिट** का अंतर होता है।
- [x] **अमान्य BCD:** `1010` से `1111` (10 से 15) अमान्य BCD कोड हैं।"""
    },

    "Boolean Algebra & Logic Simplification": {
        "title": "Comprehensive Study Notes: Boolean Algebra & K-Maps",
        "title_kn": "ಸಮಗ್ರ ಅಧ್ಯಯನ ಟಿಪ್ಪಣಿಗಳು: ಬೂಲಿಯನ್ ಆಲ್ಜೀಬ್ರಾ ಮತ್ತು ಕೆ-ಮ್ಯಾಪ್ಸ್",
        "title_hi": "विस्तृत अध्ययन नोट्स: बूलियन बीजगणित और के-मैप",
        "desc": "Master Boolean laws, De Morgan's theorems, Sum of Products (SOP), Product of Sums (POS), and 2/3/4-variable Karnaugh Maps.",
        "desc_kn": "ಬೂಲಿಯನ್ ನಿಯಮಗಳು, ಡಿ ಮಾರ್ಗನ್ಸ್ ಪ್ರಮೇಯ ಮತ್ತು ಕೆ-ಮ್ಯಾಪ್ ಮಿನಿಮೈಸೇಶನ್ ಕಲಿಯಿರಿ.",
        "desc_hi": "बूलियन नियम, डी मॉर्गन प्रमेय, SOP, POS और 4-वेरिएबल K-Map सरलीकरण समझें।",
        "content_en": """## 1. Detailed Concept Explanation
**Boolean Algebra** provides the mathematical framework for analyzing and minimizing digital switching circuits.

### Fundamental Boolean Theorems:
- **Identity Law:** $A + 0 = A, \\quad A \\cdot 1 = A$
- **Null / Annulment Law:** $A + 1 = 1, \\quad A \\cdot 0 = 0$
- **Idempotent Law:** $A + A = A, \\quad A \\cdot A = A$
- **Complement Law:** $A + A' = 1, \\quad A \\cdot A' = 0$
- **Involution Law:** $(A')' = A$
- **De Morgan's Laws (Crucial for VTU Exams):**
  $$(A + B)' = A' \\cdot B'$$
  $$(A \\cdot B)' = A' + B'$$
  *(Break the line, change the sign).*

### Karnaugh Maps (K-Maps):
A graphical method for minimizing Boolean expressions into minimal SOP or POS form without algebraic trial-and-error.
- **Gray Code Cell Ordering:** Consecutive cells differ by only 1 bit (`00, 01, 11, 10`).
- **Grouping Rule:** Groups must contain $2^k$ cells (1, 2, 4, 8, 16) in rectangular or square shapes. Wrap-around grouping is permitted across borders.

---

## 2. Key Rules & Canonical Forms
- **Minterm ($m_i$):** Product term where all variables appear (true or complemented). Corresponds to output `1` in SOP.
- **Maxterm ($M_i$):** Sum term where all variables appear. Corresponds to output `0` in POS.
- Relationship: $m_i' = M_i$.

---

## 3. Annotated Example
Simplify: $F(A, B, C) = \\sum m(1, 3, 5, 7)$
1. Group all 4 minterms:
   - $m_1 = A'B'C$
   - $m_3 = A'BC$
   - $m_5 = AB'C$
   - $m_7 = ABC$
2. In K-map, these form a single quad of 4 cells where $A$ and $B$ vary across all states while $C = 1$ remains constant.
3. Minimal Result:
   $$F = C$$

---

## 4. Quiz & VTU Exam Quick-Check Points
- [x] **De Morgan's Identity:** $(A + B)' = A'B'$ (NOR equals bubbled AND). $(AB)' = A' + B'$ (NAND equals bubbled OR).
- [x] **Redundant Groups:** Always eliminate redundant groups whose 1s are already covered by other prime implicants.
- [x] **K-Map Cell Count:** A function of $n$ variables requires exactly $2^n$ cells (e.g., 4 variables = 16 cells).""",
        "content_kn": """## 1. ಪರಿಕಲ್ಪನೆಯ ವಿವರವಾದ ವಿವರಣೆ
ಬೂಲಿಯನ್ ಬೀಜಗಣಿತವು ಡಿಜಿಟಲ್ ಸರ್ಕ್ಯೂಟ್‌ಗಳನ್ನು ಸರಳೀಕರಿಸಲು ಬಳಸುವ ಗಣಿತ ಪದ್ಧತಿಯಾಗಿದೆ.

### ಡಿ ಮಾರ್ಗನ್ಸ್ ಪ್ರಮೇಯಗಳು (De Morgan's Laws):
1. $(A + B)' = A' \\cdot B'$
2. $(A \\cdot B)' = A' + B'$

### ಕೆ-ಮ್ಯಾಪ್ (Karnaugh Map):
- ಗ್ರೂಪ್‌ಗಳು ಯಾವಾಗಲೂ $2^k$ ($1, 2, 4, 8, 16$) ಗಾತ್ರದಲ್ಲಿರಬೇಕು.
- ಅಕ್ಕಪಕ್ಕದ ಸೆಲ್‌ಗಳು ಗ್ರೇ ಕೋಡ್ ಮಾದರಿಯನ್ನು ಅನುಸರಿಸುತ್ತವೆ (`00, 01, 11, 10`).

---

## 2. ರಸಪ್ರಶ್ನೆ & VTU ಪರೀಕ್ಷಾ ತ್ವರಿತ ಪರಿಶೀಲನಾ ಪಾಯಿಂಟ್‌ಗಳು
- [x] **ಡಿ ಮಾರ್ಗನ್ಸ್ ನಿಯಮ:** $(AB)' = A' + B'$ ಮತ್ತು $(A+B)' = A'B'$.
- [x] **ಸೆಲ್‌ಗಳ ಸಂಖ್ಯೆ:** $n$ ವೇರಿಯೇಬಲ್‌ಗಳ ಕೆ-ಮ್ಯಾಪ್‌ನಲ್ಲಿ $2^n$ ಸೆಲ್‌ಗಳಿರುತ್ತವೆ (4 ವೇರಿಯೇಬಲ್ = 16 ಸೆಲ್‌ಗಳು).""",
        "content_hi": """## 1. अवधारणा का विस्तृत विवरण
बूलियन बीजगणित डिजिटल लॉजिक सर्किट को सरल बनाने का गणितीय आधार है।

### डी मॉर्गन प्रमेय:
1. $(A + B)' = A' \\cdot B'$
2. $(A \\cdot B)' = A' + B'$

### के-मैप (K-Map):
- समूहों का आकार $2^k$ (1, 2, 4, 8, 16) होना चाहिए।
- आसन्न सेल केवल 1 बिट में भिन्न होते हैं (`00, 01, 11, 10`)।

---

## 2. क्विज और VTU परीक्षा चेकपॉइंट
- [x] **डी मॉर्गन नियम:** ब्रेक द लाइन, चेंज द साइन ($(AB)' = A' + B'$).
- [x] **के-मैप सेल:** 4 वेरिएबल्स के लिए $2^4 = 16$ सेल होते हैं।"""
    },

    "Logic Gates & Universal Realization": {
        "title": "Comprehensive Study Notes: Logic Gates & Universal Realization",
        "title_kn": "ಸಮಗ್ರ ಅಧ್ಯಯನ ಟಿಪ್ಪಣಿಗಳು: ಲಾಜಿಕ್ ಗೇಟ್‌ಗಳು ಮತ್ತು ಯುನಿವರ್ಸಲ್ ಗೇಟ್‌ಗಳು",
        "title_hi": "विस्तृत अध्ययन नोट्स: लॉजिक गेट्स और यूनिवर्सल गेट्स",
        "desc": "Master basic gates (AND, OR, NOT), universal gates (NAND, NOR), XOR/XNOR gates, and building any circuit using only NAND or NOR.",
        "desc_kn": "ಮೂಲ ಗೇಟ್‌ಗಳು, ಯುನಿವರ್ಸಲ್ ಗೇಟ್‌ಗಳು (NAND/NOR) ಮತ್ತು XOR ಗೇಟ್ ಸರ್ಕ್ಯೂಟ್‌ಗಳನ್ನು ಕಲಿಯಿರಿ.",
        "desc_hi": "बेसिक गेट्स (AND, OR, NOT), यूनिवर्सल गेट्स (NAND, NOR) और XOR/XNOR गेट्स को समझें।",
        "content_en": """## 1. Detailed Concept Explanation
**Logic Gates** are the foundational physical building blocks of all digital electronic systems.

### Classification of Gates:
- **Basic Gates:** AND, OR, NOT (Inverter).
- **Universal Gates:** **NAND** and **NOR**. Any Boolean function can be realized using solely NAND gates or solely NOR gates without requiring any other gate type.
- **Arithmetic & Parity Gates:** **XOR** (Exclusive-OR) and **XNOR** (Exclusive-NOR).

### Truth Tables & Gate Functions:
- **AND:** $Y = A \\cdot B$ (Output is 1 only when ALL inputs are 1).
- **OR:** $Y = A + B$ (Output is 1 if ANY input is 1).
- **NOT:** $Y = A'$ (Inverts input).
- **NAND:** $Y = (A \\cdot B)'$ (Universal).
- **NOR:** $Y = (A + B)'$ (Universal).
- **XOR:** $Y = A \\oplus B = A'B + AB'$ (Output is 1 when inputs are unequal; **odd parity detector**).
- **XNOR:** $Y = (A \\oplus B)' = AB + A'B'$ (Output is 1 when inputs are equal; **equality / even detector**).

---

## 2. Key Rules: Minimum NAND/NOR Gates Required

| Desired Gate | Minimum NAND Gates Required | Minimum NOR Gates Required |
| :--- | :---: | :---: |
| **NOT** | **1** | **1** |
| **AND** | **2** | **3** |
| **OR** | **3** | **2** |
| **XOR** | **4** | **5** |
| **XNOR** | **5** | **4** |

---

## 3. Annotated Example
Realize an **OR Gate** using only **NAND Gates**:
- Desired function: $Y = A + B$.
- Apply double negation: $Y = ((A + B)')' = (A' \\cdot B')'$ (by De Morgan's Theorem).
- Step 1: Invert $A$ using 1 NAND gate $\\to A'$.
- Step 2: Invert $B$ using 1 NAND gate $\\to B'$.
- Step 3: Feed $A'$ and $B'$ into a 3rd NAND gate $\\to (A' \\cdot B')' = A + B$.
- Total NAND gates needed: **3**.

---

## 4. Quiz & VTU Exam Quick-Check Points
- [x] **Universal Gates:** Strictly **NAND and NOR** only.
- [x] **XOR Realization:** Requires exactly **4 NAND gates** or **5 NOR gates**.
- [x] **XNOR Realization:** Requires exactly **5 NAND gates** or **4 NOR gates**.
- [x] **XOR Buffer/Inverter Property:**
  $$A \\oplus 0 = A \\quad \\text{(Buffer)}, \\qquad A \\oplus 1 = A' \\quad \\text{(Inverter)}$$""",
        "content_kn": """## 1. ಪರಿಕಲ್ಪನೆಯ ವಿವರವಾದ ವಿವರಣೆ
ಡಿಜಿಟಲ್ ಸರ್ಕ್ಯೂಟ್‌ಗಳ ಮೂಲ ಅಡಿಪಾಯವೇ **ಲಾಜಿಕ್ ಗೇಟ್‌ಗಳು (Logic Gates)**.

### ಯುನಿವರ್ಸಲ್ ಗೇಟ್‌ಗಳು (Universal Gates):
**NAND** ಮತ್ತು **NOR** ಗೇಟ್‌ಗಳನ್ನು ಯುನಿವರ್ಸಲ್ ಗೇಟ್‌ಗಳು ಎಂದು ಕರೆಯಲಾಗುತ್ತದೆ ಏಕೆಂದರೆ ಇವುಗಳಿಂದ ಯಾವುದೇ ಇತರ ಲಾಜಿಕ್ ಗೇಟ್ ಅನ್ನು ನಿರ್ಮಿಸಬಹುದು.

### ಕನಿಷ್ಠ ಗೇಟ್‌ಗಳ ಸಂಖ್ಯೆ:
- **XOR ಗೇಟ್ ರಚಿಸಲು:** **4 NAND** ಗೇಟ್‌ಗಳು ಅಥವಾ **5 NOR** ಗೇಟ್‌ಗಳು ಬೇಕು.
- **XNOR ಗೇಟ್ ರಚಿಸಲು:** **5 NAND** ಗೇಟ್‌ಗಳು ಅಥವಾ **4 NOR** ಗೇಟ್‌ಗಳು ಬೇಕು.

---

## 2. ರಸಪ್ರಶ್ನೆ & VTU ಪರೀಕ್ಷಾ ತ್ವರಿತ ಪರಿಶೀಲನಾ ಪಾಯಿಂಟ್‌ಗಳು
- [x] **ಯುನಿವರ್ಸಲ್ ಗೇಟ್‌ಗಳು:** ಕೇವಲ **NAND ಮತ್ತು NOR**.
- [x] **XOR ಗುಣಲಕ್ಷಣ:** $A \\oplus 0 = A$ ಮತ್ತು $A \\oplus 1 = A'$.""",
        "content_hi": """## 1. अवधारणा का विस्तृत विवरण
लॉजिक गेट्स डिजिटल इलेक्ट्रॉनिक्स के मूलभूत घटक हैं।

### यूनिवर्सल गेट्स (NAND और NOR):
NAND और NOR से किसी भी लॉजिक सर्किट का निर्माण किया जा सकता है।

### आवश्यक न्यूनतम गेट्स:
- **XOR बनाने के लिए:** **4 NAND** या **5 NOR** गेट्स की आवश्यकता होती है।
- **XNOR बनाने के लिए:** **5 NAND** या **4 NOR** गेट्स की आवश्यकता होती है।

---

## 2. क्विज और VTU परीक्षा चेकपॉइंट
- [x] **यूनिवर्सल गेट्स:** केवल **NAND** और **NOR**।
- [x] **XOR समता:** विषम 1s होने पर आउटपुट 1 होता है ($A \\oplus B = A'B + AB'$)।"""
    },

    "Combinational Logic Circuits": {
        "title": "Comprehensive Study Notes: Combinational Logic Circuits",
        "title_kn": "ಸಮಗ್ರ ಅಧ್ಯಯನ ಟಿಪ್ಪಣಿಗಳು: ಕಾಂಬಿನೇಶನಲ್ ಲಾಜಿಕ್ ಸರ್ಕ್ಯೂಟ್‌ಗಳು",
        "title_hi": "विस्तृत अध्ययन नोट्स: कॉम्बिनेशनल लॉजिक सर्किट्स",
        "desc": "Master Half Adders, Full Adders, Multiplexers (MUX), Decoders, Encoders, and Demultiplexers.",
        "desc_kn": "ಹಾಫ್ ಆಡರ್, ಫುಲ್ ಆಡರ್, ಮಲ್ಟಿಪ್ಲೆಕ್ಸರ್ (MUX) ಮತ್ತು ಡಿಕೋಡರ್ ಸರ್ಕ್ಯೂಟ್‌ಗಳನ್ನು ಕಲಿಯಿರಿ.",
        "desc_hi": "हाफ एडर, फुल एडर, मल्टीप्लेक्सर (MUX), डिकोडर और एनकोडर को विस्तार से समझें।",
        "content_en": """## 1. Detailed Concept Explanation
In **Combinational Logic Circuits**, the output at any instant of time depends **solely on the current inputs**, with no feedback path or memory storage elements.

### Key Combinational Blocks:
1. **Half Adder (HA):** Adds two 1-bit numbers ($A, B$).
   - Sum: $S = A \\oplus B$
   - Carry: $C = AB$
2. **Full Adder (FA):** Adds three 1-bit inputs ($A, B, C_{in}$).
   - Sum: $S = A \\oplus B \\oplus C_{in}$
   - Carry: $C_{out} = AB + C_{in}(A \\oplus B) = AB + BC_{in} + AC_{in}$
   - Built using: **2 Half Adders + 1 OR gate**.
3. **Multiplexer (MUX / Data Selector):** Selects one of $2^n$ data inputs and routes it to a single output line based on $n$ select lines.
   - Example: A $4 \\times 1$ MUX has 4 data lines ($I_0-I_3$), 2 select lines ($S_1, S_0$), and 1 output.
4. **Decoder:** Converts an $n$-bit binary input code into at most $2^n$ unique output lines.

---

## 2. Key Rules & Architecture Formulas
- **Full Adder Construction:**
  $$\\text{1 Full Adder} = \\text{2 Half Adders} + \\text{1 OR Gate}$$
- **Multiplexer Select Line Equation:**
  $$\\text{Number of Inputs } = 2^n \\implies n = \\log_2(\\text{Inputs})$$
- **Universal Function Generator:** An $n$-variable Boolean function can always be implemented using a $2^{n-1} \\times 1$ MUX with one variable applied to data inputs, or a $2^n \\times 1$ MUX directly.

---

## 3. Annotated Example
Design a **Full Adder Carry** equation verification:
- Inputs: $A = 1, B = 1, C_{in} = 0$:
  $$S = 1 \\oplus 1 \\oplus 0 = 0 \\oplus 0 = 0$$
  $$C_{out} = (1)(1) + 0(1 \\oplus 1) = 1 + 0 = 1$$
- Sum = 0, Carry = 1 (Decimal $1 + 1 + 0 = 2_{10} = 10_2$).

---

## 4. Quiz & VTU Exam Quick-Check Points
- [x] **Full Adder Components:** Exactly **2 Half Adders and 1 OR Gate**.
- [x] **MUX Select Lines:** An $8 \\times 1$ MUX requires $\\log_2(8) = \\mathbf{3}$ select lines.
- [x] **Combinational vs Sequential:** Combinational circuits have **no clock** and **no memory**.""",
        "content_kn": """## 1. ಪರಿಕಲ್ಪನೆಯ ವಿವರವಾದ ವಿವರಣೆ
**ಕಾಂಬಿನೇಶನಲ್ ಲಾಜಿಕ್ ಸರ್ಕ್ಯೂಟ್‌ಗಳಲ್ಲಿ (Combinational Circuits)** ಪ್ರಸ್ತುತ ಔಟ್‌ಪುಟ್ ಕೇವಲ ಪ್ರಸ್ತುತ ಇನ್‌ಪುಟ್‌ಗಳ ಮೇಲೆ ಮಾತ್ರ ಅವಲಂಬಿತವಾಗಿರುತ್ತದೆ. ಇದರಲ್ಲಿ ಯಾವುದೇ ಮೆಮೊರಿ ಇರುವುದಿಲ್ಲ.

### ಪ್ರಮುಖ ಸರ್ಕ್ಯೂಟ್‌ಗಳು:
1. **ಹಾಫ್ ಆಡರ್ (Half Adder):** ಎರಡು 1-ಬಿಟ್ ಸಂಖ್ಯೆಗಳನ್ನು ಕೂಡಿಸುತ್ತದೆ ($S = A \\oplus B, C = AB$).
2. **ಫುಲ್ ಆಡರ್ (Full Adder):** ಮೂರು 1-ಬಿಟ್ ಸಂಖ್ಯೆಗಳನ್ನು ಕೂಡಿಸುತ್ತದೆ ($S = A \\oplus B \\oplus C_{in}$).
   - ರಚನೆ: **2 ಹಾಫ್ ಆಡರ್‌ಗಳು + 1 OR ಗೇಟ್**.
3. **ಮಲ್ಟಿಪ್ಲೆಕ್ಸರ್ (MUX):** $2^n$ ಇನ್‌ಪುಟ್‌ಗಳಲ್ಲಿ ಒಂದನ್ನು $n$ ಸೆಲೆಕ್ಟ್ ಲೈನ್‌ಗಳ ಆಧಾರದ ಮೇಲೆ ಆಯ್ಕೆ ಮಾಡುತ್ತದೆ.

---

## 2. ರಸಪ್ರಶ್ನೆ & VTU ಪರೀಕ್ಷಾ ತ್ವರಿತ ಪರಿಶೀಲನಾ ಪಾಯಿಂಟ್‌ಗಳು
- [x] **ಫುಲ್ ಆಡರ್:** **2 ಹಾಫ್ ಆಡರ್ + 1 OR ಗೇಟ್** ನಿಂದ ಮಾಡಲ್ಪಟ್ಟಿದೆ.
- [x] **ಸೆಲೆಕ್ಟ್ ಲೈನ್‌ಗಳು:** $8 \\times 1$ MUX ಗೆ **3 ಸೆಲೆಕ್ಟ್ ಲೈನ್‌ಗಳು** ಬೇಕು.""",
        "content_hi": """## 1. अवधारणा का विस्तृत विवरण
कॉम्बिनेशनल सर्किट्स में आउटपुट केवल वर्तमान इनपुट पर निर्भर करता है (मेमोरी नहीं होती)।

### मुख्य घटक:
- **फुल एडर (Full Adder):** 3 बिट्स को जोड़ता है। यह **2 हाफ एडर + 1 OR गेट** से बनता है।
- **मल्टीप्लेक्सर (MUX):** $2^n$ इनपुट में से 1 आउटपुट चुनता है ($n$ सेलेक्ट लाइन्स)।

---

## 2. क्विज और VTU परीक्षा चेकपॉइंट
- [x] **फुल एडर:** 2 हाफ एडर और 1 OR गेट।
- [x] **$8 \\times 1$ MUX:** इसमें $\\log_2(8) = 3$ सेलेक्ट लाइन्स होती हैं।"""
    },

    # =========================================================================
    # SUBJECT 3: ENGINEERING MATHEMATICS
    # =========================================================================
    "Matrices & Linear Systems": {
        "title": "Comprehensive Study Notes: Matrices & Linear Systems",
        "title_kn": "ಸಮಗ್ರ ಅಧ್ಯಯನ ಟಿಪ್ಪಣಿಗಳು: ಮ್ಯಾಟ್ರಿಕ್ಸ್‌ಗಳು ಮತ್ತು ಲೀನಿಯರ್ ಸಿಸ್ಟಮ್ಸ್",
        "title_hi": "विस्तृत अध्ययन नोट्स: आव्यूह (मैट्रिक्स) और रैखिक समीकरण",
        "desc": "Master matrix rank, system consistency (Rouché-Capelli theorem), Gauss elimination, eigenvalues, eigenvectors, and Cayley-Hamilton theorem.",
        "desc_kn": "ಮ್ಯಾಟ್ರಿಕ್ಸ್ ರ್ಯಾಂಕ್, ಕನ್ಸಿಸ್ಟೆನ್ಸಿ, ಐಗನ್ ಮೌಲ್ಯಗಳು (Eigenvalues) ಮತ್ತು ಕೇಲಿ-ಹ್ಯಾಮಿಲ್ಟನ್ ಪ್ರಮೇಯ ಕಲಿಯಿರಿ.",
        "desc_hi": "मैट्रिक्स रैंक, स्थिरता, आइगेनवैल्यू, आइगेनवेक्टर और केली-हैमिल्टन प्रमेय समझें।",
        "content_en": """## 1. Detailed Concept Explanation
A system of $m$ linear equations in $n$ unknowns can be compactly represented in matrix form:
$$A X = B$$
where $A$ is the $m \\times n$ coefficient matrix, $X$ is the column vector of unknowns, and $B$ is the constant vector.

### Rank and Consistency (Rouché–Capelli Theorem):
Let $[A|B]$ denote the augmented matrix:
1. **Consistent (Solutions Exist):** If $\\text{Rank}(A) = \\text{Rank}([A|B]) = r$.
   - **Unique Solution:** If $r = n$ (number of unknowns).
   - **Infinitely Many Solutions:** If $r < n$ (with $n - r$ free independent parameters).
2. **Inconsistent (No Solution):** If $\\text{Rank}(A) \\neq \\text{Rank}([A|B])$.

### Eigenvalues and Eigenvectors:
For a square matrix $A$, a non-zero vector $X$ is an eigenvector corresponding to scalar eigenvalue $\\lambda$ if:
$$A X = \\lambda X \\iff (A - \\lambda I) X = 0$$
- **Characteristic Equation:**
  $$\\det(A - \\lambda I) = 0$$
- For a $2 \\times 2$ matrix $A = \\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}$:
  $$\\lambda^2 - \\text{Trace}(A)\\lambda + \\det(A) = 0$$
- **Cayley-Hamilton Theorem:** Every square matrix satisfies its own characteristic equation ($A^2 - \\text{Trace}(A)A + \\det(A)I = 0$).

---

## 2. Key Rules & Invariant Properties
- **Sum of Eigenvalues:**
  $$\\sum_{i=1}^n \\lambda_i = \\text{Trace}(A) = \\sum_{i=1}^n a_{ii}$$
- **Product of Eigenvalues:**
  $$\\prod_{i=1}^n \\lambda_i = \\det(A)$$
- **Eigenvalues of Triangular / Diagonal Matrices:** Simply the main diagonal entries themselves.
- **Symmetric Matrix Property:** Eigenvalues of a real symmetric matrix are **always real**.

---

## 3. Annotated Example
Find eigenvalues of $A = \\begin{pmatrix} 4 & 1 \\\\ 2 & 3 \\end{pmatrix}$:
1. Compute Trace and Determinant:
   - $\\text{Trace}(A) = 4 + 3 = 7$
   - $\\det(A) = (4)(3) - (1)(2) = 12 - 2 = 10$
2. Characteristic equation:
   $$\\lambda^2 - 7\\lambda + 10 = 0$$
3. Factoring:
   $$(\\lambda - 5)(\\lambda - 2) = 0 \\implies \\lambda_1 = 5, \\quad \\lambda_2 = 2$$
4. Check invariants:
   - Sum: $5 + 2 = 7 = \\text{Trace}$ (Match!)
   - Product: $5 \\times 2 = 10 = \\det$ (Match!)

---

## 4. Quiz & VTU Exam Quick-Check Points
- [x] **Singular Matrix:** $\\det(A) = 0 \\iff$ at least one eigenvalue is **zero**.
- [x] **Homogeneous System $AX = 0$:** Always consistent (trivial solution $X = 0$). Has non-trivial solutions if and only if $\\det(A) = 0$.
- [x] **Inverse from Cayley-Hamilton:** Multiply characteristic equation by $A^{-1}$ to compute matrix inverse without adjugates.""",
        "content_kn": """## 1. ಪರಿಕಲ್ಪನೆಯ ವಿವರವಾದ ವಿವರಣೆ
ರೇಖೀಯ ಸಮೀಕರಣಗಳ ವ್ಯವಸ್ಥೆಯನ್ನು $AX = B$ ರೂಪದಲ್ಲಿ ಬರೆಯಲಾಗುತ್ತದೆ.

### ಐಗನ್ ಮೌಲ್ಯಗಳ (Eigenvalues) ನಿಯಮಗಳು:
- **ಐಗನ್ ಮೌಲ್ಯಗಳ ಮೊತ್ತ:** ಮ್ಯಾಟ್ರಿಕ್ಸ್‌ನ ಟ್ರೇಸ್‌ಗೆ (Trace - ಕರ್ಣ ರೇಖೆಯ ಮೊತ್ತ) ಸಮನಾಗಿರುತ್ತದೆ.
  $$\\lambda_1 + \\lambda_2 = \\text{Trace}(A)$$
- **ಐಗನ್ ಮೌಲ್ಯಗಳ ಗುಣಲಬ್ಧ:** ಮ್ಯಾಟ್ರಿಕ್ಸ್‌ನ ಡಿಟರ್ಮಿನೆಂಟ್ (Determinant) ಗೆ ಸಮನಾಗಿರುತ್ತದೆ.
  $$\\lambda_1 \\times \\lambda_2 = \\det(A)$$
- **ಕೇಲಿ-ಹ್ಯಾಮಿಲ್ಟನ್ ಪ್ರಮೇಯ (Cayley-Hamilton Theorem):** ಪ್ರತಿಯೊಂದು ಚೌಕ ಮ್ಯಾಟ್ರಿಕ್ಸ್ ತನ್ನದೇ ಆದ ಕ್ಯಾರಕ್ಟರಿಸ್ಟಿಕ್ ಸಮೀಕರಣವನ್ನು ತೃಪ್ತಿಪಡಿಸುತ್ತದೆ.

---

## 2. ರಸಪ್ರಶ್ನೆ & VTU ಪರೀಕ್ಷಾ ತ್ವರಿತ ಪರಿಶೀಲನಾ ಪಾಯಿಂಟ್‌ಗಳು
- [x] $\\det(A) = 0$ ಆಗಿದ್ದರೆ ಕನಿಷ್ಠ ಒಂದು ಐಗನ್ ಮೌಲ್ಯ **0** ಆಗಿರುತ್ತದೆ.
- [x] ರಿಯಲ್ ಸಿಮೆಟ್ರಿಕ್ ಮ್ಯಾಟ್ರಿಕ್ಸ್‌ನ ಐಗನ್ ಮೌಲ್ಯಗಳು ಯಾವಾಗಲೂ **ವಾಸ್ತವ (Real)** ಆಗಿರುತ್ತವೆ.""",
        "content_hi": """## 1. अवधारणा का विस्तृत विवरण
रैखिक समीकरण प्रणाली को $AX = B$ रूप में लिखा जाता है।

### आइगेनवैल्यू (Eigenvalues) के महत्वपूर्ण गुण:
- **आइगेनवैल्यू का योग:** मैट्रिक्स के ट्रेस (Trace) के बराबर होता है ($\sum \lambda_i = \text{Trace}(A)$)।
- **आइगेनवैल्यू का गुणनफल:** मैट्रिक्स के सारणिक ($\det(A)$) के बराबर होता है।
- **केली-हैमिल्टन प्रमेय:** प्रत्येक वर्ग आव्यूह अपने विशिष्ट समीकरण को संतुष्ट करता है।

---

## 2. क्विज और VTU परीक्षा चेकपॉइंट
- [x] यदि $\det(A) = 0$ है, तो कम से कम एक आइगेनवैल्यू **शून्य** होगा।
- [x] विकर्ण मैट्रिक्स के आइगेनवैल्यू उसके विकर्ण तत्व ही होते हैं।"""
    },

    "Differential Calculus": {
        "title": "Comprehensive Study Notes: Differential Calculus",
        "title_kn": "ಸಮಗ್ರ ಅಧ್ಯಯನ ಟಿಪ್ಪಣಿಗಳು: ಡಿಫರೆನ್ಷಿಯಲ್ ಕ್ಯಾಲ್ಕುಲಸ್",
        "title_hi": "विस्तृत अध्ययन नोट्स: अवकलन गणित (Differential Calculus)",
        "desc": "Master limits, standard derivatives, product/quotient/chain rules, partial differentiation, Euler's theorem, and Taylor series.",
        "desc_kn": "ಲಿಮಿಟ್ಸ್, ಚೈನ್ ರೂಲ್, ಭಾಗಶಃ ವಿಕಲನ (Partial Derivatives) ಮತ್ತು ಆಯ್ಲರ್ಸ್ ಪ್ರಮೇಯ ಕಲಿಯಿರಿ.",
        "desc_hi": "सीमा (Limits), अवकलन नियम (Chain rule), आंशिक अवकलन और यूलर प्रमेय को समझें।",
        "content_en": """## 1. Detailed Concept Explanation
**Differential Calculus** investigates the instantaneous rate of change of quantities and slopes of curves.

### Standard Derivative Rules:
- Power Rule: $\\frac{d}{dx}[x^n] = n x^{n-1}$
- Exponential: $\\frac{d}{dx}[e^{kx}] = k e^{kx}$
- Logarithmic: $\\frac{d}{dx}[\\ln x] = \\frac{1}{x}$
- Product Rule: $(uv)' = u'v + uv'$
- Quotient Rule: $\\left(\\frac{u}{v}\\right)' = \\frac{u'v - uv'}{v^2}$
- Chain Rule: $\\frac{dy}{dx} = \\frac{dy}{du} \\cdot \\frac{du}{dx}$

### Partial Differentiation:
When $z = f(x, y)$, the partial derivative $\\frac{\\partial f}{\\partial x}$ is computed by treating $y$ as an absolute constant.
- **Euler's Theorem for Homogeneous Functions:**
  If $u = f(x, y)$ is a homogeneous function of degree $n$:
  $$x \\frac{\\partial u}{\\partial x} + y \\frac{\\partial u}{\\partial y} = n \\cdot u$$

---

## 2. Annotated Example
Verify Euler's theorem for $u = x^3 + y^3$:
- Degree $n$: $f(tx, ty) = (tx)^3 + (ty)^3 = t^3(x^3 + y^3) = t^3 u \\implies n = 3$.
- Partial derivatives:
  $$\\frac{\\partial u}{\\partial x} = 3x^2, \\qquad \\frac{\\partial u}{\\partial y} = 3y^2$$
- Euler's LHS:
  $$x(3x^2) + y(3y^2) = 3(x^3 + y^3) = 3u$$
- Confirmed: $n \\cdot u = 3u$.

---

## 3. Quiz & VTU Exam Quick-Check Points
- [x] **L'Hôpital's Rule:** Applicable strictly when limits produce indeterminate forms $\\frac{0}{0}$ or $\\frac{\\infty}{\\infty}$.
- [x] **Euler's Degree Check:** Always factor $t^n$ to determine exact homogeneity degree before applying Euler's formula.""",
        "content_kn": """## 1. ಪರಿಕಲ್ಪನೆಯ ವಿವರವಾದ ವಿವರಣೆ
ಡಿಫರೆನ್ಷಿಯಲ್ ಕ್ಯಾಲ್ಕುಲಸ್ ದರ ಬದಲಾವಣೆ (Rate of Change) ಮತ್ತು ಇಳಿಜಾರುಗಳನ್ನು ಕಂಡುಹಿಡಿಯಲು ಸಹಾಯಕವಾಗಿದೆ.

### ಆಯ್ಲರ್ಸ್ ಪ್ರಮೇಯ (Euler's Theorem):
$u = f(x, y)$ ಎಂಬುದು $n$ ಡಿಗ್ರಿಯ ಹೋಮೋಜೀನಿಯಸ್ ಫಂಕ್ಷನ್ ಆಗಿದ್ದರೆ:
$$x \\frac{\\partial u}{\\partial x} + y \\frac{\\partial u}{\\partial y} = n \\cdot u$$

---

## 2. ರಸಪ್ರಶ್ನೆ & VTU ಪರೀಕ್ಷಾ ತ್ವರಿತ ಪರಿಶೀಲನಾ ಪಾಯಿಂಟ್‌ಗಳು
- [x] **L'Hôpital ನಿಯಮ:** ಕೇವಲ $\\frac{0}{0}$ ಅಥವಾ $\\frac{\\infty}{\\infty}$ ಸಂದರ್ಭದಲ್ಲಿ ಮಾತ್ರ ಅನ್ವಯಿಸುತ್ತದೆ.
- [x] **ಭಾಗಶಃ ವಿಕಲನ:** $x$ ನೊಂದಿಗೆ ಡಿಫರೆನ್ಷಿಯೇಟ್ ಮಾಡುವಾಗ $y$ ಅನ್ನು ಸ್ಥಿರಾಂಕ (Constant) ಎಂದು ಪರಿಗಣಿಸಬೇಕು.""",
        "content_hi": """## 1. अवधारणा का विस्तृत विवरण
अवकलन गणित तात्कालिक परिवर्तन की दर को मापता है।

### यूलर का प्रमेय (Euler's Theorem):
यदि $u(x, y)$ डिग्री $n$ का समघात फलन (Homogeneous function) है:
$$x \\frac{\\partial u}{\\partial x} + y \\frac{\\partial u}{\\partial y} = n \\cdot u$$

---

## 2. क्विज और VTU परीक्षा चेकपॉइंट
- [x] **L'Hôpital का नियम:** केवल $\\frac{0}{0}$ या $\\frac{\\infty}{\\infty}$ पर लागू होता है।
- [x] **आंशिक अवकलन:** $x$ के सापेक्ष अवकलन करते समय $y$ को अचर माना जाता है।"""
    },

    "Integral Calculus": {
        "title": "Comprehensive Study Notes: Integral Calculus",
        "title_kn": "ಸಮಗ್ರ ಅಧ್ಯಯನ ಟಿಪ್ಪಣಿಗಳು: ಇಂಟೆಗ್ರಲ್ ಕ್ಯಾಲ್ಕುಲಸ್",
        "title_hi": "विस्तृत अध्ययन नोट्स: समाकलन गणित (Integral Calculus)",
        "desc": "Master definite & indefinite integration, integration by parts (LIATE rule), substitution, and multiple integrals.",
        "desc_kn": "ಇಂಟಿಗ್ರೇಷನ್ ಬೈ ಪಾರ್ಟ್ಸ್, LIATE ನಿಯಮ ಮತ್ತು ನಿಶ್ಚಿತ ಇಂಟಿಗ್ರಲ್‌ಗಳನ್ನು ಕಲಿಯಿರಿ.",
        "desc_hi": "निश्चित और अनिश्चित समाकलन, खंडशः समाकलन (LIATE नियम) और प्रतिस्थापन विधि समझें।",
        "content_en": """## 1. Detailed Concept Explanation
**Integral Calculus** represents the accumulation of quantities and evaluation of areas under curves.

### Integration by Parts:
Derived from the product rule of differentiation:
$$\\int u \\, dv = u v - \\int v \\, du$$
- **LIATE Rule for Selecting $u$ (in descending priority):**
  1. **L:** Logarithmic functions ($\\ln x$)
  2. **I:** Inverse trigonometric functions ($\\arcsin x, \\arctan x$)
  3. **A:** Algebraic polynomial functions ($x^2, x^3$)
  4. **T:** Trigonometric functions ($\\sin x, \\cos x$)
  5. **E:** Exponential functions ($e^x$)

### Properties of Definite Integrals:
- **Even/Odd Function Rule:**
  $$\\int_{-a}^a f(x) \\, dx = \\begin{cases} 2 \\int_0^a f(x) \\, dx & \\text{if } f(-x) = f(x) \\text{ (Even)} \\\\ 0 & \\text{if } f(-x) = -f(x) \\text{ (Odd)} \\end{cases}$$

---

## 2. Annotated Example
Evaluate $\\int x e^x \\, dx$:
- By LIATE: Algebraic ($x$) comes before Exponential ($e^x$).
  - Let $u = x \\implies du = dx$
  - Let $dv = e^x \\, dx \\implies v = e^x$
- Apply formula:
  $$\\int x e^x \\, dx = x e^x - \\int e^x \\, dx = x e^x - e^x + C = e^x(x - 1) + C$$

---

## 3. Quiz & VTU Exam Quick-Check Points
- [x] **Odd Function Shortcut:** If integrand is odd and limits are symmetric $[-a, a]$, the integral evaluates to **0** instantly.
- [x] **Fundamental Theorem:** $\\frac{d}{dx} \\int_a^x f(t) \\, dt = f(x)$.""",
        "content_kn": """## 1. ಪರಿಕಲ್ಪನೆಯ ವಿವರವಾದ ವಿವರಣೆ
ಇಂಟೆಗ್ರಲ್ ಕ್ಯಾಲ್ಕುಲಸ್ ವಕ್ರರೇಖೆಗಳ ಕೆಳಗಿನ ವಿಸ್ತೀರ್ಣವನ್ನು ಲೆಕ್ಕಹಾಕಲು ಬಳಸಲಾಗುತ್ತದೆ.

### ಇಂಟಿಗ್ರೇಷನ್ ಬೈ ಪಾರ್ಟ್ಸ್ (LIATE Rule):
$$\\int u \\, dv = u v - \\int v \\, du$$
$u$ ಆಯ್ಕೆ ಮಾಡಲು **LIATE** ನಿಯಮ: Logarithmic, Inverse, Algebraic, Trigonometric, Exponential.

### ಸಮ ಮತ್ತು ಬೆಸ ಫಂಕ್ಷನ್ ಗುಣಲಕ್ಷಣ:
ಬೆಸ (Odd) ಫಂಕ್ಷನ್ ಆಗಿದ್ದರೆ:
$$\\int_{-a}^a f(x) \\, dx = 0$$

---

## 2. ರಸಪ್ರಶ್ನೆ & VTU ಪರೀಕ್ಷಾ ತ್ವರಿತ ಪರಿಶೀಲನಾ ಪಾಯಿಂಟ್‌ಗಳು
- [x] ಸಮ್ಮಿತೀಯ ಮಿತಿಗಳಲ್ಲಿ $[-a, a]$ ಬೆಸ ಫಂಕ್ಷನ್‌ನ ಇಂಟಿಗ್ರಲ್ ಮೌಲ್ಯ ಯಾವಾಗಲೂ **0** ಆಗಿರುತ್ತದೆ.""",
        "content_hi": """## 1. अवधारणा का विस्तृत विवरण
समाकलन गणित क्षेत्रफलों और संचयी मानों की गणना करता है।

### खंडशः समाकलन (LIATE नियम):
$$\\int u \\, dv = u v - \\int v \\, du$$
$u$ चुनने का क्रम: **L** (लॉग) $\\to$ **I** (प्रतिलोम) $\\to$ **A** (बीजीय) $\\to$ **T** (त्रिकोणमितीय) $\\to$ **E** (चरघातांकी)।

---

## 2. क्विज और VTU परीक्षा चेकपॉइंट
- [x] विषम फलन (Odd Function) के लिए $\\int_{-a}^a f(x) \\, dx = 0$ होता है।"""
    },

    # =========================================================================
    # SUBJECT 4: BASIC CIRCUIT ANALYSIS
    # =========================================================================
    "Ohm's & Kirchhoff's Laws": {
        "title": "Comprehensive Study Notes: Ohm's & Kirchhoff's Laws",
        "title_kn": "ಸಮಗ್ರ ಅಧ್ಯಯನ ಟಿಪ್ಪಣಿಗಳು: ಓಮ್ ಮತ್ತು ಕಿರ್ಚಾಫ್ ನಿಯಮಗಳು",
        "title_hi": "विस्तृत अध्ययन नोट्स: ओम और किरचॉफ के नियम",
        "desc": "Master Ohm's Law (V=IR), Kirchhoff's Current Law (KCL - charge conservation), Kirchhoff's Voltage Law (KVL - energy conservation), and circuit sign conventions.",
        "desc_kn": "ಓಮ್ಸ್ ನಿಯಮ, ಕಿರ್ಚಾಫ್ ಕರೆಂಟ್ ನಿಯಮ (KCL), ವೋಲ್ಟೇಜ್ ನಿಯಮ (KVL) ಮತ್ತು ಸೈನ್ ಕನ್ವೆನ್ಷನ್‌ಗಳನ್ನು ಕಲಿಯಿರಿ.",
        "desc_hi": "ओम का नियम ($V=IR$), KCL (आवेश संरक्षण) और KVL (ऊर्जा संरक्षण) के नियमों को समझें।",
        "content_en": """## 1. Detailed Concept Explanation
Electrical network analysis is governed by fundamental physical conservation laws.

### Ohm's Law:
At constant temperature, the current $I$ flowing through an ideal conductor is directly proportional to the potential difference $V$ across it:
$$V = I \\cdot R \\quad \\iff \\quad I = \\frac{V}{R} \\quad \\iff \\quad R = \\frac{V}{I}$$
- **Power Dissipation:**
  $$P = V \\cdot I = I^2 R = \\frac{V^2}{R} \\quad \\text{(Watts)}$$

### Kirchhoff's Current Law (KCL):
- **Physical Basis:** **Conservation of Electric Charge**.
- **Statement:** The algebraic sum of currents entering and leaving any node (junction) is zero:
  $$\\sum I_{\\text{entering}} = \\sum I_{\\text{leaving}} \\iff \\sum_{k=1}^N I_k = 0$$

### Kirchhoff's Voltage Law (KVL):
- **Physical Basis:** **Conservation of Energy**.
- **Statement:** The algebraic sum of all electrical potential differences (voltage rises and voltage drops) around any closed loop is zero:
  $$\\sum_{k=1}^M V_k = 0$$

---

## 2. Standard Sign Conventions for KVL Loops
- Moving from **$-$ to $+$** terminal of a source $\\to$ **Voltage Rise ($+V$)**.
- Moving from **$+$ to $-$** terminal of a source $\\to$ **Voltage Drop ($-V$)**.
- Traversing a resistor **in the direction of assumed current** $\\to$ **Voltage Drop ($-I R$)**.
- Traversing a resistor **against the direction of assumed current** $\\to$ **Voltage Rise ($+I R$)**.

---

## 3. Annotated Example
A closed single-loop circuit has a $12\\text{V}$ battery connected in series with resistors $R_1 = 4\\,\\Omega$ and $R_2 = 2\\,\\Omega$:
1. Apply KVL clockwise:
   $$+12 - I(4) - I(2) = 0$$
   $$12 - 6I = 0 \\implies I = 2\\text{ A}$$
2. Voltages across resistors:
   - $V_1 = 2\\text{ A} \\times 4\\,\\Omega = 8\\text{ V}$
   - $V_2 = 2\\text{ A} \\times 2\\,\\Omega = 4\\text{ V}$
3. Check KVL: $12\\text{V} - 8\\text{V} - 4\\text{V} = 0\\text{V}$ (Balanced!).

---

## 4. Quiz & VTU Exam Quick-Check Points
- [x] **Conservation Principles:** **KCL represents Conservation of Charge**; **KVL represents Conservation of Energy**.
- [x] **Ohm's Law Limitation:** Applies strictly to **linear, bilateral, ohmic** conductors at constant temperature (fails for diodes, transistors, electrolytes).
- [x] **Ideal Sources:** An ideal voltage source has **$0\\,\\Omega$ internal resistance**; an ideal current source has **$\\infty\\,\\Omega$ internal resistance**.""",
        "content_kn": """## 1. ಪರಿಕಲ್ಪನೆಯ ವಿವರವಾದ ವಿವರಣೆ
ವಿದ್ಯುತ್ ಸರ್ಕ್ಯೂಟ್ ವಿಶ್ಲೇಷಣೆಯು ಎರಡು ಪ್ರಮುಖ ನಿಯಮಗಳನ್ನು ಆಧರಿಸಿದೆ:

### ಓಮ್‌ನ ನಿಯಮ (Ohm's Law):
ಸ್ಥಿರ ತಾಪಮಾನದಲ್ಲಿ ವಾಹಕದಲ್ಲಿ ಹರಿಯುವ ಕರೆಂಟ್ ($I$) ಅದರ ತುದಿಗಳ ನಡುವಿನ ವೋಲ್ಟೇಜ್‌ಗೆ ($V$) ನೇರ ಅನುಪಾತದಲ್ಲಿರುತ್ತದೆ ($V = IR$).

### ಕಿರ್ಚಾಫ್‌ನ ಕರೆಂಟ್ ನಿಯಮ (KCL):
- ಭೌತಿಕ ತತ್ವ: **ವಿದ್ಯುತ್ ಆವೇಶದ ಸಂರಕ್ಷಣೆ (Conservation of Charge)**.
- ಯಾವುದೇ ಜಂಕ್ಷನ್‌ನಲ್ಲಿ ಒಳಬರುವ ಕರೆಂಟ್‌ಗಳ ಮೊತ್ತವು ಹೊರಹೋಗುವ ಕರೆಂಟ್‌ಗಳ ಮೊತ್ತಕ್ಕೆ ಸಮನಾಗಿರುತ್ತದೆ ($\\sum I = 0$).

### ಕಿರ್ಚಾಫ್‌ನ ವೋಲ್ಟೇಜ್ ನಿಯಮ (KVL):
- ಭೌತಿಕ ತತ್ವ: **ಶಕ್ತಿಯ ಸಂರಕ್ಷಣೆ (Conservation of Energy)**.
- ಮುಚ್ಚಿದ ಲೂಪ್‌ನಲ್ಲಿರುವ ಎಲ್ಲಾ ವೋಲ್ಟೇಜ್‌ಗಳ ಬೀಜಗಣಿತೀಯ ಮೊತ್ತವು ಶೂನ್ಯವಾಗಿರುತ್ತದೆ ($\\sum V = 0$).

---

## 2. ರಸಪ್ರಶ್ನೆ & VTU ಪರೀಕ್ಷಾ ತ್ವರಿತ ಪರಿಶೀಲನಾ ಪಾಯಿಂಟ್‌ಗಳು
- [x] **KCL = ಆವೇಶದ ಸಂರಕ್ಷಣೆ (Charge)**; **KVL = ಶಕ್ತಿಯ ಸಂರಕ್ಷಣೆ (Energy)**.
- [x] ಆದರ್ಶ ವೋಲ್ಟೇಜ್ ಮೂಲದ ಆಂತರಿಕ ರೋಧ (Internal Resistance) = **$0\\,\\Omega$**.
- [x] ಆದರ್ಶ ಕರೆಂಟ್ ಮೂಲದ ಆಂತರಿಕ ರೋಧ = **$\\infty\\,\\Omega$**.""",
        "content_hi": """## 1. अवधारणा का विस्तृत विवरण
विद्युत परिपथ विश्लेषण के दो मुख्य नियम हैं:

### ओम का नियम:
स्थिर तापमान पर चालक के सिरों के बीच का विभवांतर ($V$) उसमें बहने वाली धारा ($I$) के समानुपाती होता है ($V = IR$)।

### किरचॉफ के नियम:
1. **KCL (किरचॉफ का धारा नियम):** यह **आवेश संरक्षण (Conservation of Charge)** पर आधारित है ($\sum I = 0$)।
2. **KVL (किरचॉफ का विभव नियम):** यह **ऊर्जा संरक्षण (Conservation of Energy)** पर आधारित है ($\sum V = 0$)।

---

## 2. क्विज और VTU परीक्षा चेकपॉइंट
- [x] **KCL:** आवेश संरक्षण नियम।
- [x] **KVL:** ऊर्जा संरक्षण नियम।
- [x] आदर्श वोल्टेज स्रोत का आंतरिक प्रतिरोध = **0**, तथा आदर्श धारा स्रोत का **$\infty$** होता है।"""
    },

    "Series-Parallel Circuit Analysis": {
        "title": "Comprehensive Study Notes: Series-Parallel Circuit Analysis",
        "title_kn": "ಸಮಗ್ರ ಅಧ್ಯಯನ ಟಿಪ್ಪಣಿಗಳು: ಸರಣಿ ಮತ್ತು ಸಮಾಂತರ ಸರ್ಕ್ಯೂಟ್ ವಿಶ್ಲೇಷಣೆ",
        "title_hi": "विस्तृत अध्ययन नोट्स: श्रेणी और समानांतर परिपथ विश्लेषण",
        "desc": "Master equivalent resistance calculations, Voltage Divider Rule (VDR), Current Divider Rule (CDR), and bridge circuits.",
        "desc_kn": "ಸರಣಿ-ಸಮಾಂತರ ರೋಧಕಗಳ ಸಮಾನ ಮೌಲ್ಯ, ವೋಲ್ಟೇಜ್ ಮತ್ತು ಕರೆಂಟ್ ಡಿವೈಡರ್ ನಿಯಮಗಳನ್ನು ಕಲಿಯಿರಿ.",
        "desc_hi": "समतुल्य प्रतिरोध, वोल्टेज डिवाइडर नियम (VDR) और करंट डिवाइडर नियम (CDR) को समझें।",
        "content_en": """## 1. Detailed Concept Explanation
Complex resistor networks can be reduced systematically into equivalent single resistances.

### Series Circuits:
- **Same Current:** The identical current $I$ passes sequentially through every series component.
- **Additive Resistance:**
  $$R_{eq} = R_1 + R_2 + R_3 + \\dots + R_n$$
- **Voltage Divider Rule (VDR):**
  $$V_x = V_{\\text{total}} \\times \\frac{R_x}{R_{eq}}$$

### Parallel Circuits:
- **Same Voltage:** All parallel branches experience the exact same voltage $V$.
- **Equivalent Resistance:**
  $$\\frac{1}{R_{eq}} = \\frac{1}{R_1} + \\frac{1}{R_2} + \\dots + \\frac{1}{R_n}$$
  For **two parallel resistors**:
  $$R_{eq} = \\frac{R_1 \\times R_2}{R_1 + R_2} \\quad \\left(\\frac{\\text{Product}}{\\text{Sum}}\\right)$$
- **Current Divider Rule (CDR) for two branches:**
  $$I_1 = I_{\\text{total}} \\times \\frac{R_2}{R_1 + R_2}, \\qquad I_2 = I_{\\text{total}} \\times \\frac{R_1}{R_1 + R_2}$$
  *(Notice the opposite resistor appears in the numerator!)*

---

## 2. Annotated Example
A $60\\text{V}$ source powers $R_1 = 6\\,\\Omega$ in parallel with $R_2 = 12\\,\\Omega$, connected in series with $R_3 = 6\\,\\Omega$:
1. Parallel combination:
   $$R_p = \\frac{6 \\times 12}{6 + 12} = \\frac{72}{18} = 4\\,\\Omega$$
2. Total resistance:
   $$R_{\\text{total}} = R_p + R_3 = 4 + 6 = 10\\,\\Omega$$
3. Total Current:
   $$I_{\\text{total}} = \\frac{60\\text{V}}{10\\,\\Omega} = 6\\text{ A}$$
4. Branch current through $6\\,\\Omega$ using CDR:
   $$I_1 = 6\\text{ A} \\times \\frac{12}{6 + 12} = 6 \\times \\frac{12}{18} = 4\\text{ A}$$

---

## 3. Quiz & VTU Exam Quick-Check Points
- [x] **Parallel Equivalent Size:** $R_{eq}$ of parallel resistors is **always smaller than the smallest branch resistor**.
- [x] **Equal Resistors in Parallel:** $n$ identical resistors of value $R$ in parallel have $R_{eq} = \\frac{R}{n}$.
- [x] **CDR Trap:** To find current in $R_1$, multiply by the **other** resistor $R_2$ in the numerator.""",
        "content_kn": """## 1. ಪರಿಕಲ್ಪನೆಯ ವಿವರವಾದ ವಿವರಣೆ
ರೋಧಕಗಳ (Resistors) ಸರಣಿ ಮತ್ತು ಸಮಾಂತರ ಸಂಯೋಜನೆಗಳ ಲೆಕ್ಕಾಚಾರ:

### ಸರಣಿ (Series):
- ಕರೆಂಟ್ ಒಂದೇ ಆಗಿರುತ್ತದೆ.
- ಒಟ್ಟು ರೋಧ: $R_{eq} = R_1 + R_2 + \\dots$
- ವೋಲ್ಟೇಜ್ ಡಿವೈಡರ್ ನಿಯಮ (VDR): $V_1 = V_{total} \\times \\frac{R_1}{R_1 + R_2}$

### ಸಮಾಂತರ (Parallel):
- ವೋಲ್ಟೇಜ್ ಒಂದೇ ಆಗಿರುತ್ತದೆ.
- ಎರಡು ರೋಧಕಗಳಿಗೆ: $R_{eq} = \\frac{R_1 \\times R_2}{R_1 + R_2}$
- ಕರೆಂಟ್ ಡಿವೈಡರ್ ನಿಯಮ (CDR): $I_1 = I_{total} \\times \\frac{R_2}{R_1 + R_2}$

---

## 2. ರಸಪ್ರಶ್ನೆ & VTU ಪರೀಕ್ಷಾ ತ್ವರಿತ ಪರಿಶೀಲನಾ ಪಾಯಿಂಟ್‌ಗಳು
- [x] ಸಮಾಂತರ ರೋಧಕಗಳ ಸಮಾನ ಮೌಲ್ಯವು ಅವುಗಳಲ್ಲಿನ ಅತ್ಯಂತ ಚಿಕ್ಕ ರೋಧಕಕ್ಕಿಂತಲೂ ಕಡಿಮೆಯಾಗಿರುತ್ತದೆ.
- [x] $n$ ಸಮಾನ ರೋಧಕಗಳನ್ನು ಸಮಾಂತರವಾಗಿ ಜೋಡಿಸಿದರೆ $R_{eq} = \\frac{R}{n}$.""",
        "content_hi": """## 1. अवधारणा का विस्तृत विवरण
परिपथों में प्रतिरोधों का श्रेणी और समानांतर संयोजन:

### श्रेणी क्रम (Series):
- सभी में धारा समान होती है: $R_{eq} = R_1 + R_2 + \dots$
### समानांतर क्रम (Parallel):
- सभी सिरों पर वोल्टेज समान होता है:
  $$R_{eq} = \\frac{R_1 \\cdot R_2}{R_1 + R_2}$$
- धारा विभाजक नियम (CDR):
  $$I_1 = I_{total} \\times \\frac{R_2}{R_1 + R_2}$$

---

## 2. क्विज और VTU परीक्षा चेकपॉइंट
- [x] समानांतर प्रतिरोध का मान सबसे छोटे प्रतिरोध से भी कम होता है।
- [x] $R_1$ में धारा निकालने के लिए अंश में $R_2$ रखा जाता है।"""
    },

    "Mesh & Nodal Analysis": {
        "title": "Comprehensive Study Notes: Mesh & Nodal Analysis",
        "title_kn": "ಸಮಗ್ರ ಅಧ್ಯಯನ ಟಿಪ್ಪಣಿಗಳು: ಮೆಶ್ ಮತ್ತು ನೋಡಲ್ ವಿಶ್ಲೇಷಣೆ",
        "title_hi": "विस्तृत अध्ययन नोट्स: मेश और नोडल विश्लेषण",
        "desc": "Master loop/mesh current analysis using KVL, nodal voltage analysis using KCL, supermesh (current source), and supernode (voltage source).",
        "desc_kn": "ಮೆಶ್ (KVL) ಮತ್ತು ನೋಡಲ್ (KCL) ವಿಶ್ಲೇಷಣೆ, ಸೂಪರ್‌ಮೆಶ್ ಮತ್ತು ಸೂಪರ್‌ನೋಡ್ ತಂತ್ರಗಳನ್ನು ಕಲಿಯಿರಿ.",
        "desc_hi": "मेश करंट विश्लेषण (KVL), नोड वोल्टेज विश्लेषण (KCL), सुपरमेश और सुपरनोड को समझें।",
        "content_en": """## 1. Detailed Concept Explanation
Mesh and Nodal analysis are systematic matrix-friendly network reduction methodologies.

### Mesh Analysis (Loop Method):
- **Tool:** Applies **Kirchhoff's Voltage Law (KVL)** around independent planar meshes.
- **Variables:** Fictitious circulating loop currents ($I_1, I_2, \\dots, I_m$).
- **Number of Mesh Equations:**
  $$M = B - N + 1$$
  *(where $B$ is total branches, $N$ is total nodes).*
- **Supermesh:** Created when a current source is shared between two adjacent meshes. Remove the current source branch and write a single combined KVL equation around both meshes, augmented with a constraint equation:
  $$I_{\\text{mesh2}} - I_{\\text{mesh1}} = I_{\\text{source}}$$

### Nodal Analysis (Node-Voltage Method):
- **Tool:** Applies **Kirchhoff's Current Law (KCL)** at non-reference essential nodes.
- **Variables:** Node voltages with respect to a designated ground ($0\\text{V}$) reference node.
- **Number of Node Equations:**
  $$E = N - 1$$
- **Supernode:** Formed when a voltage source is connected between two non-reference nodes without an intervening series resistor. Enclose the source in a generalized boundary, write a combined KCL equation, and add the voltage constraint equation:
  $$V_1 - V_2 = V_{\\text{source}}$$

---

## 2. Matrix Inspection Form for Mesh & Node
For planar circuits with independent sources:
- **Mesh Matrix:**
  $$\\begin{pmatrix} R_{11} & -R_{12} \\\\ -R_{21} & R_{22} \\end{pmatrix} \\begin{pmatrix} I_1 \\\\ I_2 \\end{pmatrix} = \\begin{pmatrix} V_1 \\\\ V_2 \\end{pmatrix}$$
  *(where $R_{ii}$ is the self-resistance of mesh $i$, and $R_{ij}$ is the mutual resistance shared between meshes $i$ and $j$).*

---

## 3. Annotated Example
Two meshes sharing a $2\\,\\Omega$ resistor with a $10\\text{V}$ source in Mesh 1 ($R_1 = 4\\,\\Omega$) and Mesh 2 ($R_2 = 6\\,\\Omega$):
- Mesh 1 KVL:
  $$10 - 4I_1 - 2(I_1 - I_2) = 0 \\implies 6I_1 - 2I_2 = 10$$
- Mesh 2 KVL:
  $$-2(I_2 - I_1) - 6I_2 = 0 \\implies -2I_1 + 8I_2 = 0 \\implies I_1 = 4I_2$$
- Substitute:
  $$6(4I_2) - 2I_2 = 10 \\implies 22I_2 = 10 \\implies I_2 = \\frac{5}{11}\\text{ A}, \\quad I_1 = \\frac{20}{11}\\text{ A}$$

---

## 4. Quiz & VTU Exam Quick-Check Points
- [x] **Method Selection Rule:** If a circuit has fewer meshes than nodes, use **Mesh Analysis**. If it has fewer essential nodes than meshes, use **Nodal Analysis**.
- [x] **Planar Circuits Only:** Mesh analysis can **only be applied to planar circuits** (circuits that can be drawn on a plane without crossing wires). Nodal analysis works for all circuits.
- [x] **Supermesh Trigger:** A current source shared between two meshes.
- [x] **Supernode Trigger:** A voltage source connected between two non-reference nodes.""",
        "content_kn": """## 1. ಪರಿಕಲ್ಪನೆಯ ವಿವರವಾದ ವಿವರಣೆ
ಸರ್ಕ್ಯೂಟ್ ವಿಶ್ಲೇಷಣೆಯ ಪ್ರಮುಖ ವಿಧಾನಗಳು:

### ಮೆಶ್ ವಿಶ್ಲೇಷಣೆ (Mesh Analysis):
- **KVL** ಅನ್ನು ಬಳಸುತ್ತದೆ.
- ಸಮೀಕರಣಗಳ ಸಂಖ್ಯೆ: $M = B - N + 1$.
- ಎರಡು ಮೆಶ್‌ಗಳ ನಡುವೆ ಕರೆಂಟ್ ಸೋರ್ಸ್ ಇದ್ದಾಗ **ಸೂಪರ್‌ಮೆಶ್ (Supermesh)** ಉಂಟಾಗುತ್ತದೆ.

### ನೋಡಲ್ ವಿಶ್ಲೇಷಣೆ (Nodal Analysis):
- **KCL** ಅನ್ನು ಬಳಸುತ್ತದೆ.
- ಸಮೀಕರಣಗಳ ಸಂಖ್ಯೆ: $N - 1$.
- ಎರಡು ನೋಡ್‌ಗಳ ನಡುವೆ ವೋಲ್ಟೇಜ್ ಸೋರ್ಸ್ ಇದ್ದಾಗ **ಸೂಪರ್‌ನೋಡ್ (Supernode)** ಉಂಟಾಗುತ್ತದೆ.

---

## 2. ರಸಪ್ರಶ್ನೆ & VTU ಪರೀಕ್ಷಾ ತ್ವರಿತ ಪರಿಶೀಲನಾ ಪಾಯಿಂಟ್‌ಗಳು
- [x] ಮೆಶ್ ವಿಶ್ಲೇಷಣೆಯನ್ನು ಕೇವಲ **ಪ್ಲಾನಾರ್ (Planar)** ಸರ್ಕ್ಯೂಟ್‌ಗಳಿಗೆ ಮಾತ್ರ ಅನ್ವಯಿಸಬಹುದು. ನೋಡಲ್ ವಿಶ್ಲೇಷಣೆಯನ್ನು ಎಲ್ಲ ಸರ್ಕ್ಯೂಟ್‌ಗಳಿಗೂ ಅನ್ವಯಿಸಬಹುದು.""",
        "content_hi": """## 1. अवधारणा का विस्तृत विवरण
जटिल नेटवर्कों को हल करने की दो प्रमुख विधियां हैं:

### मेश विश्लेषण (Mesh Analysis):
- **KVL** पर आधारित। केवल **समतलीय (Planar)** परिपथों पर लागू होता है।
- दो मेश के बीच करंट सोर्स होने पर **सुपरमेश** बनता है।

### नोडल विश्लेषण (Nodal Analysis):
- **KCL** पर आधारित। समीकरणों की संख्या = $N - 1$।
- दो नोड्स के बीच वोल्टेज सोर्स होने पर **सुपरनोड** बनता है।

---

## 2. क्विज और VTU परीक्षा चेकपॉइंट
- [x] मेश विश्लेषण केवल समतलीय (Planar) सर्किट के लिए है।
- [x] नोडल विश्लेषण सभी सर्किटों के लिए सार्वभौमिक है।"""
    }
}
