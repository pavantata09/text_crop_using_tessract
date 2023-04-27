from PIL import Image
from pytesseract import pytesseract
import cv2
import argparse
import pandas as pd
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("-l", "--len", help = "lenght of string")
    parser.add_argument("-i ", "--input", help = "input folder path for images")
    parser.add_argument("-o ", "--output", help = "output folder path for crop images")
    # parser.add_argument("-t ", "--tesseractpath", help = "paths to tesseract.exe")
    args=parser.parse_args()
    # Defining paths to tesseract.exe
    # and the image we would be using
    path_to_tesseract =  r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    image_path =       args.input                 #r"C:\Users\pavan\OneDrive\Desktop\cheque.jpg"
    output_folder=args.output
    os.makedirs(image_path,exist_ok=True)
    os.makedirs(output_folder,exist_ok=True)
    
    pytesseract.tesseract_cmd = path_to_tesseract
    
    imglist=os.listdir(image_path)

    for im in imglist:
        print('path:',image_path+'/'+im) 
        img = cv2.imread(image_path+'/'+im)
        cc=pytesseract.image_to_data(img,lang="eng",output_type=pytesseract.Output.DICT)
        d=pd.DataFrame(cc)
        for i in range(d.shape[0]):
            if len(d['text'].iloc[i])>=2:        
                x,y,w,h= d[['left','top','width','height']].iloc[i]
                crop_img=img[y:y+h,x:x+w]
                img_path=''.join(output_folder+im+str(i)+'.jpg')
                cv2.imwrite(img_path,crop_img)
