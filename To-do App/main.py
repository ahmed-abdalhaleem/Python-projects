# Import Required Modules
import tkinter as tk 
from tkinter import scrolledtext
import json
from functools import partial



# Required Attributes

tasks_list = []

selected_task_index = 0

current_operation = ""



# parse json file [step 1]
try:
    with open('data/.tasks.json', 'r') as f:
        tasks_list = json.load(f)
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")



# Required Methods

# ==>> primary methods

def filter_by_status(status):

    global tasks_list
    
    filtered_list = []

    for task in tasks_list:
        if task['completed'] == status:
            filtered_list.append(task)
    
    return filtered_list


def fill_frame(frame_to_fill, list_of_tasks_to_be_filled):
    """
    frame_to_fill-----------: could be tasks_container_uncompleted_frm, tasks_container_completed_frm
    list_of_tasks_to_be_filled---: could be uncompleted tasks, completed tasks based on frame
    dict_of_controllers-----: the controllers of task 
        uncompleted---: {'finish': complete_task, 'delete': delete_task, 'edit': edit_task}
        completed-----: {'restore': complete_task, 'delete': delete_task}
    """

    global tasks_list

    if frame_to_fill == tasks_container_completed_frm:
        list_of_operations = ["delete", "restore"]
    else: 
        list_of_operations = ["delete", "edit", "finish"]

    sub_frames_list = []

    for task in list_of_tasks_to_be_filled:
        
        sub_frames_list.append(tk.Frame(master=frame_to_fill))

        index_in_frm = list_of_tasks_to_be_filled.index(task)
        
        sub_frames_list[index_in_frm].pack(fill='x', expand=True)

        tk.Button(master=sub_frames_list[index_in_frm], text=task['title'], anchor='w',
        command=partial(preview_task, tasks_list.index(task))).pack(side='left', fill='both', expand=True)

        for operation in list_of_operations:
            tk.Button(master=sub_frames_list[index_in_frm], text=operation,
            command=partial(select_task_to, operation, tasks_list.index(task))
            ).pack(side='left', fill='both')
    return


def select_task_to(operation, index):

    global selected_task_index
    global current_operation

    selected_task_index = index

    current_operation = operation

    # redirect the excution flow

    if operation == "delete":
        delete_task(index)
    elif operation == "finish":
        complete_task(index)
    elif operation == "restore":
        restore_task(index)
    elif operation == "edit":
        edit_task_button_click()
    return


def preview_task(index):

    # view the task details in the preview section 
    change_preview_section_content(index)

    # no message
    message_to_user_lbl.configure(text="")
    return



def change_status(index):

    global tasks_list
    
    tasks_list[index]['completed'] = not tasks_list[index]['completed']
    return


def change_task_position_to_the_beginnig_of_tasks_list(index):

    global tasks_list

    task = tasks_list[index]
    tasks_list.pop(index)
    tasks_list.insert(0, task)
    return


def destroy_inner_content_of_frame(frame):

    for widget in frame.winfo_children():
        widget.destroy()
    return


def hide_section_s(*list_of_sections):

    for section in list_of_sections:
        section.grid_forget()
    return


def show_section_s(*list_of_sections):

    for section in list_of_sections:
        section.grid(pady=20, padx=10, sticky='we')
    return



def change_preview_section_content(index = None):

    global tasks_list

    if index == None:
        title = "Select any task to preview here!"
        description = "Select any task to view its description here!"
        status = ""
    else:
        title = tasks_list[index]['title']
        description = tasks_list[index]['description']
        status = "completed" if tasks_list[index]['completed'] == True else "Un Completed"

    # set the task title to the title box
    selected_task_title_txt.configure(state="normal")
    selected_task_title_txt.delete('1.0', 'end')
    selected_task_title_txt.insert('1.0', title)
    selected_task_title_txt.configure(state="disabled")

    # set the task description to the description box
    selected_task_description_txt.configure(state="normal")
    selected_task_description_txt.delete('1.0', 'end')
    selected_task_description_txt.insert('1.0', description)
    selected_task_description_txt.configure(state="disabled")

    # set the status
    status_lbl.configure(text=status)
    return


def clean_preview_section():

    change_preview_section_content()
    return


def update_window_after_operations():

    clean_preview_section()
    destroy_inner_content_of_frame(tasks_container_uncompleted_frm)
    destroy_inner_content_of_frame(tasks_container_completed_frm)
    fill_frame(tasks_container_uncompleted_frm, filter_by_status(False))
    fill_frame(tasks_container_completed_frm, filter_by_status(True))
    return


# ==>> Events handling methods:
            # after any operation : update window.
            # any operation should be followed by a message.

# operations : [delete, complete, restore, edit, add]

def delete_task(index):

    global tasks_list

    # pick the old task to configure the message label
    old_task = tasks_list[index]['title']

    # delete the task from the tasks list 
    tasks_list.pop(index)

    # update the window after operation
    update_window_after_operations()

    # message 
    message_to_user_lbl.configure(text=f"Task '{old_task}' has been deleted")
    return


def complete_task(index):

    global tasks_list

    # change the task status [false => true]
    change_status(index)

    # change task position to the beginning of the tasks list
    change_task_position_to_the_beginnig_of_tasks_list(index)

    # update the window after operation
    update_window_after_operations()

    # message
    message_to_user_lbl.configure(text=f"Congratulations!\nTask: '{tasks_list[0]['title']}' has been completed.")
    return


def restore_task(index):

    global tasks_list

    # change the task status [true => false]
    change_status(index)

    # change task position to the beginning of the tasks list
    change_task_position_to_the_beginnig_of_tasks_list(index)

    # update the window after operation
    update_window_after_operations()

    # message 
    message_to_user_lbl.configure(text=f"Task: '{tasks_list[0]['title']}' has been restored to uncompleted tasks.")
    return


def edit_task_button_click():

    global tasks_list
    global selected_task_index

    # hide all frames
    hide_section_s(preview_frm, uncompleted_tasks_frm, completed_tasks_frm)

    # show entry frame
    show_section_s(entry_frm)

    # set the heading by 'Edit the task'
    entry_heading_lbl.configure(text="Edit the task")

    # show the operation title to the user
    message_to_user_lbl.configure(text="")

    # set the task wanted to edit to the entry widgets
    entry_title_txt.insert('1.0', tasks_list[selected_task_index]['title'])
    entry_description_txt.insert('1.0', tasks_list[selected_task_index]['description'])

    # set the focus to the title box
    entry_title_txt.focus_set()
    return


def add_new_task_button_click():

    global current_operation

    current_operation = "add"

    # hide all frames
    hide_section_s(preview_frm, uncompleted_tasks_frm, completed_tasks_frm)

    # show entry frame
    show_section_s(entry_frm)

    # set the heading by 'Add new task'
    entry_heading_lbl.configure(text="Add New Task")

    # set the focus to the title box
    entry_title_txt.focus_set()
    return


def submit():

    global tasks_list
    global selected_task_index
    global current_operation

    # message to user
    msg = ""

    # make sure the title is setted
    if entry_title_txt.get('1.0', 'end').strip() == '':
        message_to_user_lbl.configure(text="please, write the task title to submit.")
        return

    # if the operation is edit => delete the selected task from tasks list
    old_task_title = ""
    if current_operation == "edit":
        old_task_title = tasks_list[selected_task_index]['title']
        tasks_list.pop(selected_task_index)

    # make the task
    new_task = {
        "title": entry_title_txt.get('1.0', 'end').strip(),
        "completed": False, # is always false as the the edit operation is only allowed for umcompleted tasks.
        "description": entry_description_txt.get('1.0', 'end').strip()
    }

    # append the task to the beginnig of the tasks list
    tasks_list.insert(0, new_task)

    # clean the section
    clean_edit_add_section() # not declared

    # hide the edit/add section
    hide_section_s(entry_frm)

    # show other sections
    show_section_s(preview_frm, uncompleted_tasks_frm, completed_tasks_frm)

    # update the window after operation
    update_window_after_operations()

    # message to the user
    # if current_operation == "add":
    #     new_task_title = new_task['title']
    #     message_to_user_lbl.configure(text=f"New task: '{new_task_title}' has been added successfully!")
    # elif current_operation == "edit" and old_task_title == new_task_title:
    #     message_to_user_lbl.configure(text=f"Task: '{old_task_title}' has been edited successfully!")
    # else:
    #     message_to_user_lbl.configure(text=f"Task: '{old_task_title}' has been changed to:\n{new_task_title} successfully!")
    message_to_user_lbl.configure(
        text=f"Task is {current_operation}ed successfully!"
    )
    return


def clean_edit_add_section():

    entry_title_txt.delete('1.0', 'end')

    entry_description_txt.delete('1.0', 'end')
    return


def reset():

    global current_operation

    # if operation is edit => no changes
    if current_operation == "edit":
        message_to_user_lbl.configure(text="Please, press submit to save changes or cancel for no changes")

        # set focus to the the title box
        entry_title_txt.focus_set()
        return

    # clean the section
    clean_edit_add_section()

    # set focus to the the title box
    entry_title_txt.focus_set()
    return


def cancel():

    # clean the section
    clean_edit_add_section()

    # hide add/edit section
    hide_section_s(entry_frm)

    # show other sections
    show_section_s(preview_frm, uncompleted_tasks_frm, completed_tasks_frm)

    # no message
    message_to_user_lbl.configure(text="Select a task to preview, and manage your tasks freely!")
    return


# #############################################################################################

# Implement GUI [step 2]

# Create the main window and set configurations and make a main container in the main window.
window = tk.Tk()
window.title("Task Manager")
window.resizable(width=False, height=False)


# main container frame
main_container_frm = tk.Frame(master=window, relief='solid', border=2, padx=20, pady=20)
main_container_frm.pack()

# message to user label
message_to_user_lbl = tk.Label(
    master=main_container_frm, anchor='w',  justify='left',
    text="Hello again, You seem have awesome work today, Manage your tasks freely"
)
message_to_user_lbl.grid(sticky='nsew', padx=10, pady=0)



# #############################################################################################

# Preview tasks sections

# preview frame
preview_frm = tk.Frame(master=main_container_frm, relief='solid', border=2, padx=3, pady=3)
preview_frm.grid(pady=20, padx=10, sticky='we')


# labels for preview widgets
tk.Label(master=preview_frm, text="Title", anchor='w').grid(row=0, column=0, columnspan=4, sticky='w')
tk.Label(master=preview_frm, text="Status").grid(row=0, column=4, columnspan=2, sticky='w')
tk.Label(master=preview_frm, text="Description", anchor='w').grid(row=2, column=0, columnspan=6, sticky='w')


# selected task title text box
selected_task_title_txt = tk.Text(master=preview_frm, height=1, relief='flat', pady=2, padx=10,)
selected_task_title_txt.grid(row=1, column=0, sticky='WENS', columnspan=4)
selected_task_title_txt.insert('1.0', "Select any taks to preview here!")
selected_task_title_txt.configure(state="disabled")


# selected task description text box
selected_task_description_txt = scrolledtext.ScrolledText(master=preview_frm, height=5, relief='flat', wrap='word', pady=2, padx=10)
selected_task_description_txt.grid(row=3, column=0, sticky='WENS', columnspan=6)
selected_task_description_txt.insert('1.0', "select any task to view its description here!")
selected_task_description_txt.configure(state="disabled")


# status label
status_lbl = tk.Label(master=preview_frm, padx=15, pady=5, bg="white", width=10)
status_lbl.grid(row=1, column=4, columnspan=2, sticky='WENS', padx=5, pady=0)



# #############################################################################################

# Entry section

# Entry frame 'initially hidden'
entry_frm = tk.Frame(master=main_container_frm, relief='solid', border=2, padx=3, pady=3)

entry_heading_lbl = tk.Label(master=entry_frm)
entry_heading_lbl.pack(fill='x', expand=True)

# Horizontal dashed line
tk.Label(master=entry_frm, text=f"{'-'*170}").pack()

tk.Label(master=entry_frm, text="Title", justify='left', anchor='w').pack(fill='x', expand=True)

entry_title_txt = tk.Text(master=entry_frm, height=1, relief='flat', wrap='word', pady=2, padx=10)
entry_title_txt.pack(fill='x')

tk.Label(master=entry_frm, text="Description", justify='left', anchor='w').pack(fill='x', expand=True)

entry_description_txt = scrolledtext.ScrolledText(
    master=entry_frm,
    height=5, wrap='word'
)
entry_description_txt.pack(fill='x')


entry_control_frm = tk.Frame(master=entry_frm)
entry_control_frm.pack(fill='x', expand=True)

tk.Button(master=entry_control_frm, text="cancel", command=cancel).pack(side='left', fill='x', expand=True)
tk.Button(master=entry_control_frm, text="reset", command=reset).pack(side='left', fill='x', expand=True)
tk.Button(master=entry_control_frm, text="submit", command=submit).pack(side='left', fill='x', expand=True)



# #############################################################################################

# uncompleted tasks sections

# uncompleted tasks frame
uncompleted_tasks_frm = tk.Frame(master=main_container_frm, relief='solid', border=2, padx=3, pady=3)
uncompleted_tasks_frm.grid(pady=20, padx=10, sticky='we')


# header of uncompleted tasks frame
header_of_uncompleted_frm = tk.Frame(master=uncompleted_tasks_frm)
header_of_uncompleted_frm.pack(fill='x',expand=True)


# Uncompleted Header Label
tk.Label(master=header_of_uncompleted_frm,
    text="Uncompleted  Tasks",
    padx=10, pady=0,
    anchor="w"
    ).pack(
        fill='x', side='left', expand=True
        )


# add new task button
add_new_task_btn = tk.Button(master=header_of_uncompleted_frm,
    text="Add New Task",
    bg="violet",
    command=add_new_task_button_click
    )
add_new_task_btn.pack()


# Horizontal dash line
tk.Label(master=uncompleted_tasks_frm, text=f"{'-'*170}").pack()


# task frame
tasks_container_uncompleted_frm = tk.Frame(master=uncompleted_tasks_frm)
tasks_container_uncompleted_frm.pack(fill='x', expand=True, padx=0, pady=0)


# #############################################################################################

# Completed tasks section

# Completed Tasks frame
completed_tasks_frm = tk.Frame(master=main_container_frm, relief='solid', border=2, padx=3, pady=3)
completed_tasks_frm.grid(pady=20, padx=10, sticky='we')


# header of completed tasks frame
header_of_completed_frm = tk.Frame(master=completed_tasks_frm)
header_of_completed_frm.pack(fill='x',expand=True)


# 'Completed' Header Label
tk.Label(master=header_of_completed_frm,
    text="Completed  Tasks",
    padx=10, pady=0,
    anchor="w"
    ).pack(
        fill='x'
        )


# Horizontal dash line
tk.Label(master=header_of_completed_frm, text=f"{'-'*170}").pack()


# task frame
tasks_container_completed_frm = tk.Frame(master=completed_tasks_frm)
tasks_container_completed_frm.pack(fill='x', expand=True, padx=0, pady=0)



# put tasks in them suitable places
fill_frame(tasks_container_uncompleted_frm, filter_by_status(False))

fill_frame(tasks_container_completed_frm, filter_by_status(True))


window.mainloop()


# after the mian window is closed: save changes to json file
with open('data/.tasks.json', 'w') as f:
    json.dump(tasks_list, f, indent=4)

