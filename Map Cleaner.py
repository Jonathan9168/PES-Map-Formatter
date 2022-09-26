import os
import fileinput
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk, IcoImagePlugin

''' FORMAT OF ASSIGNMENT LINES SHOULD BE AS FOLLOWS:

    TEAMID, STDID, STADIUMNAME, FOLDER  #TEAMNAME
    OR
    TEAMID, STDID, STADIUMNAME, FOLDER

    Trailing commas are also fine 
    E.g. TEAMID, STDID, STADIUMNAME, FOLDER,,,  #TEAMNAME

    The program will work to neaten the file.

    Leave the icon in the folder or the app won't open
'''


def configure_file_path(file_path):
    if "{" and "}" in file_path:
        return file_path[1:-1]
    return file_path


def configure_name_path(file_name):
    if "}" in file_name:
        return file_name[:-1]
    return file_name


def process_file(event):
    file_path, file_name = event.data, os.path.basename(event.data)
    file_path, file_name = configure_file_path(file_path), configure_name_path(file_name)

    print("-----------------------")
    print(f'File Path: {file_path}')
    print(f'File Name: {file_name}')
    print("-----------------------")

    if file_name.endswith('.txt'):
        format_assignments(file_path)
    else:
        messagebox.showerror('Error', 'File type not supported.')


def format_assignments(file_path):
    formatted_assignments = []
    with open(file_path, encoding="utf-8") as map_teams:
        for assignment in map_teams:
            try:
                # check assignment starts with an ID. If so, format the assignment else skip the line
                print(f'Team ID: {int(assignment.split(",")[0])}')
                assignment = remove_hash_n_tabs(assignment)
                split_assignment = insert_commas(assignment)
                try:
                    if len(split_assignment) > 4 and split_assignment[-1] != "":
                        split_assignment = hash_team_name(split_assignment)
                        formatted_assignments.append(
                            f"{split_assignment[0]:<10} {split_assignment[1]:<10} {split_assignment[2]:<50} {split_assignment[3]:<50} {split_assignment[-1]:<25}".strip())
                    else:
                        formatted_assignments.append(
                            f"{split_assignment[0]:<10} {split_assignment[1]:<10} {split_assignment[2]:<50} {split_assignment[3]:<50}".strip())
                except IndexError:
                    continue
            except ValueError:
                continue
    generate_file(file_path, formatted_assignments)


def generate_file(file_path, formatted_assignments):
    """Generates a new file and saves previous as a .bak file"""
    with fileinput.FileInput(file_path, inplace=True, backup='.bak', encoding='utf-8-sig') as map_teams:
        count = 0
        for assignment in map_teams:
            try:
                int(assignment.split(",")[0])
                print(formatted_assignments[count])
                count += 1
            except ValueError:
                print(assignment.strip())
                continue
    tk.messagebox.showinfo(title="Success", message="Done")


def remove_hash_n_tabs(assignment):
    """Removes hashes and tabs
FROM ---> 121, 	   030,      San Siro, San Siro	  # Milan
TO --->   121, 	   030,      San Siro, San Siro	  , Milan"""
    assignment = assignment.replace("#", ",")
    assignment = assignment.replace("\t", "")
    return assignment


def insert_commas(assignment):
    """Adds commas to first 3 assignment strings and strips empty space from each string
E.g. TID, STID, STNAME,
"""
    split_assignment = assignment.split(",")
    for i, v in enumerate(split_assignment):
        split_assignment[i] = split_assignment[i].strip()
    for j in range(3):
        split_assignment[j] = split_assignment[j] + ","
    return split_assignment


def hash_team_name(split_assignment):
    """If a team name exists at the end of the line, add hash tag
FROM ---> 121,030,SanSiro,SanSiro,Milan
TO ---> 121,030,San Siro,San Siro,# Milan"""
    split_assignment[-1] = f"# {split_assignment[-1]}"
    return split_assignment


'''GUI canvas Enter and Leave background colour handlers'''


def on_enter(event):
    canvas.config(background="#5b5b5b")


def on_leave(event):
    canvas.config(background="grey")


'''GUI Declaration'''
root = TkinterDnD.Tk()
width, height = 280, 130
canvas = tk.Canvas(root, width=width, height=height, background="grey")
canvas.grid(columnspan=1)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', process_file)
root.dnd_bind('<<DropEnter>>', on_enter)
root.dnd_bind('<<DropLeave>>', on_leave)
root.dnd_bind('<Enter>', on_enter)
root.dnd_bind('<Leave>', on_leave)
root.resizable(False, False)

root.title("Map Cleaner")
root.iconbitmap("icon.ico")

img = Image.open("icon.ico")

img = img.resize((100, 100))
img = ImageTk.PhotoImage(img, Image.Resampling.LANCZOS)

canvas.create_image(width / 2, height / 2, anchor='center', image=img)

root.mainloop()
