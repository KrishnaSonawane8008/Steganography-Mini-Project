import pytest
from unittest.mock import MagicMock, patch
import customtkinter as ctk
from GUI import GUI_Main
from Main import LSB_Encryption, LSB_Decryption
from PIL import Image

@pytest.fixture
def gui_app():
    root = ctk.CTk()
    root.withdraw()  # hide window during tests
    bindings = {"LSB Encryption": MagicMock(), "LSB Decryption": MagicMock()}
    app = GUI_Main.GUI(root, bindings)
    yield app
    root.destroy()



def test_encryption_no_algorithm(gui_app):
    gui_app.Encryption_OptionMenu.set("None")
    gui_app.TextInputBox.insert("0.0", "Test")
    with patch.object(gui_app, "open_toplevel") as mock_alert:
        gui_app.SaveEncryptionResult()
        mock_alert.assert_called_once_with("Encryption Algorithm cannot be None")

def test_encryption_empty_input(gui_app):
    gui_app.Encryption_OptionMenu.set("LSB")
    with patch.object(gui_app, "open_toplevel") as mock_alert:
        gui_app.SaveEncryptionResult()
        mock_alert.assert_called_once_with("Input Message cannot be empty")

def test_encryption_success(gui_app):
    gui_app.Encryption_OptionMenu.set("LSB")
    gui_app.TextInputBox.insert("0.0", "Hello")
    fake_img = MagicMock()
    gui_app.zoomable_canvas.image = fake_img

    with patch.object(gui_app, "SaveImage") as mock_save:
        gui_app.FunctionBindings["LSB Encryption"].return_value = fake_img
        gui_app.SaveEncryptionResult()
        mock_save.assert_called_once_with(encrypted_img=fake_img)


def test_decryption_no_algo(gui_app):
    gui_app.Decryption_OptionMenu.set("None")
    with patch.object(gui_app, "open_toplevel") as mock_alert:
        gui_app.SaveDecryptionResult()
        mock_alert.assert_called_once_with("Decryption Algorithm cannot be None")

def test_decryption_success(gui_app):
    gui_app.Decryption_OptionMenu.set("LSB")
    fake_message = MagicMock()
    fake_img = MagicMock()
    gui_app.zoomable_canvas.image = fake_img

    with patch.object(gui_app, "SaveText") as mock_save:
        gui_app.FunctionBindings["LSB Decryption"].return_value = fake_message
        gui_app.SaveDecryptionResult()
        mock_save.assert_called_once_with(dcrypted_msg=fake_message)

# def test_correct_image_extension_selection(gui_app):
#     with patch("customtkinter.filedialog.askopenfilename", return_value="example.txt") as mock_dialog:
#         selected = gui_app.SelectImageFile()
#         # ensure the returned file is correct
#         assert selected == "example.txt"

#         # ensure the dialog was called with correct filetypes
#         mock_dialog.assert_called_once_with(filetypes=[(".txt files", "*.txt")])

@pytest.fixture
def sample_image(tmp_path):
    # Create a simple 10x10 image
    img = Image.new("RGB", (10, 10), color=(255, 255, 255))
    path = tmp_path / "test_img.png"
    img.save(path)
    return Image.open(path)



def test_LSB_Encryption_Decryption(sample_image):
    message = "Hello"
    encrypted_img = LSB_Encryption(sample_image, message)
    decrypted_message = LSB_Decryption(encrypted_img)
    assert decrypted_message == message

def test_Encryption_Decryption_symbol(sample_image):
    message = "~!@#$%^&*()_+=[]"
    encrypted_img = LSB_Encryption(sample_image, message)
    decrypted_message = LSB_Decryption(encrypted_img)
    assert decrypted_message == message

def test_Encryption_Decryption_spaces_and_linebreaks(sample_image):
    message = "Hello \n Hi"
    encrypted_img = LSB_Encryption(sample_image, message)
    decrypted_message = LSB_Decryption(encrypted_img)
    assert decrypted_message == message

def test_Encryption_Decryption_word_limit(sample_image):
    #image pixels=10x10=100 pixels
    #LSB requires 3 pixels per letter of the message, spaces and special characters included
    #the message below has 38 letters
    #a 10x10 image can handle only 100/3=33.333 (so 33) letters, the output should omit any letters after the 33rd message
    message = "1234567890_1234567890_1234567890_12345"
    encrypted_img = LSB_Encryption(sample_image, message)
    decrypted_message = LSB_Decryption(encrypted_img)
    assert decrypted_message == "1234567890_1234567890_1234567890_"