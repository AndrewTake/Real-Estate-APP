import tkinter as tk
from tkinter import messagebox
import requests


class PropertyUPdatePopup(tk.Frame):
    """ Popup Frame to Update a property """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._class_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        tk.Label(self, text="Parcel Number:").grid(row=1, column=1)
        self._parcel_number = tk.Entry(self)
        self._parcel_number.grid(row=1, column=2)
        tk.Label(self, text="Selling Price:").grid(row=2, column=1)
        self._selling_price = tk.Entry(self)
        self._selling_price.grid(row=2, column=2)
        tk.Button(self, text="Enter", command=self._submit_cb).grid(
            row=7, column=1)
        tk.Button(self, text="Close", command=self._class_cb).grid(
            row=7, column=2)

    def _submit_cb(self):
        """ Enter Property """
        data = {}
        data['parcel_number'] = self._parcel_number.get()
        data['selling_price'] = float(self._selling_price.get())

        self._property_sold(data)

    def _property_sold(self, data):
        headers = {"content-type": "application/json"}
        response = requests.put(
            "http://127.0.0.1:5000/portfolio/properties/sold", json=data, headers=headers)

        if response.status_code == 200:
            self._class_cb()
        else:
            messagebox.showerror(
                "Error", "complete repair failed" + response.text)
