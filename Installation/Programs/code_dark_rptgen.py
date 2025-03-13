#!/usr/bin/python3
"""
Program to edit from JSON file input to add more or
edit existing data and to ultimately sign and print
a text based report from this data.
"""

#################################################################################################
#
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  Copyright (C) 2025 Kaiser Permanente
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
cbobj = {}

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
parser = argparse.ArgumentParser(description="Code Dark Report Entry Package")
parser.add_argument("-j", "--json", help="Input json file", required=True)
parser.add_argument("-R", "--report_dir", help="Where we fetch/save reports", default="/code_dark/reports")
parser.add_argument("-f", "--fontsize", help="Font Size (default 12)")

args = vars(parser.parse_args())
report_dir = REPORT_DIR

jsonfile=args['json']
reportfl=jsonfile.replace(".json", ".txt")

if args['report_dir']:
    report_dir = args['report_dir']
if args['fontsize']:
    fontsize = int(args['fontsize'])
    fontstring = 'Time ' + args['fontsize']


#
# Read in JSON saved data
#
with open(jsonfile, "r") as infile:
    json_data = json.load(infile)

#
# Version check
#

version = json_data["version"]
if version < 1:
    print("Version of JSON too low: " + str(version))
    exit(1)

#
# Supply a default mrn/session if there isn't one.
#
# At this time we expect other parts of the code to thread
# mrn and session in the json file that will be edited
# at initial creation time.
#
mrn = json_data["mrn"]
if not mrn:
    mrn = "bogus"
    json_data["mrn"] = mrn

session = json_data["session"]
if not session:
    json_data["session"] = mrn
    session = "bogus"

#
# Structure of JSON data
#
# The JSON file is an object with a list of contained sub-objects and arrays.
# Most of the sub-objects are common across all report types. However,
# findings are a special type that has been genericized so we don't have
# to have a different program for each report type. This is finessed using
# an array and a couple of sub-objects to control both order of presentation,
# the format of the presentation and type of input and any padding or
# intermediate level labels.
#
# The common objects are grouped thusly:
#
# 1. Housekeeping items
#   
#  "mrn"        : Medical Record Number (passed from orthanc)
#  "session"    : Accession Number (passed from orthanc)
#  "signed"     : boolean about whether the report has been signed (and is thus read-only)
#  "signer"     : who signed the report
#  "template"   : self-referential template name to internally identify in the JSON data the template json file name
#
# 2. Age/History
#
#    Common nested object to have an entry for patient age (in years) and a free form patient history box.
#    This section is prefaced by a fixed large label "HISTORY".
#
# 3. Technique
#
#    Common nested object to describe how the study was performed, optionally containing CTDI and DLP for contrast media.
#    This ends with freeform box for comparison information.
#    This section is prefaced by a fixed large label "TECHNIQUE".
#
# 4. Findings (see below for detailed description)
#
# 5. Impressions
#
#    Common object to have a free form written impression from the radiologist drawing conclusions about the study.
#    This section is prefaced by a fixed large label "IMPRESSIONS".
#
# Findings
#
#    This section is prefaced by a fixed large label with the name "FINDINGS".
#  
#    To make this generic enough, we start with an array that consists of a sequence of strings.
#    These strings are either the string label:HDR, the string <key>:HDR:ENTRY or
#    the string <key>:HDR:BOX.
#
#    The string label:HDR indicates that for both entry purposes and printing purposes
#    a fixed label is to be inserted. The value of HDR is the literal value for that label
#    as it is to be presented.
#
#    The string label that is of the form <key>:HDR:ENTRY is a specifications for a single entry
#    on input or a single line of output in a report. The <key> portion is used as an associative
#    index into the "findings" recursive sub-object to retrieve the data associated with that key.
#    The HDR portion is the literal label for the entry of printed out in the report.
#
#    Similarly for <key>:HDR:BOX- it is the same but instead of for a single entry it's for a 
#    right-hanging box for freeform text input or printed output.
#    


#################################################################################################
#
# Window and Frame Management Code
#

#
# Root window creation
#
root=tk.Tk()
root.title(json_data["title"]  + " MRN: " + mrn + " SESSION: " + session)

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
def add_section_label(str, row):
    tlab = tk.Label(root, text=str, relief=tk.RAISED, font=(fontfamily, fontsize + 1))
    tlab.grid(sticky=tk.N+tk.W, row=row, pady=(1,1))
    return row + 1

def add_label(str, row, col):
    tlab = tk.Label(root, text=str, relief=tk.GROOVE, font=(fontfamily, fontsize))
    tlab.grid(sticky=tk.N+tk.W, row=row, column=col)
    return row + 1

""" Add a label to the column specified (usually col 0 on the left) """
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

""" Add an entry to the right of a label """
def add_label_entry(label, ivalue, row):
    tlab = tk.Label(root, text=label, anchor=tk.W, justify="left", font=(fontfamily, fontsize - 1))
    tlab.grid(sticky=tk.N+tk.W, row=row, column=0)
    tt_text = tk.StringVar()
    tt_text.set(ivalue)
    tt_entry = tk.Entry(root, textvariable=tt_text, width=90, justify="left", font=fontstring)
    tt_entry.grid(sticky=tk.W, row=row, column=1)
    return tt_text, row + 1
    
""" add an unlabeled box """
def add_box(insert, row):
    box = tk.Text(root, height=boxsize, width=90, font=fontstring)
    box.insert(tk.END, insert)
    box.grid(sticky=tk.EW, row=row, column=0, columnspan=3, pady=(0,10), padx=(0,9))
    return box, row + boxsize

""" add a box hanging to the right of a label """
def add_label_box(str, insert, row):
    tlab = tk.Label(root, text=str, anchor=tk.W, justify="left", font=(fontfamily, fontsize - 1))
    tlab.grid(sticky=tk.N+tk.W, row=row, column=0)
    box = tk.Text(root, height=boxsize, width=90, font=fontstring)
    box.insert(tk.END, insert)
    box.grid(sticky=tk.W, row=row, column=1, columnspan=2, pady=(0,10), padx=(0,10))
    return box, row + boxsize

# History Section
rowvar = add_section_label(HISTORY, rowvar)

add_label(PATIENT_AGE + " (years) ", rowvar, 0)
age_entry, rowvar = add_entry(json_data[HI][PA], 4, "right", rowvar, 1)

history_box, rowvar = add_label_box(PATIENT_HISTORY, json_data[HI][PH], rowvar)

# Technique Section
rowvar = add_section_label(TECHNIQUE, rowvar)
tek_box, rowvar = add_box(json_data[TH][DC], rowvar)

if "ctdi" in json_data[TH]:
    add_label("CTDI: ", rowvar, 0)
    ctdi_entry, rowvar = add_entry(json_data[TH]["ctdi"], 20, "left", rowvar, 1)
    add_label("DLP: ", rowvar, 0)
    dlp_entry, rowvar = add_entry(json_data[TH]["dlp"], 20, "left", rowvar, 1)

comparison_box, rowvar = add_label_box(COMPARISON, json_data[TH][CM], rowvar)

# Findings Section
rowvar = add_section_label(FINDINGS, rowvar)

for entry in json_data["fseq"]:
    words = entry.split(':')
    # Add a row when having a space
    if len(words) == 2:
        rowvar = rowvar + 1
    elif len(words) == 2:
        rowvar = add_label(words[1], rowvar, 0)
    else:
        key = words[0]
        lbl = words[1]
        typ = words[2]
        if typ == "ENTRY":
            cb, rowvar = add_label_entry(lbl, json_data[FI][key], rowvar)
        elif typ == "BOX":
            cb, rowvar = add_box(json_data[FI][key], rowvar)
        elif typ == "BOXLABEL":
            cb, rowvar = add_label_box(lbl, json_data[FI][key], rowvar)
        else:
            key = None
        if key:
            cbobj[key] = cb

# Impressions Section
rowvar = add_section_label(IMPRESSION, rowvar)
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
    if "ctdi" in json_data[TH]:
        jd[TH]["ctdi"] = ctdi_entry.get()
        jd[TH]["dlp"] = dlp_entry.get()
    jd[TH][CM] = comparison_box.get("1.0", "end-1c")

    for entry in json_data["fseq"]:
        words = entry.split(':')
        # Not worrying about headers or labels here
        if len(words) == 3:
            key = words[0]
            obj = cbobj[key]
            if typ == "ENTRY":
                jd[FI][key] = obj.get()
            elif typ == "BOX" or typ == "BOXLABEL":
                jd[FI][key] = obj.get("1.0", "end-1c")

    jd[IM] = impress_box.get("1.0", "end-1c")

    with open(jsonfile, "w") as ofile:
        json.dump(jd, ofile, indent=2)

# Define a function that will save existing data to a printable report text file
def create_report(rpt):
    save_data(json_data)
    with open(rpt, "w") as ofile:
        wrapper = textwrap.TextWrapper(width=60, replace_whitespace=False)
        print(json_data["title"], file=ofile)
        print("", file=ofile)
        print("MRN: " + mrn, file=ofile)
        print("Session: " + session, file=ofile)
        print("", file=ofile)
        print("", file=ofile)
        print(HISTORY + ":", file=ofile)
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
        if "ctdi" in json_data[TH]:
            print("CTDI: ".ljust(6) + json_data[TH]["ctdi"], file=ofile)
            print("DLP: ".ljust(6) + json_data[TH]["dlp"], file=ofile)
            print("", file=ofile)
        print(COMPARISON + ":", file=ofile)
        for line in json_data[TH][CM].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)
        print(FINDINGS, file=ofile)

        for entry in json_data["fseq"]:
            words = entry.split(':')
            if len(words) == 1:
                print("", file=ofile)
            elif len(words) == 2:
                print("", file=ofile)
                print(words[1], file=ofile)
                print("", file=ofile)
            else:
                key = words[0]
                lbl = words[1]
                typ = words[2]
                if typ == "ENTRY":
                    front = lbl + ":"
                    print(front.ljust(25) + json_data[FI][key], file=ofile)
                elif typ == "BOX" or typ == "BOXLABEL":
                    print(lbl + ":", file=ofile)
                    for line in json_data[FI][key].split('\n'):
                        print(wrapper.fill(text=line), file=ofile)

        print("", file=ofile)
        print(IMPRESSION, file=ofile)
        for line in json_data[IM].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
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
            exit(1)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Process Error", e.output)
        exit(1)

# define a function that will exit, saving data and creating on-disk report as it does so.
def exit_edit():
    save_data(json_data)
    create_report(reportfl)
    exit(0)

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
