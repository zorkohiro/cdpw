#!/usr/bin/python3
"""
Program to edit from JSON file input to add more or
edit existing data and to ultimately sign and print
a text based report from this date.
"""

#################################################################################################
#
#  WITHOUT ANY WARRANTY; without even the implied warranty of
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

#################################################################################################
#
# Constants and shorthands
#
REPORT_DIR = "/code_dark/reports"


HI = "history"
PA = "patient_age"
PH = "patient_history"
TH = "technique"
DC = "description"
FI = "findings"
CM = "comparison"
IM = "impression"
BD = "bile ducts"

HISTORY = "** HISTORY **"
PATIENT_AGE = "Patient Age"
PATIENT_HISTORY = "Patient History"

TECHNIQUE = "** TECHNIQUE **"

FINDINGS = "** FINDINGS **"
COMPARISON = "Comparison"

IMPRESSION = "** IMPRESSION **"

#
# Process command line arguments and load initial json data
#
parser = argparse.ArgumentParser(description="Report on Study Entry Package for CHEST XRAY")
parser.add_argument("-m", "--mrn", help="MRN for Study", required=True)
parser.add_argument("-s", "--session", help="Session for Study", required=True)
parser.add_argument("-R", "--report_dir", help="Where we fetch/save reports", default="/code_dark/reports")

args=vars(parser.parse_args())
mrn = args['mrn']
session = args['session']
report_dir = REPORT_DIR
if args['report_dir']:
    report_dir = args['report_dir']

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
root.title("Ultrasound Right Upper Quadrant Abdomen" + " MRN: " + mrn + " SESSION: " + session)
root.geometry('768x1250')
#
# Need this to make sure Entry fields abut labels,
# because otherwise boxes willf orce then Entry field
# to the middle of a wide box.
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
    tlab = tk.Label(root, text=str, relief=tk.RAISED)
    tlab.grid(sticky=tk.N+tk.W, row=row)
    return row + 1

def add_label(str, rowvalue, col):
    tlab = tk.Label(root, text=str, anchor=tk.W, justify="left") 
    tlab.grid(sticky=tk.N+tk.W, row=rowvalue, column=col)
    return rowvalue + 1

def add_entry(initial, w, j, row, col):
    tt_text = tk.StringVar()
    tt_text.set(initial)
    tt_entry = tk.Entry(root, textvariable=tt_text, width=w, justify=j)
    tt_entry.grid(sticky=tk.W, row=row, column=col)
    return tt_text, row + 1

def add_box(insert, row):
    box = tk.Text(root, height=4, width=90)
    box.insert(tk.END, insert)
    box.grid(sticky=tk.W, row=row, column=0, columnspan=3, pady=(0,10))
    return box, row + 4


# History Section
rowvar = add_fixed_label(HISTORY, rowvar)

add_label(PATIENT_AGE + " (years) ", rowvar, 0)
age_entry, rowvar = add_entry(json_data[HI][PA], 4, "right", rowvar, 1)

rowvar = add_label(PATIENT_HISTORY, rowvar, 0)
history_box, rowvar = add_box(json_data[HI][PH], rowvar)

# Technique Section
rowvar = add_fixed_label(TECHNIQUE, rowvar)

tek_box, rowvar = add_box(json_data[TH][DC], rowvar)

add_label(COMPARISON, rowvar, 0)
comparison_entry, rowvar = add_entry(json_data[TH][CM], 20, "left", rowvar, 1)

# Findings Section
rowvar = add_fixed_label(FINDINGS, rowvar)

rowvar = add_label("PANCREAS:", rowvar, 0)
pancreas_box, rowvar = add_box(json_data[FI]["pancreas"], rowvar)

rowvar = add_label("LIVER:", rowvar, 0)
liver_box, rowvar = add_box(json_data[FI]["liver"], rowvar)

rowvar = add_label("GALLBLADDER:", rowvar, 0)
gallbladder_box, rowvar = add_box(json_data[FI]["gallbladder"], rowvar)

rowvar = add_label("BILE DUCTS:", rowvar, 0)
add_label("Common duct measures (in mm): ", rowvar, 0)
bileduct_size, rowvar = add_entry(json_data[FI][BD]["size"], 10, "right", rowvar, 1)

add_label("which is", rowvar, 0)
bileduct_quality, rowvar = add_entry(json_data[FI][BD]["quality"], 10, "left", rowvar, 1)

bileduct_dilation, rowvar = add_box(json_data[FI][BD]["dilation"], rowvar)

rowvar =  add_label("RIGHT KIDNEY:", rowvar, 0)

add_label("Measures (in cm): ", rowvar, 0)
kidney_size, rowvar = add_entry(json_data[FI]["right kidney"]["size"], 5, "right", rowvar, 1)

kidney_box, rowvar = add_box(json_data[FI]["right kidney"]["notes"], rowvar)

rowvar = add_label("Other:", rowvar, 0)
other_box, rowvar = add_box(json_data[FI]["other"], rowvar)

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

    jd[TH][DC] = tek_box.get("1.0", "end-1c")
    jd[TH][CM] = comparison_entry.get()

    jd[FI]["pancreas"] = pancreas_box.get("1.0", "end-1c")
    jd[FI]["liver"] = liver_box.get("1.0", "end-1c")
    jd[FI]["gallbladder"] = gallbladder_box.get("1.0", "end-1c")
    jd[FI][BD]["size"] = bileduct_size.get()
    jd[FI][BD]["quality"] = bileduct_quality.get()
    jd[FI][BD]["dilation"] = bileduct_dilation.get("1.0", "end-1c")

    jd[FI]["right kidney"]["size"] = kidney_size.get()
    jd[FI]["right kidney"]["notes"] = kidney_box.get("1.0", "end-1c")

    jd[FI]["other"] = other_box.get("1.0", "end-1c")
    jd[IM] = impress_box.get("1.0", "end-1c")

    with open(jsonfile, "w") as ofile:
        json.dump(jd, ofile)

# Define a function that will save existing data to a printable report text file
def create_report(rpt):
    save_data(json_data)
    with open(rpt, "w") as ofile:
        wrapper = textwrap.TextWrapper(width=60, replace_whitespace=False)
        print("Ultrasound Upper Right Quadrant Abdomen Study", file=ofile)
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
        for line in json_data[TH][DC].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)
        print(COMPARISON + ": " + json_data[TH][CM], file=ofile)
        print("", file=ofile)
        print(FINDINGS, file=ofile)

        print("PANCREAS:", file=ofile)
        for line in json_data[FI]["pancreas"].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)

        print("LIVER:", file=ofile)
        for line in json_data[FI]["liver"].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)

        print("GALLBLADDER:", file=ofile)
        for line in json_data[FI]["gallbladder"].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)

        print("BILE DUCTS:", file=ofile)
        print("Common duct measures (in mm): " + json_data[FI][BD]["size"], file=ofile)
        print("which is " + json_data[FI][BD]["quality"], file=ofile)
        for line in json_data[FI][BD]["dilation"].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)

        print("RIGHT KIDNEY:", file=ofile)
        print("Measures (in cm): " + json_data[FI]["right kidney"]["size"], file=ofile)
        print("Notes:", file=ofile)
        for line in json_data[FI]["right kidney"]["notes"].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)

        print("Other:", file=ofile)
        for line in json_data[FI]["other"].split('\n'):
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
    rpt.signed = True

# define a function that will exit, saving data and creating on-disk report as it does so.
def exit_edit():
    save_data(json_data)
    create_report(reportfl)
    exit()

#
# Add action buttons to the end
#
sign_btn = tk.Button(root, text = 'Sign Report', command = sign_report)
sign_btn.grid(sticky=tk.W)

print_btn = tk.Button(root, text = 'Print Report', command = print_report)
print_btn.grid(sticky=tk.W)

exit_btn = tk.Button(root, text = 'Exit', command = exit_edit)
exit_btn.grid(sticky=tk.W)


#
# Enter edit tkinter loop
#
root.mainloop()
