import tkinter as tk
from tkinter import messagebox
import requests


class DeletePropertyPopup(tk.Frame):
    """ Popup Frame to remove a property """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._class_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        tk.Label(self, text="Parcel Number:").grid(row=1, column=1)
        self._parcel_number = tk.Entry(self)
        self._parcel_number.grid(row=1, column=2)
        tk.Button(self, text="Enter", command=self._submit_cb).grid(
            row=7, column=1)
        tk.Button(self, text="Close", command=self._class_cb).grid(
            row=7, column=2)

    def _submit_cb(self):
        """ Submit Property """
# parcel number is not highlighted
        self._delete_property(self._parcel_number.get())

    def _delete_property(self, parcel_number):
        response = requests.delete(
            "http://127.0.0.1:5000/portfolio/properties/" + parcel_number)

        if response.status_code == 200:
            messagebox.showinfo(
                "Has been deleted")
            self._class_cb()
        else:
            messagebox.showerror(
                "Error", "complete repair failed" + response.text)
