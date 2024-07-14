import os

print("Hello")

to_do_list = []

def user_command():
    cmd = input("Type your command:\nview(v), add(a), remove(r), edit(e), exit(x): ").lower().strip()

    if cmd in  ["add", "a"]:
        add()
        user_command()
    elif cmd in ["remove", "r"]:
        # remove()
        remove_edit('remove')
        user_command()
    elif cmd in ["edit", "e"]:
        # edit()
        remove_edit('edit')
        user_command()
    elif cmd in ["view", "v"]:
        view()
        user_command()
    elif cmd in ["exit", "x"]:
        print("Thanks")
        exit()
    else :
        os.system("clear")
        print("invalid command")
        user_command()


def add():
    view()
    added = 0
    while True:
        new_task = input("please, write the task(s), (to end, enter an empty task) :\n").strip()

        if new_task:
            to_do_list.append(new_task)
            added += 1
            continue
        else:
            if added == 0:
                print("No tasks are added.")
            elif added == 1:
                print("A new task is added successfully.")
            elif added > 1:
                print(f"There are {added} new tasks added successfully.")

            break
        


def remove_edit(cmd = 'remove'):
    """
    This method can remove and edit task based on cmd
    It removes by default.
    to edit, put the cmd "any value"
    """
    view()
    if not to_do_list: # if to do list is empty > break
        return

    while True: # validate index
        task_number = input("Enter number of task you want to remove: ").strip()
        if task_number.isnumeric():
            task_number = int(task_number)
        else:
            print("index must be a number.")
            continue

        if task_number >=1 and task_number <= len(to_do_list):
            # validation successful
            to_do_list.pop(task_number-1)
            mission = "remov"
            if cmd == "edit": # cmd might be 'edit' but still 'remove'
                new_task = input("Type the new task:\n").strip()
                if new_task: # cmd is 'edit'
                    mission = "edit"
                    to_do_list.insert(task_number-1, new_task)
            print(f"Task is {mission}ed successfully.")
            break
        else:
            print("index is out of scope.")
            continue


def view():
    os.system("clear")
    list_length = len(to_do_list)
    if list_length == 0:
        print("The list is empty.")
    else:
        for task in to_do_list:
            print(f"{ to_do_list.index(task) +1 }- {task}")
    print("=========================================")

user_command()