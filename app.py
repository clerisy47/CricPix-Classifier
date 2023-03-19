from flask import Flask, request, render_template
import cv2
import pywt
import numpy as np
import joblib 
import json

flask_app = Flask(__name__)
model = joblib.load(open("model.pkl", "rb"))

face_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_eye.xml')

with open('class_dictionary.json', 'r') as f:
    data = json.load(f)
class_dict = dict(data)

def key_from_value(dictionary, value):
    for key in dictionary:
        if dictionary[key] == value:
            return key

def get_cropped_image_if_2_eyes(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            return roi_color
        
def w2d(imArray, mode='haar', level=1):
    imArray = cv2.cvtColor(imArray,cv2.COLOR_RGB2GRAY)
    imArray =  np.float32(imArray)   
    imArray /= 255
    coeffs=pywt.wavedec2(imArray, mode, level=level)
    coeffs_H=list(coeffs)  
    coeffs_H[0] *= 0;  
    imArray_H=pywt.waverec2(coeffs_H, mode)
    imArray_H *= 255
    imArray_H =  np.uint8(imArray_H)
    return imArray_H
        
@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route("/predict", methods = ["POST"])
def predict():
    image = request.files['image']
    img = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    if img is None or img.size == 0:
        message = "Model cannot read this image."
    else:
        scalled_raw_img = cv2.resize(img, (32, 32))
        img_har = w2d(img,'db1',5)
        scalled_img_har = cv2.resize(img_har, (32, 32))
        combined_img = np.vstack((scalled_raw_img.reshape(32*32*3,1),scalled_img_har.reshape(32*32,1)))
        combined_img = combined_img.reshape(-1, 4096)

        pred =model.predict(combined_img)
        print(pred)
        message = f"The image is of {key_from_value(class_dict, pred)}"

    return render_template("index.html", message=message)


if __name__ == "__main__":
    flask_app.run(debug=True)
