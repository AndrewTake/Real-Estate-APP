import tkinter as tk
import requests
from add_condo_popup import AddCondoPopup
from add_duplex_popup import AddDuplexPopup
from property_update_popup import PropertyUPdatePopup
from delete_property_pop_up import DeletePropertyPopup


class MainAppController(tk.Frame):
    """ Main Application for GUI """

    def __init__(self, parent):
        """ Initialize Main Application """
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="Properties").grid(row=1, column=2)
        self._properties_listbox = tk.Listbox(self)
        self._properties_listbox.grid(row=2, column=1, columnspan=5)

        tk.Button(self, text="Add Condo",
                  command=self._add_condo).grid(row=3, column=1)

        tk.Button(self, text="Add Duplex",
                  command=self._add_duplex).grid(row=3, column=2)

        tk.Button(self, text="Sell Property",
                  command=self._property_sold).grid(row=3, column=3)

        tk.Button(self, text="Delete Property",
                  command=self._delete_property).grid(row=3, column=4)

        tk.Button(self, text="Quit", command=self._quit_callback).grid(
            row=4, column=2)

        self._update_properties_list()

    def _add_condo(self):
        """ Add Condo Popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddCondoPopup(self._popup_win, self._close_condo_cb)

    def _close_condo_cb(self):
        """ Close Add Condo Popup """
        self._popup_win.destroy()
        self._update_properties_list()

    def _add_duplex(self):
        """ Add Duplex Popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddDuplexPopup(self._popup_win, self._close_duplex_cb)

    def _close_duplex_cb(self):
        """ Close Add Duplex Popup """
        self._popup_win.destroy()
        self._update_properties_list()

    def _property_sold(self):
        """ Property is sold Popup """
        self._popup_win = tk.Toplevel()
        self._popup = PropertyUPdatePopup(
            self._popup_win, self._close_update_cb)

    def _close_update_cb(self):
        """ Close Update Popup """
        self._popup_win.destroy()
        self._update_properties_list()

    def _delete_property(self):
        """ remove device Popup """
        self._popup_win = tk.Toplevel()
        self._popup = DeletePropertyPopup(
            self._popup_win, self._close_remove_cb)

    def _close_remove_cb(self):
        """ Close remove device Repair Popup """
        self._popup_win.destroy()
        self._update_properties_list()

    def _quit_callback(self):
        """ Quit """
        self.quit()

    def _update_properties_list(self):
        """ Update the List of Property Descriptions """
        response = requests.get(
            "http://127.0.0.1:5000/portfolio/properties/all/Condo")

        self._properties_listbox.delete(0, tk.END)
        condo_descs = response.json()
        for condo_desc in condo_descs:
            self._properties_listbox.insert(tk.END, condo_desc)

        response = requests.get(
            "http://127.0.0.1:5000/portfolio/properties/all/Duplex")

        duplex_descs = response.json()
        for duplex_desc in duplex_descs:
            self._properties_listbox.insert(tk.END, duplex_desc)


if __name__ == "__main__":
    root = tk.Tk()
    MainAppController(root).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()
