import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

for _ in range(10):
    _, frame = cap.read()
frame = cv2.resize(frame, (640, 480))
frame = cv2.flip(frame, 1)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (25, 25), 0)
background = gray

# cv2.imshow("Background", background)
last_frame = gray

while True:
    # Reading, resizing, and flipping the frame
    _, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.flip(frame, 1)

    # Processing the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (25, 25), 0)

    abs_diff = cv2.absdiff(last_frame, gray)
    last_frame = gray
    _, ad_mask = cv2.threshold(abs_diff, 15, 255, cv2.THRESH_BINARY)
    # dilated_mask = cv2.dilate(ad_mask, None, iterations=2)

    contours, _ = cv2.findContours(ad_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        # avoid small movements
        if cv2.contourArea(contour) < 1000:
            continue

        # this means movement detected
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Abs diff mask", ad_mask)
    cv2.imshow("Webcam", frame)
    # cv2.imshow("Dilated mask", dilated_mask)

    if cv2.waitKey(1) == ord('q'):
        break

