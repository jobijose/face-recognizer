import glob
import os

import dlib
import cv2 as cv2
import numpy as np
from datetime import datetime, timedelta
import logging
import paho.mqtt.client as mqtt

# Provide MQTT Broker host
MQTT_BROKER = "localhost"
# Topic on which frame will be published
MQTT_TOPIC = "devices/camera/face_recognizer"
RECIEVE_TOPIC= "/devices/attic/docksocket/state"
ON = "ON"
OFF = "OFF"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

frame = np.zeros((240, 320, 3), np.uint8)

last_time = datetime.min
last_state = OFF

def on_message(client, userdata, msg):
    received_data = msg.payload.decode("utf-8")
    logger.info(f"Message recieved in {msg.topic} with message {received_data}")
    global last_time, last_state
    last_state = received_data = ON if received_data == "ON" else OFF
    if last_state == ON:
        last_time = datetime.now()
        

# Phao-MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.username_pw_set(username="user", password="######")
# Establishing Connection with the Broker
client.connect(MQTT_BROKER, 1883)
client.on_message = on_message
client.subscribe(RECIEVE_TOPIC, 2)
client.loop_start()


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
            logger.debug("distance = {}".format(dist))
            if(dist < 0.6):
                check_and_publish(ON)
                return "success"
            else:
                check_and_publish(OFF)
                return "face not recognized"
      
    if len(live_img_detect) == 0:
        check_and_publish(OFF)
            

def initialize_data_set():
    for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
        logger.debug("Processing file: {}".format(f))
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

def check_and_publish(message):
    global last_time, last_state
    past_time = datetime.now() - timedelta(hours=1)
    logger.debug(f"Past time: {past_time} and last time: {last_time}")
    if last_time < past_time:
        if last_state != message:
            client.publish(MQTT_TOPIC, message)
            logger.info(f"Message published with message: {message}")
            last_state = message
            client.publish(MQTT_TOPIC, message)
        if last_state == ON:
            last_time = datetime.now()
    else:
        if message == ON:
            if last_state == OFF:
                logger.info(f"Message published with message: {message}")
                client.publish(MQTT_TOPIC, message)
            last_state = message
            last_time = datetime.now()
