## 
# Python script to brute force broken pixels
# 
# Input:
#   Border = 2 px
#   QRCode ver 1 @ 21x21 (would assume it could go higher, just didnt do code for it)
# Output:
#   Generates a png file that gets replaced every permutation for testing (not the most efficient) but it was a down and dirty script
#   Once QRCode is found it prints the "data"

from PIL import Image
import qrcode
import cv2
orig_img = 'madeQRcodeHere.png' ## name of hand drawn img


img_size = [24,24] ## hand drawn image in GIMP with a boarder of 2 px and individual pixels are 1x1

blk = (0,0,0)           # Set tupple for the color black
wht = (255,255,255)     # Set tupple for the color white

## these are the dodgy pixels Get these from GIMP   Future me MIGHT make it detect the dodgy ones, but not likely ;)
lost_pixels = [
    [19,11],[20,11],[21,11],[22,11],
    [19,12],[20,12],[21,12],[22,12],
    [19,17],[20,17],
    [19,18],[20,18],
    [19,19],[20,19],
    [19,20],[20,20],
]

img = Image.open(orig_img)       # file name of the qrcode
new_img = img                    # create new img canvas
pixels = new_img.load()          # create pixel matrix

def print_list(d,l):                                      # this takes the pixels to change (white and black)
    my_bin = str(bin(d))[2:]                              # Lazy way to treat the pixels like binary to toggle them all
    my_bin = ((len(lost_pixels)-len(my_bin))*'0')+my_bin  # Length of the lost_pixels is 16. The total pixels to change 2^16 this will change to match the qty of the xy pixels

    for x in range(len(my_bin)):                          # Loops through the 'binary' and changes 1's to black 0's to white
        if my_bin[x] == '1': #Write pixel to black
            pixels[lost_pixels[x][0],lost_pixels[x][1]] = blk
        else: #Write pixel to white
            pixels[lost_pixels[x][0],lost_pixels[x][1]] = wht
    new_img.save('tmpqr.png')

def check_qr(tmp='tmpqr.png'):                            # Checks to see if newly created qrcode is valid
    tmpimg = cv2.imread(tmp)                              # Reads in the qrcode
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(tmpimg)
    if data != "": 
      print(data)                 # if valid will print out data (the flag)
      break                       # if incorrect flag is found (not sure if this can happen with all the error correction) can comment this out

for pixel_loc in range(len(lost_pixels)):                #loop through all the posibilities 2^16 thats alot 65535
    print_list(pixel_loc,lost_pixels)
    check_qr()
