# HemaVision

HemaVision is a Flask-based web application that estimates hemoglobin (Hb) levels from eye images using image processing techniques.

## Features
- Upload an image of an eye
- Detect the region of interest (ROI) and process it
- Extract color information and estimate Hb levels
- Display results with visualized ROI images

## Installation

### Prerequisites
Make sure you have Python installed on your system.

### Clone the Repository
```bash
git clone https://github.com/your-username/HemaVision.git
cd HemaVision
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Download Haarcascade Classifier
Ensure that `haarcascade_eye.xml` is in the project directory. You can download it from OpenCV's GitHub repository:
```bash
wget https://github.com/opencv/opencv/raw/master/data/haarcascades/haarcascade_eye.xml
```

## Usage

### Run the Application
```bash
python app.py
```
The app will run on `http://127.0.0.1:5000/` by default.

### Steps to Use
1. Open the web app in a browser.
2. Select gender and upload an eye image.
3. Click submit to process the image.
4. View the estimated hemoglobin level and processed eye images.

## Project Structure
```
HemaVision/
│-- static/
│   ├── HemaVisionLogo.jpg
│   ├── slicebg.mp4
│   ├── ROI_1.jpg
│   ├── ROI_Reduced.jpg
│-- templates/
│   ├── index.html
│   ├── result.html
│-- app.py
│-- haarcascade_eye.xml
│-- requirements.txt
│-- README.md
```

## Dependencies
- Flask
- OpenCV (cv2)
- NumPy

## Future Improvements
- Improve eye detection using deep learning models
- Add support for real-time video processing
- Enhance the UI with better design elements

## License
This project is licensed under the MIT License.

## Author
[Your Name](https://github.com/your-username)

