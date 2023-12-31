import tkinter as tk
from tkinter import ttk
import networkx as nx
import community  # python-louvain library
from networkx.algorithms.community import girvan_newman, kernighan_lin_bisection
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk  


background_label = None

def create_graph():
    # Define and return the graph
    G = nx.Graph()
    G.add_edges_from([
        (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5), (4, 6),
        (6, 7), (7, 8), (2, 9), (5, 10), (9, 11), (3, 8), (11, 12)
    ])
    return G

def display_graph(frame, G, partition, algorithm, complexity):
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Configure grid for the frame
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=0)

    fig = plt.figure(figsize=(5, 4))
    plt.clf()
    pos = nx.spring_layout(G)
    if isinstance(partition, dict):  # Louvain partition
        nx.draw(G, pos, with_labels=True, node_color=list(partition.values()), cmap=plt.cm.viridis)
    else:  # Girvan-Newman or Kernighan-Lin partition
        color_map = ['blue' if node in partition[0] else 'green' for node in G]
        nx.draw(G, pos, node_color=color_map, with_labels=True)
    plt.title(f"{algorithm} - Time Complexity: {complexity}")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, sticky='nsew', pady=(0, 10))

    # Time Complexity Label
    tk.Label(frame,font=("Times New Roman", 20, "bold") ,text=f"Time Complexity: {complexity}").grid(row=1, column=0, sticky='ew')

    # Return button
    return_btn = tk.Button(frame, text="Return to Main",bg="#F7F7DF",command=lambda: show_frame(main_frame))
    return_btn.grid(row=2, column=0, sticky='ew')

def show_frame(frame):
    frame.tkraise()

def louvain_partition():
    G = create_graph()
    partition = community.best_partition(G)
    display_graph(louvain_frame, G, partition, "Louvain", "O(m log n)")
    show_frame(louvain_frame)

def girvan_newman_partition():
    G = create_graph()
    communities = girvan_newman(G)
    partition = tuple(sorted(c) for c in next(communities))
    display_graph(girvan_newman_frame, G, partition, "Girvan-Newman", "O(m^2n)")
    show_frame(girvan_newman_frame)


def update_background(event):
    global background_label
    image = Image.open(r"C:\Users\cemer\Downloads\image_bg.png")  # Make sure the path is correct
    image = image.resize((event.width, event.height), Image.Resampling.LANCZOS)  # Updated resizing method

    # Update the image of the label
    background_image = ImageTk.PhotoImage(image)
    background_label.config(image=background_image)
    background_label.image = background_image  # Keep a reference!


def kernighan_lin_partition():
    G = create_graph()
    partition = kernighan_lin_bisection(G)
    display_graph(kernighan_lin_frame, G, partition, "Kernighan-Lin", "O(n^2)")
    show_frame(kernighan_lin_frame)

def center_screen_geometry(screen_width, screen_height, window_width, window_height):
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    return f"{window_width}x{window_height}+{x}+{y}"

root = tk.Tk()
root.title("Graph Partitioning Algorithms")
root.geometry(center_screen_geometry(screen_width=root.winfo_screenwidth(),
                                    screen_height=root.winfo_screenheight(),
                                    window_width=600,
                                    window_height=600))

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

main_frame = tk.Frame(root,bg="#0A3433")
louvain_frame = tk.Frame(root)
girvan_newman_frame = tk.Frame(root)
kernighan_lin_frame = tk.Frame(root)

for frame in (main_frame, louvain_frame, girvan_newman_frame, kernighan_lin_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Configure grid for main_frame to manage buttons and the new label
main_frame.grid_columnconfigure(0, weight=1)

# Adjusting grid row configuration to include the label
for i in range(4):  # Three buttons + one label
    main_frame.grid_rowconfigure(i, weight=1)



# Load and set the background image
background_image = ImageTk.PhotoImage(file=r"C:\Users\cemer\Downloads\image_bg.png")  # Use raw string literal for file path
background_label = tk.Label(main_frame, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
main_frame.bind("<Configure>", update_background)

# Adding a new label at the top of the main_frame for instructions
#instruction_label = tk.Label(main_frame, text="Please select a graph partitioning algorithm",font=("Times New Roman", 12, "bold"),bg="#F7F7DF")
#instruction_label.grid(row=0, column=0, sticky='ew', padx=20, pady=10)

# Adding buttons with specified active background and foreground colors
tk.Button(main_frame, text="Louvain Partitioning", bg="#F7F7DF", activebackground="#F7F7DF",font=("Times New Roman", 12, "bold") ,command=louvain_partition).grid(row=1, column=0, sticky='nsew', padx=20, pady=2)
tk.Button(main_frame, text="Girvan-Newman Partitioning", bg="#F7F7DF", activebackground="#F7F7DF",font=("Times New Roman", 12, "bold") ,command=girvan_newman_partition).grid(row=2, column=0, sticky='nsew', padx=20, pady=2)
tk.Button(main_frame, text="Kernighan-Lin Partitioning", bg="#F7F7DF", activebackground="#F7F7DF",font=("Times New Roman", 12, "bold") ,command=kernighan_lin_partition).grid(row=3, column=0, sticky='nsew', padx=20, pady=2)

show_frame(main_frame)

root.mainloop()
