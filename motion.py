# import cv2 

# def noise():
#     cap = cv2.VideoCapture(0)

#     while True:
#         _, frame1 = cap.read()
#         _, frame2 = cap.read()

#         diff = cv2.absdiff(frame2, frame1)
#         diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

#         diff = cv2.blur(diff, (5,5))
#         _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

#         contr, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
#         if len(contr) > 0:
#             max_cnt = max(contr, key=cv2.contourArea)
#             x,y,w,h = cv2.boundingRect(max_cnt)
#             cv2.rectangle(frame1, (x, y), (x+w, y+h), (0,255,0), 2)
#             cv2.putText(frame1, "MOTION", (10,80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)

#         else:
#             cv2.putText(frame1, "NO-MOTION", (10,80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2)

#         cv2.imshow("esc. to exit", frame1)

#         if cv2.waitKey(1) == 27:
#             cap.release()
#             cv2.destroyAllWindows()
#             break

from pushbullet import Pushbullet
import cv2
import pyaudio
import numpy as np

def noise():
    cap = cv2.VideoCapture(0)
    pb = Pushbullet("o.ccBV28puTI1WHF7bjKeRT2miHIXbFwxJ")
    p = pyaudio.PyAudio()
    
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)
    except Exception as e:
        print(f"Error opening audio stream: {e}")
        return

    while True:
        _, frame1 = cap.read()
        _, frame2 = cap.read()

        diff = cv2.absdiff(frame2, frame1)
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        diff = cv2.blur(diff, (5, 5))
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        contr, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contr) > 0:
            max_cnt = max(contr, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(max_cnt)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame1, "MOTION", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            push = pb.push_note("Motion Alert!", "Some Motion Dected")
        else:
            cv2.putText(frame1, "NO-MOTION", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

        # Process audio data (example: print RMS value)
        try:
            audio_data = np.frombuffer(stream.read(1024), dtype=np.int16)
            rms = np.sqrt(np.mean(np.square(audio_data)))
            print(f"Audio RMS: {rms}")
        except Exception as e:
            print(f"Error processing audio data: {e}")

        cv2.imshow("esc. to exit", frame1)

        if cv2.waitKey(1) == 27:
            cap.release()
            cv2.destroyAllWindows()
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

# noise()
