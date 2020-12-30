# Cynapto_Task

**AIM**: To Read a given 720p video in `.mp4` format, then count and display the number of unique faces detected on current frame. Then Save the newly created 
         video in 720p, 20 FPS in `.mp4` format.
         
File Structure:

         |- efficient_face_recognition.py*
         |- Input_video.mp4*
         |- README.md*
         |- Experimenting_with_cython 
                  |
                  |- build
                  |- efficient_face_recognition.c*
                  |- efficient_face_recognition.cp37-win_amd64.pyd*
                  |- efficient_face_recognition.pyx*
                  |- efficient_face_recognition.html*

Here is the general approach towards achieving the primary objective of the assignment:

1. `efficient_face_recognition.py` is the main python script that performs the said AIM of the assignment. 
2. It reads the `Input_video.mp4` video file frame by frame then stores it into a `numpy` list of BGR image sequnce of each frame of the video.
3. After getting total number of frames read from the video, the entire array is distributed into n "chunks" where n = #CPU cores.
4. By distributing the work into individual CPU cores, we call a worker function that using the `face_recognition` library to find `face_encodings` and `bounding_boxes`              of all the faces in current frame.
5. `face_encoding` is a 128 dimenstional representation of the faces in frame. `bounding_boxes` contains the *left_top* and *right_bottom* co-ordinates of the bounding boxes for      the face.
6. For each frame, we take in all the face_encoding and see if the total number of distinct face_encoding matches the #bounding_boces.
7. *If yes*: That means all the faces on the frame are distinct.
   *If No*:
