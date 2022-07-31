import cv2
import face_recognition
import numpy as np

imgpath1="C:/Users/DELL/Desktop/Python Projects/FaceRecognition/ImagesDatabase/jeffbezos.jpg"
imgpath2 = "C:/Users/DELL/Desktop/Python Projects/FaceRecognition/ImagesDatabase/apj.jpg"

print(imgpath1)
imgJeff = face_recognition.load_image_file(imgpath1)
print(imgpath2)
imgTest = face_recognition.load_image_file(imgpath2)

#converting BGR to RGB
imgJeff = cv2.cvtColor(imgJeff,cv2.COLOR_BGR2RGB)
imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)

print("Processing img 1")
faceLocation = face_recognition.face_locations(imgJeff)[0]
encode_img = face_recognition.face_encodings(imgJeff)[0]
cv2.rectangle(imgJeff,(faceLocation[3],faceLocation[0]),(faceLocation[1],faceLocation[2]),(255,255,0),2)

print("Processing img 2")
faceLocation2 = face_recognition.face_locations(imgTest)[0]
encode_img2 = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest,(faceLocation2[3],faceLocation2[0]),(faceLocation2[1],faceLocation2[2]),(255,255,0),2)

results = face_recognition.compare_faces([encode_img], encode_img2)
faceDistance = face_recognition.face_distance([encode_img],encode_img2)
print("Face Match = ",results)
print("face Distance = ",faceDistance)

print("Displaying img")
cv2.putText(imgTest,f"{results} {round(faceDistance[0],2)}",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
cv2.imshow('Jeff Bezos',imgJeff)
cv2.imshow('test image',imgTest)
cv2.waitKey(0)



