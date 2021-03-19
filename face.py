
import face_recognition
import cv2
import numpy as np
from datetime import datetime
from openpyxl import Workbook
workbook = Workbook()
sheet = workbook.active
now = datetime.now()

video_capture = cv2.VideoCapture(0)
lisha_image = face_recognition.load_image_file("LISHA.jpeg")
lisha_face_encoding = face_recognition.face_encodings(lisha_image)[0]

dhanam_image = face_recognition.load_image_file("DHANAM.jpeg")
dhanam_face_encoding = face_recognition.face_encodings(dhanam_image)[0]

dhanam_image = face_recognition.load_image_file("NANDHINI.jpeg")
dhanam_face_encoding = face_recognition.face_encodings(dhanam_image)[0]

known_face_encodings = [
    lisha_face_encoding,
    dhanam_face_encoding
]
known_face_names = [
    "lisha",
    "dhanam",
    "nandhini"
]


while True:

    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            print (now)
            sheet["A1"] = now
            print (name)
            sheet["B1"] = name
            print ('present')
            sheet["C1"] = 'present'
	    
            workbook.save(filename="attenance.xlsx")
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
