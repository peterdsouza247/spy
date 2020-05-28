import cv2, time, pandas
from datetime import datetime

first_frame = None
status_change = [None, None]
times = []
df = pandas.DataFrame(columns = ["Start", "End"])

OBJ_MIN_SIZE_FOR_DETECTION = 10000

video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    status = 0
    grey_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey_img = cv2.GaussianBlur(grey_img, (21, 21), 0)

    if first_frame is None:
        first_frame = grey_img
        continue

    delta_frame = cv2.absdiff(first_frame, grey_img)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

    (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in cnts:
        if cv2.contourArea(contour) < OBJ_MIN_SIZE_FOR_DETECTION:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    status_change.append(status)
    status_change = status_change[-2:]
    if status_change[-1] == 1 and status_change[-2] == 0:
        times.append(datetime.now())
    if status_change[-1] == 0 and status_change[-2] == 1:
        times.append(datetime.now())

    cv2.imshow("spy", frame)
    key=cv2.waitKey(1)

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

for i in range(0, len(times), 2):
    df = df.append({"Start":times[i], "End":times[i+1]}, ignore_index = True)

df.to_csv("reporter.csv")

video.release()
cv2.destroyAllWindows()
