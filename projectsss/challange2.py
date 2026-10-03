import tkinter as tk
from tkinter import messagebox
import requests


def translate_word():
    text = entry.get().strip()

    if not text:
        messagebox.showwarning("Warning", "Please enter a word!")
        return

    url = "https://api.mymemory.translated.net/get"

    params = {
        "q": text,
        "langpair": "en|de"
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            translation = data["responseData"]["translatedText"]

            result_label.config(
                text=f"German: {translation}"
            )

        else:
            result_label.config(
                text="Translation failed."
            )

    except requests.exceptions.RequestException:
        messagebox.showerror(
            "Error",
            "Could not connect to the internet."
        )


# =========================
# GUI
# =========================

window = tk.Tk()

window.title("German Translator")
window.geometry("500x350")
window.resizable(False, False)


title_label = tk.Label(
    window,
    text="🇩🇪 German Translator",
    font=("Arial", 22, "bold")
)

title_label.pack(pady=30)


instruction_label = tk.Label(
    window,
    text="Enter an English word:"
)

instruction_label.pack()


entry = tk.Entry(
    window,
    font=("Arial", 16),
    width=30
)

entry.pack(pady=15)


translate_button = tk.Button(
    window,
    text="Translate",
    font=("Arial", 14),
    command=translate_word
)

translate_button.pack(pady=10)


result_label = tk.Label(
    window,
    text="German: ---",
    font=("Arial", 18, "bold")
)

result_label.pack(pady=30)


window.mainloop()