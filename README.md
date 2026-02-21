# Smart Helmet Violation Detection System

A computer vision-based system to detect motorcyclists without helmets and capture their license plates.

## Features
- **Real-time Detection**: Identifies riders not wearing helmets using YOLOv8.
- **ANPR Intergration**: Extracts license plate numbers using EasyOCR.
- **Violation Logging**: Automatically saves evidence (image + plate number) to a SQLite database.
- **Web Dashboard**: Live video feed and historical violation log.

## Directory Structure
```
smart_helmet_system/
├── data/               # Stores database and evidence images
├── models/             # Place your YOLOv8 weights here (helmet_yolov8.pt)
├── src/
│   ├── core/           # Detection modules (camera, detector, anpr)
│   ├── web/            # Flask application and frontend
│   └── database.py     # Database schema
├── requirements.txt
└── main.py             # Entry point
```

## Setup & Installation

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Model Setup**:
    - Download or train a YOLOv8 model to detect `['helmet', 'no_helmet', 'license_plate']`.
    - Place the model file at `models/helmet_yolov8.pt`.
    - *Note*: If not found, the system defaults to standard `yolov8n.pt` for demonstration (logic will vary).

3.  **Run the System**:
    ```bash
    python main.py
    ```

4.  **Access Dashboard**:
    Open [http://localhost:5000](http://localhost:5000) in your web browser.

## Customization
- **Camera Source**: Modify `src/web/app.py` -> `VideoStream(src=0)` (change `0` to video file path for testing).
- **Detection Logic**: Adjust `src/core/detector.py` to match your specific model classes.

## Technologies
- Python 3.x
- OpenCV & Ultralytics YOLOv8
- EasyOCR
- Flask & SQLAlchemy
- Bootstrap 5
