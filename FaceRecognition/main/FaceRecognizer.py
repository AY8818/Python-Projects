import numpy as np
import face_recognition
import cv2
import os
from datetime import datetime

img_database_path = "C:/Users/DELL/Desktop/Python Projects/FaceRecognition/ImagesDatabase"
images = []
DB_Img_Names = []
myList = os.listdir(img_database_path)
print(myList)
for i in myList:
    current_Img = cv2.imread(f"{img_database_path}/{i}")
    images.append(current_Img)
    DB_Img_Names.append(os.path.splitext(i)[0])
print(DB_Img_Names)


def calcEncodings(images):
    encodedList=[]
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodedList.append(encode)
    return encodedList

def loggingIntoDatabase(name):
    logFilePath = "C:/Users/DELL/Desktop/Python Projects/FaceRecognition/LoggerDatabase/WebcamLogs.csv"
    with open(logFilePath,'r+') as f:
        retrivedDataList = f.readline()
        namesList=[]
        for data in retrivedDataList:
            currData = data.split(",")
            namesList.append(currData[0])
        if name not in namesList:
            now = datetime.now()
            currTime = now.strftime("%H:%M:%S")
            f.writelines(f"\n{name},{currTime}")

encode_List_From_DB = calcEncodings(images)
print(len(encode_List_From_DB))
print("Complete !!!")

#Initialize Webcam
print("Accessing webcam")
cap = cv2.VideoCapture(0) #Accessing thge webcam
print("webcam active")
while True:

    success, img = cap.read() #This will give us our image
    compressed_img = cv2.resize(img,(0,0),None,0.25,0.25) #reducing image size to 1/4th of the OG size by using 0.25
    compressed_img = cv2.cvtColor(compressed_img,cv2.COLOR_BGR2RGB) #converting it into RGB
    # Finding the encoding of our webcam
    facesInCurrFrame = face_recognition.face_locations(compressed_img)
    encodingOfCurFrame = face_recognition.face_encodings(compressed_img,facesInCurrFrame)

    #iterating through all the faces we have found and comparing it with the images in the DB
    for encode,faceLoc in zip(encodingOfCurFrame,facesInCurrFrame):

        matches = face_recognition.compare_faces(encode_List_From_DB,encode)#finding the matches
        faceDis = face_recognition.face_distance(encode_List_From_DB,encode) #finding the face distance

        matchedEncodingIndx = np.argmin(faceDis) #gives the minimum facedistance index after matching the image in database

        if matches[matchedEncodingIndx]: #finds the name for the matched minimum face index
            name = DB_Img_Names[matchedEncodingIndx].upper()
            print(name)

            y1,x2,y2,x1 = faceLoc #extracting all the coordinate values from the list
            y1 = y1 * 4 # making it retturn it into original size since we are using real image to display the rectangle
            x2 = x2 * 4
            y2 = y2 * 4
            x1 = x1 * 4

            cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),2) #displayes the square on the face detected
            # on image in the webcam in real time
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(255,0,0),cv2.FILLED)  #displayes the square to write name
            print("logging Entry into DB")
            loggingIntoDatabase(name)  # sending the name to get logged in db
            print("Logging Successfull..!!!")

            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2) #displays the name
        cv2.imshow('webcam',img) #making webcam screen on display
        cv2.waitKey(1)







