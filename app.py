from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
from logic import decide_career_category
import mysql.connector




app = Flask(__name__)
app.secret_key = "career_planner_secret"

@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session["user"] = email
            session["history"] = []
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirmPassword"]

        if password != confirm:
            return render_template("signup.html", error="Passwords do not match")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password)
            )
            conn.commit()
        except:
            return render_template("signup.html", error="Email already exists")
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/history")
def history():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM career_history WHERE user_email=%s ORDER BY created_at DESC",
        (session["user"],)
    )

    history = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("history.html", history=history)


@app.route("/result", methods=["POST"])
def result():
    if "user" not in session:
        return redirect(url_for("login"))

    # Get student data from form
    maths = int(request.form["maths"])
    science = int(request.form["science"])
    english = int(request.form["english"])
    hobbies = request.form["hobbies"].split(",")

    # Analyze career category
    analysis = decide_career_category(maths, science, english, hobbies)

    # ✅ Save result to database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO career_history (user_email, career_category, strengths) VALUES (%s, %s, %s)",
        (
            session["user"],
            analysis["career_category"],
            ", ".join(analysis["strengths"])
        )
    )
    conn.commit()
    cursor.close()
    conn.close()

    # ✅ AI PROMPT
    prompt = f"""
You are a career guidance counselor.

Student Details:
Career Category: {analysis['career_category']}
Strengths: {', '.join(analysis['strengths'])}
Maths Level: {analysis['maths_level']}
Science Level: {analysis['science_level']}
English Level: {analysis['english_level']}
Hobbies: {', '.join(hobbies)}

Explain suitable career options in simple language also include fields based on hobbies.
"""

    ai_result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="ignore"
    )

    return render_template(
        "result.html",
        analysis=analysis,
        ai_output=ai_result.stdout
    )


# @app.route("/result", methods=["POST"])
# def result():
#     if "user" not in session:
#         return redirect(url_for("login"))

#     # Get student data from form
#     maths = int(request.form["maths"])
#     science = int(request.form["science"])
#     english = int(request.form["english"])
#     hobbies = request.form["hobbies"].split(",")

#     # Analyze career category
#     analysis = decide_career_category(maths, science, english, hobbies)
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#     "INSERT INTO career_history (user_email, career_category, strengths) VALUES (%s, %s, %s)",
#     (
#         session["user"],
#         analysis["career_category"],
#         ", ".join(analysis["strengths"])
#     )
# )

# conn.commit()
# cursor.close()
# conn.close()


#     # # Save result to session history
#     # session["history"].append({
#     #     "career": analysis["career_category"],
#     #     "strengths": analysis["strengths"]
#     # })
#     # session.modified = True

#     # 🔹 Create your prompt for AI
#     prompt = f"""
# You are a career guidance counselor.

# Student Details:
# Career Category: {analysis['career_category']}
# Strengths: {', '.join(analysis['strengths'])}
# Maths Level: {analysis['maths_level']}
# Science Level: {analysis['science_level']}
# English Level: {analysis['english_level']}
# Hobbies: {', '.join(hobbies)}

# Explain suitable career options in simple language.
# """

   

#     ai_result = subprocess.run(
#         ["ollama", "run", "llama3"],  # replace 'llama3' with your model name if different
#         input=prompt,
#         text=True,
#         capture_output=True,
#         encoding="utf-8",
#         errors="ignore"
#     )

#     # Pass analysis and AI output to template
#     return render_template(
#         "result.html",
#         analysis=analysis,
#         ai_output=ai_result.stdout  # this will show the AI description
#     )




@app.route("/logout")
def logout():
    session.clear()   # clears everything safely
    return redirect(url_for("home"))


# DB
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",        # keep empty if using XAMPP default
        database="career_planner"
    )


if __name__ == "__main__":
    app.run(debug=True)
