import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Tkinter Test")
    root.geometry("200x100")
    label = tk.Label(root, text="Tkinter is working!")
    label.pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    main()
