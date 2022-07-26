import tkinter as tk
from tkinter import messagebox
import requests


class AddCondoPopup(tk.Frame):
    """ Popup Frame to Add a Condo """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        tk.Label(self, text="Parcel Number:").grid(row=1, column=1)
        self._parcel_number = tk.Entry(self)
        self._parcel_number.grid(row=1, column=2)

        tk.Label(self, text="Street Name:").grid(row=2, column=1)
        self._street_name = tk.Entry(self)
        self._street_name.grid(row=2, column=2)

        tk.Label(self, text="City:").grid(row=3, column=1)
        self._city = tk.Entry(self)
        self._city.grid(row=3, column=2)

        tk.Label(self, text="Postal Code:").grid(row=4, column=1)
        self._postal_code = tk.Entry(self)
        self._postal_code.grid(row=4, column=2)

        tk.Label(self, text="Purchase Price:").grid(row=5, column=1)
        self._purchase_price = tk.Entry(self)
        self._purchase_price.grid(row=5, column=2)

        tk.Label(self, text="HOA Fee:").grid(row=7, column=1)
        self._hoa_fee = tk.Entry(self)
        self._hoa_fee.grid(row=7, column=2)

        tk.Label(self, text="Developer Name:").grid(row=8, column=1)
        self._developer_name = tk.Entry(self)
        self._developer_name.grid(row=8, column=2)

        tk.Label(self, text="Unit Number:").grid(row=9, column=1)
        self._unit = tk.Entry(self)
        self._unit.grid(row=9, column=2)

        tk.Button(self, text="Enter", command=self._submit_cb).grid(
            row=11, column=1)
        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=11, column=2)

    def _submit_cb(self):
        """ Submit Condo """
        data = {}
        data['parcel_number'] = self._parcel_number.get()
        data['street_name'] = self._street_name.get()
        data['city'] = self._city.get()
        data['postal_code'] = self._postal_code.get()
        data['purchase_price'] = float(self._purchase_price.get())
        data['hoa_fee'] = int(self._hoa_fee.get())
        data['developer_name'] = self._developer_name.get()
        data['unit'] = int(self._unit.get())
        data['type'] = "Condo"

        # Implement your code here
        self._add_condo(data)

    def _add_condo(self, data):
        """ Adds a point to the backend grid """
        headers = {"content-type": "application/json"}
        response = requests.post(
            "http://127.0.0.1:5000/portfolio/properties", json=data, headers=headers)

        if response.status_code == 200:
            messagebox.showinfo(
                "Condo has been added")
            self._close_cb()
        else:
            messagebox.showerror(
                "Error", "Add Condo Request Failed" + response.text)
