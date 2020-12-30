from multiprocessing import Pool        # Pythons Multiprocessing Library
import multiprocessing
import cv2                              #
import numpy as np
import face_recognition                 # Library that has pretrained models for face recognition
import time
from tqdm import tqdm                   # tqdm to visually show task progress


# Function that reads the video frames and returns it in frames Variable:
# By default it can read video of any length, but one can press ESC read the frames to that point in the video


def read_frames(input_path):
    video_path = input_path  # Path to the Video File:
    cap = cv2.VideoCapture(video_path)
    frames = []  # Variable that will be storing the entire video frame vise

    while (True):
        ret, frame = cap.read()
        if (ret):
            cv2.imshow("video", frame)
            frames.append(frame)
            if (cv2.waitKey(1) == 27):
                break
        else:
            break
    cv2.destroyAllWindows()
    cap.release()
    frames = np.array(frames)
    return frames


# Function that takes RGB image as input and returns # Faces in the image, and their 128-dim Feature vector:
# Count_distinct_faces also return face_encodings of each frame which can be used to count total #unique faces
# till current frame.
def Count_distinct_faces(rgb, boxes):
    # encodings variable holds the 128-dim features in the current frame
    encodings = face_recognition.face_encodings(rgb, boxes)
    face_count = 0
    if (len(boxes) != 0):
        if (len(boxes) == 1):
            face_count = 1

        elif (len(boxes) > 1):
            for encoding in encodings:
                result = (face_recognition.compare_faces(encodings, encoding, tolerance=0.3))

                if (result.count(True) == 1):
                    # print("All distinct Faces in the frame")
                    face_count += 1
            if (face_count != len(boxes)):
                diff = len(boxes) - face_count
                if (2 <= diff <= 3):
                    face_count += 1
    # print("{} Unique Faces detected in the Frame".format(face_count))

    return face_count, encodings


# Function is also a worker function:
# > It is provided with a chunk of video frames out of the total video frames.
# > An instance of this function runs on each core of the PC to:
#       1. Detect the faces in each frame in the given chunk of the video.
#       2. Mark the Faces with Green Squares using cv2.rectangle().
#       3. Then the function calls Count_distinct_faces(rgb, boxes) to get #faces in current frame.
#       4. It then prints the #faces in current frames on the left top corner of each frame.
#       5. It then returns the frames that have faces and #faces written on it, to be reassembled.

def Prepare_frames(frames_seq):
    marked_frames = np.empty_like(frames_seq)

    for i, frame in tqdm(enumerate(frames_seq)):
        rgb = cv2.resize(frame, (int(frame.shape[1] / 1.5), int(frame.shape[0] / 1.5)))
        rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model='cnn')
        for box in boxes:
            cv2.rectangle(frame, (int(box[3] * 1.5), int(box[0] * 1.5)), (int(box[1] * 1.5), int(box[2] * 1.5)),
                          (0, 255, 0), 2)
        # print("1 frame converted now:", len(boxes))

        no_of_faces, face_encoders = Count_distinct_faces(rgb, boxes)

        font = cv2.FONT_HERSHEY_DUPLEX

        # A completely unnecessary if else ladder performance wise,
        # But completely necessary to have a good english sence when printing #faces in current frame.
        if (no_of_faces == 0):
            text = "No Faces Detected :("
        elif (no_of_faces == 1):
            text = str(no_of_faces) + " Unique Face"
        else:
            text = str(no_of_faces) + " Unique Faces"
        # print(frame.shape)
        cv2.putText(frame, text, (0, 40), font, 1, (100, 100, 240))
        marked_frames[i] = frame

    # marked_frames = np.array(marked_frames)
    print("Batch Done")
    return marked_frames


# This Function saves the resulting video as the output video at 20 FPS.
def save_video(result, final_video):
    i = 0

    for res in result:
        for frame in res:
            final_video[i] = frame
            i += 1

    out = cv2.VideoWriter("Output_Video.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 20, (1280, 720))
    for frame in tqdm(final_video):
        out.write(frame)
        cv2.imshow("Finally", frame)
        cv2.waitKey(24)
    cv2.destroyAllWindows()

    print("Video saved by the name Output_Video,mp4:")



if __name__ == '__main__':
    # Some variables that store paths:
    # TO change the input video or output video path one can change the following variables.
    # I was originally planning on doing argpars, but since I am using Pycharm and run scripts from there directly
    # I haven't used argparse.

    input_path = './Input Video/Input_video.mp4'
    output_path = "Output_Video.mp4"
    frames = read_frames(input_path)
    frame_seq = np.array_split(frames, multiprocessing.cpu_count())

    print("Printing OriginalSizes:")
    print("Total: {}, Batch 1: {}, Batch 2: {}, Batch 3: {}, Batch 4: {}, Total Again:{}".format(len(frames),
                                                                                                 len(frame_seq[0]),
                                                                                                 len(frame_seq[1]),
                                                                                                 len(frame_seq[2]),
                                                                                                 len(frame_seq[3]),
                                                                                                (len(frame_seq[0]) +
                                                                                                 len(frame_seq[1]) +
                                                                                                 len(frame_seq[2]) +
                                                                                                 len(frame_seq[3])
                                                                                                )
                                                                                                )
          )
    print()

    print("Starting Face_Detection Process:")
    print()

    pool = Pool(multiprocessing.cpu_count())
    start = time.time()
    result = pool.map(Prepare_frames, frame_seq)
    pool.close()
    pool.join()

    print()
    print("Face Detection Done, now printing dimensions of results:")
    print("Total: {}, Segment1: {}, Segment2: {}, Segment3: {}, Segment4: {}, Total Again:{}".format(len(result),
                                                                                                     len(result[0]),
                                                                                                     len(result[1]),
                                                                                                     len(result[2]),
                                                                                                     len(result[3]),
                                                                                                     (len(result[0]) +
                                                                                                      len(result[1]) +
                                                                                                      len(result[2]) +
                                                                                                      len(result[3])
                                                                                                      )
                                                                                                     )
          )

    end = time.time()
    print()
    print("Time taken by 4 Cores: {}s".format(end - start))
    print("All processing Done")
    print()
    print("Now Saving Video:")

    final_video = np.empty_like(frames)
    save_video(result, final_video)

