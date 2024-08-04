import tkinter as tk
import _tkinter
import sqlite3
from tkinter import messagebox
from typing import Callable


class OperatorScreen:
    def create_screen(
        self, root: tk.Tk, back_screen: Callable, database_manager: object = None
    ) -> None:
        self.database_manager = database_manager
        self.back_screen = back_screen
        self.root = root
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Bus Reservation System |")
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
            text="Add Bus Operator Details",
            font=("Lao UI", 20, "bold"),
            bg="SkyBlue2",
        )
        sub_title.grid(row=2, column=0, pady=10)

        self.operator_id = tk.IntVar()
        operator_id_label = tk.Label(
            frame, text="Operator ID: ", font=("Lao UI", 11, "bold"), bg="SkyBlue1"
        )
        operator_id_entry = tk.Entry(frame, textvariable=self.operator_id)
        operator_id_label.grid(row=0, column=0, padx=5, pady=5)
        operator_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.operator_name = tk.StringVar()
        operator_name_label = tk.Label(
            frame, text="Operator Name: ", font=("Lao UI", 11, "bold"), bg="SkyBlue1"
        )
        operator_name_entry = tk.Entry(frame, textvariable=self.operator_name)
        operator_name_label.grid(row=0, column=2, padx=5, pady=5)
        operator_name_entry.grid(row=0, column=3, padx=5, pady=5)

        self.operator_address = tk.StringVar()
        operator_address_label = tk.Label(
            frame,
            text="Operator Address: ",
            font=("Lao UI", 11, "bold"),
            bg="SkyBlue1",
        )
        operator_address_entry = tk.Entry(frame, textvariable=self.operator_address)
        operator_address_label.grid(row=0, column=4, padx=5, pady=5)
        operator_address_entry.grid(row=0, column=5, padx=5, pady=5)

        self.operator_phone = tk.StringVar()
        operator_phone_label = tk.Label(
            frame, text="Operator Phone: ", font=("Lao UI", 11, "bold"), bg="SkyBlue1"
        )
        operator_phone_entry = tk.Entry(frame, textvariable=self.operator_phone)
        operator_phone_label.grid(row=1, column=1, padx=5, pady=5)
        operator_phone_entry.grid(row=1, column=2, padx=5, pady=5)

        self.operator_email = tk.StringVar()
        operator_email_label = tk.Label(
            frame, text="Operator Email: ", font=("Lao UI", 11, "bold"), bg="SkyBlue1"
        )
        operator_email_entry = tk.Entry(frame, textvariable=self.operator_email)
        operator_email_label.grid(row=1, column=3, padx=5, pady=5)
        operator_email_entry.grid(row=1, column=4, padx=5, pady=5)

        add_operator_but = tk.Button(
            frame,
            text="Add Operator",
            font=("Lao UI", 11, "bold"),
            bg="SkyBlue4",
            fg="white",
            command=self.add_details,
        )
        add_operator_but.grid(row=2, column=2, padx=5, pady=5)
        edit_operator_but = tk.Button(
            frame,
            text="Edit Operator",
            font=("Lao UI", 11, "bold"),
            bg="SkyBlue4",
            fg="white",
            command=lambda: self.add_details(True),
        )
        edit_operator_but.grid(row=2, column=3, padx=5, pady=5)
        back_but = tk.Button(
            frame,
            text="Back",
            font=("Lao UI", 12, "bold"),
            bg="SkyBlue4",
            fg="white",
            command=lambda: self.back_screen(
                root=self.root, database_manager=self.database_manager
            ),
        )
        back_but.grid(row=3, column=4, pady=60)
        frame.grid(row=3, column=0, pady=50, padx=400)
        self.editable_frame = tk.Frame(self.root, bg="SkyBlue1")
        self.info_label = tk.Label(
            self.editable_frame,
            bg="SkyBlue1",
        )
        self.root.mainloop()

    def add_details(self, edit_operator: bool = False) -> None:
        try:
            self.database_manager.operator_table.add_operator(
                self.operator_id.get(),
                self.operator_name.get(),
                self.operator_address.get(),
                self.operator_phone.get(),
                self.operator_email.get(),
                edit_operator,
            )
        except _tkinter.TclError:
            messagebox.showerror("Error", "Operator ID can only be of integer type")
            return
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Operator ID already exists")
            return
        except Exception as e:
            messagebox.showerror("Error", e)
            return
        if edit_operator:
            msg_part = "edited"
        else:
            msg_part = "added"
        messagebox.showinfo("Success", f"Operator details {msg_part} successfully")
        self.info_label.config(
            text=f"{self.operator_id.get()},{self.operator_name.get()},\
{self.operator_address.get()}, {self.operator_phone.get()}\
{self.operator_email.get()}",
            font=("Lao UI", 10, "bold"),
            bg="SkyBlue3",
        )
        self.info_label.grid(row=0, column=0)
        self.editable_frame.grid(row=3, column=0, pady=30, padx=400)


if __name__ == "__main__":
    root = tk.Tk()
    app = OperatorScreen()
    app.create_screen(root, app.create_screen)
