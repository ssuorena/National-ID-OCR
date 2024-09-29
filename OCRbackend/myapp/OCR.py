import easyocr
import jdatetime
from hezar.models import Model
from PIL import Image, ImageEnhance, ImageDraw
import pandas as pd
import numpy as np
import cvlib as cv
from keras.preprocessing.image import img_to_array

from keras.models import load_model
# load pre-trained model
GDmodel =load_model('Models/gender_detection.model')

import cv2
from matplotlib import pyplot as plt


# Perform OCR using EasyOCR
reader = easyocr.Reader(['fa','ar'])  # 'en' for English, 'fa' for Persian (Farsi)
model = Model.load("hezarai/crnn-fa-printed-96-long")


from flair.data import Sentence
from flair.models import SequenceTagger
# load tagger
tagger = SequenceTagger.load("PooryaPiroozfar/Flair-Persian-NER")

cityCode = pd.read_excel('cityCode.xlsx')



def face_crop(image_path):
    image = cv2.imread(image_path)
    face, confidence = cv.detect_face(image)
    for idx, f in enumerate(face):
    
         # get corner points of face rectangle       
        (startX, startY) = f[0], f[1]
        (endX, endY) = f[2], f[3]
    
        # draw rectangle over face
        cv2.rectangle(image, (startX,startY), (endX,endY), (0,255,0), 2)
    
        # crop the detected face region
        face_crop = np.copy(image[startY:endY,startX:endX])
    
        # preprocessing for gender detection model
        face_crop = cv2.resize(face_crop, (96,96))
        face_crop = face_crop.astype("float") / 255.0
        face_crop = img_to_array(face_crop)
        face_crop = np.expand_dims(face_crop, axis=0)
    return face_crop

def GenderDetection(pic):
    classes = ['man','woman']
    # apply gender detection on face
    conf = GDmodel.predict(pic)[0]
    print(conf)
    
    # get label with max accuracy
    idx = np.argmax(conf)
    label = classes[idx]
    
    label = "{}: {:.2f}%".format(label, conf[idx] * 100)
    return label


def contains_digit(s):
    return any(char.isdigit() for char in s)

def is_only_words(s):
    for char in s:
        if not (char.isalpha() or char.isspace()):
            return False
    return True


def resize_image_with_aspect_ratio(image_path, output_path, width=None, height=None):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Unable to read image from path: {image_path}")

    # Get the original dimensions
    original_height, original_width = image.shape[:2]

    # Calculate the new dimensions while maintaining the aspect ratio
    if width is None and height is None:
        raise ValueError("Either width or height must be specified")

    if width is not None:
        # Calculate the new height to maintain the aspect ratio
        new_width = width
        new_height = int((new_width / original_width) * original_height)
        interpolation_method = cv2.INTER_LINEAR if new_width > original_width else cv2.INTER_AREA
    else:
        # Calculate the new width to maintain the aspect ratio
        new_height = height
        new_width = int((new_height / original_height) * original_width)
        interpolation_method = cv2.INTER_LINEAR if new_height > original_height else cv2.INTER_AREA

    # Resize the image with the best interpolation method
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=interpolation_method)

    # Save the resized image
    cv2.imwrite(output_path, resized_image)
    print(f"Resized image saved to {output_path}")
    

def validator(ini_string):
    getVals = [val for val in ini_string if val.isnumeric()]
    n = "".join(getVals)
    try:

        digits = [int(digit) for digit in n]
        
        if len(digits) != 10:
            return False
        else:
            sum = digits[0]*10 + digits[1]*9 + digits[2]*8 + digits[3]*7 + digits[4]*6 + digits[5]*5 + digits[6]*4 + digits[7]*3 + digits[8]*2
            rem = sum % 11
        
            if rem < 2:
                if digits[9] == rem:
                    return True
            else:
                if digits[9] == (11-rem):

                    return True
                else:
                    return False
    except:
        return False


def textClassifier(text):
    # make example sentence
    sentence = Sentence(text)    
    try:
        # predict NER tags
        tagger.predict(sentence)
        return sentence.tag
    except:
        
        return 0

def convert_persian_to_english(persian_number_str):
    persian_to_english_map = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9'
    }

    english_number_str = ''.join(persian_to_english_map.get(char, char) for char in persian_number_str)
    return english_number_str
    

def persian_date_to_datetime(persian_date_str, format='%Y/%m/%d'):
    """
    Convert a Persian date string to a Python datetime object.

    :param persian_date_str: The Persian date string (e.g., '1403/04/01')
    :param format: The format of the Persian date string (default is '%Y/%m/%d')
    :return: A Python datetime object
    """
    try: 
        # Parse the Persian date string to a jdatetime object
        persian_date = jdatetime.datetime.strptime(persian_date_str, format)
        
        # Convert the jdatetime object to a Python datetime object
        gregorian_date = persian_date.togregorian()
        
        return True ,gregorian_date
    except:
        return False ,0

# Function to preprocess the image
# Load the image
def preprocess2(image_path):
     # Replace with your image path
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply a threshold to get black and near-black regions
    # Adjust the threshold value as needed
    threshold_value = 200  # Adjust this value to include more or fewer gray shades
    _, binary_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY_INV)
    pil_image = Image.fromarray(binary_image)
    
    return pil_image


def preprocess_image(image_path):
    image = Image.open(image_path)
    
    # Resize image for better OCR performance
    image = image.resize((image.width * 1, image.height * 1), Image.Resampling.LANCZOS)
    
    # Convert image to grayscale
    image = image.convert('L')
    
    # Enhance image contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.5)
    
    return image

# Function to crop the text boxes
def crop_text_boxes(image, ocr_results,acc):
    cropped_images = []
    for (bbox, text, prob) in ocr_results:
        if prob > acc:  # Adjust probability threshold as needed
            # Get the coordinates of the bounding box
            x_min = min([coord[0] for coord in bbox])
            x_max = max([coord[0] for coord in bbox])
            y_min = min([coord[1] for coord in bbox])
            y_max = max([coord[1] for coord in bbox])
            
            # Crop the image using the bounding box coordinates
            cropped_image = image.crop((x_min, y_min, x_max, y_max))
            cropped_images.append((cropped_image, text,max([x_max,x_min]),max([y_max,y_min]),min([y_max,y_min])))
    return cropped_images

def ID_OCR(image_path,width):
    image = Image.open(image_path)
    # Perform OCR using EasyOCR
    ######################################################phase 1########################################################
    results = reader.readtext(np.array(image),slope_ths=0.5,width_ths = 0.5 )
    
    # Crop text boxes
    cropped_images = crop_text_boxes(image, results,acc=0.25)
    
    dates = {'persian':[],'date':[]}
    names = []
    strings = []
    info={}
    info["Family Name"]=None 
    info["Name"]=None 
    info["Father's Name"]=None
    Id_flag = False
    # Save and display the cropped images
    #model = Model.load("hezarai/crnn-fa-printed-96-long")
    for i, (cropped_image, text,w,h,h_min) in enumerate(cropped_images):
        main_path = 'Working images/'
        cropped_image_path = f'cropped_text_{i}.png'
        cropped_image.save(main_path + cropped_image_path)
        if contains_digit(text.replace(" ", "")):
            plate_text = model.predict( main_path + cropped_image_path)
            n = plate_text[0]['text']
            #print('number is:',n)
            if ('/' not in n) and (len(n)==10):
                #print('ID number is:',w,h_min)
                #print('path:',cropped_image_path)
                W2=w
                H2=h_min
                Id_flag = True
                
        else:
            n=''
        nationalCode = validator(n)
        if nationalCode :
            cropped_image.save(main_path+"nationalcode.png")
            info["ID"]=n
            #print(w,h_min)
            W=w
            H=h_min
            city = cityCode[cityCode['code'].str.contains(convert_persian_to_english(n[:3]))]
            if len(city)!=0:
                info["City"] = city['city'].iloc[0]

        label = textClassifier(text)
        #print('text:  ', text, 'label: ',label)
        strings.append((text,h))
        if label in['PER','LOC','ORG']:
            names.append((text,h))
         
        birthFlage,converted_date = persian_date_to_datetime(n)
    
        if birthFlage:
            dates['persian'].append(n)
            dates['date'].append(converted_date)
            
    sorted_strings = sorted(names, key=lambda x: x[1], reverse=False)
    if len(sorted_strings)==3:
        family_name = sorted_strings[1][0]
        name = sorted_strings[0][0]
        fathers_name = sorted_strings[2][0]
    print('phase1 complete')
    ######################################################phase 2########################################################
    if ('ID' not in info) or (len(dates['persian'])<2):
        output_path = main_path+'Resized_image.png'
        resize_image_with_aspect_ratio(image_path, output_path=main_path+'Resized_image.png', width=width, height=None)
        dates = {'persian':[],'date':[]}
        names = []
        strings = []
        processed_image = preprocess_image(image_path)
        results = reader.readtext(np.array(processed_image),slope_ths=0.5,width_ths = 0.5 )
        cropped_images = crop_text_boxes(processed_image, results,acc=0.25)
        for i, (cropped_image, text,w,h,h_min) in enumerate(cropped_images):
            cropped_image_path = f'cropped_text_{i}.png'
            cropped_image.save(main_path+cropped_image_path)
            if contains_digit(text.replace(" ", "")):
                plate_text = model.predict( main_path+cropped_image_path)
                n = plate_text[0]['text']
                #print('number is:',n)
            else:
                n=''
            if Id_flag == False:
                if ('/' not in n) and (len(n)==10):
                    #print('number is:',n)
                    #print('path:',cropped_image_path)
                    W2=w
                    H2=h_min
                    Id_flag = True
            if ('ID' not in info):
                nationalCode = validator(n)
                if nationalCode :
                    cropped_image.save(main_path+"nationalcode.png")
                    info["ID"]=n
                    #print('phase2 ID:',w,h_min)
                    W=w
                    H=h_min
                    city = cityCode[cityCode['code'].str.contains(convert_persian_to_english(n[:3]))]
                    if len(city)!=0:
                        info["City"] = city['city'].iloc[0]
                
            birthFlage,converted_date = persian_date_to_datetime(n)
    
            if birthFlage:
                dates['persian'].append(n)
                dates['date'].append(converted_date)

    print('phase2 complete')
    ######################################################first results########################################################

    if len(dates['date'])>1:
        if(dates['date'][0]<dates['date'][1]):
            info["birsth date_per"]=dates['persian'][0]
            info["birsth date"]=dates['date'][0]
        if(dates['date'][1]<dates['date'][0]):
            info["birsth date_per"]=dates['persian'][1]
            info["birsth date"]=dates['date'][1]
    
    
    sorted_strings = sorted(names, key=lambda x: x[1], reverse=False)
    
    # Assign roles based on sorted order
    #print('sortedis:',sorted_strings)
    if len(sorted_strings)==3:
        family_name = sorted_strings[1][0]
        name = sorted_strings[0][0]
        fathers_name = sorted_strings[2][0]
    if 'ID' in info:
        crop = image.crop((0,H-((0.03)*H), W+((0.03)*W), image.size[1]))
    if ('ID' not in info) and Id_flag:
        print('crop by flag')
        crop = image.crop((0,H2-((0.03)*H2), W2+((0.03)*W2), image.size[1]))
        #print('picture is not valid')
        info['Error']='Could not found ID'
    if('ID' not in info) and Id_flag==False:
        info['Error']='Could not found ID'
        crop = image
        print('picture is not valid')
    

    #print('Info',info)
    print('phase3 complete')
        ######################################################phase 3########################################################
            
    # Perform OCR using EasyOCR
    results = reader.readtext(np.array(crop),slope_ths=0.5,width_ths = 1 )
    
    # Crop text boxes
    cropped_images = crop_text_boxes(crop, results,acc=0.15)
    
    names = []
    strings = []

    if (len(dates['persian'])<2):
        dates = {'persian':[],'date':[]}
    
    for i, (cropped_image, text,w,h,h_min) in enumerate(cropped_images):
        cropped_image_path = f'cropped_text_{i}.png'
        cropped_image.save(main_path+cropped_image_path)
        if ('ID' not in info) or (len(dates['persian'])<2):
            if contains_digit(text):
                plate_text = model.predict( main_path +cropped_image_path)
                n = plate_text[0]['text'] 
            else:
                n=''
        
        label = textClassifier(text)
        
        if contains_digit(text)==False and is_only_words(text) :
            strings.append((text,h))
        
        if label in['PER','LOC','ORG']:
            names.append((text,h))

        if (len(dates['persian'])<2):
            birthFlage,converted_date = persian_date_to_datetime(n)
        
            if birthFlage:
                dates['persian'].append(n)
                dates['date'].append(converted_date)
    
        
        
    
    if len(dates['date'])>1:
        if(dates['date'][0]<dates['date'][1]):
            info["birsth date_per"]=dates['persian'][0]
            info["birsth date"]=dates['date'][0]
        if(dates['date'][1]<dates['date'][0]):
            info["birsth date_per"]=dates['persian'][1]
            info["birsth date"]=dates['date'][1]
    
    
    sorted_strings = sorted(names, key=lambda x: x[1], reverse=False)
    S_strings = sorted(strings, key=lambda x: x[1], reverse=False)
    
    # Assign roles based on sorted order
    if (info["Family Name"]==None or info["Name"]==None or info["Father's Name"]==None):
        if len(sorted_strings)==3:
            family_name = sorted_strings[1][0]
            name = sorted_strings[0][0]
            fathers_name = sorted_strings[2][0]
        if len(S_strings)==3:
            family_name = S_strings[1][0]
            name = S_strings[0][0]
            fathers_name = S_strings[2][0]
        
        else:
            next = False
            try:
                family_name = S_strings[2][0]
                name = S_strings[1][0]
                fathers_name = S_strings[4][0]
            except:
                next=True
            if next:
                try:
                   
                    family_name = S_strings[2][0]
                    name = S_strings[1][0]
                    fathers_name = S_strings[3][0]
                except:
                    family_name = "None"
                    name = "None"
                    fathers_name = "None"
    
        info["Family Name"]=family_name
        info["Name"]=name
        info["Father's Name"]=fathers_name

    pic = face_crop(image_path)
    #plt.imshow(pic[0])
    gender = GenderDetection(pic)
    gender = gender.split(': ')
    if float(gender[1].replace('%',''))>=99:
        info['Gender']=gender[0]
    print('phase4 complete')
    return info , crop,S_strings,pic[0]


    