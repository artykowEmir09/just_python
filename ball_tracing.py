from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time


# -----------------------------
# Argument parsing
# -----------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="Video file path")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="Maximum buffer size")
args = vars(ap.parse_args())


# -----------------------------
# Color boundaries in HSV
# -----------------------------
colors = {
    "green": ((29, 86, 6), (64, 255, 255)),
    "blue": ((90, 50, 50), (130, 255, 255)),
    "red": ((0, 50, 50), (10, 255, 255)),
    "yellow": ((20, 100, 100), (30, 255, 255))
}


# -----------------------------
# Initialize tracked points
# -----------------------------
pts = {
    color: deque(maxlen=args["buffer"])
    for color in colors
}


# -----------------------------
# Start video capture
# -----------------------------
if args.get("video", False):
    vs = cv2.VideoCapture(args["video"])
else:
    vs = VideoStream(src=0).start()

time.sleep(2.0)


# -----------------------------
# Main loop
# -----------------------------
while True:

    frame = vs.read()

    # Video file returns different data
    if args.get("video", False):
        if isinstance(frame, tuple):
            frame = frame[1]

    # Stop if no frame
    if frame is None:
        break


    # -----------------------------
    # Resize frame
    # -----------------------------
    frame = imutils.resize(frame, width=600)


    # -----------------------------
    # Blur image
    # -----------------------------
    blurred = cv2.GaussianBlur(
        frame,
        (11, 11),
        0
    )


    # -----------------------------
    # Convert BGR → HSV
    # -----------------------------
    hsv = cv2.cvtColor(
        blurred,
        cv2.COLOR_BGR2HSV
    )


    # -----------------------------
    # Process every color
    # -----------------------------
    for color, (lower, upper) in colors.items():

        lower = np.array(lower)
        upper = np.array(upper)

        # Create mask
        mask = cv2.inRange(
            hsv,
            lower,
            upper
        )


        # Remove small noise
        mask = cv2.erode(
            mask,
            None,
            iterations=2
        )

        # Restore object area
        mask = cv2.dilate(
            mask,
            None,
            iterations=2
        )


        # -----------------------------
        # Find contours
        # -----------------------------
        cnts = cv2.findContours(
            mask.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        cnts = imutils.grab_contours(cnts)

        center = None


        # -----------------------------
        # If object detected
        # -----------------------------
        if len(cnts) > 0:

            # Find biggest object
            c = max(
                cnts,
                key=cv2.contourArea
            )


            # Minimum enclosing circle
            ((x, y), radius) = cv2.minEnclosingCircle(c)


            # Calculate moments
            M = cv2.moments(c)


            # Prevent division by zero
            if M["m00"] != 0:

                center = (
                    int(M["m10"] / M["m00"]),
                    int(M["m01"] / M["m00"])
                )


                # -----------------------------
                # Draw detected object
                # -----------------------------
                if radius > 10:

                    cv2.circle(
                        frame,
                        (int(x), int(y)),
                        int(radius),
                        (0, 255, 0),
                        2
                    )

                    cv2.circle(
                        frame,
                        center,
                        5,
                        (0, 0, 255),
                        -1
                    )


        # -----------------------------
        # Save center point
        # -----------------------------
        pts[color].appendleft(center)


        # -----------------------------
        # Draw tracking line
        # -----------------------------
        for i in range(
            1,
            len(pts[color])
        ):

            if (
                pts[color][i - 1] is None
                or pts[color][i] is None
            ):
                continue


            cv2.line(
                frame,
                pts[color][i - 1],
                pts[color][i],
                (0, 255, 0),
                2
            )


    # -----------------------------
    # Show frame
    # -----------------------------
    cv2.imshow(
        "Color Tracking",
        frame
    )


    # -----------------------------
    # Press Q to quit
    # -----------------------------
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


# -----------------------------
# Cleanup
# -----------------------------
if args.get("video", False):
    vs.release()
else:
    vs.stop()

cv2.destroyAllWindows()