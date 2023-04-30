# Tune
from tkinter import *
import subprocess
import os
import time
import tkinter as tk
from tkinter import TclError, ttk, messagebox

control_password = '123'
work_dir = os.getcwd() + "\\"
window = tk.Tk()
hour_var = [tk.IntVar() for i in range(24)]
youtube_var = tk.BooleanVar()
all_days_var = tk.BooleanVar()
saves = {'Monday': [],
         'Tuesday': [],
         'Wednesday': [],
         'Thursday': [],
         'Friday': [],
         'Saturday': [],
         'Sunday': []}


def create_pass_frame(container):
    global password_submit_btn, password_entry
    frame = ttk.Frame(container)
    tk.Label(frame, text='Enter password:').grid(row=0, column=0, padx=6)
    password_entry = tk.Entry(frame, show="*", width=25)
    password_entry.grid(row=0, column=1)
    password_submit_btn = tk.Button(frame, text='Submit', width=10, command=lambda pass_entry=password_entry: check_pass(pass_entry))
    password_submit_btn.grid(row=0, column=2, padx=8)
    return frame


def check_pass(password_entry):
    password = password_entry.get()
    if password == control_password:
        button_frame = create_button_frame(window)
        button_frame.grid(column=0, row=1, sticky=N)

        youtube_frame = create_youtube_frame(window)
        youtube_frame.grid(column=0, row=2, sticky=SW, padx=5, pady=10)

        input_frame = create_input_frame(window, hour_var)
        input_frame.grid(column=1, row=1, rowspan=2)

        down_button_frame = create_down_button_frame(window)
        down_button_frame.grid(column=0, columnspan=2, row=3)

        # password_submit_btn['state'] = DISABLED
        # password_entry.delete(0, 'end')
        # password_entry['state'] = DISABLED
        pass_frame.destroy()
    else:
        messagebox.showwarning("Error", "Wrong password!")
        window.destroy()


# create frame of buttons for days of week
def create_button_frame(container):
    global save_days

    frame = ttk.Frame(container)
    for row, key in enumerate(saves.keys()):
        globals()[key.lower()] = ttk.Button(frame, text=key, command=lambda day_of_week=key: show_day(day_of_week))
        globals()[key.lower()].grid(column=0, row=row)
        globals()['save_' + key.lower()] = ttk.Button(frame, text='Save', state=DISABLED,
                                                      command=lambda day_of_week=key: save_day(day_of_week))
        globals()['save_' + key.lower()].grid(column=1, row=row)

    check_all = tk.Checkbutton(frame, text='All days tune', variable=all_days_var, command=activator)
    check_all.grid(column=0, row=7, sticky=W)

    save_days = ttk.Button(frame, text='Save', width=10, command=save_all, state=DISABLED)
    save_days.grid(column=0, row=8, columnspan=2, sticky=EW)

    for widget in frame.winfo_children():
        widget.grid(padx=5, pady=5)

    return frame


def create_youtube_frame(container):
    global search_entry, query, submit_button, hours_scale, minutes_scale, youtube_hours, youtube_minutes

    frame = ttk.Frame(container)

    run_youtube = tk.Checkbutton(frame, text='Run Youtube', variable=youtube_var, command=you_tube)
    run_youtube.grid(column=0, row=0, sticky=W)

    youtube_hours = tk.IntVar()
    youtube_minutes = tk.IntVar()

    hours_label = tk.Label(frame, text="Hours:")
    hours_label.grid(row=1, column=0, columnspan=2, sticky=EW)
    hours_scale = tk.Scale(frame, from_=0, to=23, orient="horizontal", variable=youtube_hours)
    hours_scale.grid(row=2, column=0, columnspan=2,  sticky=EW)

    minutes_label = tk.Label(frame, text="Minutes:")
    minutes_label.grid(row=3, column=0, columnspan=2, sticky=EW)
    minutes_scale = tk.Scale(frame, from_=0, to=55, resolution=5, orient="horizontal", variable=youtube_minutes)
    minutes_scale.grid(row=4, column=0, columnspan=2, sticky=EW)


    search_label = Label(frame, text='Search for:')
    search_label.grid(column=0, row=5, sticky=W)

    query = StringVar()
    search_entry = Entry(frame, width=30, textvariable=query, state=DISABLED)
    search_entry.grid(column=0, row=7, columnspan=2)

    submit_button = ttk.Button(frame, text='Submit', state=DISABLED, command=lambda my_query=query: submit(my_query))
    submit_button.grid(column=0, row=8, sticky=W)

    for widget in frame.winfo_children():
        widget.grid(padx=5, pady=3)

    return frame


def create_input_frame(container, var):
    global hours_check
    frame = ttk.Frame(container)
    hours_check = [tk.Checkbutton(frame, text=f'{i}', variable=var[i], onvalue=1, offvalue=0, state=DISABLED) for i in
                   range(24)]
    for i in range(24):
        hours_check[i].grid(column=0, row=int(f'{i}'), sticky=W)
    for widget in frame.winfo_children():
        widget.grid(padx=50)
    # Check saved hours
    load_saves()
    if all(saves[day_of_week] == saves['Monday'] for day_of_week in saves):
        [var[i].set(1) for i in saves['Monday']]
        for hour in hours_check:
            hour['state'] = NORMAL
        all_days_var.set(1)
        activator()
    return frame


def create_down_button_frame(container):
    frame = ttk.Frame(container)
    ttk.Button(frame, text='Reboot', command=reboot_pc).grid(column=0, row=0)
    ttk.Button(frame, text='Quit', command=window.quit).grid(column=1, row=0)
    ttk.Button(frame, text='Clean all', command=clean_all).grid(column=3, row=0)
    ttk.Button(frame, text='Block all', command=block_all).grid(column=4, row=0)
    for widget in frame.winfo_children():
        widget.grid(padx=4, pady=15)
    return frame


def submit(query):
    if youtube_var.get():
        save_hours()
        with open(work_dir + 'hours.dat', 'a') as saved_hours_w:
            saved_hours_w.write(f'Youtube {youtube_hours.get()}:{youtube_minutes.get()} {query.get()}')


def you_tube():
    if youtube_var.get():
        search_entry['state'] = NORMAL
        submit_button['state'] = NORMAL
        hours_scale['state'] = NORMAL
        minutes_scale['state'] = NORMAL
    else:
        search_entry.delete(0, 'end')
        search_entry['state'] = DISABLED
        submit_button['state'] = DISABLED
        youtube_hours.set(0)
        hours_scale['state'] = DISABLED
        youtube_minutes.set(0)
        minutes_scale['state'] = DISABLED
        save_hours()


def disable_button(*button_name):
    for button in button_name:
        button['state'] = DISABLED


def enable_button(*button_name):
    for button in button_name:
        button['state'] = NORMAL


def load_saves():
    if os.path.isfile(work_dir + 'hours.dat'):
        with open(work_dir + 'hours.dat', 'r') as saved_hours:
            for day in saved_hours.readlines():
                raw_info = day.strip().split()
                if raw_info[0] != 'Youtube':
                    saves[raw_info[0]] = [int(i) for i in raw_info[1:]]
                else:
                    youtube_var.set(1)
                    search_entry['state'] = NORMAL
                    submit_button['state'] = NORMAL
                    youtube_time = raw_info[1].split(':')
                    youtube_hours.set(int(youtube_time[0]))
                    youtube_minutes.set(int(youtube_time[1]))
                    search_entry.insert(0, raw_info[2:])


def show_day(day_of_week):
    # enable checkbuttons
    for hour in hours_check:
        hour['state'] = NORMAL
    # disable all "Save" buttons
    for key in saves.keys():
        disable_button(globals()['save_' + key.lower()])
    # enable one "Save" button
    enable_button(globals()['save_' + day_of_week.lower()])
    for i in range(24):
        hour_var[i].set(0)
    if saves[day_of_week]:
        for hour in saves[day_of_week]:
            hour_var[hour].set(1)
    return day_of_week


# Enable or disable buttons by checkbox
def activator():
    # If checkbox is checked:
    if all_days_var.get():
        enable_button(save_days)
        # Disable buttons of days and saves. Names are from dict "saves"
        for key in saves.keys():
            disable_button(globals()[key.lower()])
            disable_button(globals()['save_' + key.lower()])
        # Activate checkboxes
        for hour in hours_check:
            hour['state'] = NORMAL
        # Set checkboxes to 0
        for i in range(24):
            hour_var[i].set(0)

        # Check if values of hours are the same for every day. If so - activate checkboxes
        if all(saves[day_of_week] == saves['Monday'] for day_of_week in saves):
            [hour_var[i].set(1) for i in saves['Monday']]
    else:
        disable_button(save_days)
        # Set checkboxes to 0
        for i in range(24):
            hour_var[i].set(0)
        # Deactivate checkboxes
        for hour in hours_check:
            hour['state'] = DISABLED
        # Enable buttons of days and saves
        for key in saves.keys():
            enable_button(globals()[key.lower()])


def save_hours():
    with open(work_dir + 'hours.dat', 'w') as saved_hours:
        for day_of_week in saves.keys():
            saved_hours.write(str(day_of_week) + ' ')
            for hour in saves[day_of_week]:
                saved_hours.write(str(hour) + ' ')
            saved_hours.write("\n")


def save_day(day_of_week):
    saves[day_of_week] = [i for i in range(24) if hour_var[i].get() == 1]
    save_hours()
    if youtube_var.get():
        with open(work_dir + 'hours.dat', 'a') as saved_hours_w:
            saved_hours_w.write(f'Youtube {youtube_hours.get()}:{youtube_minutes.get()} {query.get()}')


def save_all():
    state = [hour_var[i].get() for i in range(24)]
    for day_of_week in saves:
        saves[day_of_week] = [i for i in range(24) if state[i] == 1]
    save_hours()
    if youtube_var.get():
        with open(work_dir + 'hours.dat', 'a') as saved_hours_w:
            saved_hours_w.write(f'Youtube {youtube_hours.get()}:{youtube_minutes.get()} {query.get()}')


def block_all():
    for i in range(24):
        hour_var[i].set(1)


def clean_all():
    for i in range(24):
        hour_var[i].set(0)


def reboot_pc():
    subprocess.run(['shutdown', '-s'])
    time.sleep(3)
    window.quit()


def create_main_window():
    global pass_frame
    window.title('Power off schedule')
    window.resizable(False, False)
    # try:
    #     # windows only (remove the minimize/maximize button)
    #     window.attributes('-toolwindow', True)
    # except TclError:
    #     print('Not supported on your platform')
    pass_frame = create_pass_frame(window)
    pass_frame.grid(column=0, row=0, sticky=N, columnspan=2, pady=8)
    window.mainloop()

if __name__ == '__main__':
    create_main_window()
    window.mainloop()
