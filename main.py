"""
This Pomodoro timer application, built using Python's tkinter library, helps users manage their work and break sessions
through the classic Pomodoro Technique. The application has a simple user interface with visual and auditory cues,
supporting macOS notifications to alert users when it's time to work or take a break.

Modules and Libraries:
    tkinter: Used for building the graphical user interface (GUI).
    subprocess: Used to send macOS notifications and prevent the system from going to sleep during sessions.

Functions:
    reset(event):
        Resets the timer and UI elements when the reset button is double-clicked.
        Cancels any ongoing countdown, resets the session count (reps), clears tick marks, and re-enables the start
        button.
    notify_mac(title, message):
        Sends notifications to macOS users. The title and message content can be customized.
    start_counting():
        Manages the transition between work and break sessions based on the reps count.
        Updates the UI and sends notifications to the user, ensuring that the start button is disabled during active
        sessions.
    count_down(n):
        Handles the countdown mechanism, updating the timer display every second.
        When the countdown reaches zero, it triggers the next session (work or break) and updates the tick marks after
        each completed work session.
"""
# ---------------------------- IMPORTS -----------------------------#
from tkinter import *
import subprocess

# from tkinter import messagebox (in case I change my mind about the warning)
# Importing the necessary modules from the tkinter library.
# The wildcard import (*) brings in all tkinter classes and functions.

# ---------------------------- CONSTANTS ------------------------------- #
# Defining constant values for colors and fonts used in the UI,
# as well as the duration for work, short break, and long break sessions.
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
BUTTON_COLOR = "#FFE8C5"
FONT_NAME = "Courier"
WORK_MIN = 25  # Work session duration in minutes
SHORT_BREAK_MIN = 5  # Short break duration in minutes
LONG_BREAK_MIN = 20  # Long break duration in minutes

# ---------------------------- Global Variables ----------------------------#
# Declaring global variables to keep track of the session count (reps),
# the tick marks (ticks) to show progress, and the timer for scheduling the countdown.
reps = 0
ticks = ""
timer = ""


# ---------------------------- TIMER RESET ------------------------------- #
# Placeholder for the timer reset function, which is  used
# to reset the timer and UI elements when the user clicks the reset button.
# Reset function to stop the current timer and reset all variables/UI elements to their initial state.
def reset(event):
    global timer, reps, ticks

    # Optional: Use a confirmation dialog before resetting (commented out).
    # if messagebox.askokcancel("Confirm Reset", "Are you sure you want to reset the timer?"):

    window.after_cancel(timer)  # Cancel the scheduled count_down function.
    reps = 0  # Reset the session counter.
    ticks = ""  # Clear the tick marks.

    # Reset the timer display, tick mark label, and timer label to their default states.
    canvas.itemconfig(canvas_text, text=f"{WORK_MIN}:00")  # Reset the timer display on the canvas.
    tick_lbl.config(text=ticks)  # Clear the tick mark label.
    timer_lbl.config(text="Timer", fg=GREEN)  # Reset the timer label.
    start_btn.config(state="normal")  # Re-enable the Start button.


# ---------------------------- NOTIFICATIONS ------------------------------- #
def notify_mac(title, message):
    subprocess.run([
        "osascript", "-e",
        f'display notification "{message}" with title "{title}"'
    ])


# ---------------------------- TIMER MECHANISM ------------------------------- #
# Placeholder for the timer mechanism function, which will later be used
# to manage the transition between work and break sessions.
# Start counting function to initiate the timer mechanism.
def start_counting():
    start_btn.config(state="disabled")  # Disable the start button to prevent multiple clicks.
    # Convert work, short break, and long break durations from minutes to seconds.
    work_sec = WORK_MIN * 60
    short_brk_sec = SHORT_BREAK_MIN * 60
    long_brk_sec = LONG_BREAK_MIN * 60

    # Bring attention to the app before starting next countdown
    window.deiconify()  # Restore if minimized
    window.lift()  # Bring to top
    window.focus_force()  # Force focus

    global reps, ticks
    if reps < 15:  # Continue the cycle for a total of 15 repetitions (7 work sessions + 7 short breaks + 1 long break).
        reps += 1

        if reps % 2 == 1:  # Odd-numbered reps represent work sessions.
            if reps > 1:
                notify_mac(title="Work Time!", message="Time to focus.")  # Send notification before starting countdown
            timer_lbl.config(text="Work", fg=GREEN)  # Update the label to indicate a work session.
            count_down(work_sec - 1)  # Start the countdown for the work session.

        elif reps % 8 == 0:  # Every 8th rep is a long break.
            timer_lbl.config(text="Rest", fg=RED)  # Update the label to indicate a long break.
            notify_mac(title="Rest Time!", message="Take some rest.")  # Send notification before starting countdown
            count_down(long_brk_sec - 1)  # Start the countdown for the long break.

        else:  # Even-numbered reps (except for the 8th) represent short breaks.
            timer_lbl.config(text="Break", fg=PINK)  # Update the label to indicate a short break.
            notify_mac(title="Break Time!", message="Be back feeling refreshed.")  # Notify before starting countdown
            count_down(short_brk_sec)  # Start the countdown for the short break.
    else:  # After 15 repetitions, the Pomodoro session is complete.
        ticks += "✓️"  # Add a final tick mark.
        tick_lbl.config(text=ticks)  # Update the tick mark label.
        timer_lbl.config(text="Done!", fg="dark green")  # Indicate that the Pomodoro session is complete.


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
# Function to manage the countdown timer.
def count_down(n):
    global ticks, timer
    minutes = n // 60  # Calculate the number of minutes
    seconds = n % 60  # Calculate the number of seconds

    if n >= 0:  # If there is still time left
        display_text = f"{minutes}:{seconds}"
        if seconds < 10:  # Ensures the seconds are displayed with two digits
            display_text = f"{minutes}:0{seconds}"
        canvas.itemconfig(canvas_text, text=display_text)  # Update the canvas with the new time
        timer = window.after(1000, count_down, n - 1)  # Call count_down again after 1 second

    else:

        start_counting()  # Start the next session (work/break) when countdown is complete

        if reps % 2 == 0:  # Add a tick mark for every completed work session
            ticks += "✓️"
        elif reps % 9 == 0:  # Reset tick marks after 4 work sessions (Pomodoro cycles)
            ticks = ""
        tick_lbl.config(text=ticks)  # Update the tick mark label


# ---------------------------- UI SETUP ------------------------------- #
# Set up the user interface components using Tkinter

# Window
window = Tk()
window.title("Pomodoro (Tomato)")  # Set the title of the window
window.config(pady=50, padx=100, bg=YELLOW)  # Configure padding and background color

# Timer label
timer_lbl = Label(text="Timer", bg=YELLOW, pady=10, fg=GREEN, font=(FONT_NAME, 45, "normal"))
timer_lbl.grid(column=1, row=0)  # Position the timer label at the top center


# Canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)  # Create a canvas for drawing
tomato_img = PhotoImage(file="tomato.png")  # Load the tomato image for display
canvas.create_image(100, 112, image=tomato_img)  # Position the tomato image on the canvas
canvas_text = canvas.create_text(100, 130, text=f"{WORK_MIN}:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)  # Position the canvas in the center

# ---------------------------- BUTTONS ------------------------------- #
# Functions and UI components for the Start and Reset buttons.

# Create the Start button with the above start_counting function as its command.
start_btn = Button(text="Start", font=(FONT_NAME, 16, "bold"), highlightthickness=0, command=start_counting)
start_btn.grid(column=0, row=2)  # Position the Start button in the UI.

# Create the Reset button with the above reset function as its command.
reset_btn = Button(text="Reset", font=(FONT_NAME, 16, "bold"), highlightthickness=0)
reset_btn.bind("<Double-1>", reset)  # Resets after double click
reset_btn.grid(column=2, row=2)  # Position the Reset button in the UI.

# ---------------------------- TICK MARK LABEL ------------------------------- #
# Label to display tick marks indicating the number of completed work sessions.
tick_lbl = Label(text="", fg=GREEN, bg=YELLOW, highlightthickness=0, font=("", 35, "bold"))
tick_lbl.grid(column=1, row=3)  # Position the tick mark label below the canvas.

# ---------------------------- MAINLOOP ------------------------------- #
# Start the Tkinter event loop to listen for user interactions.
subprocess.Popen(["caffeinate"])  # Start caffeinate to prevent sleep
window.mainloop()
