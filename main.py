import tkinter as tk
from admin_screens import admin
from database import database_manager
from user_screens import booking_screen
from user_screens import check_screen


class Application:
    def __init__(self):
        self.root = None
        self.admin_screen = admin.ApplicationAdmin()
        self.booking_screen = booking_screen.BookingScreen()
        self.check_screen = check_screen.BookingCheckScreen()
        self.database_manager = database_manager.DatabaseManager("221b105_booking_db.db")

    def splash_screen(self):
        self.root = tk.Tk()
        self.root.title("Bus Reservation System")
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.root.config(bg="SkyBlue1")
        frame = tk.Frame(self.root, bg="SkyBlue1")
        logo = tk.PhotoImage(file="bus_img.png")
        label = tk.Label(frame, image=logo, bg="SkyBlue1")
        label.grid(row=0, column=0, padx=250, pady=10)
        title = tk.Label(
            frame,
            text="Bus Reservation System",
            font=("Lao UI", 30, "bold"),
            bg="SkyBlue4",
        )
        title.grid(row=1, column=0)
        name = tk.Label(
            frame, text="Name: Ashutosh Sultania", font=("Lao UI", 15), bg="SkyBlue1"
        )
        name.grid(row=2, column=0, pady=5)
        eno = tk.Label(
            frame,
            text="Enrollment No: 221B105 (B4)",
            font=("Lao UI", 15),
            bg="SkyBlue1",
        )
        eno.grid(row=3, column=0)
        mobile = tk.Label(
            frame, text="Mobile: 7905278231", font=("Lao UI", 15), bg="SkyBlue1"
        )
        mobile.grid(row=4, column=0)
        footer = tk.Label(
            frame,
            text="Submitted To: Dr. Mahesh Kumar",
            font=("Lao UI", 20, "bold"),
            bg="SkyBlue4",
        )
        footer.grid(row=5, column=0, pady=70)
        name = tk.Label(
            frame,
            text="Project Based Learning (AP LAB 1)",
            font=("Lao UI", 18),
            bg="SkyBlue1",
        )
        name.grid(row=6, column=0, pady=5)
        frame.grid(row=0, column=0, padx=300, pady=100)
        self.root.bind('<KeyPress>',self.home_screen)
        self.root.mainloop()

    def home_screen(self, caller_root: tk.Tk = None):
        if caller_root and type(caller_root)==tk.Tk:
            caller_root.destroy()
        else:
            self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Bus Reservation System")
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        
        self.root.config(bg="SkyBlue1")
        frame = tk.Frame(self.root, bg="SkyBlue1")
        logo = tk.PhotoImage(file="bus_img.png")
        label = tk.Label(self.root, image=logo, bg="SkyBlue1")
        label.grid(row=0, column=0, padx=250, pady=10)
        title = tk.Label(
            self.root,
            text="Bus Reservation System",
            font=("Lao UI", 30, "bold"),
            bg="SkyBlue4",
        )
        title.grid(row=1, column=0)
        book_but = tk.Button(
            frame,
            text="Book Ticket",
            font=("Lao UI", 12, "bold"),
            bg="SkyBlue4",
            fg="white",
            command=lambda: self.booking_screen.create_screen(
                self.root, self.home_screen, self.database_manager
            ),
        )
        book_but.grid(row=0, column=0, padx=5)
        check_but = tk.Button(
            frame,
            text="Check Ticket",
            font=("Lao UI", 12, "bold"),
            bg="SkyBlue4",
            fg="white",
            command=lambda: self.check_screen.create_screen(
                self.root, self.home_screen, self.database_manager
            ),
        )
        check_but.grid(row=0, column=1, padx=5)
        add_but = tk.Button(
            frame,
            text="Add Bus",
            font=("Lao UI", 12, "bold"),
            bg="SkyBlue4",
            fg="white",
            command=lambda: self.admin_screen.create_admin_screen(
                self.root, self.home_screen, self.database_manager
            ),
        )
        add_but.grid(row=0, column=2, padx=5)
        info_label = tk.Label(
            frame,
            text="For Admin Only",
            font=("Lao UI", 10, "bold"),
            bg="SkyBlue3",
        )
        info_label.grid(row=1, column=2, pady=5)
        frame.grid(row=2, column=0, pady=100, padx=500)
        self.root.mainloop()


application = Application()
application.splash_screen()