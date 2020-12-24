import cv2
import face_recognition

frames = []
video_path = './Input Video/Captain_America_ Civil_War.mp4'
cap = cv2.VideoCapture(video_path)


while(True):
    ret, frame = cap.read()
    if(ret):
        cv2.imshow("video", frame)
        frames.append(frame)
        if (cv2.waitKey(1) == 27):
            break
    else:
        break

for frame in frames:
    cv2.imshow("Playback", frame)
    cv2.waitKey(20)