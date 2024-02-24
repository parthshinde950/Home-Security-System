
import cv2
import time
import numpy as np
from pushbullet import Pushbullet

def find_motion():
    pb = Pushbullet("o.ccBV28puTI1WHF7bjKeRT2miHIXbFwxJ")
    motion_detected = False
    is_start_done = False

    cap = cv2.VideoCapture(0)

    print("waiting for 2 seconds")
    time.sleep(2)

    _, frm1 = cap.read()
    frm1_gray = cv2.cvtColor(frm1, cv2.COLOR_BGR2GRAY)

    # Initialize variables for frame averaging
    num_frames_to_average = 10
    frame_buffer = [frm1_gray] * num_frames_to_average

    while True:
        _, frm2 = cap.read()
        frm2_gray = cv2.cvtColor(frm2, cv2.COLOR_BGR2GRAY)

        # Add current frame to buffer
        frame_buffer.pop(0)
        frame_buffer.append(frm2_gray)

        # Average frames in buffer
        averaged_frame = np.mean(frame_buffer, axis=0).astype(np.uint8)

        # Calculate absolute difference between averaged frame and previous frame
        diff = cv2.absdiff(frm1_gray, averaged_frame)

        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contours = [c for c in contours if cv2.contourArea(c) > 25]

        if len(contours) > 5:
            push = pb.push_note("Motion Alert!", "Some Motion Detected")
            cv2.putText(thresh, "motion detected", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
            motion_detected = True
            is_start_done = False

        elif motion_detected and len(contours) < 3:
            if not is_start_done:
                start = time.time()
                is_start_done = True

            end = time.time()

            print(end - start)
            if (end - start) > 4:
                print("running again")
                motion_detected = False
                is_start_done = False
                time.sleep(1)
                continue

        else:
            cv2.putText(thresh, "no motion detected", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

        cv2.imshow("winname", thresh)

        frm1_gray = frm2_gray

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# find_motion()
