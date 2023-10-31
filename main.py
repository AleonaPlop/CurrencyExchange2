import requests
import tkinter as tk
from tkinter import ttk, messagebox


def convert_currency():
    from_currency = from_currency_combobox.get().upper()
    to_currency = to_currency_combobox.get().upper()
    amount_str = amount_entry.get()

    # Check if either combobox is empty
    if not from_currency or not to_currency:
        messagebox.showerror("Missing Selection",
                             "Please select currencies in both 'From Currency' and 'To Currency' comboboxes.")
        return

    # Check if the amount is a valid float
    try:
        amount = float(amount_str)
        if amount <= 0:
            messagebox.showerror("Invalid Amount", "Amount must be greater than zero.")
            return
    except ValueError:
        messagebox.showerror("Invalid Amount", "Please enter a valid numeric amount.")
        return

    try:
        response = requests.get(
            f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}")
        response.raise_for_status()
        data = response.json()
        result_label.config(text=f"{amount} {from_currency} is {data['rates'][to_currency]} {to_currency}")
    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Error: {e}")


def on_currency_change(event):
    from_currency = from_currency_combobox.get()
    to_currency = to_currency_combobox.get()

    # Disable the selected currency in the other combobox
    from_currency_combobox['values'] = [currency for currency in currencies if currency != to_currency]
    to_currency_combobox['values'] = [currency for currency in currencies if currency != from_currency]


root = tk.Tk()
root.title("Currency Converter")

# Center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - root.winfo_reqwidth()) / 2
y = (screen_height - root.winfo_reqheight()) / 2
root.geometry("+%d+%d" % (x, y))

# Disable window resizing
root.resizable(width=False, height=False)

currencies = ["RON", "EUR", "USD", "GBP", "CHF", "BGN", "HUF"]

from_currency_label = tk.Label(root, text="From Currency:")
from_currency_combobox = ttk.Combobox(root, values=currencies, state="readonly")
from_currency_combobox.bind("<<ComboboxSelected>>", on_currency_change)

to_currency_label = tk.Label(root, text="To Currency:")
to_currency_combobox = ttk.Combobox(root, values=currencies, state="readonly")
to_currency_combobox.bind("<<ComboboxSelected>>", on_currency_change)

amount_label = tk.Label(root, text="Amount:")
amount_entry = tk.Entry(root)

convert_button = tk.Button(root, text="Convert", command=convert_currency)
result_label = tk.Label(root, text="Result will be shown here")

from_currency_label.grid(row=0, column=0)
from_currency_combobox.grid(row=0, column=1)
to_currency_label.grid(row=1, column=0)
to_currency_combobox.grid(row=1, column=1)
amount_label.grid(row=2, column=0)
amount_entry.grid(row=2, column=1)
convert_button.grid(row=3, columnspan=2)
result_label.grid(row=4, columnspan=2)

root.mainloop()
