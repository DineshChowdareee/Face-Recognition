

from flask import Flask, render_template, Response
import cv2
import face_recognition
import numpy as np
app=Flask(__name__)
camera = cv2.VideoCapture(0)

dinesh_image = face_recognition.load_image_file("Krish/krish.jpg")
dinesh_face_encoding = face_recognition.face_encodings(dinesh_image)[0]


sheshank_image = face_recognition.load_image_file("Bradley/bradley.jpg")
sheshank_face_encoding = face_recognition.face_encodings(sheshank_image)[0]

nithish_image = face_recognition.load_image_file("Nithish/nithi.jpg")
nithish_face_encoding = face_recognition.face_encodings(nithish_image)[0]

known_face_encodings = [
    dinesh_face_encoding,
    sheshank_face_encoding,
    nithish_face_encoding
]
known_face_names = [
    "Dinesh",
    "Sheshank",
    "Nithish"
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def gen_frames():  
    while True:
        success, frame = camera.read() 
        if not success:
            break
        else:
        
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
           
            rgb_small_frame = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
            
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

               
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    app.run(debug=True)