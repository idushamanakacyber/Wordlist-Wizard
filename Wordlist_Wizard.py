import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import itertools
import string
import os

def generate_wordlist(length, charset, filepath):
    combinations = [''.join(p) for p in itertools.product(charset, repeat=length)]

    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(filepath, 'w', encoding='utf-8') as f:
        for item in combinations:
            f.write(f"{item}\n")

    messagebox.showinfo("✅ Done!", f"Wordlist saved to:\n{filepath}\n\nTotal: {len(combinations):,} entries.")

def start_generation():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("❌ Invalid Input", "Please enter a valid positive integer.")
        return

    if length > 5:
        warning_label.config(text="⚠️ Warning: High lengths may freeze or crash slow devices.", fg="red")
    else:
        warning_label.config(text="")

    choice = charset_var.get()
    charset_options = {
        "🔢 Numbers [0-9]": ("numbers", string.digits),
        "🔡 Lowercase [a-z]": ("lowercase", string.ascii_lowercase),
        "🔠 Uppercase [A-Z]": ("uppercase", string.ascii_uppercase),
        "🔤 Mixed Case [a-zA-Z]": ("mixedcase", string.ascii_letters),
        "🔣 Alphanum [0-9a-zA-Z]": ("alphanum", string.ascii_letters + string.digits),
        "💥 All + Symbols": ("allsymbols", string.ascii_letters + string.digits + string.punctuation),
        "🎯 Ultimate Symbols": ("ultimate", string.ascii_letters + string.digits + string.punctuation +
            '±√∑∏∞∫≠≈≥≤∇∂∈∉∪∩∅∧∨∃∀∴∵∝∠⊥≡≅' +
            '←→↑↓↔↕⇐⇒⇑⇓↦↩↪⟶⟹⟸' +
            '~!@#$%^&*_+-=[]\\|;,./<>?' +
            '■□▢▲△▼▽●○◯◆◇★☆▷◁◬◭◮' +
            ' ' + '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾₊₋₌₍₎')
    }

    charset_label, charset = charset_options.get(choice, (None, None))
    if not charset:
        messagebox.showerror("⚠️ Error", "Please choose a valid character set.")
        return

    filename = f"{length}char_{charset_label}.txt"
    save_dir = filedialog.askdirectory(title="📁 Select Folder to Save Wordlist")
    if not save_dir:
        return

    full_path = os.path.join(save_dir, filename)
    generate_wordlist(length, charset, full_path)

# ====== GUI Setup ======
app = tk.Tk()
app.title("💻 Wordlist Wizard 🧙‍♂️ - by Idusha Manaka")
app.geometry("600x500")
app.resizable(False, False)

# Set dark theme colors
bg_color = "#000000"
fg_color = "#00FF00"
entry_bg = "#111111"
highlight_color = "#00FF00"

app.configure(bg=bg_color)

# ======= Layout Frame ========
frame = tk.Frame(app, bg=bg_color)
frame.pack(padx=20, pady=20, fill='both', expand=True)

def styled_label(text, **kwargs):
    fg = kwargs.pop("fg", fg_color)  # Use fg if provided, else default to fg_color
    return tk.Label(frame, text=text, fg=fg, bg=bg_color, font=("Consolas", 11, "bold"), **kwargs)
def styled_entry():
    return tk.Entry(frame, fg=fg_color, bg=entry_bg, insertbackground=fg_color,
                    highlightbackground=highlight_color, highlightcolor=highlight_color,
                    highlightthickness=1, font=("Consolas", 11))

def styled_button(text, command):
    return tk.Button(frame, text=text, command=command, fg=bg_color, bg=fg_color,
                     activebackground="#003300", font=("Consolas", 11, "bold"), relief='flat')

# Widgets
styled_label("🔢 Enter Password Length:").pack(anchor='w')
length_entry = styled_entry()
length_entry.pack(fill='x', pady=5)

styled_label("🎛️ Choose Character Set:").pack(anchor='w')
charset_var = tk.StringVar()
charset_combo = ttk.Combobox(frame, textvariable=charset_var, state="readonly", font=("Consolas", 10))
charset_combo['values'] = [
    "🔢 Numbers [0-9]",
    "🔡 Lowercase [a-z]",
    "🔠 Uppercase [A-Z]",
    "🔤 Mixed Case [a-zA-Z]",
    "🔣 Alphanum [0-9a-zA-Z]",
    "💥 All + Symbols",
    "🎯 Ultimate Symbols"
]
charset_combo.pack(fill='x', pady=5)

# Warning label
warning_label = styled_label("", fg="red")
warning_label.pack(anchor='center', pady=(5, 0))

styled_label("📂 File saved as: <length>char_<type>.txt").pack(anchor='center', pady=5)
styled_button("🚀 Generate Wordlist", start_generation).pack(pady=15)

# Extra static warning text
styled_label("⚠️ If you have a low-performance device,", fg="orange").pack()
styled_label("   do NOT enter a value greater than 5 for password length.", fg="orange").pack()

app.mainloop()
