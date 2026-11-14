import tkinter as tk


# =========================
# RESUME ANALYZER FUNCTION
# =========================
def analyze():
    # Resume text'i al
    text = resume.get("1.0", tk.END).lower()

    # Aranacak skills
    skills = [
        "python",
        "javascript",
        "java",
        "c++",
        "html",
        "css",
        "react",
        "node.js",
        "sql",
        "mysql",
        "mongodb",
        "git",
        "github",
        "docker",
        "aws",
        "flask",
        "django",
        "fastapi",
        "typescript",
        "php"
    ]

    # Resume içerisinde bulunan skill'leri bul
    found = [skill for skill in skills if skill in text]

    # Sonucu göster
    result.config(
        text=f"🟢 Skills Found: {len(found)}\n"
             f"🔹 {', '.join(found) if found else 'None'}"
    )


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title("AI Resume Analyzer")
root.geometry("500x450")
root.resizable(False, False)


# =========================
# TITLE
# =========================

title = tk.Label(
    root,
    text="🤖 AI Resume Analyzer",
    font=("Arial", 22, "bold")
)

title.pack(pady=20)


# =========================
# RESUME TEXT BOX
# =========================

resume = tk.Text(
    root,
    height=12,
    width=50
)

resume.pack()


# =========================
# ANALYZE BUTTON
# =========================

analyze_button = tk.Button(
    root,
    text="Analyze Resume",
    command=analyze,
    font=("Arial", 13, "bold")
)

analyze_button.pack(pady=15)


# =========================
# RESULT LABEL
# =========================

result = tk.Label(
    root,
    text="Paste your resume above.",
    font=("Arial", 13),
    wraplength=450,
    justify="left"
)

result.pack(pady=10)


# =========================
# START PROGRAM
# =========================

root.mainloop()