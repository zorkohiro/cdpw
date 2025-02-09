#!/usr/bin/python3
# Program to run setuid root to set time/date on Code Dark workstation
# Gratefully copied from https://geeksforgeeks/python-tkinter-entry-widget

import subprocess
import tkinter as tk
from tkinter import messagebox
root=tk.Tk()
root.geometry("380x90")
root.title("Set System Local Time")

dstr_var = tk.StringVar()


# defining a function that will
# get the date and time entered
def submit():
    dstr = dstr_var.get()
    if len(dstr) != 10:
        messagebox.showerror("Error", "Wrong Length")
        dstr_var.set("")
    else:
        try:
            mon = int(dstr[0:2])
            day = int(dstr[2:4])
            hr = int(dstr[4:6])
            minute = int(dstr[6:8])
            yr = int(dstr[8:10])
        except:
            messagebox.showerror("Error", "non-integer entries")
            dstr_var.set("")
            return
        if mon < 1 or mon > 12:
            messagebox.showerror("Error", "bad month value")
            return
        if day < 1 or day > 31:
            messagebox.showerror("Error", "bad day value")
            return
        if hr < 0 or hr > 23:
            messagebox.showerror("Error", "bad hour value")
            return
        if minute < 0 or minute >= 60:
            messagebox.showerror("Error", "bad minute value")
            return
        if yr < 24 or yr > 30:
            messagebox.showerror("Error", "bad year value")
            return
        try:
            result = subprocess.run(["/usr/bin/sudo", "-n", "/usr/bin/date", dstr], capture_output=True, text=True)
            if result.returncode != 0:
                messagebox.showerror("Error", result.stderr)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", e.output)
        exit()

dstr_label = tk.Label(root, text = 'Set New Time (MMDDhhmmYY)', font=('calibre', 10, 'normal'))
dstr_entry = tk.Entry(root, textvariable = dstr_var, font=('calibre', 10,'normal'))

expl_label1 = tk.Label(root, text = 'MM = month, DD = day, hh = hour, mm = minute, YY = year', font=('calibre', 9, 'normal'))
sub_btn1 = tk.Button(root,text = 'Set New Time', command = submit)

dstr_label.grid(row=0, column=0)
dstr_entry.grid(row=0, column=1)
expl_label1.grid(row=1, column=0, columnspan=2, sticky=tk.E)
sub_btn1.grid(row=2, column=0, columnspan=2, stick=tk.E)

root.mainloop()
