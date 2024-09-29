# OCR Service for ID Cards

This service provides Optical Character Recognition (OCR) for ID cards using Django and several libraries such as EasyOCR, Keras, and Flair. The main functionality is to extract information from images of ID cards, including the ID number, name, birth date, and gender.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoint](#api-endpoint)
- [Project Structure](#project-structure)


## Features

- Upload an image of an ID card and get extracted information.
- Detect and extract the ID number, name, birth date, and gender.
- Perform OCR using EasyOCR.
- Use pre-trained models for gender detection and named entity recognition (NER).

## Requirements

- Python 3.11.5
- Django
- Django REST framework
- Pillow
- EasyOCR
- Keras
- OpenCV
- Flair
- Pandas
- NumPy

## Installation

1. Clone the repository:

```bash
git https://github.com/ssuorena/National-ID-OCR.git
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Run the Django development server:

```bash
python manage.py runserver
```

## Usage

To use the OCR service, send a POST request to the `/upload/` endpoint with an image file of the ID card.

### Example request:

```bash
curl -X POST -F 'image=@path/to/your/image.jpg' http://localhost:8000/upload/
```

### Example response:

```json
{
    "Info": {
        "ID": "1234567890",
        "Family Name": "Doe",
        "Name": "John",
        "Father's Name": "Smith",
        "City": "Tehran",
        "birsth date_per": "1400/01/01",
        "birsth date": "2021-03-21T00:00:00",
        "Gender": "man"
    },
    "Prtrate": [
        image in  UTF-8 format
    ]
}
```

## API Endpoint

### POST /upload/

Uploads an image and returns the extracted information.

**Request:**

- `image`: The image file of the ID card.

**Response:**

- `Info`: A dictionary containing extracted information such as ID, name, family name, father's name, city, birth date, and gender.
- `Prtrate`: An array of prtrate extracted from the ID card.

## Project Structure

```plaintext
OCRbackend/
│
├── cityCode.xlsx
├── db.sqlite3
├── Dockerfile
├── manage.py
├── myapp/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── views.py
│   ├── OCR.py
│   └── ...
├── Models/
│   ├── gender_detection.model
│   └── smallervggnet.py
├── OCRbackend/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── User_ID_Card/
├── Working images/
├── requirements.txt
└── README.md
```


## Authors
- [Suorena Saeedi](https://github.com/ssuorena)