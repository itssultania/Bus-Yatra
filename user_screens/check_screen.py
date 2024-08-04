import tkinter as tk
import sqlite3
import re
from tkinter import messagebox
from typing import Callable


class BookingCheckScreen:
    def create_screen(
        self, root: tk.Tk, back_screen: Callable, database_manager: object = None
    ) -> None:
        self.database_manager = database_manager
        self.back_screen = back_screen
        self.root = root
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
        sub_title = tk.Label(
            self.root,
            text="Check Your Booking",
            font=("Lao UI", 20, "bold"),
            bg="SkyBlue2",
        )
        sub_title.grid(row=2, column=0, pady=10)

        self.phone_number = tk.StringVar()
        phone_number_label = tk.Label(
            frame, text="Phone Number: ", font=("Lao UI", 11, "bold"), bg="SkyBlue1"
        )
        phone_number_entry = tk.Entry(frame, textvariable=self.phone_number)
        phone_number_label.grid(row=0, column=0, padx=5, pady=5)
        phone_number_entry.grid(row=0, column=1, padx=5, pady=5)

        check_booking = tk.Button(
            frame,
            text="Check Booking",
            font=("Lao UI", 11, "bold"),
            bg="SkyBlue4",
            fg="white",
            command=self.check_booking,
        )
        check_booking.grid(row=0, column=3, padx=5, pady=5)

        back_but = tk.Button(
            frame,
            text="Back",
            font=("Lao UI", 12, "bold"),
            bg="SkyBlue4",
            fg="white",
            command=lambda: self.back_screen(self.root),
        )
        back_but.grid(row=0, column=4, padx=5, pady=30)
        frame.grid(row=3, column=0, pady=50, padx=400)
        self.root.mainloop()

    def check_booking(self):
        phone_number = self.phone_number.get()
        if not phone_number:
            raise Exception("Phone number is required")
        if not re.match(r"^[0-9]{10}$", phone_number):
            raise Exception("Phone number must be 10 digits long")
        try:
            booking_details = self.database_manager.booking_table.get_booking_details(
                phone_number
            )
            if not booking_details:
                messagebox.showerror("Error", "No booking found with this phone number")
                return
            # store booking_details in a variable
            for booking_detail in enumerate(booking_details, start=1):
                self.passanger_name = booking_detail[1][0]
                self.passager_gender = booking_detail[1][1]
                self.seat_count = booking_detail[1][2]
                self.passanger_mobile_no = booking_detail[1][3]
                self.passanger_age = booking_detail[1][4]
                self.operator_name = booking_detail[1][5]
                self.source = booking_detail[1][6]
                self.destination = booking_detail[1][7]
                self.bus_fare = booking_detail[1][8]
                self.running_date = booking_detail[1][9]
                self.booking_date = booking_detail[1][10]
                self.show_booking_details(booking_detail[0])
        except sqlite3.Error:
            messagebox.showerror("Error", "Something went wrong")
            return

    def show_booking_details(self, count=1):
        messagebox.showinfo(
            f"Your Ticket {count}",
      f"PASSENGER NAME: {self.passanger_name}\n\
        PASSANGER GENDER: {self.passager_gender}\n\
        SEAT COUNT: {self.seat_count}\n\
        PASSANGER MOBILE NUMBER: {self.passanger_mobile_no}\n\
        PASSANGER AGE: {self.passanger_age}\n\
        OPERATOR NAME: {self.operator_name}\n\
        SOURCE: {self.source}\n\
        DESTINATION: {self.destination}\n\
        BUS FARE: Rs. {self.bus_fare}\n\
        RUNNING DATE: {self.running_date}\n\
        BOOKING DATE: {self.booking_date}",
        )