import cv2
from imutils import paths
import face_recognition
import os
input_video_path = './Input Video/Captain_America_ Civil_War.mp4'

cap = cv2.VideoCapture(input_video_path)
scaling_factor = 1.5
total_encodings = []
flag = False

def recognize_uniquefaces(rgb, boxes):
    curr_encodings = face_recognition.face_encodings(rgb, boxes)
    # total_encodings.append(curr_encodings)
    if (len(total_encodings) == 0):
        total_encodings.append(curr_encodings)
        print("This ran once")
    else:
        for encoding in curr_encodings:
            results = face_recognition.api.compare_faces(total_encodings, encoding, tolerance=0.2)
            # print(len(encoding))
            #for result in results:
            #    print(result)

            print("result", results)
            '''if (result == True for result in results):
                print("No new face in scene")
            else:
                print("A new Face found")'''
        #pass

while(True):
    ret, frame = cap.read()
    rgb = cv2.resize(frame, (int(frame.shape[1]/scaling_factor), int(frame.shape[0]/scaling_factor)))
    if (ret):
        # cv2.imshow("frame", frame)
        rgb = cv2.cvtColor(rgb ,cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model='cnn')
        if (len(boxes) != 0):
            recognize_uniquefaces(rgb, boxes)

        for box in boxes:
            cv2.rectangle(frame, (int(box[3]*scaling_factor), int(box[0]*scaling_factor)), (int(box[1]*scaling_factor), int(box[2]*scaling_factor)), (0, 255, 0), 2)
            # cv2.rectangle(frame, (int(box[3]), int(box[0])), (int(box[1]), int(box[2])), (0, 255, 0), 2)
            # print("Printing individually:", box[0])
        cv2.imshow("Faces", frame)
        if (cv2.waitKey(1) == 27):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
