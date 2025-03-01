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
parser = argparse.ArgumentParser(description="Report on Study Entry Package for CT Abdomen Pelvis With Contrast")
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
root.title("CT Abdomen Pelvis With Contrast" + " MRN: " + mrn + " SESSION: " + session)

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
tek_box, rowvar = add_box(json_data[TH][DC], rowvar)

add_label("CTDI: ", rowvar, 0)
ctdi_entry, rowvar = add_entry(json_data[TH]["ctdi"], 20, "left", rowvar, 1)

add_label("DLP: ", rowvar, 0)
dlp_entry, rowvar = add_entry(json_data[TH]["dlp"], 20, "left", rowvar, 1)

add_label(COMPARISON, rowvar, 0)
comparison_box, rowvar = add_label_box(COMPARISON, json_data[TH][CM], rowvar)

# Findings Section
rowvar = add_fixed_label(FINDINGS, rowvar)

add_label("LUNG BASES", rowvar, 0)
lung_entry, rowvar = add_entry(json_data[FI]["lung"], -1, "left", rowvar, 1)

add_label("LIVER", rowvar, 0)
liver_entry, rowvar = add_entry(json_data[FI]["liver"], -1, "left", rowvar, 1)

add_label("GALLBLADDER/BILE DUCTS", rowvar, 0)
gbd_entry, rowvar = add_entry(json_data[FI]["gbd"], -1, "left", rowvar, 1)

add_label("SPLEEN", rowvar, 0)
spleen_entry, rowvar = add_entry(json_data[FI]["spleen"], -1, "left", rowvar, 1)

add_label("PANCREAS", rowvar, 0)
pancreas_entry, rowvar = add_entry(json_data[FI]["pancreas"], -1, "left", rowvar, 1)

add_label("ADRENAL GLANDS", rowvar, 0)
adrenal_entry, rowvar = add_entry(json_data[FI]["adrenal"], -1, "left", rowvar, 1)

add_label("KIDNEYS", rowvar, 0)
kidneys_entry, rowvar = add_entry(json_data[FI]["kidneys"], -1, "left", rowvar, 1)

add_label("BOWEL", rowvar, 0)
bowel_entry, rowvar = add_entry(json_data[FI]["bowel"], -1, "left", rowvar, 1)

add_label("MESENTERY/LYMPH NODES", rowvar, 0)
meslymph_entry, rowvar = add_entry(json_data[FI]["meslymph"], -1, "left", rowvar, 1)

add_label("PERITONEUM", rowvar, 0)
peritoneum_entry, rowvar = add_entry(json_data[FI]["peritoneum"], -1, "left", rowvar, 1)

add_label("AORTA/VESSELS", rowvar, 0)
aorta_entry, rowvar = add_entry(json_data[FI]["aorta"], -1, "left", rowvar, 1)

add_label("BLADDER", rowvar, 0)
bladder_entry, rowvar = add_entry(json_data[FI]["bladder"], -1, "left", rowvar, 1)

add_label("PELVIC STRUCTURES", rowvar, 0)
pelvis_entry, rowvar = add_entry(json_data[FI]["pelvic"], -1, "left", rowvar, 1)

add_label("SOFT TISSUES", rowvar, 0)
soft_entry, rowvar = add_entry(json_data[FI]["soft tissues"], -1, "left", rowvar, 1)

add_label("BONES", rowvar, 0)
bones_entry, rowvar = add_entry(json_data[FI]["bones"], -1, "left", rowvar, 1)

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
    jd[TH]["ctdi"] = ctdi_entry.get()
    jd[TH]["dlp"] = dlp_entry.get()
    jd[TH][CM] = comparison_box.get("1.0", "end-1c")

    jd[FI]["lung"] = lung_entry.get()
    jd[FI]["liver"] = liver_entry.get()
    jd[FI]["gbd"] = gbd_entry.get()
    jd[FI]["spleen"] = spleen_entry.get()
    jd[FI]["pancreas"] = pancreas_entry.get()
    jd[FI]["adrenal"] = adrenal_entry.get()
    jd[FI]["kidneys"] = kidneys_entry.get()
    jd[FI]["bowel"] = bowel_entry.get()
    jd[FI]["meslymph"] = meslymph_entry.get()
    jd[FI]["peritoneum"] = peritoneum_entry.get()
    jd[FI]["aorta"] = aorta_entry.get()
    jd[FI]["bladder"] = bladder_entry.get()
    jd[FI]["pelvic"] = pelvis_entry.get()
    jd[FI]["soft tissues"] = soft_entry.get()
    jd[FI]["bones"] = bones_entry.get()

    jd[IM] = impress_box.get("1.0", "end-1c")

    with open(jsonfile, "w") as ofile:
        json.dump(jd, ofile)

# Define a function that will save existing data to a printable report text file
def create_report(rpt):
    save_data(json_data)
    with open(rpt, "w") as ofile:
        wrapper = textwrap.TextWrapper(width=60, replace_whitespace=False)
        print("CT Abdomen Pelvis With Contrast Study", file=ofile)
        print("", file=ofile)
        print("MRN: " + mrn, file=ofile)
        print("Session: " + session, file=ofile)
        print("", file=ofile)
        print("", file=ofile)
        print(HISTORY, file=ofile)
        print("", file=ofile)
        print(PATIENT_AGE + " (years):  " + json_data[HI][PA], file=ofile)
        print(PATIENT_HISTORY + "", file=ofile)
        for line in json_data[HI][PH].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)
        print("", file=ofile)
        print(TECHNIQUE, file=ofile)
        for line in json_data[TH][DC].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)
        print("CTDI: ".ljust(6) + json_data[TH]["ctdi"], file=ofile)
        print("DLP: ".ljust(6) + json_data[TH]["dlp"], file=ofile)
        print(COMPARISON + ": " + json_data[TH][CM], file=ofile)
        print("", file=ofile)
        print(FINDINGS, file=ofile)

        print("LUNG BASES:".ljust(25) + json_data[FI]["lung"], file=ofile)
        print("LIVER:".ljust(25) + json_data[FI]["liver"], file=ofile)
        print("GALLBLADDER/BILE DUCTS:".ljust(25) + json_data[FI]["gbd"], file=ofile)
        print("SPLEEN:".ljust(25) + json_data[FI]["spleen"], file=ofile)
        print("PANCREAS:".ljust(25) + json_data[FI]["pancreas"], file=ofile)
        print("ADRENAL GLANDS:".ljust(25) + json_data[FI]["adrenal"], file=ofile)
        print("KIDNEYS:".ljust(25) + json_data[FI]["kidneys"], file=ofile)
        print("BOWEL:".ljust(25) + json_data[FI]["bowel"], file=ofile)
        print("MESENTERY/LYMPH NODES:".ljust(25) + json_data[FI]["meslymph"], file=ofile)
        print("PERITONEUM:".ljust(25) + json_data[FI]["peritoneum"], file=ofile)
        print("AORTA/VESSELS:".ljust(25) + json_data[FI]["aorta"], file=ofile)
        print("BLADDER:".ljust(25) + json_data[FI]["bladder"], file=ofile)
        print("PELVIC STRUCTURES:".ljust(25) + json_data[FI]["pelvic"], file=ofile)
        print("SOFT TISSUES:".ljust(25) + json_data[FI]["soft tissues"], file=ofile)
        print("BONES:".ljust(25) + json_data[FI]["bones"], file=ofile)

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
