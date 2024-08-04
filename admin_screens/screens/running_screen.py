import tkinter as tk
import _tkinter
import sqlite3
from tkinter import messagebox
from typing import Callable


class RunningScreen:
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
            text="Add Bus Running Details",
            font=("Lao UI", 20, "bold"),
            bg="SkyBlue2",
        )
        sub_title.grid(row=2, column=0, pady=10)

        self.bus_id = tk.IntVar()
        bus_id_label = tk.Label(
            frame, text="Bus ID: ", font=("Lao UI", 11, "bold"), bg="SkyBlue1"
        )
        bus_id_entry = tk.Entry(frame, textvariable=self.bus_id)
        bus_id_label.grid(row=0, column=0, padx=5, pady=5)
        bus_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.running_date = tk.StringVar()
        running_date_label = tk.Label(
            frame,
            text="Running Date (YYYY-MM-DD): ",
            font=("Lao UI", 11, "bold"),
            bg="SkyBlue1",
        )
        running_date_entry = tk.Entry(frame, textvariable=self.running_date)
        running_date_label.grid(row=0, column=2, padx=5, pady=5)
        running_date_entry.grid(row=0, column=3, padx=5, pady=5)

        self.seat_available = tk.IntVar()
        seat_available_label = tk.Label(
            frame,
            text="Seat Available: ",
            font=("Lao UI", 11, "bold"),
            bg="SkyBlue1",
        )
        seat_available_entry = tk.Entry(frame, textvariable=self.seat_available)
        seat_available_label.grid(row=0, column=4, padx=5, pady=5)
        seat_available_entry.grid(row=0, column=5, padx=5, pady=5)

        add_running_but = tk.Button(
            frame,
            text="Add Running Details",
            font=("Lao UI", 11, "bold"),
            bg="SkyBlue4",
            fg="white",
            command=self.add_details,
        )
        add_running_but.grid(row=2, column=2, padx=5, pady=5)
        del_route_but = tk.Button(
            frame,
            text="Delete Running Details",
            font=("Lao UI", 11, "bold"),
            bg="SkyBlue4",
            fg="white",
            command=self.delete_details,
        )
        del_route_but.grid(row=2, column=3, padx=5, pady=5)
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

    def add_details(self) -> None:
        try:
            self.database_manager.running_table.add_running(
                self.bus_id.get(),
                self.running_date.get(),
                self.seat_available.get(),
            )
        except _tkinter.TclError:
            messagebox.showerror(
                "Error", "BUS ID and Seat Available can only be of integer type"
            )
            return
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error", "BUS ID and Running Date combination must be unique"
            )
            return
        except Exception as e:
            messagebox.showerror("Error", e)
            return
        messagebox.showinfo("Success", "Running Details Added Successfully")
        self.info_label.config(
            text=f"{self.bus_id.get()},{self.running_date.get()},\
    {self.seat_available.get()}",
            font=("Lao UI", 10, "bold"),
            bg="SkyBlue3",
        )
        self.info_label.grid(row=0, column=0)
        self.editable_frame.grid(row=3, column=0, pady=30, padx=400)

    def delete_details(self) -> None:
        try:
            self.database_manager.running_table.delete_running(
                self.bus_id.get(), self.running_date.get()
            )
        except _tkinter.TclError:
            messagebox.showerror("Error", "Route ID or Running Date is invalid")
            return
        except Exception as e:
            messagebox.showerror("Error", e)
            return
        messagebox.showinfo("Success", "Running Details Deleted Successfully")


if __name__ == "__main__":
    root = tk.Tk()
    app = RunningScreen()
    app.create_screen(root, app.create_screen)
