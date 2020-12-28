from multiprocessing import Pool
import cv2
import face_recognition

# Video explaining basic multithreading: https://www.youtube.com/watch?v=vbtxtvuCFRM
frames = []

class single_frame_detection:

    def create_video_snippets(self, frames):
        total = len(frames)
        total_threads = 2
        frames1 = frames[:int(len(frames)/2)]
        frames2 = frames[int(len(frames)/2):]

        '''
        print("Total Frames: ", len(frames))
        print("Calculated Frames in 1st snippet: {}, Actual Frames in 1st Snippet: {}".format(len(frames)/2, len(frames1)))
        print("Calculated Frames in 2nd snippet: {}, Actual Frames in 2nd Snippet: {}".format(len(frames)/2+1, len(frames2)))

        print("All Frames accounted for") if (len(frames) == (len(frames1) + len(frames2))) else print("{} frames missing".format(len(frames) - (len(frames1) + len(frames2))))
        
        for frame in frames1:
            cv2.imshow("snippet1", frame)
            cv2.waitKey(1)
        for frame in frames2:
            cv2.imshow("snippet2", frame)
            cv2.waitKey(1)
        '''
        return frames1, frames2

    def detect_faces(self, frame_seq, num):
        for frame in frame_seq:
            cv2.imshow(str(num), frame)
            cv2.waitKey(20)
        cv2.destroyAllWindows()


def read_frames():
    video_path = './Input Video/Captain_America_ Civil_War.mp4'
    cap = cv2.VideoCapture(video_path)

    scaling_factor = 1.5

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

def multi_face_detection(frame_seq1, frame_seq2):
    a = single_frame_detection()
    b = single_frame_detection()
    pool = Pool(processes=2)
    p1 = pool.apply_async(a.detect_faces, [frame_seq1, 1])
    p2 = pool.apply_async(b.detect_faces, [frame_seq2, 2])

    pool.close()
    pool.join()



read_frames()

ob1 = single_frame_detection()
frames1, frames2 = ob1.create_video_snippets(frames)
multi_face_detection(frames1, frames2)



