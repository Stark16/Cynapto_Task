import cv2
import face_recognition


frames = []
video_path = './../Videos/Input_video.mp4'
cap = cv2.VideoCapture(video_path)

scaling_factor = 1.5


while(True):
    ret, frame = cap.read()
    if(ret):
        cv2.imshow("video", frame)
        frames.append(frame)
        if (cv2.waitKey(1) == 27):
            break
    else:
        break
cv2.destroyAllWindows()
cap.release()


def count_distict_faces(rgb, boxes):
    encodings = face_recognition.face_encodings(rgb, boxes)
    face_count = 0
    if (len(boxes) != 0):
        if (len(boxes) == 1):
            face_count = 1

        elif (len(boxes)>1):
            true_set = 0
            for encoding in encodings:
                result = (face_recognition.compare_faces(encodings, encoding, tolerance=0.3))

                if (result.count(True) == 1):
                    # print("All distict Faces in the frame")
                    face_count += 1
            if (face_count != len(boxes)):
                diff = len(boxes) - face_count
                if (2 <= diff <= 3):
                    face_count += 1
    #print("{} Unique Faces detected in the Frame".format(face_count))

    return face_count, encodings


def count_total_faces(face_encoders):
    pass



for frame in frames:
    rgb = cv2.resize(frame, (int(frame.shape[1] / scaling_factor), int(frame.shape[0] / scaling_factor)))
    # cv2.imshow("frame", frame)
    rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model='cnn')
    for box in boxes:
        cv2.rectangle(frame, (int(box[3]*scaling_factor), int(box[0]*scaling_factor)), (int(box[1]*scaling_factor), int(box[2]*scaling_factor)), (0, 255, 0), 2)
        # cv2.rectangle(frame, (int(box[3]), int(box[0])), (int(box[1]), int(box[2])), (0, 255, 0), 2)
        # print("Printing individually:", box[0])
    # print(len(boxes))
    no_of_faces, face_encoders = count_distict_faces(rgb, boxes)
    if (no_of_faces != 0):
        total_no_faces = count_total_faces(face_encoders)

    font = cv2.FONT_HERSHEY_DUPLEX
    if (no_of_faces == 0):
        text = "No Faces Detected :("
    elif(no_of_faces == 1):
        text = str(no_of_faces) + " Unique Face"
    else:
        text = str(no_of_faces) + " Unique Faces"
    #print(frame.shape)
    cv2.putText(frame, text, (0, 40), font, 1, (100, 100, 240))

    cv2.imshow("Faces", frame)
    if (cv2.waitKey(30) == 27):
            break
