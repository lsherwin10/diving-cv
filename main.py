import cv2
import mediapipe as mp
import numpy as np

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 750

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

BODY_PARTS = {
    "LEFT_WRIST": mp_pose.PoseLandmark.LEFT_WRIST,
    "LEFT_ELBOW": mp_pose.PoseLandmark.LEFT_ELBOW,
    "LEFT_SHOULDER": mp_pose.PoseLandmark.LEFT_SHOULDER,
    "LEFT_HIP": mp_pose.PoseLandmark.LEFT_HIP,
    "LEFT_KNEE": mp_pose.PoseLandmark.LEFT_KNEE,
    "LEFT_ANKLE": mp_pose.PoseLandmark.RIGHT_ANKLE,
    "RIGHT_WRIST": mp_pose.PoseLandmark.RIGHT_WRIST,
    "RIGHT_ELBOW": mp_pose.PoseLandmark.RIGHT_ELBOW,
    "RIGHT_SHOULDER": mp_pose.PoseLandmark.RIGHT_SHOULDER,
    "RIGHT_HIP": mp_pose.PoseLandmark.RIGHT_HIP,
    "RIGHT_KNEE": mp_pose.PoseLandmark.RIGHT_KNEE,
    "RIGHT_ANKLE": mp_pose.PoseLandmark.RIGHT_ANKLE,
}

# VIDEO REFERENCE: https://www.youtube.com/watch?v=06TE_U21FK4


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


def get_landmark_coords(landmarks, first, mid, end):
    first_landmark = BODY_PARTS[first]
    mid_landmark = BODY_PARTS[mid]
    end_landmark = BODY_PARTS[end]
    first_coords = [
        landmarks[first_landmark.value].x,
        landmarks[first_landmark.value].y,
    ]
    mid_coords = [
        landmarks[mid_landmark.value].x,
        landmarks[mid_landmark.value].y,
    ]
    end_coords = [
        landmarks[end_landmark.value].x,
        landmarks[end_landmark.value].y,
    ]

    return first_coords, mid_coords, end_coords


def get_joint_angle(first, mid, end):
    angle = calculate_angle(first, mid, end)

    return angle, tuple(np.multiply(mid, [WINDOW_WIDTH, WINDOW_HEIGHT]).astype(int))


# Takes in a list of 3-tuples of joint strings and returns a list of tuples
# containing the angle and tuple of coordinates for that angle to be drawn at
def get_joint_angle_list(landmarks, joint_groups):
    result = []
    for group in joint_groups:
        try:
            result.append(get_joint_angle(*get_landmark_coords(landmarks, *group)))
        except:
            pass

    return result


# VIDEO FEED
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            joint_groups = [
                ("LEFT_SHOULDER", "LEFT_ELBOW", "LEFT_WRIST"),
                ("RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"),
                ("LEFT_HIP", "LEFT_KNEE", "LEFT_ANKLE"),
                ("RIGHT_HIP", "RIGHT_KNEE", "RIGHT_ANKLE"),
                ("LEFT_SHOULDER", "LEFT_HIP", "LEFT_KNEE"),
                ("RIGHT_SHOULDER", "RIGHT_HIP", "RIGHT_KNEE"),
            ]

            joint_angles = get_joint_angle_list(landmarks, joint_groups)

            # Visualize angles
            for joint_angle in joint_angles:
                cv2.putText(
                    image,
                    str(joint_angle[0]),
                    joint_angle[1],
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

        except:
            pass

        # Render detections
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
        )

        cv2.imshow("Mediapipe Feed", image)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
