import glob
import os

import dlib
from flask import Flask, request
from waitress import serve
import cv2 as cv2
import numpy as np

import paho.mqtt.client as mqtt

MQTT_BROKER = "escanor.local"
# Topic on which frame will be published
MQTT_TOPIC = "devices/camera/face_recognizer"

frame = np.zeros((240, 320, 3), np.uint8)

# Phao-MQTT Client
client = mqtt.Client()
client.username_pw_set(username="##", password="#####")
# Establishing Connection with the Broker
client.connect(MQTT_BROKER, 1883)


face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
faces_folder_path = "./images"

predictor_path = "./model/shape_predictor_5_face_landmarks.dat"
face_rec_model_path = "./model/dlib_face_recognition_resnet_model_v1.dat"
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)
img_representation = []

def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
        
    return faces

def use_cv2(frame) :

    video_frame = frame  # read frames from the video
   
    faces = detect_bounding_box(
        video_frame
    )  # apply the function we created to the video frame

    
def recognizer(live_image):
   
    live_img_detect = detector(live_image, 1)
    print("No of face detected: " + str(len(live_img_detect)))
    face_descriptor = np.empty(1)
    for k, d in enumerate(live_img_detect):
        live_shape = sp(live_image, d)
        live_aligned_face = dlib.get_face_chip(live_image, live_shape)
        face_descriptor = face_rec_model.compute_face_descriptor(live_aligned_face)
        face_descriptor = np.array(face_descriptor)
        for arr in img_representation:
            dist = find_euclidean_distance(arr, face_descriptor)
            print("distance = {}".format(dist))
            if(dist < 0.6):
                client.publish(MQTT_TOPIC, "ON")
                return "success"
            else:
                return "failed"
        

app = Flask(__name__)

@app.post('/devices/images')
def recognizeImage():
    img = request.files['image'].read()

    # print(request.get_data())
    # img = base64.b64decode(img)
    # converting into numpy array from buffer
    # print(type(img))
    npimg = np.frombuffer(img, dtype=np.uint8)
    # img = cv2.imread("./1.jpg")
    
    # Decode to Original Frame
    # frame = cv2.imdecode(npimg, 1)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # cv2.imshow('image', gray_frame) 
    # filename =  "abc.jpg"
    
    # with open(filename, 'wb') as file:
    #     file.write(img)
    # use_cv2(frame)
    recognizer(gray_frame)
    return "success"

def initialize_data_set():
    for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
        print("Processing file: {}".format(f))
        img = dlib.load_rgb_image(f)

        img_detected = detector(img, 1)

        # Now process each face we found.
        for k, d in enumerate(img_detected):
            shape = sp(img, d)
            aligned_img = dlib.get_face_chip(img, shape)        
            img_array_represent = face_rec_model.compute_face_descriptor(aligned_img)
            img_array_represent = np.array(img_array_represent)
            img_representation.append(img_array_represent)
            
def find_euclidean_distance(source, test):
    ed = source - test
    ed = np.sum(np.multiply(ed, ed))
    ed = np.sqrt(ed)
    return ed

if __name__ == '__main__':
    initialize_data_set()
    serve(app, host='0.0.0.0', port='9090')
