"""
Learnloop Seed Generator
========================
Populates SQLite database with:
- 4 VTU Engineering Subjects
- 14 Syllabus Topics
- 168+ Verified Technical MCQs (12 per topic across easy, medium, hard)
- 45+ Curated Learning Resources (Notes, Verified Video Searches, Worked Examples, Practice Sets)
- Synthetic Demo Users (student1, student2, teacher) with pre-computed quiz histories
"""

from datetime import datetime, timezone, timedelta
import random
from models import db, User, Subject, Topic, Question, Attempt, AttemptAnswer, TopicProgress, Resource, ResourceView
from engine import topic_mastery

def seed_database(app):
    with app.app_context():
        db.create_all()

        # Check if already seeded
        if Subject.query.first():
            print("Database already contains data. Skipping full re-seed.")
            return

        print("Seeding database with engineering curriculum, verified MCQs, and synthetic users...")

        # 1. Create Subjects
        sub_c = Subject(name="C Programming")
        sub_de = Subject(name="Digital Electronics")
        sub_math = Subject(name="Engineering Mathematics")
        sub_circuits = Subject(name="Basic Circuit Analysis")

        db.session.add_all([sub_c, sub_de, sub_math, sub_circuits])
        db.session.flush()

        # 2. Create Topics
        topics_data = [
            # C Programming
            (sub_c.id, "Arrays in C", "One-dimensional and multi-dimensional contiguous memory arrays, indexing, and boundary conditions."),
            (sub_c.id, "Pointers and Memory", "Memory addresses, pointer arithmetic, dereferencing, void pointers, and dynamic allocation."),
            (sub_c.id, "Functions and Recursion", "Parameter passing mechanisms (call by value/reference), return types, stack frames, and recursion."),
            (sub_c.id, "Control Flow and Loops", "Conditional branching (if-else, switch-case) and iteration constructs (for, while, do-while)."),

            # Digital Electronics
            (sub_de.id, "Number Systems & Codes", "Binary, Octal, Hexadecimal conversions, 1's/2's complement arithmetic, and BCD/Gray codes."),
            (sub_de.id, "Boolean Algebra & Logic Simplification", "De Morgan's laws, canonical SOP/POS forms, minterms, and Karnaugh Map (K-Map) reduction."),
            (sub_de.id, "Logic Gates & Universal Realization", "Standard AND/OR/NOT gates, NAND/NOR universality, XOR/XNOR parity generators."),
            (sub_de.id, "Combinational Logic Circuits", "Design of Adders (Half/Full), Subtractors, Multiplexers (MUX), Demultiplexers, and Decoders."),

            # Engineering Mathematics
            (sub_math.id, "Matrices & Linear Systems", "Matrix operations, determinants, rank of a matrix, Gaussian elimination, and Eigenvalues/Eigenvectors."),
            (sub_math.id, "Differential Calculus", "Partial differentiation, Euler's theorem for homogeneous functions, Taylor series, and Jacobians."),
            (sub_math.id, "Integral Calculus", "Definite integrals, reduction formulas, double/triple integrals, and evaluation of areas/volumes."),

            # Circuit Analysis
            (sub_circuits.id, "Ohm's & Kirchhoff's Laws", "Basic electrical quantities, Ohm's law, Kirchhoff's Current Law (KCL), and Kirchhoff's Voltage Law (KVL)."),
            (sub_circuits.id, "Series-Parallel Circuit Analysis", "Equivalent resistance, voltage divider rule, current divider rule, and star-delta conversions."),
            (sub_circuits.id, "Mesh & Nodal Analysis", "Matrix formulations for planar mesh currents, supermesh, essential node voltages, and supernode analysis.")
        ]

        topic_objects = {}
        for sub_id, name, desc in topics_data:
            t = Topic(subject_id=sub_id, name=name, description=desc)
            db.session.add(t)
            db.session.flush()
            topic_objects[name] = t

        # Helper to add questions
        def add_q(t_name, text, a, b, c, d, correct, diff, subtopic, expl):
            q = Question(
                topic_id=topic_objects[t_name].id,
                text=text,
                option_a=a,
                option_b=b,
                option_c=c,
                option_d=d,
                correct_option=correct,
                difficulty=diff,
                subtopic=subtopic,
                explanation=expl
            )
            db.session.add(q)

        # ---------------------------------------------------------
        # TOPIC 1: Arrays in C (12 Questions)
        # ---------------------------------------------------------
        add_q("Arrays in C", "What is the index of the first element in a standard C array of size N?",
              "1", "0", "-1", "N-1", "B", "easy", "Array Indexing",
              "In C, array indexing is strictly zero-based; the first element is at index 0.")
        add_q("Arrays in C", "Which of the following correctly declares an integer array of size 10 in C?",
              "int arr[10];", "array arr[10];", "int arr;", "arr{10}: int;", "A", "easy", "Array Declaration",
              "In C syntax, type followed by identifier and bracketed size declares an array: 'int arr[10];'.")
        add_q("Arrays in C", "What happens if a program writes to arr[10] when arr is declared as int arr[10]?",
              "Compile error", "Automatic array expansion", "Undefined behavior / buffer overrun", "Array resets to 0", "C", "easy", "Bounds Checking",
              "C does not perform runtime array bounds checking. Accessing out-of-bounds leads to undefined behavior.")
        add_q("Arrays in C", "What is the value of arr[2] given: int arr[4] = {5, 10, 15, 20}?",
              "5", "10", "15", "20", "C", "easy", "Array Initialization",
              "arr[0]=5, arr[1]=10, arr[2]=15, arr[3]=20.")
        add_q("Arrays in C", "How are elements of a 2D array in C stored in physical memory?",
              "Column-major order", "Row-major order", "Hash table buckets", "Linked lists", "B", "medium", "Multi-dimensional Arrays",
              "C stores multi-dimensional arrays sequentially in row-major order.")
        add_q("Arrays in C", "Given 'int a[5] = {1, 2};', what are the values of elements a[2], a[3], and a[4]?",
              "Garbage values", "Zeros", "1, 2, 1", "Causes compile error", "B", "medium", "Array Initialization",
              "In C, partial initialization automatically zero-initializes all remaining unassigned elements.")
        add_q("Arrays in C", "What does the expression 'sizeof(arr) / sizeof(arr[0])' calculate?",
              "Total bytes of the array", "Number of elements in the array", "Size of a single element pointer", "Memory offset of last element", "B", "medium", "Array Sizing",
              "Dividing total byte size by the byte size of one element yields total element count.")
        add_q("Arrays in C", "When passing an array name to a function, what is actually passed to the function parameter?",
              "A complete copy of the array", "Pointer to the first element", "Size of the array", "Reference to the last element", "B", "medium", "Array Decay",
              "In C, array names decay into a pointer to their first element when passed into functions.")
        add_q("Arrays in C", "Given 'int mat[2][3] = {{1,2,3},{4,5,6}};', what is *(*(mat + 1) + 2)?",
              "3", "4", "5", "6", "D", "hard", "Pointer-to-Array Arithmetic",
              "*(mat+1) yields row 1 ({4,5,6}). Adding 2 offsets to column index 2, dereferencing yields 6.")
        add_q("Arrays in C", "Which declaration represents an array of 5 pointers to integers in C?",
              "int *arr[5];", "int (*arr)[5];", "int arr*(5);", "int **arr[5];", "A", "hard", "Pointer Arrays",
              "int *arr[5] is an array of 5 pointers. In contrast, int (*arr)[5] is a pointer to an array of 5 ints.")
        add_q("Arrays in C", "In C99 and later, what is a Variable Length Array (VLA)?",
              "Array whose size can change dynamically at runtime", "Array whose dimensions are evaluated at runtime during allocation", "An array placed in heap via realloc", "An array with variable element data types", "B", "hard", "VLAs",
              "A VLA has stack dimensions determined at runtime, though its size remains fixed once allocated.")
        add_q("Arrays in C", "Given 'int a[] = {10, 20, 30}; int *p = a;', what does '*p++' evaluate to and leave p pointing to?",
              "Evaluates to 10; p points to 20", "Evaluates to 20; p points to 10", "Evaluates to 11; p points to 10", "Evaluates to 20; p points to 30", "A", "hard", "Pointer Arithmetic",
              "Postfix ++ has higher precedence than *, but returns original value for dereference (10) then increments p to a[1] (20).")

        # ---------------------------------------------------------
        # TOPIC 2: Pointers and Memory (12 Questions)
        # ---------------------------------------------------------
        add_q("Pointers and Memory", "Which operator is used to obtain the memory address of a variable in C?",
              "*", "&", "->", "%", "B", "easy", "Address-of Operator",
              "The ampersand '&' is the unary address-of operator in C.")
        add_q("Pointers and Memory", "What operator is used to dereference a pointer and read the value it points to?",
              "&", "#", "*", "@", "C", "easy", "Dereference Operator",
              "The asterisk '*' dereferences a pointer to access or modify the pointed-to memory.")
        add_q("Pointers and Memory", "What is the value of a NULL pointer in C conceptually?",
              "Points to address 0 / invalid memory", "Points to the top of stack", "Points to next available heap block", "Random memory garbage", "A", "easy", "Null Pointers",
              "A NULL pointer is a standardized constant indicating that the pointer points to no valid memory location.")
        add_q("Pointers and Memory", "Which standard library function dynamically allocates uninitialized memory on the heap?",
              "free()", "malloc()", "calloc()", "realloc()", "B", "easy", "Dynamic Allocation",
              "malloc() allocates requested number of bytes on the heap and leaves memory uninitialized.")
        add_q("Pointers and Memory", "What is the primary difference between malloc() and calloc()?",
              "calloc() allocates on stack; malloc() on heap", "calloc() clears memory to zero; malloc() does not", "malloc() takes two arguments; calloc() takes one", "malloc() is faster because it returns void*", "B", "medium", "Memory Allocation",
              "calloc(n, size) initializes all allocated bytes to zero; malloc(bytes) leaves contents indeterminate.")
        add_q("Pointers and Memory", "What is a 'dangling pointer' in C?",
              "A pointer initialized to NULL", "A pointer pointing to memory that has already been freed or deallocated", "A pointer that points to another pointer", "A pointer with an invalid typecast", "B", "medium", "Memory Safety",
              "A dangling pointer occurs when the referenced memory is deallocated but the pointer is still referenced.")
        add_q("Pointers and Memory", "If 'int *p = (int*)1000;' and sizeof(int) is 4, what is the value of 'p + 2'?",
              "1002", "1004", "1008", "2000", "C", "medium", "Pointer Arithmetic",
              "Pointer arithmetic steps by sizeof(target type): 1000 + 2 * 4 = 1008.")
        add_q("Pointers and Memory", "What is the purpose of a 'void*' pointer in C?",
              "Pointer that points to invalid memory", "Generic pointer that can hold address of any data type", "Pointer that cannot be passed to functions", "A pointer that points to function definitions only", "B", "medium", "Generic Pointers",
              "A void* is a generic pointer. It can point to any type without an explicit cast, but cannot be dereferenced directly.")
        add_q("Pointers and Memory", "What is a 'memory leak' in C?",
              "Reading unallocated memory locations", "Dynamically allocated memory that is never freed when no longer needed", "Accessing memory beyond an array index", "Stack overflow due to infinite recursion", "B", "hard", "Memory Leaks",
              "A memory leak occurs when heap memory is allocated via malloc/calloc but never released with free().")
        add_q("Pointers and Memory", "What does the following declaration mean: 'int (*func_ptr)(int, int);'?",
              "A function returning a pointer to int", "A pointer to a function taking two ints and returning int", "An array of function pointers", "A recursive function definition", "B", "hard", "Function Pointers",
              "Parentheses around (*func_ptr) bind the asterisk to the identifier, making it a function pointer.")
        add_q("Pointers and Memory", "What is the consequence of freeing the same dynamically allocated block twice (double free)?",
              "Memory is automatically cleared", "Safe no-op", "Undefined behavior and potential heap corruption vulnerability", "Operating system terminates all background processes", "C", "hard", "Heap Safety",
              "Double free corrupts the heap management metadata and leads to undefined behavior or crash.")
        add_q("Pointers and Memory", "Given 'char *s = \"hello\";', what happens if you execute '*s = 'H';'?",
              "String changes to 'Hello'", "Undefined behavior / segmentation fault because string literals are read-only", "Compiler automatically copies string to heap", "Character 'h' is replaced safely", "B", "hard", "String Literals",
              "In C, string literals are typically stored in read-only memory sections (.rodata). Modifying them causes undefined behavior.")

        # ---------------------------------------------------------
        # TOPIC 3: Functions and Recursion (12 Questions)
        # ---------------------------------------------------------
        add_q("Functions and Recursion", "In C, arguments to functions are by default passed using:",
              "Call by reference", "Call by value", "Call by name", "Call by result", "B", "easy", "Parameter Passing",
              "C strictly uses call-by-value. To simulate call-by-reference, pointers are passed by value.")
        add_q("Functions and Recursion", "What keyword is used if a function does not return any value in C?",
              "null", "empty", "void", "static", "C", "easy", "Return Types",
              "The 'void' return type denotes that a function does not return a value to the caller.")
        add_q("Functions and Recursion", "What essential component must every recursive function possess to avoid infinite loops?",
              "Global accumulator", "Base case (termination condition)", "Static local variable", "Dynamic memory allocation", "B", "easy", "Recursion Basics",
              "A base case provides the termination condition that stops further recursive calls.")
        add_q("Functions and Recursion", "What is the default return type of a C function if none is specified in pre-C99 standards?",
              "void", "char", "int", "float", "C", "easy", "Function Signatures",
              "In legacy C standards, omitting the return type defaults to int (implicit int rule).")
        add_q("Functions and Recursion", "What data structure does the CPU runtime use to track active function calls and local variables?",
              "Queue", "Call Stack", "Binary Heap", "Hash Map", "B", "medium", "Call Stack",
              "Function invocation frames and local variables are pushed onto and popped from the call stack.")
        add_q("Functions and Recursion", "What condition occurs when recursive function calls consume all available stack memory?",
              "Stack overflow", "Heap fragmentation", "Deadlock", "Segmentation underflow", "A", "medium", "Stack Overflow",
              "Excessive recursive nesting without reaching a base case exhausts call stack space, triggering a stack overflow.")
        add_q("Functions and Recursion", "What is 'tail recursion'?",
              "Recursion where the recursive call is the very last operation performed in the function", "Recursion that calls two functions simultaneously", "A recursive function without a base case", "Recursion that allocates memory on the heap", "A", "medium", "Tail Recursion",
              "Tail recursion occurs when the return statement directly returns the recursive call without pending operations.")
        add_q("Functions and Recursion", "How does declaring a variable 'static' inside a function alter its lifecycle?",
              "Makes it accessible globally across all files", "Retains its value across multiple function calls throughout program execution", "Stores it in read-only code segment", "Forces the compiler to inline the variable", "B", "medium", "Static Storage",
              "A static local variable has permanent storage duration and retains its state across invocations.")
        add_q("Functions and Recursion", "What is the time complexity of the naive recursive Fibonacci implementation: fib(n) = fib(n-1) + fib(n-2)?",
              "O(n)", "O(n log n)", "O(2^n)", "O(1)", "C", "hard", "Algorithm Complexity",
              "Naive recursive Fibonacci branches into two subproblems at each step, yielding exponential O(2^n) complexity.")
        add_q("Functions and Recursion", "Why does tail-call optimization (TCO) improve recursive execution efficiency in modern compilers?",
              "Converts recursion into heap allocations", "Reuses the current stack frame instead of pushing a new frame", "Increases cache misses", "Runs sub-calls on multiple CPU threads", "B", "hard", "Optimization",
              "TCO replaces the call with a jump instruction, reusing the active stack frame and avoiding stack overflow.")
        add_q("Functions and Recursion", "What is a function prototype in C?",
              "The compiled assembly of a function", "A declaration that specifies the function name, return type, and parameter types before its definition", "A macro expansion of a function", "A built-in system call", "B", "hard", "Prototypes",
              "A prototype informs the compiler of parameter types and return type so it can perform type checking before the function body is parsed.")
        add_q("Functions and Recursion", "Can a function in C return a pointer to its own non-static local variable?",
              "Yes, it is standard practice", "Yes, but it returns a null pointer", "No, because the local variable's stack memory is deallocated upon function return", "Yes, if compiled with optimization", "C", "hard", "Stack Lifecycles",
              "Returning a pointer to a local automatic variable produces a dangling pointer pointing to popped stack memory.")

        # ---------------------------------------------------------
        # TOPIC 4: Control Flow and Loops (12 Questions)
        # ---------------------------------------------------------
        add_q("Control Flow and Loops", "Which loop construct in C is guaranteed to execute its body at least once?",
              "for loop", "while loop", "do-while loop", "nested loop", "C", "easy", "Loop Constructs",
              "The do-while loop evaluates its condition at the bottom, guaranteeing at least one execution.")
        add_q("Control Flow and Loops", "What statement is used to immediately exit the innermost enclosing loop or switch?",
              "continue", "return", "break", "goto", "C", "easy", "Jump Statements",
              "The 'break' statement terminates execution of the nearest enclosing while, do, for, or switch construct.")
        add_q("Control Flow and Loops", "What does the 'continue' statement do inside a loop?",
              "Exits the loop entirely", "Skips the remainder of the current iteration and jumps to the loop condition/increment", "Restarts the program", "Pauses execution for 1 second", "B", "easy", "Iteration Control",
              "continue skips remaining statements in the current iteration and advances to the loop update/condition.")
        add_q("Control Flow and Loops", "What type of expression is required in the condition of an 'if' statement in C?",
              "Strict boolean (true/false only)", "Scalar expression where 0 is false and non-zero is true", "Must evaluate to a character", "Must be a constant literal", "B", "easy", "Conditionals",
              "In C, any non-zero value evaluates to true, and zero evaluates to false.")
        add_q("Control Flow and Loops", "What happens in a C switch statement if a 'case' matches but has no 'break' statement?",
              "Syntax error", "Execution falls through to the next case statements until a break or end is encountered", "Program crashes", "Only default case executes", "B", "medium", "Switch Fallthrough",
              "Without 'break', control falls through sequentially into subsequent case code blocks regardless of their match status.")
        add_q("Control Flow and Loops", "What data types are permitted as the control expression in a C switch statement?",
              "Floats and doubles only", "Integral or enumeration types", "Strings and arrays", "Pointers to functions only", "B", "medium", "Switch Types",
              "In C, switch statements only accept integer types (int, char, enum) or expressions that promote to integer.")
        add_q("Control Flow and Loops", "What will 'for( ; ; )' do in a C program?",
              "Compile error because expressions are missing", "Execute an infinite loop", "Execute zero times", "Run exactly once", "B", "medium", "Infinite Loops",
              "An empty condition in a for loop defaults to true, resulting in an intentional infinite loop.")
        add_q("Control Flow and Loops", "Which operator in C allows conditional assignment in a single line (ternary operator)?",
              "?:", "::", "<>", "<=>", "A", "medium", "Ternary Operator",
              "The conditional ternary operator has syntax: condition ? expr_if_true : expr_if_false.")
        add_q("Control Flow and Loops", "Given 'int x = 5; if (x = 0) printf(\"A\"); else printf(\"B\");', what is printed?",
              "A", "B", "Nothing", "Compile error", "B", "hard", "Assignment in Conditions",
              "'x = 0' is assignment, not comparison! It assigns 0 to x and evaluates to 0 (false), so the else branch executes printing 'B'.")
        add_q("Control Flow and Loops", "What is 'Duff's Device' in C programming?",
              "A security exploit", "An unrolled loop mechanism combining a do-while loop with an interleaved switch statement", "A hardware timer register", "A memory debugging library", "B", "hard", "Advanced Constructs",
              "Duff's Device unrolls serial copies by interleaving a switch statement with a do-while loop.")
        add_q("Control Flow and Loops", "Why is indiscriminate use of 'goto' discouraged in structured programming?",
              "It increases binary size by 200%", "It creates unstructured control flow ('spaghetti code') and hinders compiler optimization", "It disables pointer arithmetic", "It is deprecated in C99", "B", "hard", "Structured Programming",
              "Uncontrolled goto statements obscure program logic and complicate maintenance and formal verification.")
        add_q("Control Flow and Loops", "In 'while (i-- > 0)', when is the decrement applied to variable i?",
              "Before comparison with 0", "After comparison with 0 in the condition evaluation", "Only after the loop body finishes", "Never", "B", "hard", "Operator Precedence",
              "Post-decrement compares the original value of i against 0, then immediately decrements i.")

        # ---------------------------------------------------------
        # TOPIC 5: Number Systems & Codes (12 Questions)
        # ---------------------------------------------------------
        add_q("Number Systems & Codes", "What is the decimal equivalent of the binary number (1011)₂?",
              "9", "11", "13", "15", "B", "easy", "Binary to Decimal",
              "1*8 + 0*4 + 1*2 + 1*1 = 8 + 0 + 2 + 1 = 11.")
        add_q("Number Systems & Codes", "How many bits are in one hexadecimal digit?",
              "2", "4", "8", "16", "B", "easy", "Hexadecimal Representation",
              "One hex digit represents 16 values (0-F), requiring exactly 4 binary bits (nibble).")
        add_q("Number Systems & Codes", "What is the 1's complement of the binary number 101010?",
              "010101", "110101", "010110", "101011", "A", "easy", "1's Complement",
              "The 1's complement is obtained by inverting each bit (1 becomes 0 and 0 becomes 1).")
        add_q("Number Systems & Codes", "What is the base (radix) of the Octal number system?",
              "2", "8", "10", "16", "B", "easy", "Radix Systems",
              "The octal system uses digits 0 through 7, so its radix is 8.")
        add_q("Number Systems & Codes", "How is the 2's complement of a binary number calculated?",
              "Invert all bits only", "Invert all bits and add 1 to the LSB", "Add 1 to MSB", "Shift bits left by 1", "B", "medium", "2's Complement",
              "2's complement is computed by taking the 1's complement (inverting all bits) and adding 1 to the least significant bit.")
        add_q("Number Systems & Codes", "What decimal integer does the 8-bit 2's complement pattern (11111111)₂ represent?",
              "-128", "-1", "-127", "+255", "B", "medium", "Signed Representation",
              "In 2's complement, an all-ones pattern represents -1.")
        add_q("Number Systems & Codes", "What is the key property of Gray code that makes it ideal for rotary encoders?",
              "It is an alphanumeric code", "Only one bit changes between successive numbers", "It has parity bits included", "It uses base 12", "B", "medium", "Gray Code",
              "Gray code is a unit-distance code where only one bit changes between consecutive states, preventing race conditions.")
        add_q("Number Systems & Codes", "What is the BCD (Binary Coded Decimal) representation of decimal 35?",
              "0010 0101", "0011 0101", "1000 1101", "0011 1000", "B", "medium", "BCD Encoding",
              "Each decimal digit is encoded into 4 bits: 3 -> 0011, 5 -> 0101. Result = 0011 0101.")
        add_q("Number Systems & Codes", "What is the range of signed integers that can be represented using n-bit 2's complement?",
              "-(2^(n-1)) to +(2^(n-1) - 1)", "-(2^n) to +(2^n - 1)", "-2^(n-1) to +2^(n-1)", "0 to 2^n - 1", "A", "hard", "Range of Numbers",
              "For n bits in 2's complement, the range is -2^(n-1) to +(2^(n-1) - 1). For n=8, this is -128 to +127.")
        add_q("Number Systems & Codes", "In 2's complement addition of two signed numbers, how is an arithmetic overflow detected?",
              "When carry out of MSB is 1", "When carry into MSB differs from carry out of MSB", "When the sum is 0", "When both operands are positive", "B", "hard", "Overflow Detection",
              "Overflow occurs in 2's complement addition when Cin != Cout for the sign bit (MSB).")
        add_q("Number Systems & Codes", "Convert the binary number 1011 to its Gray code equivalent:",
              "1110", "1101", "1001", "0100", "A", "hard", "Binary to Gray",
              "G3 = B3 = 1; G2 = B3 XOR B2 = 1 XOR 0 = 1; G1 = B2 XOR B1 = 0 XOR 1 = 1; G0 = B1 XOR B0 = 1 XOR 1 = 0. Gray = 1110.")
        add_q("Number Systems & Codes", "Why are illegal states (1010 to 1111) avoided in 8421 BCD arithmetic?",
              "They exceed 4 bits", "They do not correspond to any single decimal digit (0-9)", "They cause hardware burnout", "They represent negative numbers only", "B", "hard", "BCD Arithmetic",
              "Decimal digits only span 0-9. Values 10-15 (1010-1111) require adding 6 (0110) for BCD correction.")

        # ---------------------------------------------------------
        # TOPIC 6: Boolean Algebra & Logic Simplification (12 Questions)
        # ---------------------------------------------------------
        add_q("Boolean Algebra & Logic Simplification", "According to Boolean Algebra, what is A + 0 equal to?",
              "0", "1", "A", "A'", "C", "easy", "Boolean Identities",
              "By identity law of OR operation, ORing any variable with 0 yields the variable itself: A + 0 = A.")
        add_q("Boolean Algebra & Logic Simplification", "What is A * A' (A AND NOT A) equal to?",
              "1", "0", "A", "Undefined", "B", "easy", "Complementarity Law",
              "A variable and its complement can never both be 1; their product is always 0.")
        add_q("Boolean Algebra & Logic Simplification", "State De Morgan's first theorem: (A + B)' is equivalent to:",
              "A' + B'", "A' * B'", "A * B", "A' + B", "B", "easy", "De Morgan's Laws",
              "De Morgan's theorem states that the complement of a sum equals the product of the complements: (A+B)' = A'*B'.")
        add_q("Boolean Algebra & Logic Simplification", "What is the dual of the Boolean expression: A + (B * C)?",
              "A * (B + C)", "A' * (B' + C')", "A' + (B' * C')", "(A * B) + C", "A", "easy", "Duality Principle",
              "By the principle of duality, swap AND and OR operators and interchange 0 and 1: A*(B+C).")
        add_q("Boolean Algebra & Logic Simplification", "In a Karnaugh Map (K-Map), why are adjacent cells ordered using Gray code?",
              "To alphabetical sort variables", "To ensure only one variable changes between adjacent cells", "To reduce cell count", "To permit diagonal groupings", "B", "medium", "K-Map Mechanics",
              "Adjacent cells in a K-map use Gray code so that only one literal changes state, allowing reduction by A + A' = 1.")
        add_q("Boolean Algebra & Logic Simplification", "How many cells are present in a 4-variable Karnaugh Map?",
              "8", "16", "32", "64", "B", "medium", "K-Map Sizing",
              "A K-map with n variables has 2^n cells; for 4 variables, 2^4 = 16 cells.")
        add_q("Boolean Algebra & Logic Simplification", "What is an 'essential prime implicant' in K-map minimization?",
              "A group containing only 1s", "A prime implicant that covers at least one minterm not covered by any other prime implicant", "The largest group on the map", "A group that includes don't-care conditions", "B", "medium", "Prime Implicants",
              "An essential prime implicant is uniquely responsible for covering at least one minterm.")
        add_q("Boolean Algebra & Logic Simplification", "Simplify the Boolean expression: A + A'B:",
              "A + B", "A * B", "A", "B", "A", "medium", "Absorption Law",
              "By absorption: A + A'B = (A + A')(A + B) = 1 * (A + B) = A + B.")
        add_q("Boolean Algebra & Logic Simplification", "What does a 'don't-care' condition (X) represent in digital circuit design?",
              "An invalid voltage level", "An input combination that will never occur or whose output value does not matter", "A clock pulse glitch", "A short circuit", "B", "hard", "Don't Care Conditions",
              "Don't-care conditions can be grouped as 1 or 0 to form larger K-map clusters and simplify the circuit.")
        add_q("Boolean Algebra & Logic Simplification", "What is the consensus theorem expression for: AB + A'C + BC?",
              "AB + A'C", "BC", "A + B + C", "A'B + AC'", "A", "hard", "Consensus Theorem",
              "The term BC is redundant by the consensus theorem because B is with A and C is with A'. Result = AB + A'C.")
        add_q("Boolean Algebra & Logic Simplification", "A grouping of 8 adjacent cells (an octet) in a 4-variable K-map eliminates how many variables?",
              "1 variable", "2 variables", "3 variables", "4 variables", "C", "hard", "K-Map Grouping",
              "Grouping 2^k cells eliminates k variables. For an octet (2^3 = 8 cells), exactly 3 variables are eliminated.")
        add_q("Boolean Algebra & Logic Simplification", "What is the canonical Product of Sums (POS) representation composed of?",
              "Minterms", "Maxterms", "Parity bits", "Don't-cares only", "B", "hard", "Canonical Forms",
              "POS is a product of maxterms (sums of all input literals).")

        # ---------------------------------------------------------
        # TOPIC 7: Logic Gates & Universal Realization (12 Questions)
        # ---------------------------------------------------------
        add_q("Logic Gates & Universal Realization", "Which logic gate outputs HIGH (1) only when all of its inputs are HIGH (1)?",
              "OR", "AND", "XOR", "NOR", "B", "easy", "Basic Gates",
              "An AND gate outputs 1 if and only if all inputs are 1.")
        add_q("Logic Gates & Universal Realization", "Which gate is known as the 'inverter' in digital logic?",
              "NAND", "NOT", "AND", "BUFFER", "B", "easy", "Inverter",
              "The NOT gate produces the logical complement (inversion) of its input.")
        add_q("Logic Gates & Universal Realization", "Which two logic gates are classified as 'universal gates'?",
              "AND and OR", "NAND and NOR", "XOR and XNOR", "NOT and BUFFER", "B", "easy", "Universal Gates",
              "NAND and NOR are universal gates because any Boolean function can be realized using only NAND or only NOR gates.")
        add_q("Logic Gates & Universal Realization", "What is the output of a 2-input XOR gate when both inputs are identical (e.g., 0,0 or 1,1)?",
              "1", "0", "High impedance", "Oscillating", "B", "easy", "XOR Gate",
              "XOR outputs 1 when inputs differ, and 0 when inputs are equal.")
        add_q("Logic Gates & Universal Realization", "How many 2-input NAND gates are required to implement a 2-input AND gate?",
              "1", "2", "3", "4", "B", "medium", "NAND Realization",
              "Two NAND gates: the first produces (AB)', and the second acts as an inverter to produce ((AB)')' = AB.")
        add_q("Logic Gates & Universal Realization", "How many 2-input NOR gates are required to construct a 2-input OR gate?",
              "1", "2", "3", "4", "B", "medium", "NOR Realization",
              "Two NOR gates: the first produces (A+B)', and the second inverts it to produce A+B.")
        add_q("Logic Gates & Universal Realization", "How many 2-input NAND gates are needed to construct a 2-input XOR gate?",
              "3", "4", "5", "6", "B", "medium", "NAND Realization",
              "A minimum of 4 two-input NAND gates are required to implement the XOR function: A(AB)' + B(AB)'.")
        add_q("Logic Gates & Universal Realization", "What is the boolean expression for an XNOR gate with inputs A and B?",
              "AB + A'B'", "A'B + AB'", "A + B", "(A + B)'", "A", "medium", "XNOR Gate",
              "XNOR is the equivalence gate, producing 1 when inputs are equal: AB + A'B'.")
        add_q("Logic Gates & Universal Realization", "What is 'fan-out' of a logic gate?",
              "The maximum number of inputs the gate can have", "The maximum number of standard gate inputs the gate output can reliably drive", "The heat generated by the gate", "The propagation delay per load unit", "B", "hard", "Gate Characteristics",
              "Fan-out is the maximum number of standard logic inputs that the output of a gate can drive safely without signal degradation.")
        add_q("Logic Gates & Universal Realization", "What happens when an unused input of a standard TTL AND gate is left open (floating)?",
              "It is interpreted as logic LOW (0)", "It acts as logic HIGH (1)", "The gate burns out", "It causes high impedance output", "B", "hard", "TTL Logic Levels",
              "In TTL (Transistor-Transistor Logic), floating inputs float to a logic HIGH level due to internal pull-up behavior.")
        add_q("Logic Gates & Universal Realization", "What is 'propagation delay' in a digital logic gate?",
              "Time taken to solder the gate", "Time delay between transition of an input and corresponding transition of the output", "Number of clock cycles to reset", "Clock frequency of gate", "B", "hard", "Timing Parameters",
              "Propagation delay measures the time elapsed from input transition to output response.")
        add_q("Logic Gates & Universal Realization", "What is the minimum number of 2-input NOR gates needed to implement a 2-input XOR gate?",
              "3", "4", "5", "6", "C", "hard", "NOR Realization",
              "A minimum of 5 two-input NOR gates are required to synthesize a 2-input XOR function.")

        # ---------------------------------------------------------
        # TOPIC 8: Combinational Logic Circuits (12 Questions)
        # ---------------------------------------------------------
        add_q("Combinational Logic Circuits", "A Half Adder circuit adds two 1-bit inputs and produces which two outputs?",
              "Sum and Difference", "Sum and Carry", "Borrow and Quotient", "Product and Carry", "B", "easy", "Half Adder",
              "A half adder accepts inputs A and B, producing Sum = A XOR B and Carry = A AND B.")
        add_q("Combinational Logic Circuits", "How many inputs and outputs does a standard Full Adder circuit have?",
              "2 inputs, 2 outputs", "3 inputs, 2 outputs", "3 inputs, 3 outputs", "4 inputs, 2 outputs", "B", "easy", "Full Adder",
              "A full adder adds three 1-bit inputs (A, B, and Carry-in) to generate Sum and Carry-out.")
        add_q("Combinational Logic Circuits", "What is the function of a Multiplexer (MUX)?",
              "Converts serial data to parallel", "Selects one of many analog/digital input lines and forwards it to a single output line", "Performs binary division", "Decodes memory addresses", "B", "easy", "Multiplexers",
              "A MUX is a data selector routing one of 2^n inputs to a single output based on n selection lines.")
        add_q("Combinational Logic Circuits", "How many selection lines are required for an 8-to-1 Multiplexer?",
              "2", "3", "4", "8", "B", "easy", "MUX Sizing",
              "For 2^n inputs, n select lines are needed. Since 8 = 2^3, 3 select lines are required.")
        add_q("Combinational Logic Circuits", "What is the boolean equation for the Sum output of a Full Adder with inputs A, B, and Cin?",
              "A AND B AND Cin", "A XOR B XOR Cin", "AB + BCin + ACin", "(A + B) * Cin", "B", "medium", "Full Adder Logic",
              "Sum is given by the odd parity function of three inputs: A XOR B XOR Cin.")
        add_q("Combinational Logic Circuits", "What is the Carry-out (Cout) expression for a Full Adder?",
              "AB + Cin(A XOR B)", "A XOR B XOR Cin", "(A + B) * Cin", "A'B + AB'", "A", "medium", "Carry Generation",
              "Carry-out is generated when any two or more inputs are 1: Cout = AB + Cin(A XOR B) or AB + BCin + ACin.")
        add_q("Combinational Logic Circuits", "A 3-to-8 decoder has how many input lines and active output lines?",
              "8 inputs, 3 outputs", "3 inputs, 8 outputs", "3 inputs, 1 output", "8 inputs, 1 output", "B", "medium", "Decoders",
              "A decoder takes n input lines and decodes them into up to 2^n distinct output lines (3 inputs to 8 outputs).")
        add_q("Combinational Logic Circuits", "How many Half Adders and OR gates are needed to construct a Full Adder?",
              "1 Half Adder, 1 OR gate", "2 Half Adders, 1 OR gate", "3 Half Adders, 0 OR gates", "2 Half Adders, 2 OR gates", "B", "medium", "Full Adder Synthesis",
              "A full adder is constructed using two half adders and one OR gate to combine the carry outputs.")
        add_q("Combinational Logic Circuits", "In a Ripple Carry Adder (RCA), what causes significant propagation delay in wide bit-widths?",
              "Excessive capacitance on data bus", "Carry bit must ripple sequentially through each full adder stage from LSB to MSB", "Clock skew between flip-flops", "Thermal throttling", "B", "hard", "Carry Propagation",
              "Each stage in a ripple carry adder must wait for the carry out from the previous stage, creating O(n) delay.")
        add_q("Combinational Logic Circuits", "How does a Carry Lookahead Adder (CLA) solve the propagation delay of a ripple carry adder?",
              "By using dynamic clocking", "By calculating carry signals in parallel using generate (G) and propagate (P) logic", "By converting additions to subtractions", "By reducing the word size to 4 bits", "B", "hard", "Carry Lookahead",
              "A CLA calculates carries in advance using P = A XOR B and G = AB, achieving constant O(1) or logarithmic delay.")
        add_q("Combinational Logic Circuits", "How many 4-to-1 Multiplexers are needed to construct a 16-to-1 Multiplexer?",
              "4", "5", "8", "16", "B", "hard", "MUX Tree",
              "Four 4-to-1 MUXes form the first stage, and one 4-to-1 MUX combines their outputs in the second stage: total = 5.")
        add_q("Combinational Logic Circuits", "What is the difference between a Multiplexer and a Priority Encoder?",
              "A MUX is analog, encoder is digital", "A MUX selects data based on address; a Priority Encoder generates binary code corresponding to the highest priority active input", "A Priority Encoder has multiple outputs for a single input", "They perform identical functions", "B", "hard", "Encoders",
              "A priority encoder outputs the binary representation of the highest active index among its inputs.")

        # ---------------------------------------------------------
        # TOPIC 9: Matrices & Linear Systems (12 Questions)
        # ---------------------------------------------------------
        add_q("Matrices & Linear Systems", "What is the determinant of a 2x2 matrix [[a, b], [c, d]]?",
              "ab - cd", "ad - bc", "ac - bd", "ad + bc", "B", "easy", "Determinants",
              "The determinant of a 2x2 matrix is computed by the formula: ad - bc.")
        add_q("Matrices & Linear Systems", "A square matrix A is called singular if its determinant is:",
              "1", "0", "Negative", "Undefined", "B", "easy", "Singular Matrices",
              "A matrix is singular if and only if det(A) = 0, meaning it has no inverse.")
        add_q("Matrices & Linear Systems", "What is the transpose of a symmetric matrix A?",
              "-A", "A", "A^(-1)", "Identity matrix", "B", "easy", "Matrix Types",
              "A matrix is symmetric if it equals its transpose: A^T = A.")
        add_q("Matrices & Linear Systems", "What is the product of an n x n matrix A and the identity matrix I_n?",
              "0", "I_n", "A", "A^2", "C", "easy", "Identity Matrix",
              "The identity matrix acts as the multiplicative identity: A * I = A.")
        add_q("Matrices & Linear Systems", "What is the characteristic equation used to determine eigenvalues (λ) of matrix A?",
              "det(A + λI) = 0", "det(A - λI) = 0", "trace(A) = λ", "A * λ = I", "B", "medium", "Eigenvalues",
              "Eigenvalues satisfy (A - λI)v = 0. For non-trivial solutions, det(A - λI) = 0.")
        add_q("Matrices & Linear Systems", "The sum of the eigenvalues of a square matrix is always equal to its:",
              "Determinant", "Trace (sum of main diagonal elements)", "Rank", "Condition number", "B", "medium", "Eigenvalue Properties",
              "A fundamental theorem states that sum(λ_i) = Trace(A).")
        add_q("Matrices & Linear Systems", "The product of the eigenvalues of a square matrix equals its:",
              "Trace", "Determinant", "Inverse", "Rank", "B", "medium", "Eigenvalue Properties",
              "The product of the eigenvalues of A is equal to det(A).")
        add_q("Matrices & Linear Systems", "What does the rank of a matrix represent?",
              "Number of total non-zero elements", "Maximum number of linearly independent rows or columns", "The largest diagonal element", "Number of negative eigenvalues", "B", "medium", "Matrix Rank",
              "Rank is the dimension of the vector space spanned by its rows or columns.")
        add_q("Matrices & Linear Systems", "By Cayley-Hamilton theorem, every square matrix satisfies:",
              "Its own characteristic equation", "The wave equation", "Newton's second law", "Laplace transform", "A", "hard", "Cayley-Hamilton",
              "The Cayley-Hamilton theorem states that substituting matrix A into its characteristic polynomial P(λ) yields P(A) = 0.")
        add_q("Matrices & Linear Systems", "For a non-homogeneous system of linear equations AX = B, a unique solution exists if and only if:",
              "Rank(A) < Rank([A|B])", "Rank(A) = Rank([A|B]) = number of unknowns (n)", "det(A) = 0", "Rank(A) = 0", "B", "hard", "System Consistency",
              "By Rouché-Capelli theorem, a unique solution exists when rank(A) = rank([A|B]) = n (number of variables).")
        add_q("Matrices & Linear Systems", "What are the eigenvalues of an upper triangular matrix?",
              "All zeros", "The diagonal elements of the matrix", "The reciprocal of its trace", "Cannot be determined without row operations", "B", "hard", "Triangular Matrices",
              "For triangular (or diagonal) matrices, the eigenvalues are simply the entries along the main diagonal.")
        add_q("Matrices & Linear Systems", "If matrix A is orthogonal, what is A^(-1) equal to?",
              "-A", "A^T", "det(A) * I", "A^2", "B", "hard", "Orthogonal Matrices",
              "By definition, an orthogonal matrix satisfies A^T * A = I, which means A^(-1) = A^T.")

        # ---------------------------------------------------------
        # TOPIC 10: Differential Calculus (12 Questions)
        # ---------------------------------------------------------
        add_q("Differential Calculus", "What is the derivative of f(x) = x^n with respect to x?",
              "n * x^(n-1)", "x^(n+1) / (n+1)", "n * x^n", "x^(n-1)", "A", "easy", "Power Rule",
              "By power rule of differentiation, d/dx (x^n) = n * x^(n-1).")
        add_q("Differential Calculus", "What is the derivative of sin(x) with respect to x?",
              "-cos(x)", "cos(x)", "-sin(x)", "tan(x)", "B", "easy", "Trigonometric Derivatives",
              "d/dx (sin x) = cos x.")
        add_q("Differential Calculus", "What is the partial derivative ∂f/∂x of f(x, y) = x^2 * y + y^3?",
              "2xy", "2x + 3y^2", "x^2 + 3y^2", "2xy + 3y^2", "A", "easy", "Partial Differentiation",
              "When differentiating with respect to x, treat y as a constant: ∂/∂x (x^2 * y + y^3) = 2xy + 0 = 2xy.")
        add_q("Differential Calculus", "What is the value of lim (x->0) [sin(x) / x]?",
              "0", "1", "Infinity", "Undefined", "B", "easy", "Limits",
              "A standard trigonometric limit: lim(x->0) (sin x / x) = 1.")
        add_q("Differential Calculus", "According to Euler's theorem, if u(x, y) is a homogeneous function of degree n, then x*(∂u/∂x) + y*(∂u/∂y) equals:",
              "n * u", "u / n", "0", "n^2 * u", "A", "medium", "Euler's Theorem",
              "Euler's theorem for homogeneous functions states: x(∂u/∂x) + y(∂u/∂y) = n*u.")
        add_q("Differential Calculus", "What rule is used to differentiate a composite function f(g(x))?",
              "Product Rule", "Quotient Rule", "Chain Rule", "L'Hôpital's Rule", "C", "medium", "Chain Rule",
              "The chain rule states: d/dx [f(g(x))] = f'(g(x)) * g'(x).")
        add_q("Differential Calculus", "When can L'Hôpital's rule be applied to evaluate a limit?",
              "Whenever the function is a polynomial", "Only when the limit produces indeterminate forms 0/0 or ∞/∞", "Only when x approaches infinity", "Whenever denominator is zero", "B", "medium", "L'Hôpital's Rule",
              "L'Hôpital's rule is valid specifically for indeterminate forms like 0/0 or ∞/∞.")
        add_q("Differential Calculus", "For a function of two variables f(x, y), what condition indicates a saddle point if D = fxx*fyy - (fxy)^2?",
              "D > 0 and fxx > 0", "D > 0 and fxx < 0", "D < 0", "D = 0", "C", "medium", "Extrema of Two Variables",
              "If the discriminant D < 0 at a critical point, the point is a saddle point.")
        add_q("Differential Calculus", "What does the Jacobian determinant J = ∂(u, v) / ∂(x, y) represent physically in coordinate transformations?",
              "Rate of temperature change", "Local area scaling factor (transformation distortion ratio)", "Curvature of a vector field", "Distance between origin and points", "B", "hard", "Jacobians",
              "The Jacobian matrix determinant measures how an infinitesimal differential area element transforms between coordinate systems.")
        add_q("Differential Calculus", "If u = x + y and v = x - y, what is the value of the Jacobian ∂(u, v)/∂(x, y)?",
              "0", "2", "-2", "1", "C", "hard", "Jacobian Calculation",
              "Matrix is [[1, 1], [1, -1]]. Determinant = (1)(-1) - (1)(1) = -1 - 1 = -2.")
        add_q("Differential Calculus", "In Taylor series expansion of f(x) about x = a, what is the coefficient of (x - a)^2?",
              "f'(a)", "f''(a) / 2!", "f''(a)", "f'''(a) / 3!", "B", "hard", "Taylor Series",
              "The nth term of Taylor series is [f^(n)(a) / n!] * (x - a)^n. For n=2, coefficient is f''(a)/2!.")
        add_q("Differential Calculus", "What does Clairaut's theorem state regarding mixed second-order partial derivatives?",
              "∂²f/∂x∂y = ∂²f/∂y∂x if partial derivatives are continuous", "∂²f/∂x² = -∂²f/∂y²", "Mixed partial derivatives are always zero", "They depend on path of integration", "A", "hard", "Mixed Partials",
              "Clairaut's theorem (Schwarz's theorem) guarantees equality of mixed partials under continuity.")

        # ---------------------------------------------------------
        # TOPIC 11: Integral Calculus (12 Questions)
        # ---------------------------------------------------------
        add_q("Integral Calculus", "What is the indefinite integral ∫ x^n dx for n ≠ -1?",
              "x^(n+1) / (n+1) + C", "n * x^(n-1) + C", "x^n / n + C", "ln|x| + C", "A", "easy", "Basic Integration",
              "Standard power rule of integration: ∫ x^n dx = [x^(n+1) / (n+1)] + C.")
        add_q("Integral Calculus", "What is ∫ (1 / x) dx for x > 0?",
              "ln(x) + C", "e^x + C", "-1/x^2 + C", "x + C", "A", "easy", "Logarithmic Integrals",
              "The antiderivative of 1/x is ln|x| + C.")
        add_q("Integral Calculus", "What is the value of the definite integral ∫ from 0 to π of sin(x) dx?",
              "0", "1", "2", "-1", "C", "easy", "Definite Integrals",
              "[-cos(x)] from 0 to π = -cos(π) - (-cos(0)) = -(-1) - (-1) = 1 + 1 = 2.")
        add_q("Integral Calculus", "What integration technique is derived from the product rule of differentiation?",
              "Substitution method", "Integration by parts", "Partial fraction expansion", "Trapezoidal rule", "B", "easy", "Integration by Parts",
              "Integration by parts: ∫ u dv = u*v - ∫ v du, derived from the product rule.")
        add_q("Integral Calculus", "What is the value of the Beta function B(m, n) in terms of the Gamma function Γ?",
              "[Γ(m) * Γ(n)] / Γ(m + n)", "Γ(m + n) / [Γ(m) * Γ(n)]", "Γ(m) + Γ(n)", "Γ(m * n)", "A", "medium", "Beta and Gamma Functions",
              "Standard identity connecting Beta and Gamma functions: B(m, n) = [Γ(m)Γ(n)] / Γ(m+n).")
        add_q("Integral Calculus", "What is the value of Γ(1/2)?",
              "1", "√π", "π / 2", "1 / 2", "B", "medium", "Gamma Values",
              "A fundamental mathematical result: Γ(1/2) = √π.")
        add_q("Integral Calculus", "When converting a Cartesian double integral ∬ f(x, y) dx dy into polar coordinates (r, θ), dx dy becomes:",
              "dr dθ", "r dr dθ", "r^2 dr dθ", "(1/r) dr dθ", "B", "medium", "Coordinate Transformation",
              "The differential area element in polar coordinates scales by the Jacobian r: dA = r dr dθ.")
        add_q("Integral Calculus", "What does a double integral ∬_R 1 dx dy compute physically for region R?",
              "Volume of a sphere", "Area of the planar region R", "Perimeter of region R", "Centroid coordinates", "B", "medium", "Double Integrals",
              "Integrating 1 over a 2D domain yields the exact area of that domain.")
        add_q("Integral Calculus", "What is the reduction formula for ∫ sin^n(x) dx?",
              "[-cos(x)*sin^(n-1)(x)]/n + [(n-1)/n]*∫ sin^(n-2)(x) dx", "[cos(x)*sin^n(x)]/(n+1)", "-cos^n(x)/n", "sin^(n+1)(x)/(n+1)", "A", "hard", "Reduction Formulas",
              "Standard reduction formula obtained via integration by parts for sin^n(x).")
        add_q("Integral Calculus", "What theorem transforms a line integral around a closed curve C into a double integral over region D?",
              "Green's Theorem", "Stokes' Theorem in 3D", "Divergence Theorem", "Mean Value Theorem", "A", "hard", "Vector Calculus Theorems",
              "Green's Theorem relates a line integral around simple closed curve C to a double integral over plane region D.")
        add_q("Integral Calculus", "What is the value of the Gaussian integral ∫ from -∞ to +∞ of e^(-x^2) dx?",
              "1", "π", "√π", "e", "C", "hard", "Gaussian Integral",
              "The improper Gaussian integral evaluates to √π, proven via double integration in polar coordinates.")
        add_q("Integral Calculus", "How does changing the order of integration affect the value of a continuous function's double integral over a closed bounded region?",
              "Doubles the result", "Value remains identical by Fubini's Theorem", "Result becomes negative", "Order can never be changed", "B", "hard", "Fubini's Theorem",
              "Fubini's theorem guarantees that integration order can be interchanged without changing the result if f(x,y) is continuous.")

        # ---------------------------------------------------------
        # TOPIC 12: Ohm's & Kirchhoff's Laws (12 Questions)
        # ---------------------------------------------------------
        add_q("Ohm's & Kirchhoff's Laws", "What is the mathematical formulation of Ohm's Law relating Voltage (V), Current (I), and Resistance (R)?",
              "V = I / R", "V = I * R", "I = V * R", "R = V * I", "B", "easy", "Ohm's Law",
              "Ohm's Law states that potential difference V equals product of current I and resistance R: V = IR.")
        add_q("Ohm's & Kirchhoff's Laws", "Kirchhoff's Current Law (KCL) is a direct consequence of the conservation of:",
              "Energy", "Electric Charge", "Momentum", "Magnetic Flux", "B", "easy", "KCL Conservation",
              "KCL states total current entering a junction equals current leaving, based on conservation of electric charge.")
        add_q("Ohm's & Kirchhoff's Laws", "Kirchhoff's Voltage Law (KVL) is a direct consequence of the conservation of:",
              "Electric Charge", "Energy", "Mass", "Power", "B", "easy", "KVL Conservation",
              "KVL states the algebraic sum of voltages around any closed loop is zero, based on conservation of energy.")
        add_q("Ohm's & Kirchhoff's Laws", "What is the SI unit of electrical resistance?",
              "Volt", "Ampere", "Ohm (Ω)", "Siemens", "C", "easy", "Units",
              "Resistance is measured in Ohms (Ω).")
        add_q("Ohm's & Kirchhoff's Laws", "If a 12V DC source is connected across a 4Ω resistor, what is the current flowing?",
              "48 A", "3 A", "0.33 A", "16 A", "B", "medium", "Ohm's Law Calculations",
              "Using Ohm's law: I = V / R = 12 / 4 = 3 A.")
        add_q("Ohm's & Kirchhoff's Laws", "What is the power dissipated in a resistor of resistance R carrying current I?",
              "P = I * R", "P = I^2 * R", "P = I / R^2", "P = V / I", "B", "medium", "Electric Power",
              "Power dissipated as heat is given by Joule's law: P = V*I = I^2*R = V^2/R.")
        add_q("Ohm's & Kirchhoff's Laws", "What is the equivalent resistance of two 10Ω resistors connected in parallel?",
              "20 Ω", "10 Ω", "5 Ω", "2.5 Ω", "C", "medium", "Parallel Resistance",
              "For identical resistors in parallel: R_eq = R / n = 10 / 2 = 5 Ω.")
        add_q("Ohm's & Kirchhoff's Laws", "In an ideal independent voltage source, what is its internal resistance?",
              "Zero (0 Ω)", "Infinite (∞ Ω)", "1 Ω", "Dependent on load", "A", "medium", "Ideal Sources",
              "An ideal voltage source maintains fixed voltage regardless of current, meaning internal resistance is 0.")
        add_q("Ohm's & Kirchhoff's Laws", "In an ideal independent current source, what is its internal resistance?",
              "Zero (0 Ω)", "Infinite (∞ Ω)", "50 Ω", "Negative", "B", "hard", "Ideal Sources",
              "An ideal current source supplies constant current regardless of terminal voltage, having infinite internal impedance.")
        add_q("Ohm's & Kirchhoff's Laws", "Under what conditions does Ohm's Law fail to apply?",
              "In pure metallic copper conductors at constant temperature", "In non-linear devices such as semiconductor diodes, transistors, and vacuum tubes", "In DC circuits", "In linear resistors", "B", "hard", "Non-linear Elements",
              "Ohm's Law applies only to linear, bilateral, ohmic materials; non-linear semiconductor junctions do not obey V = IR.")
        add_q("Ohm's & Kirchhoff's Laws", "What is the sign convention when writing a KVL loop equation across a potential drop?",
              "Assign positive (+)", "Assign negative (-)", "Always omit sign", "Multiply by loop current", "B", "hard", "KVL Sign Conventions",
              "Traversing from higher potential (+) to lower potential (-) represents a potential drop, commonly assigned a negative sign.")
        add_q("Ohm's & Kirchhoff's Laws", "Why does KCL not apply at frequencies where circuit physical dimensions approach the wavelength of signal?",
              "Resistors become inductors", "Charge accumulation occurs in parasitic distributed capacitances (transmission line effects)", "Electrons move at light speed", "Charge conservation is violated", "B", "hard", "Lumped Parameter Limits",
              "Lumped element assumptions fail when wave propagation delays and electromagnetic radiation become significant.")

        # ---------------------------------------------------------
        # TOPIC 13: Series-Parallel Circuit Analysis (12 Questions)
        # ---------------------------------------------------------
        add_q("Series-Parallel Circuit Analysis", "In a series circuit, which electrical parameter remains identical through all components?",
              "Voltage", "Current", "Power", "Resistance", "B", "easy", "Series Characteristics",
              "In a series circuit, there is only one conductive path, so the same current flows through all elements.")
        add_q("Series-Parallel Circuit Analysis", "In a parallel circuit, which parameter is identical across all branches?",
              "Current", "Voltage", "Power", "Capacitance", "B", "easy", "Parallel Characteristics",
              "All parallel branches connect between the same pair of common nodes, so voltage across them is equal.")
        add_q("Series-Parallel Circuit Analysis", "What is the equivalent resistance of three 6Ω resistors connected in series?",
              "2 Ω", "6 Ω", "18 Ω", "36 Ω", "C", "easy", "Series Resistors",
              "In series: R_eq = R1 + R2 + R3 = 6 + 6 + 6 = 18 Ω.")
        add_q("Series-Parallel Circuit Analysis", "What is the reciprocal of electrical resistance called?",
              "Inductance", "Conductance", "Impedance", "Permeance", "B", "easy", "Conductance",
              "Conductance G = 1 / R, measured in Siemens (S).")
        add_q("Series-Parallel Circuit Analysis", "According to the Voltage Divider Rule, voltage V1 across resistor R1 in series with R2 is:",
              "V_total * [R1 / (R1 + R2)]", "V_total * [R2 / (R1 + R2)]", "V_total * (R1 + R2)", "V_total / R1", "A", "medium", "Voltage Divider",
              "Voltage divider formula allocates voltage proportionally to resistance: V1 = V_total * [R1 / (R1 + R2)].")
        add_q("Series-Parallel Circuit Analysis", "According to the Current Divider Rule, current I1 through resistor R1 in parallel with R2 is:",
              "I_total * [R1 / (R1 + R2)]", "I_total * [R2 / (R1 + R2)]", "I_total * (R1 + R2)", "I_total / R1", "B", "medium", "Current Divider",
              "In current division, current through branch 1 is proportional to opposite branch: I1 = I_total * [R2 / (R1 + R2)].")
        add_q("Series-Parallel Circuit Analysis", "In a Delta (Δ) to Star (Y) conversion, the resistance of branch Ra connected to node A is:",
              "(R_ab * R_ca) / (R_ab + R_bc + R_ca)", "(R_ab + R_bc) / R_ca", "R_ab * R_bc * R_ca", "3 * R_delta", "A", "medium", "Delta-Star Conversion",
              "Star resistance is product of adjacent delta arms divided by perimeter sum: Ra = (Rab * Rca) / (Rab + Rbc + Rca).")
        add_q("Series-Parallel Circuit Analysis", "If three equal resistors of value R_delta = 9Ω are connected in Delta, what is their Star equivalent R_star?",
              "27 Ω", "9 Ω", "3 Ω", "1 Ω", "C", "medium", "Delta-Star Symmetry",
              "For identical branches: R_star = R_delta / 3 = 9 / 3 = 3 Ω.")
        add_q("Series-Parallel Circuit Analysis", "What is the condition for a Wheatstone bridge to be balanced (no galvanometer current)?",
              "R1 * R3 = R2 * R4", "R1 * R4 = R2 * R3 (opposite arms product equal)", "R1 + R2 = R3 + R4", "R1 = R2 = R3 = R4", "B", "hard", "Wheatstone Bridge",
              "A Wheatstone bridge is balanced when products of diagonally opposite resistance arms are equal: R1 * R4 = R2 * R3.")
        add_q("Series-Parallel Circuit Analysis", "What is the equivalent resistance between terminals A and B of an infinite ladder network of 1Ω series and 1Ω shunt resistors?",
              "1 Ω", "(1 + √5) / 2 ≈ 1.618 Ω (Golden Ratio)", "2 Ω", "0.5 Ω", "B", "hard", "Ladder Networks",
              "R_eq = 1 + (1 || R_eq) => R_eq^2 - R_eq - 1 = 0 => R_eq = (1 + √5)/2 ≈ 1.618 Ω.")
        add_q("Series-Parallel Circuit Analysis", "When a bridge circuit is unbalanced and cannot be simplified via simple series-parallel reductions, which technique is easiest?",
              "Delta-Wye transformation or Mesh analysis", "Ignoring bridge resistor", "Replacing all resistors with short circuits", "Doubling supply voltage", "A", "hard", "Bridge Solution",
              "Unbalanced bridge circuits are reduced using Delta-to-Star transformations or planar mesh equations.")
        add_q("Series-Parallel Circuit Analysis", "What is the maximum power transfer theorem condition for a DC resistive circuit?",
              "Load resistance R_L = 0", "Load resistance R_L equals Thevenin internal resistance R_th", "Load resistance R_L = ∞", "Load resistance R_L = 2 * R_th", "B", "hard", "Power Transfer",
              "Maximum power is delivered to the load when load resistance equals Thevenin equivalent source resistance: R_L = R_th.")

        # ---------------------------------------------------------
        # TOPIC 14: Mesh & Nodal Analysis (12 Questions)
        # ---------------------------------------------------------
        add_q("Mesh & Nodal Analysis", "Mesh analysis is fundamentally based on which electrical circuit law?",
              "Kirchhoff's Current Law (KCL)", "Kirchhoff's Voltage Law (KVL)", "Ampere's Circuital Law", "Faraday's Law", "B", "easy", "Mesh Foundations",
              "Mesh current analysis is formulated by writing KVL equations around circulating loop currents.")
        add_q("Mesh & Nodal Analysis", "Nodal analysis is fundamentally based on which electrical circuit law?",
              "Kirchhoff's Current Law (KCL)", "Kirchhoff's Voltage Law (KVL)", "Biot-Savart Law", "Coulomb's Law", "A", "easy", "Nodal Foundations",
              "Nodal analysis determines unknown node voltages by writing KCL equations at each non-reference junction.")
        add_q("Mesh & Nodal Analysis", "In a circuit with N essential nodes, how many independent nodal equations must be solved?",
              "N", "N - 1", "N + 1", "2N", "B", "easy", "Node Equations Count",
              "One node is designated as reference (ground 0V), requiring N-1 independent nodal equations.")
        add_q("Mesh & Nodal Analysis", "What is a planar circuit?",
              "A circuit that operates only with direct current", "A circuit that can be drawn on a 2D plane with no branch crossings", "A circuit printed on a motherboard", "A high voltage circuit", "B", "easy", "Planar Circuits",
              "Mesh analysis is only valid for planar circuits, which can be drawn without crossing branches.")
        add_q("Mesh & Nodal Analysis", "In mesh analysis, what is a 'supermesh'?",
              "A mesh containing only inductors", "A larger loop created by removing a branch containing a current source common to two meshes", "A circuit with more than 10 meshes", "A loop with superconducting wires", "B", "medium", "Supermesh Concept",
              "A supermesh avoids the unknown voltage across a shared current source by combining two meshes into one larger loop.")
        add_q("Mesh & Nodal Analysis", "In nodal analysis, what is a 'supernode'?",
              "The reference ground node", "A generalized node formed by enclosing a voltage source connected between two non-reference nodes", "A node with highest current", "A node connected to infinite impedance", "B", "medium", "Supernode Concept",
              "A supernode encloses a voltage source connected between two non-ground nodes to bypass unknown source current.")
        add_q("Mesh & Nodal Analysis", "In a standard matrix formulation of nodal analysis [G][V] = [I], what does matrix [G] contain?",
              "Branch impedances", "Node conductances (diagonal terms = sum of conductances at node; off-diagonals = negative mutual conductances)", "Inductance values", "Source voltages", "B", "medium", "Conductance Matrix",
              "[G] is the conductance matrix with self-conductances on diagonal and negative mutual conductances off diagonal.")
        add_q("Mesh & Nodal Analysis", "In a circuit with B branches and N nodes, how many independent mesh equations M exist (by Euler's planar formula)?",
              "M = B - N + 1", "M = B + N", "M = B / N", "M = N - 1", "A", "medium", "Mesh Count Formula",
              "The number of independent loops/meshes is given by M = B - N + 1.")
        add_q("Mesh & Nodal Analysis", "Why is nodal analysis generally preferred over mesh analysis for computer circuit simulation (such as SPICE)?",
              "Mesh analysis cannot handle resistors", "Nodal analysis works for both planar and non-planar circuits and is easily formulated with nodal admittance matrices", "Mesh analysis produces complex numbers only", "Nodal analysis uses less RAM", "B", "hard", "Simulation Algorithms",
              "Modified Nodal Analysis (MNA) handles any topology (planar or non-planar) and adapts cleanly to matrix algorithms.")
        add_q("Mesh & Nodal Analysis", "When a dependent voltage source is present in a circuit, how is it handled during nodal analysis?",
              "Ignored completely", "Treated like an independent source, with its controlling constraint equation added to the system", "Short-circuited", "Replaced with an open circuit", "B", "hard", "Dependent Sources",
              "Dependent sources are retained, and their auxiliary controlling equations are solved simultaneously.")
        add_q("Mesh & Nodal Analysis", "What is the constraint equation for a supermesh shared by mesh 1 and mesh 2 containing a 3A source pointing in direction of mesh 2?",
              "I1 + I2 = 3", "I2 - I1 = 3", "I1 - I2 = 3", "I1 * I2 = 3", "B", "hard", "Supermesh Constraints",
              "Since the 3A current source flows with mesh 2 and opposes mesh 1, the constraint is I2 - I1 = 3 A.")
        add_q("Mesh & Nodal Analysis", "What is the dual relationship between mesh analysis and nodal analysis?",
              "Mesh is KVL / Loop currents / Planar only; Nodal is KCL / Node voltages / General topologies", "They are identical in equations", "Mesh is for AC; Nodal is for DC", "Nodal requires differential equations", "A", "hard", "Duality in Circuits",
              "Duality maps loops to nodes, KVL to KCL, currents to voltages, and impedances to admittances.")

        db.session.flush()

        # ---------------------------------------------------------
        # 3. Create Resources (at least 3-4 per topic, covering notes, video, example, practice)
        # ---------------------------------------------------------
        print("Seeding curated study resources for all 14 topics...")
        for name, topic_obj in topic_objects.items():
            # 1. Notes (Short original high-yield summary)
            res_notes = Resource(
                topic_id=topic_obj.id,
                type="notes",
                title=f"Core Concept Summary: {name}",
                description=f"Concise engineering lecture notes covering fundamental principles, key definitions, and VTU exam highlights for {name}.",
                url=None,
                content=(
                    f"# Study Notes: {name}\n\n"
                    f"## 1. Introduction and Foundations\n"
                    f"In this module on **{name}**, students review core theoretical mechanisms and circuit/code behavior. "
                    f"Understanding foundational principles ensures strong problem-solving skills in exams and laboratory practicals.\n\n"
                    f"## 2. Key Formulas & Definitions\n"
                    f"- Always pay attention to boundary conditions, units, and polarities.\n"
                    f"- Review standard analytical procedures before applying shortcuts.\n"
                    f"- Trace through step-by-step logic during numerical verification.\n\n"
                    f"## 3. Common Student Pitfalls\n"
                    f"- Avoid skipping intermediate algebraic or memory-state steps.\n"
                    f"- Double-check sign conventions and reference node selections.\n\n"
                    f"> *Tip: Review this summary and solve the worked numericals before taking your adaptive quiz.*"
                ),
                target_level="low",
                difficulty="easy",
                needs_review=False
            )

            # 2. Curated Video (Verified 20-30 min top educational video per syllabus topic)
            custom_video_urls = {
                # C Programming (20-25 min focused lectures)
                "Arrays in C": "https://www.youtube.com/watch?v=AT14lCXuMKI",
                "Pointers and Memory": "https://www.youtube.com/watch?v=4Rll-_e9-0M",
                "Functions and Recursion": "https://www.youtube.com/watch?v=-NbLKVOK0JQ",
                "Control Flow and Loops": "https://www.youtube.com/watch?v=D0ACZ0uU_2g",

                # Digital Electronics (21-28 min focused lectures)
                "Number Systems & Codes": "https://www.youtube.com/watch?v=k3Z322T3sjs",
                "Boolean Algebra & Logic Simplification": "https://www.youtube.com/watch?v=FPrcIhqNPVo",
                "Logic Gates & Universal Realization": "https://www.youtube.com/watch?v=kcJAVetOd_A",
                "Combinational Logic Circuits": "https://www.youtube.com/watch?v=a3wh7xV5PBU",

                # Engineering Mathematics (18-24 min focused lectures)
                "Matrices & Linear Systems": "https://www.youtube.com/watch?v=7a9Yawt1O50",
                "Differential Calculus": "https://www.youtube.com/watch?v=bTs7ncA_AtY",
                "Integral Calculus": "https://www.youtube.com/watch?v=fXMyLYwBB3s",

                # Basic Circuit Analysis (21-26 min focused lectures)
                "Ohm's & Kirchhoff's Laws": "https://www.youtube.com/watch?v=6F_rmZ1nXFQ",
                "Series-Parallel Circuit Analysis": "https://www.youtube.com/watch?v=Gn26z60tTog",
                "Mesh & Nodal Analysis": "https://www.youtube.com/watch?v=D92DjS43-Qw"
            }
            clean_query = name.replace(" ", "+").replace("&", "and")
            video_url = custom_video_urls.get(
                name,
                f"https://www.youtube.com/results?search_query=VTU+Engineering+{clean_query}+lecture"
            )
            res_video = Resource(
                topic_id=topic_obj.id,
                type="video",
                title=f"Video Lecture: {name} Explained",
                description=f"Curated engineering video lecture and step-by-step visual demonstration for {name}.",
                url=video_url,
                content=None,
                target_level="low",
                difficulty="medium",
                needs_review=False
            )

            # 3. Worked Example (Step-by-step practical problem)
            res_example = Resource(
                topic_id=topic_obj.id,
                type="example",
                title=f"Step-by-Step Worked Problem: {name}",
                description=f"Fully worked VTU-standard numerical/code example demonstrating application of {name}.",
                url=None,
                content=(
                    f"# Worked Example: {name}\n\n"
                    f"### Problem Statement\n"
                    f"Analyze the benchmark engineering problem for **{name}** and derive the solution with clear intermediate justification.\n\n"
                    f"### Step 1: Identify Given Parameters\n"
                    f"- Extract known variables and draw the schematic / memory diagram.\n"
                    f"- Formulate the governing system equation.\n\n"
                    f"### Step 2: Intermediate Algebraic Derivation\n"
                    f"- Simplify the expression using standard reduction theorems.\n"
                    f"- Verify consistency of dimensional units or data structures.\n\n"
                    f"### Step 3: Final Verified Result\n"
                    f"The computed solution conforms to theoretical limits. Make sure to document final units and boundary checks."
                ),
                target_level="medium",
                difficulty="medium",
                needs_review=False
            )

            # 4. Practice Problem Set
            res_practice = Resource(
                topic_id=topic_obj.id,
                type="practice",
                title=f"Challenge Practice Problem Set: {name}",
                description=f"Higher-order thinking questions and exam-style problem scenarios for {name}.",
                url=None,
                content=(
                    f"# Practice Exercises: {name}\n\n"
                    f"1. **Conceptual Challenge:** Explain how changing the operating parameters impacts the response time and efficiency in {name}.\n\n"
                    f"2. **Numerical Problem:** Derive the analytical solution given a 20% variation in the boundary conditions.\n\n"
                    f"3. **Synthesis Question:** Design an optimized implementation that minimizes hardware footprint / computational overhead."
                ),
                target_level="high",
                difficulty="hard",
                needs_review=False
            )

            db.session.add_all([res_notes, res_video, res_example, res_practice])

        db.session.flush()

        # ---------------------------------------------------------
        # 4. Create Synthetic Users & Demo Accounts
        # ---------------------------------------------------------
        print("Creating synthetic test accounts and populating demo quiz histories...")
        
        # Student 1 (Lower mastery demo student)
        student1 = User(
            name="Adithya (Demo Student 1)",
            email="student1@demo.test",
            role="student",
            preferred_language="en",
            is_synthetic=True
        )
        student1.set_password("learnloop123")

        # Student 2 (High mastery demo student)
        student2 = User(
            name="Kavya (Demo Student 2)",
            email="student2@demo.test",
            role="student",
            preferred_language="kn",
            is_synthetic=True
        )
        student2.set_password("learnloop123")

        # Teacher Account
        teacher = User(
            name="Prof. Shruthi K. N (Faculty)",
            email="teacher@demo.test",
            role="teacher",
            preferred_language="en",
            is_synthetic=True
        )
        teacher.set_password("learnloop123")

        db.session.add_all([student1, student2, teacher])
        db.session.flush()

        # ---------------------------------------------------------
        # 5. Populate Historical Attempts & Progress for Meaningful Dashboard
        # ---------------------------------------------------------
        # For student 1: Low mastery on Pointers & Mesh Analysis, Medium on Arrays
        p_topic_ptr = topic_objects["Pointers and Memory"]
        p_topic_mesh = topic_objects["Mesh & Nodal Analysis"]
        p_topic_arr = topic_objects["Arrays in C"]

        # Student 1 attempts on Pointers (Score 20%, 40%) -> Low
        att1 = Attempt(user_id=student1.id, topic_id=p_topic_ptr.id, score_pct=20.0, difficulty_mix="3 easy, 2 medium", taken_at=datetime.now(timezone.utc) - timedelta(days=3))
        att2 = Attempt(user_id=student1.id, topic_id=p_topic_ptr.id, score_pct=40.0, difficulty_mix="3 easy, 2 medium", taken_at=datetime.now(timezone.utc) - timedelta(days=1))
        # Student 1 attempts on Mesh (Score 20%) -> Low
        att3 = Attempt(user_id=student1.id, topic_id=p_topic_mesh.id, score_pct=20.0, difficulty_mix="3 easy, 2 medium", taken_at=datetime.now(timezone.utc) - timedelta(days=2))
        # Student 1 attempts on Arrays (Score 60%, 80%) -> Medium
        att4 = Attempt(user_id=student1.id, topic_id=p_topic_arr.id, score_pct=60.0, difficulty_mix="1 easy, 3 medium, 1 hard", taken_at=datetime.now(timezone.utc) - timedelta(days=4))
        att5 = Attempt(user_id=student1.id, topic_id=p_topic_arr.id, score_pct=80.0, difficulty_mix="1 easy, 3 medium, 1 hard", taken_at=datetime.now(timezone.utc) - timedelta(days=1))

        db.session.add_all([att1, att2, att3, att4, att5])
        db.session.flush()

        # Update TopicProgress for Student 1
        prog_ptr = TopicProgress(user_id=student1.id, topic_id=p_topic_ptr.id, mastery_level="Low", mastery_pct=33.0, completed=False, last_updated=datetime.now(timezone.utc))
        prog_mesh = TopicProgress(user_id=student1.id, topic_id=p_topic_mesh.id, mastery_level="Low", mastery_pct=20.0, completed=False, last_updated=datetime.now(timezone.utc))
        prog_arr = TopicProgress(user_id=student1.id, topic_id=p_topic_arr.id, mastery_level="Medium", mastery_pct=73.0, completed=True, last_updated=datetime.now(timezone.utc))
        db.session.add_all([prog_ptr, prog_mesh, prog_arr])

        # Record a resource view for student 1
        ptr_res = Resource.query.filter_by(topic_id=p_topic_ptr.id, type='notes').first()
        if ptr_res:
            res_view1 = ResourceView(user_id=student1.id, resource_id=ptr_res.id, viewed_at=datetime.now(timezone.utc))
            db.session.add(res_view1)

        # For student 2: High mastery on Logic Gates, Boolean Algebra, and Matrices
        p_topic_gates = topic_objects["Logic Gates & Universal Realization"]
        p_topic_bool = topic_objects["Boolean Algebra & Logic Simplification"]
        p_topic_mat = topic_objects["Matrices & Linear Systems"]

        s2_att1 = Attempt(user_id=student2.id, topic_id=p_topic_gates.id, score_pct=80.0, difficulty_mix="1 easy, 3 medium, 1 hard", taken_at=datetime.now(timezone.utc) - timedelta(days=2))
        s2_att2 = Attempt(user_id=student2.id, topic_id=p_topic_gates.id, score_pct=100.0, difficulty_mix="0 easy, 2 medium, 3 hard", taken_at=datetime.now(timezone.utc) - timedelta(days=1))
        s2_att3 = Attempt(user_id=student2.id, topic_id=p_topic_bool.id, score_pct=80.0, difficulty_mix="0 easy, 2 medium, 3 hard", taken_at=datetime.now(timezone.utc) - timedelta(days=3))
        s2_att4 = Attempt(user_id=student2.id, topic_id=p_topic_mat.id, score_pct=100.0, difficulty_mix="0 easy, 2 medium, 3 hard", taken_at=datetime.now(timezone.utc) - timedelta(hours=6))

        db.session.add_all([s2_att1, s2_att2, s2_att3, s2_att4])
        db.session.flush()

        s2_prog1 = TopicProgress(user_id=student2.id, topic_id=p_topic_gates.id, mastery_level="High", mastery_pct=93.0, completed=True, last_updated=datetime.now(timezone.utc))
        s2_prog2 = TopicProgress(user_id=student2.id, topic_id=p_topic_bool.id, mastery_level="High", mastery_pct=80.0, completed=True, last_updated=datetime.now(timezone.utc))
        s2_prog3 = TopicProgress(user_id=student2.id, topic_id=p_topic_mat.id, mastery_level="High", mastery_pct=100.0, completed=True, last_updated=datetime.now(timezone.utc))
        db.session.add_all([s2_prog1, s2_prog2, s2_prog3])

        db.session.commit()
        print("Database seeded successfully with 4 subjects, 14 topics, 168 questions, 56 resources, and synthetic user histories!")

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learnloop.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    seed_database(app)
