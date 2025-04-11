import tkinter as tk
from tkinter import ttk, messagebox
import random
from PIL import Image, ImageTk

# Define grammar
grammar = {
    "S": [["NP", "VP"]],
    "NP": [["Det", "Noun"], ["Noun"]],
    "VP": [["Verb", "NP"], ["Verb"]],
    "Det": [["the"], ["a"],["an"]],
    "Noun": [["dog"], ["cat"]],
    "Verb": [["chases"], ["eats"]]
}

# Function to compute FIRST sets
def compute_first():
    first = {key: set() for key in grammar}
    
    def first_of(symbol):
        if symbol not in grammar:
            return {symbol}
        if first[symbol]:
            return first[symbol]
        for production in grammar[symbol]:
            for prod_symbol in production:
                first[symbol] |= first_of(prod_symbol)
                if prod_symbol not in grammar:
                    break
        return first[symbol]
    
    for non_terminal in grammar:
        first_of(non_terminal)
    
    return {key: list(value) for key, value in first.items()}

# Function to tokenize input sentence
def tokenize(sentence):
    return sentence.lower().split()

# Recursive descent parsing function
def parse(tokens):
    def S():
        saved = tokens[:]
        if NP() and VP():
            return True
        tokens[:] = saved[:]
        return False

    def NP():
        saved = tokens[:]
        if Det() and Noun():
            return True
        tokens[:] = saved[:]
        if Noun():
            return True
        tokens[:] = saved[:]
        return False

    def VP():
        saved = tokens[:]
        if Verb() and NP():
            return True
        tokens[:] = saved[:]
        if Verb():
            return True
        tokens[:] = saved[:]
        return False

    def Det():
        if tokens and tokens[0] in ["the", "a"]:
            tokens.pop(0)
            return True
        return False

    def Noun():
        if tokens and tokens[0] in ["dog", "cat"]:
            tokens.pop(0)
            return True
        return False

    def Verb():
        if tokens and tokens[0] in ["chases", "eats"]:
            tokens.pop(0)
            return True
        return False

    return S()

# Function to check the grammar of the entered sentence
def check_grammar():
    sentence = entry.get()
    tokens = tokenize(sentence)
    
    first_sets = compute_first()
    first_output = "\n".join([f"{key}: {', '.join(value)}" for key, value in first_sets.items()])
    messagebox.showinfo("First Sets", first_output)
    
    tokens_copy = tokens[:]
    if parse(tokens_copy) and not tokens_copy:
        messagebox.showinfo("Result", "The sentence is grammatically correct! 🎉")
    else:
        messagebox.showerror("Result", "The sentence is NOT grammatically correct! ❌")

# Function to change background color dynamically
def change_color():
    colors = ["#FF5733", "#33FF57", "#3357FF", "#F4FF33", "#FF33A8", "#33FFF9", "#FFA500", "#800080"]
    root.configure(bg=random.choice(colors))
    root.after(500, change_color)  

# GUI Setup
root = tk.Tk()
root.title("🌟 Fun Grammar Checker for Kids 🌟")
root.attributes('-fullscreen', True)
root.configure(bg="#000000")

# Start changing colors immediately
change_color()

frame = ttk.Frame(root, padding=20)
frame.pack(fill=tk.BOTH, expand=True)

# Load cartoon image
try:
    cartoon_img = Image.open("download (1).png")  
    cartoon_img = cartoon_img.resize((200, 200))
    cartoon_photo = ImageTk.PhotoImage(cartoon_img)

    cartoon_label = tk.Label(frame, image=cartoon_photo, bg="#000000")
    cartoon_label.pack(pady=10)
except Exception as e:
    print("Error loading cartoon image:", e)

# Label for text input
label = ttk.Label(frame, text="✏️ Enter a sentence:", font=("Comic Sans MS", 18), background="#000000", foreground="white")
label.pack(pady=10)

# Entry field
entry = ttk.Entry(frame, width=50, font=("Comic Sans MS", 16))
entry.pack(pady=10)

# Style for buttons
style = ttk.Style()
style.configure("TButton", font=("Comic Sans MS", 16), padding=10, background="#000000")

# Function to create hover effect
def on_enter(e):
    e.widget.configure(style="Hover.TButton")

def on_leave(e):
    e.widget.configure(style="TButton")

# Hover button style (lightning effect)
style.configure("Hover.TButton", font=("Comic Sans MS", 16), padding=10, background="yellow", foreground="black")

# Check Grammar button
check_button = ttk.Button(frame, text="✅ Check Grammar", command=check_grammar, style="TButton")
check_button.pack(pady=10)
check_button.bind("<Enter>", on_enter)  # Change on hover
check_button.bind("<Leave>", on_leave)  # Revert when not hovering

# Exit button
exit_button = ttk.Button(frame, text="❌ Exit", command=root.quit, style="TButton")
exit_button.pack(pady=10)
exit_button.bind("<Enter>", on_enter)  # Change on hover
exit_button.bind("<Leave>", on_leave)  # Revert when not hovering

root.mainloop()




