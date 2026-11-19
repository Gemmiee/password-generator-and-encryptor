import customtkinter as ctk
import random
import hashlib
import os
import sys
import tkinter as tk


def resource_path(relative):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)

ctk.set_appearance_mode("light")                                   # "dark", "light" or "system"
ctk.set_default_color_theme("blue")

app = ctk.CTk()                                                     # the window
app.title("Infinite password generator")
app.geometry("600x600")
app.configure(fg_color="#EEF3FF")                                 # window background color

# window/taskbar icon
if sys.platform.startswith("win"):
    app.iconbitmap(resource_path("icons/app.ico"))                  # also stops ctk from swapping in its own icon
else:
    app_icons = [tk.PhotoImage(file=resource_path(f"icons/icon_{s}.png")) for s in (16, 32, 48, 64)]
    app.iconphoto(True, *app_icons)


# this will play part for our password generator
lower = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
symbols = "!@#$%^&*()"

levels = {"Low": lower, "Medium": lower + upper, "Strong": lower + upper + digits + symbols}

# ------------------ functions ------------------

def generate_password():
    list_of_letters = levels[btn_seg.get()]   # our letters pool based on the password difficulty
    pass_length=int(roller_length.get())      # the lenth of the password based on the roller
    password = ''.join(random.choice(list_of_letters) for _ in range(pass_length))  # pick random letters, with a for loop based on the password length. Join them together side by side TEEHEE
    entry_password.delete(0, ctk.END)         # delete the password from beginning to end
    entry_password.insert(0,password)         # 0= start from the beginning


def encrypt_password():
    algorithm = btn_algorithms.get()          # get the selected algorithm

    if algorithm == "Ceasar":
        Ceasar()
    elif algorithm == "SHA-256":
        SHA256()
    elif algorithm == "SHA-512":
        SHA512()
    elif algorithm == "MD5":
        MD5()


def Ceasar():
    alphabet = levels["Strong"]               # we want to encrypt using the strongest letters pool always
    pass_to_encrypt = entry_password.get()    # get the password from the entry
    key = 3                                   # shift by 3 letters
    encrypted = ""

    for i in range (len(pass_to_encrypt)):
        pos = alphabet.index(pass_to_encrypt[i])        # get the position of the letters in the alphabet
        new_pos = (pos + key) % len(alphabet)           # shift the position by 3 and modulo to wrap around
        encrypted += alphabet[new_pos]                  # add the new letter to the encrypted string

    entry_encrypted.delete(0, ctk.END)                  # delete the password from beginning to end
    entry_encrypted.insert(0,encrypted)                 # 0= start from the beginning


def SHA256():
    pass_to_encrypt = entry_password.get()                                    # get the password from the entry
    encrypted = hashlib.sha256(pass_to_encrypt.encode("utf-8")).hexdigest()   # hash the password

    entry_encrypted.delete(0, ctk.END)
    entry_encrypted.insert(0,encrypted)


def SHA512():
    pass_to_encrypt = entry_password.get()                                    # get the password from the entry
    encrypted = hashlib.sha512(pass_to_encrypt.encode("utf-8")).hexdigest()   # hash the password

    entry_encrypted.delete(0, ctk.END)
    entry_encrypted.insert(0,encrypted)


def MD5():
    pass_to_encrypt = entry_password.get()                                    # get the password from the entry
    encrypted = hashlib.md5(pass_to_encrypt.encode("utf-8")).hexdigest()      # hash the password

    entry_encrypted.delete(0, ctk.END)
    entry_encrypted.insert(0,encrypted)


def clear_entries():
    entry_password.delete(0, ctk.END)
    entry_encrypted.delete(0, ctk.END)


def copy(who):
    app.clipboard_clear()                                   # clear the clipboard first

    if who == "password":
        app.clipboard_append(entry_password.get())          # copy the password
    elif who == "encrypted":
        app.clipboard_append(entry_encrypted.get())         # copy the encrypted password


# ------------------ widgets/ UI ------------------

lbl_h1 = ctk.CTkLabel(app, text="Password Generator",               # heading
                   font=("Courier", 24, "bold"),
                   text_color="#25154F",
                   fg_color="#B2C3FA",
                   corner_radius=10,)
lbl_h1.pack(pady=10)
lbl_p = ctk.CTkLabel(app, text="Pick your password criteria and encrypt it!", # paragraph under title
                   font=("Courier", 16, "italic"),
                   text_color="#25154F",
                   fg_color="#EEF3FF",)
lbl_p.pack()

tk_difficulty_frame = ctk.CTkFrame(app, fg_color="#455599")       # frame for difficulty
tk_difficulty_frame.pack(pady=5)                                    # pack also shows the thing on screen

lbl_difficulty = ctk.CTkLabel(tk_difficulty_frame,
                              text="Pick your difficulty level",
                              font=("Courier", 16, "bold"),
                              text_color="#F7F8FF")
btn_seg = ctk.CTkSegmentedButton(tk_difficulty_frame,               # button, soon to be segmented
                         values=list(levels))
btn_seg.set("Medium")                                               # set default value

lbl_difficulty.pack(side="left", padx=10, pady=10)
btn_seg.pack(side="left", padx=10, pady=10)

lbl_decor = ctk.CTkLabel(app, text="-------------------------------------------------------", # decorative line
                         font=("Courier", 16,),
                         text_color="#4D6BA3")
lbl_decor.pack(pady=5)


lbl_pass_length = ctk.CTkLabel(app, text="Pick your password length",
                              font=("Courier", 16),
                              text_color="#25154F")

lbl_pass_length.pack(pady=2)
roller_length = ctk.CTkSlider(app, from_=6, to=20,                  # length roller
                                 number_of_steps=14,
                                 width=200)
roller_length.set(12)                                               # set default value
roller_length.pack(pady=5)

btn_generate = ctk.CTkButton(app, text="Generate Password",        # generate button
                             font=("Courier", 16, "bold"),
                             text_color="#F7F8FF",
                             fg_color="#25154F",
                             command=generate_password)
btn_generate.pack(pady=5)


tk_password_frame = ctk.CTkFrame(app, fg_color="#EEF3FF")        # frame for password
tk_password_frame.pack(pady=5)                                     # pack also shows the thing on screen
entry_password = ctk.CTkEntry(tk_password_frame,
                              placeholder_text="Your password will appear here", # entry for password
                              font=("Courier", 16),
                              width= 400)
entry_password.pack(side="left", padx=10,pady=10)

btn_copy_password = ctk.CTkButton(tk_password_frame, text="Copy",   # copy button
                             font=("Courier", 16, "bold"),
                             text_color="#F7F8FF",
                             fg_color="#652475",
                             width= 100,
                             command=lambda: copy("password"))
btn_copy_password.pack(side="left", padx=10, pady=10)

tk_algorithm_frame = ctk.CTkFrame(app, fg_color="#EEF3FF")
tk_algorithm_frame.pack(pady=5)

lbl_select_algorithm = ctk.CTkLabel(tk_algorithm_frame, text="Select your encryption algorithm",
                                    font=("Courier", 16),
                                    text_color="#25154F")
lbl_select_algorithm.pack(side="left", padx=10, pady=10)


btn_algorithms = ctk.CTkOptionMenu(tk_algorithm_frame, values=["SHA-256", "SHA-512", "MD5", "Ceasar"],  # dropdown for algorithms
                                   font=("Courier", 16),
                                   fg_color="#455599",
                                   button_color="#25154F",
                                   button_hover_color="#25154F",
                                   dropdown_fg_color="#455599",
                                   dropdown_text_color="#F7F8FF",)
btn_algorithms.set("SHA-256")                                         # set default value
btn_algorithms.pack(side="left", padx=10, pady=10)

         

btn_encrypt = ctk.CTkButton(app, text="Encrypt Password",        # generate button
                             font=("Courier", 16, "bold"),
                             text_color="#F7F8FF",
                             fg_color="#25154F",
                             command=encrypt_password)
btn_encrypt.pack(pady=5)

tk_encrypted_frame = ctk.CTkFrame(app, fg_color="#EEF3FF")        # frame for encrypted
tk_encrypted_frame.pack(pady=5) 

entry_encrypted = ctk.CTkEntry(tk_encrypted_frame,
                              placeholder_text="Encrypted password will appear here", # entry for password
                              font=("Courier", 16),
                              width= 400)
entry_encrypted.pack(side="left", padx=10, pady=10)

btn_copy_password = ctk.CTkButton(tk_encrypted_frame, text="Copy",   # copy button
                             font=("Courier", 16, "bold"),
                             text_color="#F7F8FF",
                             fg_color="#652475",
                             width= 100,
                             command=lambda: copy("encrypted"))
btn_copy_password.pack(side="left", padx=10, pady=10)

lbl_decor2 = ctk.CTkLabel(app, text="-------------------------------------------------------",
                         font=("Courier", 16,),
                         text_color="#4D6BA3")
lbl_decor2.pack(pady=20)

btn_clear = ctk.CTkButton(app, text="Clear Entries and Start Again!",        # clear the passwords
                             font=("Courier", 16, "bold"),
                             text_color="#F7F8FF",
                             fg_color="#A0337F",
                             command=clear_entries)
btn_clear.pack(pady=5)





if __name__ == "__main__":
    app.mainloop()