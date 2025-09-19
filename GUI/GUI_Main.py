import customtkinter as ctk
from GUI import Alert
from GUI import ZoomableCanvas as ZC
from GUI import CollapsiblePane as CPane

class GUI():
    def __init__(self, root, bindings):

        self.Root=root
        self.root_width, self.root_height=1000, 800
        root.geometry(str(self.root_width)+"x"+str(self.root_height))


        self.FunctionBindings=bindings


        root.rowconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        self.canvasframe=ctk.CTkFrame(root)
        self.canvasframe.grid(row=0, column=1, sticky="nsew")

        self.canvasframe.columnconfigure(0, weight=1)
        self.canvasframe.rowconfigure(1, weight=1)


        self.zoomable_canvas=ZC.Zoom_Advanced(mainframe=self.canvasframe, path="Blub Penguin.jpg")
        self.zoomable_canvas.grid(row=1, column=0, sticky="nswe")

        self.Image_AddressBar=ctk.CTkLabel(self.canvasframe, text=self.zoomable_canvas.image_path, fg_color="#1f6aa5")
        self.Image_AddressBar.grid(row=0, column=0, sticky="we")


        sidepanel=ctk.CTkFrame(root, fg_color="#262626")
        sidepanel.grid(row=0, column=0, sticky="ns")
        # sidepanel.rowconfigure(1, weight=1)
        # sidepanel.rowconfigure(2, weight=1)
        sidepanel.columnconfigure(0, weight=1)
        #==================================================================================================================================================================================

        #========================================================Invisible Label===========================================================================================================
        invisiblelabel=ctk.CTkLabel(sidepanel, text="", width=250, height=0, fg_color="#262626")
        invisiblelabel.grid(row = 0, column = 0, padx=0)
        #==================================================================================================================================================================================


        #========================================================Select Image Button========================================================================================================
        OpenImageButton=ctk.CTkButton(sidepanel, text="\u2795 Select Image", anchor="w", command=self.SelectImageFile, corner_radius=32)
        OpenImageButton.grid(row = 1, column = 0, sticky="w", pady=10)
        OpenImageButton.cget("font").configure(size=15)
        #===================================================================================================================================================================================

        # print("\u25BE")#down arrow
        # print("\u25B8")#right pointing arrow
        #========================================================Encryption Pane===========================================================================================================
        Encryption_cpane = CPane.CollapsiblePane(sidepanel, '\u25BC Encrypt', '\u25B6 Encrypt')
        Encryption_cpane.grid(row = 2, column = 0, pady=5, sticky="we")
        
        EncryptionType_container=ctk.CTkFrame(Encryption_cpane.frame, fg_color="#1f6aa5", corner_radius=0)
        EncryptionType_container.grid(row = 0, column = 0, pady=5, sticky="we")
        EncryptionType_container.columnconfigure(0, weight=1)
        EncryptionType_container.columnconfigure(1, weight=1)

        self.Encryption_type_Label=ctk.CTkLabel(EncryptionType_container, text="Encryption Algo", fg_color="#1f6aa5", corner_radius=0, anchor="w")
        self.Encryption_type_Label.grid(row = 0, column = 0, padx=(5,0), sticky="we")

        self.Encryption_OptionMenu=ctk.CTkOptionMenu(EncryptionType_container, values=["None", "LSB"], fg_color="#3796de", corner_radius=0)
        self.Encryption_OptionMenu.grid(row = 0, column = 1, padx=(0,5), sticky="we")


        TextInput_Label=ctk.CTkLabel(Encryption_cpane.frame, text="Input Message", fg_color="#1f6aa5", corner_radius=0, anchor="w")
        TextInput_Label.grid(row = 1, column = 0, padx=(5,0), sticky="we")
        self.TextInputBox=ctk.CTkTextbox(Encryption_cpane.frame, height=100)
        self.TextInputBox.grid(row = 2, column = 0, padx=5, sticky="we")
        

        SaveButton = ctk.CTkButton(Encryption_cpane.frame, text ="Encrypt Image & Save Result", corner_radius=32, fg_color="#3796de", command=self.SaveEncryptionResult)
        SaveButton.grid(row = 3, column = 0, pady = 10, padx=5, sticky="we")
        #===================================================================================================================================================================================


        #==================================================================Decryption Pane==================================================================================================
        Decryption_cpane = CPane.CollapsiblePane(sidepanel, '\u25BC Decrypt', '\u25B6 Decrypt')
        Decryption_cpane.grid(row = 3, column = 0, pady=5, sticky="we")

        DecryptionType_container=ctk.CTkFrame(Decryption_cpane.frame, fg_color="#1f6aa5", corner_radius=0)
        DecryptionType_container.grid(row = 0, column = 0, pady=5, sticky="we")
        DecryptionType_container.columnconfigure(0, weight=1)
        DecryptionType_container.columnconfigure(1, weight=1)

        self.Decryption_type_Label=ctk.CTkLabel(DecryptionType_container, text="Decryption Algo", fg_color="#1f6aa5", corner_radius=0, anchor="w")
        self.Decryption_type_Label.grid(row = 0, column = 0, padx=(5,0), sticky="we")

        self.Decryption_OptionMenu=ctk.CTkOptionMenu(DecryptionType_container, values=["None", "LSB"], fg_color="#3796de", corner_radius=0)
        self.Decryption_OptionMenu.grid(row = 0, column = 1, padx=(0,5), sticky="we")

        SaveButton2 = ctk.CTkButton(Decryption_cpane.frame, text ="Decrypt Image & Save Result", corner_radius=32, fg_color="#3796de", command=self.SaveDecryptionResult)
        SaveButton2.grid(row = 1, column = 0, pady = 10, padx=5, sticky="we")
        #===================================================================================================================================================================================


    def SelectImageFile(self):
        """Opens a file selection dialog and prints the selected file path."""
        file_path = ctk.filedialog.askopenfilename(
            initialdir="C:/Users/GIGABYTE/OneDrive/Desktop/CustomTkinter",  # Sets the initial directory to open in
            title="Select a File",
            filetypes=(("Images", "*.png"), ("Images", "*.png"))
        )
        if file_path:  # Check if a file was actually selected
            print(f"Selected file: {file_path}")
            for child in self.canvasframe.winfo_children():
                child.destroy()
            self.zoomable_canvas=ZC.Zoom_Advanced(mainframe=self.canvasframe, path=file_path)
            self.zoomable_canvas.grid(row=1, column=0, sticky="nswe")

            self.Image_AddressBar=ctk.CTkLabel(self.canvasframe, text="Image: "+self.zoomable_canvas.image_path, fg_color="#1f6aa5")
            self.Image_AddressBar.grid(row=0, column=0, sticky="we")
    

    def SaveImage(self, encrypted_img):
        """Opens a file dialog to save a file and prints the selected path."""
        file_path = ctk.filedialog.asksaveasfilename(
            filetypes=[("Save Image", "*.png"), ("All files", "*.*")], # Filter file types
            title="Save File As" # Title of the dialog window
        )
        if file_path:  # If a file path was selected (user didn't cancel)
            print(f"File will be saved to: {file_path}")
            encrypted_img.save(file_path+".png")
            # You would typically write your data to this file_path here
    
    def SaveText(self, dcrypted_msg):
        """Opens a file dialog to save a file and prints the selected path."""
        file_path = ctk.filedialog.asksaveasfilename(
            filetypes=[("Save Text", "*.txt"), ("All files", "*.*")], # Filter file types
            title="Save File As" # Title of the dialog window
        )
        if file_path:  # If a file path was selected (user didn't cancel)
            print(f"File will be saved to: {file_path}")
            with open(file_path, 'w') as f:
                f.write(dcrypted_msg)
            # You would typically write your data to this file_path here
            


    def SaveEncryptionResult(self):
        InputText=self.TextInputBox.get("0.0", ctk.END)
        EncryptionType=self.Encryption_OptionMenu.get()
        if EncryptionType=="None":
            self.open_toplevel("Encryption Algorithm cannot be None")
        elif InputText.replace(" ", "").replace("\n", "")=="":
            self.open_toplevel("Input Message cannot be empty")
        else:
            if(EncryptionType=="LSB"):
                encrypted_img=self.FunctionBindings["LSB Encryption"](message=InputText.replace("\n", ""), image=self.zoomable_canvas.image )
                self.SaveImage(encrypted_img=encrypted_img)
    
    def SaveDecryptionResult(self):
        DecryptionType=self.Decryption_OptionMenu.get()
        if DecryptionType=="None":
            self.open_toplevel("Decryption Algorithm cannot be None")
        else:
            if(DecryptionType=="LSB"):
                decrypted_msg=self.FunctionBindings["LSB Decryption"](image=self.zoomable_canvas.image )
                self.SaveText(dcrypted_msg=decrypted_msg)


    def open_toplevel(self, DisplayText):
        Alert.ToplevelWindow(text=DisplayText, root=self.Root)