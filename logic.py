def classify_marks(mark):
    if mark >= 75:
        return "High"
    elif mark >= 50:
        return "Medium"
    else:
        return "Low"


def decide_career_category(maths, science, english, hobbies):
    maths_level = classify_marks(maths)
    science_level = classify_marks(science)
    english_level = classify_marks(english)

    strengths = []

    if maths_level == "High":
        strengths.append("Mathematics")
    if science_level == "High":
        strengths.append("Science")
    if english_level == "High":
        strengths.append("Communication")

    # Career category rules
    if maths_level == "High" and science_level == "High":
        category = "Engineering / IT"
    elif science_level == "High" and "Biology" in hobbies:
        category = "Medical / Life Science"
    elif english_level == "High":
        category = "Arts / Humanities"
    elif maths_level == "Medium" and "Business" in hobbies:
        category = "Commerce / Management"
    else:
        category = "Skill-Based / General Careers"

    return {
        "maths_level": maths_level,
        "science_level": science_level,
        "english_level": english_level,
        "strengths": strengths,
        "career_category": category
    }


# ---------- TEST ----------
if __name__ == "__main__":
    student_result = decide_career_category(
        maths=85,
        science=78,
        english=70,
        hobbies=["Coding", "Football"]
    )

    print("Career Analysis Result:\n")
    for key, value in student_result.items():
        print(f"{key}: {value}")
        
        

