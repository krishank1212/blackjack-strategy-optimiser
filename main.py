import tkinter as tk
from tkinter import messagebox, ttk
from simulation import simulate_games
# from betting_strategies import martingale
def main():
    try:
        decks = int(input("Enter the number of decks (default is 6): "))
    except ValueError:
        print("Invalid input. Using default of 6 decks.")
        decks = 6
        
    try:
        games = int(input("Enter the number of games to simulate (default is 100000): "))
    except ValueError:
        print("Invalid input. Using default of 100,000 games.")
        games = 100000
        
    # try:
    #     betting_strategy = input("Would you like to use the Martingale betting strategy? (yes/no, default is no): ").strip().lower()
    #     if betting_strategy == 'yes':
    #         betting_strategy = martingale
    #         try:
    #             table_limit = float(input("Enter the table limit for betting (default is no limit): "))
    #             if table_limit <= 0:
    #                 raise ValueError("Table limit must be greater than 0.")
    #         except ValueError:
    #             print("Invalid input. Using no limit for betting.")
    #             table_limit = None
    #     else:
    #         betting_strategy = lambda x, y, z: 1  # Default betting strategy
    #         table_limit = None
    # except Exception as e:
    #     print(f"Error in betting strategy input: {e}. Using default betting strategy.")
    #     betting_strategy = lambda x, y,: 1
        
    
        
    simulate_games(games, decks, betting_strategy=lambda prev, bet, limit: 1, plot=True)

    
if __name__ == "__main__":
    main()
    

# import tkinter as tk
# from tkinter import ttk, messagebox
# from simulation import simulate_games
# from betting_strategies import martingale

# def run_simulation():
#     try:
#         decks = int(decks_var.get())
#     except ValueError:
#         messagebox.showerror("Error", "Please enter a valid number of decks.")
#         return

#     try:
#         games = int(games_var.get())
#     except ValueError:
#         messagebox.showerror("Error", "Please enter a valid number of games.")
#         return

#     # Betting strategy
#     if strategy_var.get() == "Martingale":
#         strategy = martingale
#         try:
#             limit_value = table_limit_var.get()
#             table_limit = float(limit_value) if limit_value.strip() else None
#             if table_limit is not None and table_limit <= 0:
#                 raise ValueError
#         except ValueError:
#             messagebox.showwarning("Warning", "Invalid table limit. Using no limit.")
#             table_limit = None
#     else:
#         strategy = lambda x, y, z: 1  # Flat betting
#         table_limit = None

#     # Run the simulation
#     results = simulate_games(games, decks, strategy, True, table_limit)
#     print(results)
#     output_text.set(results)


# # Build GUI
# root = tk.Tk()
# root.title("Blackjack Simulator")

# # Number of decks
# tk.Label(root, text="Number of Decks:").pack(pady=5)
# decks_var = tk.StringVar(value="6")
# tk.Entry(root, textvariable=decks_var).pack()

# # Number of games
# tk.Label(root, text="Number of Games:").pack(pady=5)
# games_var = tk.StringVar(value="100000")
# tk.Entry(root, textvariable=games_var).pack()

# # Betting strategy
# tk.Label(root, text="Betting Strategy:").pack(pady=5)
# strategy_var = tk.StringVar(value="Flat")
# strategy_menu = ttk.Combobox(root, textvariable=strategy_var, values=["Flat", "Martingale"])
# strategy_menu.pack()

# # Table limit (only for Martingale)
# tk.Label(root, text="Table Limit (optional, Martingale only):").pack(pady=5)
# table_limit_var = tk.StringVar(value="")
# tk.Entry(root, textvariable=table_limit_var).pack()

# # Run button
# tk.Button(root, text="Run Simulation", command=run_simulation).pack(pady=10)

# # Output display
# output_text = tk.StringVar()
# tk.Message(root, textvariable=output_text, justify="left").pack(pady=10)

# if __name__ == "__main__":
#     print("Starting Blackjack Simulator...")
#     root.mainloop()
