import tkinter as tk
from tkinter import messagebox

def append_to_entry(value):
    if entry1.focus_get() == entry1:  # Ensure focus is on the first entry
        entry1.insert(tk.END, value)
    elif entry2.focus_get() == entry2:  # Ensure focus is on the second entry
        entry2.insert(tk.END, value)
    else:
        entry1.focus()
        entry1.insert(tk.END, value)

def clear_entry():
    if entry1.focus_get() == entry1:
        entry1.delete(0, tk.END)
    elif entry2.focus_get() == entry2:
        entry2.delete(0, tk.END)

def perform_calculation():
    try:
        # Get user inputs
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        operation = operation_var.get()

        # Perform the selected operation
        if operation == "Add(+)":
            result = num1 + num2
        elif operation == "Subtract(-)":
            result = num1 - num2
        elif operation == "Multiply(*)":
            result = num1 * num2
        elif operation == "Divide(/)":
            if num2 == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            result = num1 / num2
        else:
            messagebox.showerror("Error", "Please select a valid operation.")
            return

        # Display the result
        result_label.config(text=f"Result: {result:.2f}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")
    except ZeroDivisionError as e:
        messagebox.showerror("Math Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Calculator")
root.geometry("300x400")

# Input fields and labels
input_frame = tk.Frame(root)
input_frame.pack(pady=7)

label1 = tk.Label(input_frame, text="Enter first number:")
label1.grid(row=0, column=0, padx=5, pady=5)
entry1 = tk.Entry(input_frame)
entry1.grid(row=0, column=1, padx=5, pady=5)

label2 = tk.Label(input_frame, text="Enter second number:")
label2.grid(row=1, column=0, padx=5, pady=5)
entry2 = tk.Entry(input_frame)
entry2.grid(row=1, column=1, padx=5, pady=5)

# Result label
result_label = tk.Label(root, text="Result: ", font=("Arial", 10))
result_label.pack(pady=5)

# Operation choice
operation_var = tk.StringVar(value="Select Operation")
operations_menu = tk.OptionMenu(root, operation_var, "Add(+)", "Subtract(-)", "Multiply(*)", "Divide(/)")
operations_menu.pack(pady=5)

# Number keypad frame
keypad_frame = tk.Frame(root)
keypad_frame.pack(pady=5)

buttons = [
    ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
    ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
    ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
    ('0', 3, 1), ('.', 3, 0), ('C', 3, 2)
]

for (text, row, col) in buttons:
    if text == 'C':
        button = tk.Button(keypad_frame, text=text, command=clear_entry, width=4, height=2)
    else:
        button = tk.Button(keypad_frame, text=text, command=lambda t=text: append_to_entry(t), width=4, height=2)
    button.grid(row=row, column=col, padx=4, pady=4)

# Calculate button
calculate_button = tk.Button(root, text="Calculate", command=perform_calculation)
calculate_button.pack(pady=10)



# Run the main loop
root.mainloop()
