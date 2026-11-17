import urllib.request
import urllib.parse
import re
import json

topics = [
    ("Arrays in C", "Arrays in C programming tutorial Neso Academy"),
    ("Pointers and Memory", "Pointers in C C++ Full Course freeCodeCamp"),
    ("Functions and Recursion", "Functions and Recursion in C programming Neso Academy"),
    ("Control Flow and Loops", "Loops in C programming tutorial Bro Code"),
    ("Number Systems & Codes", "Number Systems Introduction Decimal Binary Octal Hexadecimal The Organic Chemistry Tutor"),
    ("Boolean Algebra & Logic Simplification", "Introduction to Karnaugh Maps Combinational Logic The Organic Chemistry Tutor"),
    ("Logic Gates & Universal Realization", "Logic Gates CrashCourse Computer Science"),
    ("Combinational Logic Circuits", "Introduction to Combinational Circuits Neso Academy"),
    ("Matrices & Linear Systems", "Linear transformations and matrices 3Blue1Brown"),
    ("Differential Calculus", "The essence of calculus 3Blue1Brown"),
    ("Integral Calculus", "Integration and the fundamental theorem of calculus 3Blue1Brown"),
    ("Ohm's & Kirchhoff's Laws", "How To Solve Any Resistors In Series and Parallel Combination Circuit Problems in Physics The Organic Chemistry Tutor"),
    ("Series-Parallel Circuit Analysis", "Series and Parallel Circuits The Organic Chemistry Tutor"),
    ("Mesh & Nodal Analysis", "Mesh Current Problems Electronics Circuit Analysis The Organic Chemistry Tutor")
]

results = {}

for topic_name, search_query in topics:
    print(f"Searching for: {topic_name} ('{search_query}')...")
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            # Find videoIds
            video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
            # Find unique video_ids maintaining order
            seen = set()
            unique_vids = []
            for vid in video_ids:
                if vid not in seen:
                    seen.add(vid)
                    unique_vids.append(vid)
            
            # Verify with oEmbed
            verified = False
            for vid in unique_vids[:5]:
                v_url = f"https://www.youtube.com/watch?v={vid}"
                oembed_url = f"https://www.youtube.com/oembed?url={urllib.parse.quote(v_url)}&format=json"
                o_req = urllib.request.Request(oembed_url, headers={"User-Agent": "Mozilla/5.0"})
                try:
                    with urllib.request.urlopen(o_req, timeout=5) as o_resp:
                        data = json.loads(o_resp.read().decode())
                        title = data.get("title", "")
                        author = data.get("author_name", "")
                        print(f"  [SUCCESS] {topic_name} -> {v_url} | {title} by {author}")
                        results[topic_name] = {
                            "url": v_url,
                            "title": title,
                            "author": author
                        }
                        verified = True
                        break
                except Exception as e:
                    continue
            if not verified:
                print(f"  [FAILED] Could not verify video for {topic_name}")
    except Exception as e:
        print(f"  [ERROR] {topic_name}: {e}")

print("\n--- SUMMARY DICT FOR seed.py ---")
print(json.dumps(results, indent=2))

