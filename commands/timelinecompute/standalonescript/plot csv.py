# Import the necessary modules
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import filedialog

def getPath():
    root=tk.Tk()
    root.overrideredirect(True)
    root.attributes("-alpha", 0)
    root.update()
    path = filedialog.askopenfilename(initialdir="/", title="Select A CSV File", filetypes=[("csv", "*.csv")])
    root.update()
    root.destroy()
    return(path)
 
# Initialize the lists for X and Y
data = pd.read_csv(getPath())
  
df = pd.DataFrame(data)
  
X = list(df.iloc[:, 1])
Y = list(df.iloc[:, 2])
  
# Plot the data using bar() method
plt.barh(X, Y, color='b')
plt.xlabel("Time")
plt.ylabel("Feature")
plt.title("Compute Times")
plt.show()