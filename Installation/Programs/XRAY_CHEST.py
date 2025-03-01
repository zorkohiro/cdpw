#!/usr/bin/python3
"""
Program to edit from JSON file input to add more or
edit existing data and to ultimately sign and print
a text based report from this date.
"""

#################################################################################################
#
#  Copyright (C) 2024 Kaiser Permanente
#
#  This program is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#


#################################################################################################
#
# Imports
#
import subprocess
import tkinter as tk
import json
import textwrap
import argparse

#################################################################################################
#
# Variables
#
radiologist = "Dr Roberts"
rowvar = 0
fontfamily = 'Times'
fontsize = 12
fontstring = fontfamily + ' ' + str(fontsize)
boxsize = 3

#################################################################################################
#
# Constants and shorthands
#
REPORT_DIR = "/code_dark/reports"


HI = "history"
PA = "patient_age"
PH = "patient_history"
TH = "technique"
VI = "views"
FI = "findings"
CM = "comparison"
IM = "impression"

HISTORY = "** HISTORY **"
PATIENT_AGE = "Patient Age"
PATIENT_HISTORY = "Patient History"

TECHNIQUE = "** TECHNIQUE **"
VIEWS = "Views"

FINDINGS = "** FINDINGS **"
COMPARISON = "Comparison"

IMPRESSION = "** IMPRESSION **"

#
# Process command line arguments and load initial json data
#
parser = argparse.ArgumentParser(description="Report on Study Entry Package for Chest X-Ray")
parser.add_argument("-m", "--mrn", help="MRN for Study", required=True)
parser.add_argument("-s", "--session", help="Session for Study", required=True)
parser.add_argument("-R", "--report_dir", help="Where we fetch/save reports", default="/code_dark/reports")
parser.add_argument("-f", "--fontsize", help="Font Size (default 12)")

args=vars(parser.parse_args())
mrn = args['mrn']
session = args['session']
report_dir = REPORT_DIR
if args['report_dir']:
    report_dir = args['report_dir']
if args['fontsize']:
    fontsize = int(args['fontsize'])
    fontstring = 'Time ' + args['fontsize']

reportnm = "study" + "_" + mrn + "_" + session
jsonfile = report_dir + "/" + reportnm + ".json"
reportfl = report_dir + "/" + reportnm + ".txt"

#
# Read in JSON saved data
#
with open(jsonfile, "r") as infile:
    json_data = json.load(infile)

#################################################################################################
#
# Window and Frame Management Code
#

#
# Root window creation
#
root=tk.Tk()
root.title("X-Ray Chest Study" + " MRN: " + mrn + " SESSION: " + session)

#
# Need this to make sure Entry fields abut labels,
# because otherwise boxes willf orce then Entry field
# to the middle of a 80 wide box.
#
root.grid_columnconfigure(1, weight=1)

#
# Display sections with labels and text boxes,
# using data read in as existing values.
#

#
# Shorthand functions
#
def add_fixed_label(str, row):
    tlab = tk.Label(root, text=str, relief=tk.RAISED, font=(fontfamily, fontsize + 1))
    tlab.grid(sticky=tk.N+tk.W, row=row, pady=(1,0))
    return row + 1

def add_label(str, row, col):
    tlab = tk.Label(root, text=str, anchor=tk.W, justify="left", font=(fontfamily, fontsize - 1))
    tlab.grid(sticky=tk.N+tk.W, row=row, column=col)
    return row + 1

def add_entry(initial, w, j, row, col):
    tt_text = tk.StringVar()
    tt_text.set(initial)
    if w < 0:
            tt_entry = tk.Entry(root, textvariable=tt_text, justify=j, font=fontstring)
            tt_entry.grid(sticky=tk.EW, row=row, column=col)
    else:
            tt_entry = tk.Entry(root, textvariable=tt_text, width=w, justify=j, font=fontstring)
            tt_entry.grid(sticky=tk.W, row=row, column=col)
    return tt_text, row + 1

def add_box(insert, row):
    box = tk.Text(root, height=boxsize, width=90, font=fontstring)
    box.insert(tk.END, insert)
    box.grid(sticky=tk.EW, row=row, column=0, columnspan=3, pady=(0,10), padx=(0,9))
    return box, row + boxsize

def add_label_box(str, insert, row):
    tlab = tk.Label(root, text=str, anchor=tk.W, justify="left", font=(fontfamily, fontsize - 1))
    tlab.grid(sticky=tk.N+tk.W, row=row, column=0)
    box = tk.Text(root, height=boxsize, width=90, font=fontstring)
    box.insert(tk.END, insert)
    box.grid(sticky=tk.W, row=row, column=1, columnspan=2, pady=(0,10), padx=(0,10))
    return box, row + boxsize


# History Section
rowvar = add_fixed_label(HISTORY, rowvar)

add_label(PATIENT_AGE + " (years) ", rowvar, 0)
age_entry, rowvar = add_entry(json_data[HI][PA], 4, "right", rowvar, 1)

history_box, rowvar = add_label_box(PATIENT_HISTORY, json_data[HI][PH], rowvar)

# Technique Section
rowvar = add_fixed_label(TECHNIQUE, rowvar)

views_box, rowvar = add_label_box(VIEWS, json_data[TH][VI], rowvar)

comparison_box, rowvar = add_label_box(COMPARISON, json_data[TH][CM], rowvar)

# Findings Section
rowvar = add_fixed_label(FINDINGS, rowvar)
findings_box, rowvar = add_box(json_data[FI], rowvar)

# Impressions Section
rowvar = add_fixed_label(IMPRESSION, rowvar)
impress_box, rowvar = add_box(json_data[IM], rowvar)

#################################################################################################
#
# Data interactions with tkinter frame/boxes plus action functions
#

#
# Define a function that will save data to a datafile.
# As a side effect, it updates existing data from labels and text boxes
#
def save_data(jd):
    """ Update from tkinter box areas """
    jd[HI][PA] = age_entry.get()
    jd[HI][PH] = history_box.get("1.0", "end-1c")
    jd[TH][VI] = views_box.get("1.0", "end-1c")
    jd[TH][CM] = comparison_box.get("1.0", "end-1c")
    jd[FI] = findings_box.get("1.0", "end-1c")
    jd[IM] = impress_box.get("1.0", "end-1c")
    with open(jsonfile, "w") as ofile:
        json.dump(jd, ofile)

# Define a function that will save existing data to a printable report text file
def create_report(rpt):
    save_data(json_data)
    with open(rpt, "w") as ofile:
        wrapper = textwrap.TextWrapper(width=60, replace_whitespace=False)
        print("X-Ray Chest Study", file=ofile)
        print("", file=ofile)
        print("MRN: " + mrn, file=ofile)
        print("Session: " + session, file=ofile)
        print("", file=ofile)
        print("", file=ofile)
        print(HISTORY, file=ofile)
        print("", file=ofile)
        print(PATIENT_AGE + " (years):  " + json_data[HI][PA], file=ofile)
        print(PATIENT_HISTORY + ":", file=ofile)
        for line in json_data[HI][PH].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)
        print("", file=ofile)
        print(TECHNIQUE, file=ofile)
        print(VIEWS + ":", file=ofile)
        for line in json_data[TH][VI].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)
        print(COMPARISON + ": " + json_data[TH][CM], file=ofile)
        print("", file=ofile)
        print(FINDINGS, file=ofile)
        for line in json_data[FI].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)
        print("", file=ofile)
        print(IMPRESSION, file=ofile)
        for line in json_data[IM].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)
        print("", file=ofile)
        """ PRINT SIGNING RADIOLIGIST NAME """

# Define a function that will print the report after saving text output to a file
def print_report():
    save_data(json_data)
    create_report(reportfl)
    try:
        result = subprocess.run(["enscript", "-B", reportfl ], capture_output=True, text=True)
        if result.returncode != 0:
            messagebox.showerror("Subprocess Error", result.stderr)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Process Error", e.output)

# Define a function that will sign the report
def sign_report():
    json_data["signed"] = True
    json_data["signer"] = radiologist
    save_data(json_data)
    try:
        result = subprocess.run(["chmod", "-w", jsonfile ], capture_output=True, text=True)
        if result.returncode != 0:
            messagebox.showerror("Subprocess Error", result.stderr)
            exit()
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Process Error", e.output)
        exit()

# define a function that will exit, saving data and creating on-disk report as it does so.
def exit_edit():
    save_data(json_data)
    create_report(reportfl)
    exit()

#
# Add action buttons to the end
#
rowvar = rowvar + 1
sign_btn = tk.Button(root, text = 'Sign Report', command = sign_report)
sign_btn.grid(sticky=tk.W, column=0, row=rowvar)

print_btn = tk.Button(root, text = 'Print Report', command = print_report)
print_btn.grid(sticky=tk.W, column=1, row=rowvar)

exit_btn = tk.Button(root, text = 'Exit', command = exit_edit)
exit_btn.grid(sticky=tk.W, column=2, row=rowvar)


#
# Enter edit tkinter loop
#
root.mainloop()
