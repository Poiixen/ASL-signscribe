# ASL Sign Language Detector

For many of us, if we're away from our screens, we have the ability to use text-to-speech. 

For many mute and hard-of-hearing people, this isn't an option. This project was built to provide more inclusive solutions for their community. 
With the intention of scalability, this project could output key letters just as quickly as a person signs words. 

## Overview

A real-time, ASL sign detector designed to recognize and interpret American Sign Language (ASL) gestures. This was created during Colorstack's 2024 Winter Hackathon, so the scope of the image-recognition was limited to the ASL alphabet because of time restraints.


https://github.com/user-attachments/assets/38d2ae34-de5a-46d2-a0ea-07325aa0fc05


## Installation

Run the command `pip install -r requirements.txt` to install dependencies.

Then, launch "eyes.py" in src/ to start the localhost.

## Technology Stack

### Frontend
- **HTML**: Structuring the web interface.
- **CSS**: Styling the application for a clean and user-friendly design.
- **JavaScript**: Enabling dynamic interactions and client-side logic.

### Backend
- **Flask**: Python-based web framework for handling API requests and rendering templates.

### Machine Learning
- **Mediapipe**: Detecting hand landmarks for ASL recognition.
- **Scikit-learn**: Used for model training and prediction.
- **Pickle**: Storing and loading the trained ML model.

### Computer Vision
- **OpenCV**: Processing and analyzing video frames in real-time.

### Deployment
- **Flask Server**: Running the backend locally or on a cloud platform.

  
## Notes:
- Due to financial limitations (and how slow Python is as a language), this application *does not* run in production and *is not* publicly accessible via URL
- Because of time restraints, the model was only trained with my hands and about 300 images per letter.
