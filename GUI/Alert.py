import customtkinter as ctk


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, text, root, *args, **kwargs):
        super().__init__(*args, **kwargs)

        AlertWin_w=300
        AlertWin_h=100


        self.geometry(str(int(AlertWin_w))+"x"+str(int(AlertWin_h))+"+"+str( int(root.winfo_x()+(root.winfo_width()/2)-(AlertWin_w/2)) )+"+"+str( int(root.winfo_y()+(root.winfo_height()/2)-(AlertWin_h/2)) ) )

        self.attributes("-topmost", True)
        self.grab_set()

        self.label = ctk.CTkLabel(self, text=text)
        self.label.pack(padx=20, pady=20)