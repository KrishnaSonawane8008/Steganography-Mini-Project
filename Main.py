import customtkinter as ctk
from PIL import Image, ImageTk
from GUI import GUI_Main
import Utilities as ut



def LSB_Encryption(image:Image, message):
    print("LSB encryption Called")
    binary_list=ut.Message_to_BinaryList(message)
    new_img=image.copy()

    if new_img.mode!="RGB":
        new_img=new_img.convert("RGB")
    width, height= new_img.size
    print(width, height)


    pixels=new_img.getdata()#contains all the pixel values as a tuple of 3 integers: (R,G,B)
    changed_pixels=[]
    stop_bit_manupulation=False
    for b_indx in range(len(binary_list)):
        current_char_binary=binary_list[b_indx]
        for i in range(3):#this loop alters the LSB of 3 pixels from the image using the binary of a character from the message

            if(b_indx*3+i>len(pixels)-1):#if pixel is not present in image
                stop_bit_manupulation=True
                break

            current_pixel=pixels[b_indx*3+i]#contains three values in a tuple (R, G, B), R, G,& B are integers in the range of 0-255
            current_pixel_binary=[ut.int_to_binary(current_pixel[0]), ut.int_to_binary(current_pixel[1]), ut.int_to_binary(current_pixel[2])]#binary of the integers in (R,G,B)
            
            current_pixel_binary[0]=current_pixel_binary[0][:-1]+current_char_binary[i*3]
            current_pixel_binary[1]=current_pixel_binary[1][:-1]+current_char_binary[i*3+1]
            if((i*3+2)<len(current_char_binary)-1):
                current_pixel_binary[2]=current_pixel_binary[2][:-1]+current_char_binary[i*3+2]
            else:
                if(b_indx<len(binary_list)-1):
                    current_pixel_binary[2]=current_pixel_binary[2][:-1]+'1'
                else:
                    current_pixel_binary[2]=current_pixel_binary[2][:-1]+'0'
            
            changed_pixels.append( (    ut.binary_to_int(current_pixel_binary[0]), 
                                        ut.binary_to_int(current_pixel_binary[1]), 
                                        ut.binary_to_int(current_pixel_binary[2]) 
                                    ) )
            
        if(stop_bit_manupulation):
            break
    

    pixel_put_count=0
    stop_putting_pixels=False
    for y in range(height):
        for x in range(width):
            new_img.putpixel((x,y), changed_pixels[pixel_put_count])
            # print("Put Pixel: ", changed_pixels[pixel_put_count], " at: ", x,",",y)
            pixel_put_count+=1
            if(pixel_put_count==len(changed_pixels)):
                stop_putting_pixels=True
                break
        if(stop_putting_pixels):
            break
    

    return new_img
    
            
            
            

def LSB_Decryption(image):
    img=image
    new_img=img.copy()
    if new_img.mode!="RGB":
        new_img=new_img.convert("RGB")

    pixels=new_img.getdata()
    binary_list=[]
    for pix_indx in range(0, len(pixels), 3):
        char_binary=""
        
        pix1=pixels[pix_indx]
        pix1_binary=( ut.int_to_binary(pix1[0]), ut.int_to_binary(pix1[1]), ut.int_to_binary(pix1[2])  )
        char_binary+=pix1_binary[0][-1]+pix1_binary[1][-1]+pix1_binary[2][-1]
        if(pix_indx+1<len(pixels)):
            pix2=pixels[pix_indx+1]
            pix2_binary=( ut.int_to_binary(pix2[0]), ut.int_to_binary(pix2[1]), ut.int_to_binary(pix2[2])  )
            char_binary+=pix2_binary[0][-1]+pix2_binary[1][-1]+pix2_binary[2][-1]
        if(pix_indx+2<len(pixels)):
            pix3=pixels[pix_indx+2]
            pix3_binary=( ut.int_to_binary(pix3[0]), ut.int_to_binary(pix3[1]), ut.int_to_binary(pix3[2])  )
            char_binary+=pix3_binary[0][-1]+pix3_binary[1][-1]+pix3_binary[2][-1]

        if(len(char_binary[:-1])<8):
            break
        binary_list.append(char_binary[:-1])
        if(char_binary[-1]=='0'):
            break

    return ut.BinaryList_to_Message(binary_list)



# LSB_Decryption(image=Image.open("Blub Penguin.jpg"))






bindings={"LSB Encryption":LSB_Encryption, "LSB Decryption":LSB_Decryption}

# Encrypt("hi")
if __name__ == "__main__":
    root=ctk.CTk()
    gui=GUI_Main.GUI(root=root, bindings=bindings)
    root.mainloop()