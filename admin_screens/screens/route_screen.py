import tkinter as tk
import _tkinter
import sqlite3
from tkinter import messagebox
from typing import Callable


class RouteScreen:
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
            text="Add Bus Route Details",
            font=("Lao UI", 20, "bold"),
            bg="SkyBlue2",
        )
        sub_title.grid(row=2, column=0, pady=10)

        self.route_id = tk.IntVar()
        route_id_label = tk.Label(
            frame, text="Route ID: ", font=("Lao UI", 11, "bold"), bg="SkyBlue1"
        )
        route_id_entry = tk.Entry(frame, textvariable=self.route_id)
        route_id_label.grid(row=0, column=0, padx=5, pady=5)
        route_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.station_name = tk.StringVar()
        station_name_label = tk.Label(
            frame, text="Station Name: ", font=("Lao UI", 11, "bold"), bg="SkyBlue1"
        )
        station_name_entry = tk.Entry(frame, textvariable=self.station_name)
        station_name_label.grid(row=0, column=2, padx=5, pady=5)
        station_name_entry.grid(row=0, column=3, padx=5, pady=5)

        self.station_id = tk.IntVar()
        station_id_label = tk.Label(
            frame,
            text="Station ID: ",
            font=("Lao UI", 11, "bold"),
            bg="SkyBlue1",
        )
        station_id_entry = tk.Entry(frame, textvariable=self.station_id)
        station_id_label.grid(row=0, column=4, padx=5, pady=5)
        station_id_entry.grid(row=0, column=5, padx=5, pady=5)

        # self.operator_phone = tk.StringVar()
        # operator_phone_label = tk.Label(
        #     frame, text="Operator Phone: ", font=("Lao UI", 11, "bold"), bg="SkyBlue1"
        # )
        # operator_phone_entry = tk.Entry(frame, textvariable=self.operator_phone)
        # operator_phone_label.grid(row=1, column=1, padx=5, pady=5)
        # operator_phone_entry.grid(row=1, column=2, padx=5, pady=5)

        # self.operator_email = tk.StringVar()
        # operator_email_label = tk.Label(
        #     frame, text="Operator Email: ", font=("Lao UI", 11, "bold"), bg="SkyBlue1"
        # )
        # operator_email_entry = tk.Entry(frame, textvariable=self.operator_email)
        # operator_email_label.grid(row=1, column=3, padx=5, pady=5)
        # operator_email_entry.grid(row=1, column=4, padx=5, pady=5)

        add_route_but = tk.Button(
            frame,
            text="Add Route",
            font=("Lao UI", 11, "bold"),
            bg="SkyBlue4",
            fg="white",
            command=self.add_details,
        )
        add_route_but.grid(row=2, column=2, padx=5, pady=5)
        del_route_but = tk.Button(
            frame,
            text="Delete Route",
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
            self.database_manager.route_table.add_route(
                self.route_id.get(),
                self.station_name.get(),
                self.station_id.get(),
            )
        except _tkinter.TclError:
            messagebox.showerror(
                "Error", "Station ID & Route ID can only be of integer type"
            )
            return
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Route and Station ID already exists")
            return
        except Exception as e:
            messagebox.showerror("Error", e)
            return
        messagebox.showinfo("Success", "Route Added Successfully")
        self.info_label.config(
            text=f"{self.route_id.get()},{self.station_name.get()},\
    {self.station_id.get()}",
            font=("Lao UI", 10, "bold"),
            bg="SkyBlue3",
        )
        self.info_label.grid(row=0, column=0)
        self.editable_frame.grid(row=3, column=0, pady=30, padx=400)

    def delete_details(self) -> None:
        try:
            self.database_manager.route_table.delete_route(
                self.route_id.get(), self.station_id.get()
            )
        except _tkinter.TclError:
            messagebox.showerror(
                "Error", "Route ID and Route Station ID can only be of integer type"
            )
            return
        except Exception as e:
            messagebox.showerror("Error", e)
            return
        messagebox.showinfo("Success", "Route Deleted Successfully")


if __name__ == "__main__":
    root = tk.Tk()
    app = RouteScreen()
    app.create_screen(root, app.create_screen)
