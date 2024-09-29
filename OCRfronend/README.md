# National ID Card OCR Fornt-end

This project is a Streamlit-based web application for optical character recognition (OCR) on national ID cards. Users can upload an image of their ID card, and the application will analyze the image and extract relevant information such as name, family name, ID number, city of birth, birth date, and gender. The extracted information is then displayed on the webpage.

## Features

- Upload an image of a national ID card (supports jpg, jpeg, and png formats).
- Send the uploaded image to an API endpoint for analysis.
- Display extracted information such as name, family name, ID number, city of birth, birth date, and gender.
- Show the portrait extracted from the ID card image, if available.

## Requirements

- Python 3.7 or higher
- Streamlit
- Requests
- Matplotlib

## Installation

1. Clone the repository:

   ```bash
   git clone https://gitlab.daricdp.ir/ticket/frontend/national_id_ocr_frontend.git
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:

   ```bash
   streamlit run App.py
   ```

2. Open your web browser and go to `http://localhost:8501`.

3. Upload an image of your national ID card using the file uploader.

4. Wait for the analysis to complete. The extracted information will be displayed on the webpage.

## Code Overview

```python
import streamlit as st
import requests
from matplotlib import pyplot as plt

# API endpoint
url = 'http://127.0.0.1:8000/api/upload/'
portre = False
st.logo('Static Images/logo darik-01.png')
st.title('Daric dp')
st.title('National ID Card OCR')

st.divider()
st.write('Please take a picture from your national ID card and upload it...')
st.image('Static Images/ID_card.PNG', width=200, caption='ID card image style')

# Upload image file
uploaded_file = st.file_uploader("Choose an ID card image...", type=["jpg", "jpeg", "png"])
print(uploaded_file)

if uploaded_file is not None:
    files = {'image': uploaded_file}
    # Send a POST request
    with st.spinner('Analysing your ID card...'):
        try:
            response = requests.post(url, files=files, timeout=100)
            # Check if the request was successful
            if response.status_code == 200:
                col1, col2 = st.columns(2)
                st.success('Analysing is done!', icon="✅")
                Data = response.json()
                if 'Info' in Data:
                    data = Data['Info']
                else:
                    data = {}
                if 'Prtrate' in Data:
                    portrate = Data['Prtrate']
                    portre = True

                col2.markdown(
                    """
                <style>
                [data-testid="stMetricValue"] {
                    font-size: 30px;
                }
                </style>
                """,
                    unsafe_allow_html=True,
                )
                if 'Name' in data:
                    col2.metric(label="نام", value=data['Name'])
                    
                if 'Family Name' in data:
                    col2.metric(label="نام خانوادگی", value=data['Family Name'])
                    
                if "Father's Name" in data:
                    col2.metric(label="نام پدر", value=data["Father's Name"])
                    
                if 'ID' in data:
                    col2.metric(label='کد ملی', value=data['ID'])
                    
                if 'City' in data:
                    col2.metric(label='محل تولد', value=data['City'])
                    
                if 'birsth date_per' in data:
                    col2.metric(label='تاریخ تولد', value=data['birsth date_per'])
                    
                if 'Gender' in data:
                    if data['Gender'] == 'man':
                        gen = 'مرد'
                    else:
                        gen = 'زن'
                    col2.metric(label='جنسیت', value=gen)
                    
                if portre:
                    plt.imshow(portrate)
                    plt.axis('off')
                    portrate_path = 'saved_figure.png'
                    plt.savefig(portrate_path)
                    col1.image(portrate_path, caption='آواتار استخراج شده از کارت ملی')
            else:
                error = 'Failed to upload image:' + str(response.status_code) + str(response.text)
                st.error('This is an error:' + '\n' + error, icon="🚨")
        except requests.RequestException as e:
            st.error('This is an error with server:' + '\n' + str(e), icon="🚨")
```

## Notes

- Ensure that the API endpoint specified in the `url` variable is running and accessible.
- The extracted portrait image, if available, is displayed on the left side of the webpage.
- The text is displayed in Persian (Farsi).

## Authors
- [Suorena Saeedi](https://github.com/ssuorena)