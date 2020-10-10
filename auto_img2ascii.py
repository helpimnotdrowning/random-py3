import PIL.Image
from datetime import datetime

class ANSICol:
    # special codes
    reset = '\033[0m'
col = ANSICol

ASCII_CHARS = ["@","Q","$","&","G","8","0","%","d","#","o","M","6","9","P","W","B","e","5","h","K","u","s","4","x","z","2","A","3","v","c","]","i","7","J","F","{","N","[","}","1","R","y",")","(","t","l","?","|","*","/","<","=",">","+","~","!",";","-","_",":","'","`","´"," "," "]
ASCII_CHARS_REVERSED = [' ',' ','´','`',"'",':','_','-',';','!','~','+','>','=','<','/','*','|','?','l','t','(',')','y','R','1','}','[','N','{','F','J','7','i',']','c','v','3','A','2','z','x','4','s','u','K','h','5','e','B','W','P','9','6','M','o','#','d','%','0','8','G','&','$','Q','@']
pixels = {}
asciiLines = {}

def RGB2ANSI(red=0, green=0, blue=0, isBG=0):
    if isBG == 0:
        ansiColor = "\033[38;2;{};{};{}m".format(red, green, blue)
    else:
        ansiColor = "\033[48;2;{};{};{}m".format(red, green, blue)
    return ansiColor

def log(string):
    print("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]: " + str(string))

def resize(image, new_width = 100):
    width, height = image.size
    new_height = new_width * height // width // 2
    print(new_width,new_height)
    return image.resize((new_width, new_height))
    
def to_greyscale(image):
    return image.convert("L")

def pixel_to_ascii(image):
    pixels = image.getdata()
    log(pixels)
    ascii_str = "";
    for pixel in pixels:
        ascii_str += ASCII_CHARS_REVERSED[pixel//4];
    return ascii_str
    
def main():
    path = input("Enter the path to the image fiel : \n")
    
    ascii_img2 = ''
    
    try: image = PIL.Image.open(path)
    except: log(path, "Unable to find image ")
    
    width,height = image.size
    image = resize(image,200) #resize image
    
    for x in range(width):
        for y in range(height):
            try: log("Color of " + str((x,y)) + " is " + str(image.getpixel((x,y))))  # debug log of the color of each pixel
            except: break  #log("fuck")  # ignore the ~50~ actually 950 errors generated by above line :)
            #print(RGB2ANSI(image.getpixel((x,y))[0],image.getpixel((x,y))[1],image.getpixel((x,y))[2]) + str(image.getpixel((x,y))))
    log("size of image is " + str(width * height))
    
    greyscale_image = to_greyscale(image)  # convert to grayscale
    
    ascii_str = pixel_to_ascii(greyscale_image)  # convert to ascii
    
    img_width = greyscale_image.width
    
    ascii_str_len = len(ascii_str)
    
    ascii_img = ""
    
    #Split the string based on width of the image
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i+img_width] + "\n"
    
    for x in range(len(ascii_img.splitlines())):
        for y in range(x):
            log("pixel at {} , {} is ".format(x,y) + str(image.getpixel((x,y))))
    log(image.size)
    print(ascii_img)
    
main()
