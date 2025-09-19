import customtkinter as ctk

class CollapsiblePane(ctk.CTkFrame):
    """
     -----USAGE-----
    collapsiblePane = CollapsiblePane(parent, 
                          expanded_text =[string],
                          collapsed_text =[string])

    collapsiblePane.pack()
    button = Button(collapsiblePane.frame).pack()
    """

    def __init__(self, parent, expanded_text ="Collapse <<",
                               collapsed_text ="Expand >>"):

        ctk.CTkFrame.__init__(self, parent)

        # These are the class variable
        # see a underscore in expanded_text and _collapsed_text
        # this means these are private to class
        self.parent = parent
        self._expanded_text = expanded_text
        self._collapsed_text = collapsed_text
        self._corner_radius=0
        # Here weight implies that it can grow it's
        # size if extra space is available
        # default weight is 0
        # self.rowconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        


        # Tkinter variable storing integer value
        self._variable = False

        # Checkbutton is created but will behave as Button
        # cause in style, Button is passed
        # main reason to do this is Button do not support
        # variable option but checkbutton do
        self._button = ctk.CTkButton(self, command = self._activate, corner_radius=0, anchor="w")
        self._button.grid(row = 0, column = 0, sticky="we")
        self._button.cget("font").configure(size=15)

        # This will create a separator

        self.frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1f6aa5")
        self.frame.columnconfigure(0, weight=1)

        # This will call activate function of class
        self._activate()

    def _activate(self):
        if self._variable==False:

            # As soon as button is pressed it removes this widget
            # but is not destroyed means can be displayed again
            self.frame.grid_forget()

            # This will change the text of the checkbutton
            self._button.configure(text = self._collapsed_text)
            self._variable=True

        elif self._variable==True:
            # increasing the frame area so new widgets
            # could reside in this container
            self.frame.grid(row = 1, column = 0, sticky="we")
            self._button.configure(text = self._expanded_text)
            self._variable=False

    def toggle(self):
        """Switches the label frame to the opposite state."""
        self._variable.set(not self._variable.get())
        self._activate()