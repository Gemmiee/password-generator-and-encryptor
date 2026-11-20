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

app = ctk.CTk(className="PasswordGenerator")                        # the window; className lets Linux match it to the menu entry + icon
app.title("Infinite password generator")
app.geometry("600x850")
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
    if not entry_password.get():                                # in case the password entry is empty
        show_encrypted("Please generate a password first!")
        return

    algorithm = btn_algorithms.get()                            # get the selected algorithm

    if algorithm == "Caesar cipher":
        Caesar()
    elif algorithm == "SHA-256":
        SHA256()
    elif algorithm == "SHA-512":
        SHA512()
    elif algorithm == "MD5":
        MD5()


def show_encrypted(text):
    entry_encrypted.delete("1.0", "end")                # textbox positions are "line.char", "1.0" = the very start
    entry_encrypted.insert("1.0", text)


def Caesar():
    alphabet = levels["Strong"]               # we want to encrypt using the strongest letters pool always
    pass_to_encrypt = entry_password.get()    # get the password from the entry
    key = int(roller_caesar_length.get())     # shift by the value from the key
    encrypted = ""

    for i in range (len(pass_to_encrypt)):
        pos = alphabet.index(pass_to_encrypt[i])        # get the position of the letters in the alphabet
        new_pos = (pos + key) % len(alphabet)           # shift the position by the key and modulo to wrap around
        encrypted += alphabet[new_pos]                  # add the new letter to the encrypted string

    show_encrypted(encrypted)


def caesar_key(key):
    roller_caesar_number.configure(text=int(key))


def algorithm_changed(choice):                              # the option menu passes the picked option
    if choice == "Caesar cipher":
        tk_caesar_section.pack(pady=2, before=btn_encrypt)  # before= puts it back above the encrypt button
    else:
        tk_caesar_section.pack_forget()                     # hides it without deleting it


def SHA256():
    pass_to_encrypt = entry_password.get()                                    # get the password from the entry
    encrypted = hashlib.sha256(pass_to_encrypt.encode("utf-8")).hexdigest()   # hash the password

    show_encrypted(encrypted)


def SHA512():
    pass_to_encrypt = entry_password.get()                                    # get the password from the entry
    encrypted = hashlib.sha512(pass_to_encrypt.encode("utf-8")).hexdigest()   # hash the password

    show_encrypted(encrypted)


def MD5():
    pass_to_encrypt = entry_password.get()                                    # get the password from the entry
    encrypted = hashlib.md5(pass_to_encrypt.encode("utf-8")).hexdigest()      # hash the password

    show_encrypted(encrypted)


def clear_entries():
    entry_password.delete(0, ctk.END)
    entry_encrypted.delete("1.0", "end")


def copy(who):
    app.clipboard_clear()                                   # clear the clipboard first

    if who == "password":
        app.clipboard_append(entry_password.get())          # copy the password
    elif who == "encrypted":
        app.clipboard_append(entry_encrypted.get("1.0", "end-1c"))  # end-1c skips the newline a textbox always adds


def password_length(value):                                   # the slider passes its new value
    roller_number.configure(text=int(value))                  # int() so 13.0 shows as 13

# ------------------ widgets/ UI ------------------

# ------------------ GENERATOR ------------------


lbl_h1_password = ctk.CTkLabel(app, text="Password Generator",         # password heading
                   font=("Courier", 24, "bold"),
                   text_color="#25154F",
                   fg_color="#B2C3FA",
                   corner_radius=10,)
lbl_h1_password.pack(pady=5)
lbl_p = ctk.CTkLabel(app, text="------------------- Random generate a password! -------------------", # paragraph under title
                   font=("Courier", 14, "italic"),
                   text_color="#5E498F",
                   fg_color="#EEF3FF",)
lbl_p.pack()



lbl_difficulty = ctk.CTkLabel(app,
                              text="Pick your password difficulty",
                              font=("Courier", 16),
                              text_color="#25154F")
btn_seg = ctk.CTkSegmentedButton(app,
                         values=list(levels),
                         width= 300,
                         height= 40,)
btn_seg.set("Medium")                                               # set default value

lbl_difficulty.pack(pady=(10,0))
btn_seg.pack(pady=(0,20))


lbl_pass_length = ctk.CTkLabel(app, text="Pick your password length",
                              font=("Courier", 16),
                              text_color="#25154F")


tk_roller_frame = ctk.CTkFrame(app, fg_color="#EEF3FF")           # frame for the roller and the roller number
roller_length = ctk.CTkSlider(tk_roller_frame, from_=6, to=20,      # length roller
                                 number_of_steps=14,
                                 width=200,
                                 command= password_length)

roller_number = ctk.CTkLabel(tk_roller_frame, text = "12",
                             font=("Courier", 14),
                             text_color="#5E498F",
                             width=30,                              # fixed width so 9 vs 12 doesn't shift the slider
                             anchor="w")                            # keep the number hugging the slider's side
roller_length.set(12)                                               # set default value
lbl_pass_length.pack()
tk_roller_frame.pack(pady=2)
roller_length.pack(side="left", padx= 5, pady=2)
roller_number.pack(side="left", padx= 5, pady=2)


btn_generate = ctk.CTkButton(app, text="Generate Password",         # generate button
                             font=("Courier", 16, "bold"),
                             text_color="#F7F8FF",
                             fg_color="#25154F",
                             command=generate_password)
btn_generate.pack(pady=(20,5))


tk_password_frame = ctk.CTkFrame(app, fg_color="#EEF3FF")        # frame for password
tk_password_frame.pack(pady=5)                                     # pack also shows the thing on screen
entry_password = ctk.CTkEntry(tk_password_frame,
                              placeholder_text="Your password will appear here", # entry for password
                              font=("Courier", 16),
                              width= 400)
entry_password.pack(side="left", padx=5,pady=5)

btn_copy_password = ctk.CTkButton(tk_password_frame, text="Copy",   # copy button
                             font=("Courier", 16, "bold"),
                             text_color="#F7F8FF",
                             fg_color="#652475",
                             width= 100,
                             command=lambda: copy("password"))
btn_copy_password.pack(side="left", padx=5, pady=5)




# ------------------ ENCRYPTOR ------------------



lbl_h1_encrypted = ctk.CTkLabel(app, text="Encryptor",         # encrypted heading
                   font=("Courier", 24, "bold"),
                   text_color="#25154F",
                   fg_color="#B2C3FA",
                   corner_radius=10,)
lbl_h1_encrypted.pack(pady=(30,0))
lbl_p = ctk.CTkLabel(app, text="--------------------- Encrypt your password! ---------------------", # paragraph under title
                   font=("Courier", 14, "italic"),
                   text_color="#5E498F",
                   fg_color="#EEF3FF",)
lbl_p.pack(pady=(0,10))



tk_encrypted_frame = ctk.CTkFrame(app, fg_color="#DAE1FA")        # parent frame for encrypted
tk_encrypted_frame.pack(pady=5) 


tk_algorithm_frame = ctk.CTkFrame(tk_encrypted_frame, fg_color="#DAE1FA")
tk_algorithm_frame.pack(pady=5)

lbl_select_algorithm = ctk.CTkLabel(tk_algorithm_frame, text="Select your encryption algorithm",
                                    font=("Courier", 16),
                                    text_color="#25154F")
lbl_select_algorithm.pack(side="left", padx=10, pady=10)


btn_algorithms = ctk.CTkOptionMenu(tk_algorithm_frame, values=["SHA-256", "SHA-512", "MD5", "Caesar cipher"],  # dropdown for algorithms
                                   font=("Courier", 16),
                                   fg_color="#455599",
                                   button_color="#25154F",
                                   button_hover_color="#25154F",
                                   dropdown_fg_color="#455599",
                                   dropdown_text_color="#F7F8FF",
                                   width= 170,
                                   anchor= "w",
                                   command=algorithm_changed)         # show/hide the caesar key slider
btn_algorithms.set("SHA-256")                                         # set default value
btn_algorithms.pack(side="left", padx=10, pady=10)


# caesar label + slider live in one frame so they can be shown/hidden together
tk_caesar_section = ctk.CTkFrame(tk_encrypted_frame, fg_color="#DAE1FA")

lbl_caesar_length = ctk.CTkLabel(tk_caesar_section, text="Select your Caesar cipher key",
                                 font=("Courier", 16),
                                text_color="#25154F")

tk_roller_caesar_frame = ctk.CTkFrame(tk_caesar_section, fg_color="#DAE1FA")           # frame for the ceasar key roller and the key number
roller_caesar_length = ctk.CTkSlider(tk_roller_caesar_frame, from_=3, to=9,               # length roller
                                 number_of_steps=6,
                                 width=200,
                                 command= caesar_key)

roller_caesar_number = ctk.CTkLabel(tk_roller_caesar_frame, text = "5",
                             font=("Courier", 14),
                             text_color="#5E498F",
                             width=30,
                             anchor="w")
roller_caesar_length.set(5)
lbl_caesar_length.pack()
tk_roller_caesar_frame.pack(pady=2)
# tk_caesar_section isn't packed here: it starts hidden since SHA-256 is the default
roller_caesar_length.pack(side="left", padx= 5, pady=(5,0))
roller_caesar_number.pack(side="left", padx= 5, pady=(5,0))
        



btn_encrypt = ctk.CTkButton(tk_encrypted_frame, text="Encrypt Password",           # generate button
                             font=("Courier", 16, "bold"),
                             text_color="#F7F8FF",
                             fg_color="#25154F",
                             command=encrypt_password)
btn_encrypt.pack(pady=5)



""" my problem with entry_encrypted... :/
    the encrypted passwords were too large for the 'entry' boundaries
    and leaked outside, making it very anti-pleasing to the eye.
    - Fix was: instead of an 'entry' I made it a 'textbox' so that
    i could use the wrap="char" parameter for the break lines
"""


entry_encrypted = ctk.CTkTextbox(tk_encrypted_frame,                # textbox, not entry like before
                                 font=("Courier", 16),
                                 width=400,
                                 height=110,
                                 border_width= 2,
                                 wrap="char")                       # break anywhere
entry_encrypted.pack(side="left", padx=10, pady=10)
entry_encrypted.insert("0.0", "encrypted password will appear here")

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
lbl_decor2.pack(pady=10)

btn_clear = ctk.CTkButton(app, text="Clear Entries and Start Again!",        # clear the passwords
                             font=("Courier", 16, "bold"),
                             text_color="#F7F8FF",
                             fg_color="#A0337F",
                             command=clear_entries)
btn_clear.pack(pady=5)





if __name__ == "__main__":
    app.mainloop()