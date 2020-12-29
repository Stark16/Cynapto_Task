from multiprocessing import Pool, Process, Array
import cv2
import numpy as np
import multiprocessing
import face_recognition
import time



def read_frames():
    video_path = './Input Video/Input_video.mp4'
    cap = cv2.VideoCapture(video_path)
    frames = []

    while (True):
        ret, frame = cap.read()
        if (ret):
            cv2.imshow("video", frame)
            frames.append(frame)
            if (cv2.waitKey(30) == 27):
                break
        else:
            break
    cv2.destroyAllWindows()
    cap.release()
    frames = np.array(frames)
    return frames


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


def prepare_frames(frames_seq):
    marked_frames = np.empty_like(frames_seq)

    for i, frame in enumerate(frames_seq):
        rgb = cv2.resize(frame, (int(frame.shape[1] / 1.5), int(frame.shape[0] / 1.5)))
        rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model='cnn')
        for box in boxes:
            cv2.rectangle(frame, (int(box[3]*1.5), int(box[0]*1.5)), (int(box[1]*1.5), int(box[2]*1.5)), (0, 255, 0), 2)
        # print("1 frame converted now:", len(boxes))

        '''no_of_faces, face_encoders = count_distict_faces(rgb, boxes)

        font = cv2.FONT_HERSHEY_DUPLEX
        if (no_of_faces == 0):
            text = "No Faces Detected :("
        elif (no_of_faces == 1):
            text = str(no_of_faces) + " Unique Face"
        else:
            text = str(no_of_faces) + " Unique Faces"
        # print(frame.shape)
        cv2.putText(frame, text, (0, 40), font, 1, (100, 100, 240))'''
        marked_frames[i] = frame

    #marked_frames = np.array(marked_frames)
    print()
    print("1 bunch Done")

    return marked_frames

'''def split_frames(no_processors, frames):
    interval_width = len(frames)//no_processors
    frame_seq = []
    for i in range(no_processors):
        frame_seq.append(frames[i:(i+1)*interval_width])
    frame_seq = np.array(frame_seq)
    print("Shape of each frame chunk: Seq1: ".format(frame_seq.shape))'''



if __name__ == '__main__':
    frames = read_frames()
    print("Total Frames: ", len(frames))



    frame_seq1 = frames[:len(frames)//2]
    frame_seq2 = frames[len(frames)//2:]
    frame_seq3 = frame_seq1[:len(frame_seq1)//2]
    frame_seq4 = frame_seq1[len(frame_seq1)//2:]
    frame_seq5 = frame_seq2[:len(frame_seq2)//2]
    frame_seq6 = frame_seq2[len(frame_seq2)//2:]



    print("Total: {}, Segment1: {}, Segment2: {}, Segment3: {}, Segment4: {}, Total Again:{}".format(len(frames), len(frame_seq3),
                                                                                                                                 len(frame_seq4), len(frame_seq5),
                                                                                                                                 len(frame_seq6),
                                                                                                                                 (len(frame_seq3)+len(frame_seq4)+
                                                                                                                                 len(frame_seq5)+len(frame_seq6))))

    frame_seq = np.array([frame_seq3, frame_seq4, frame_seq5, frame_seq6])



    start = time.time()
    #prepare_frames(frames)
    end = time.time()
    print("Time takes by single core: {}ms".format(end-start))


    pool = Pool(processes=4)

    start = time.time()


    result = pool.map(prepare_frames, frame_seq)
    pool.close()
    pool.join()

    print("Total: {}, Segment1: {}, Segment2: {}, Segment3: {}, Segment4: {}, Total Again:{}".format(len(result),
                                                                                                     len(result[0]),
                                                                                                     len(result[1]),
                                                                                                     len(result[2]),
                                                                                                     len(result[3]),
                                                                                                     (len(
                                                                                                         result[0]) + len(
                                                                                                         result[1]) +
                                                                                                      len(
                                                                                                          result[2]) + len(
                                                                                                                 result[3]))))
    end = time.time()
    print("Time taken by 2 Cores: {}ms".format(end-start))

    print("All processing Done")


    final_video = np.empty_like(frames)

    i=0
    for res in result:
        for frame in res:
            final_video[i] = frame
            i +=1


    for frame in final_video:
        cv2.imshow("Finally", frame)
        cv2.waitKey(30)
    cv2.destroyAllWindows()
















'''def prepare_frames():
    for frame in frames:
        rgb = cv2.resize(frame, (int(frame.shape[1] / 1.5), int(frame.shape[0] / 1.5)))
        # cv2.imshow("frame", frame)
        rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model='cnn')
        for box in boxes:
            cv2.rectangle(frame, (int(box[3] * 1.5), int(box[0] * 1.5)),
                          (int(box[1] * 1.5), int(box[2] * 1.5)), (0, 255, 0), 2)
        cv2.imshow("Single_Core", frame)
        cv2.waitKey(1)
        print("woking: {}".format(len(boxes)))
    cv2.destroyAllWindows()

def prepare_frames_core1(n):
    for i in range(n):
        print("Sequnce 1 Runnig")
        
        rgb1 = cv2.resize(frame1, (int(frame1.shape[1] / 1.5), int(frame1.shape[0] / 1.5)))
        # cv2.imshow("frame", frame)
        rgb1 = cv2.cvtColor(rgb1, cv2.COLOR_BGR2RGB)
        boxes1 = face_recognition.face_locations(rgb1, model='cnn')
        for box in boxes1:
            cv2.rectangle(frame1, (int(box[3] * 1.5), int(box[0] * 1.5)),
                          (int(box[1] * 1.5), int(box[2] * 1.5)), (0, 255, 0), 2)
        
        cv2.imshow("1st_Core", frame1)
        cv2.waitKey(1)
        print("Working {} Sequence 1")
    cv2.destroyAllWindows()
    

def prepare_frames_core2(n):
    for j in range(10000):
        print("Sequence {} Running".format(len(n)))
        rgb2 = cv2.resize(frame2, (int(frame2.shape[1] / 1.5), int(frame2.shape[0] / 1.5)))
        # cv2.imshow("frame", frame)
        rgb2 = cv2.cvtColor(rgb2, cv2.COLOR_BGR2RGB)
        boxes2 = face_recognition.face_locations(rgb2, model='cnn')
        for box in boxes2:
            cv2.rectangle(frame2, (int(box[3] * 1.5), int(box[0] * 1.5)),
                          (int(box[1] * 1.5), int(box[2] * 1.5)), (0, 255, 0), 2)
        
        cv2.imshow("2nd_Core", frame2)
        cv2.waitKey(1)
        print("Working {} Sequence 2")
        cv2.destroyAllWindows()
        '''