import subprocess
from logic import decide_career_category

# ---- Student Input (temporary, will come from form later) ----
maths = 85
science = 78
english = 70
hobbies = ["Coding", "Football"]

# ---- Step 1: Rule-based analysis ----
analysis = decide_career_category(maths, science, english, hobbies)

# ---- Step 2: Build AI prompt ----
prompt = f"""
You are a professional career guidance counselor.

Student Analysis:
- Career Category: {analysis['career_category']}
- Strengths: {', '.join(analysis['strengths'])}
- Maths Level: {analysis['maths_level']}
- Science Level: {analysis['science_level']}
- English Level: {analysis['english_level']}
- Hobbies: {', '.join(hobbies)}

Task:
Explain suitable career options for this student.
Keep the explanation clear, practical, and student-friendly.
"""

# ---- Step 3: Call Ollama ----
result = subprocess.run(
    ["ollama", "run", "llama3"],
    input=prompt,
    text=True,
    capture_output=True,
    encoding="utf-8",
    errors="ignore"
)

# ---- Output ----
print("\n=== AI Career Guidance ===\n")
print(result.stdout)

