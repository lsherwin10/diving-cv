import cv2
import mediapipe as mp
import numpy as np

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


def get_joint_angle(first, mid, end, width, height):
    angle = calculate_angle(first, mid, end)

    return angle, tuple(np.multiply(mid, [width, height]).astype(int))


def get_joint_angle_list(landmarks, joint_groups, width, height):
    result = dict()
    for label, group in joint_groups.items():
        try:
            result[label] = get_joint_angle(
                *get_landmark_coords(landmarks, *group), width, height
            )
        except:
            pass

    return result


cap = cv2.VideoCapture("diving.mov")
line_height = 20

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    if not cap.isOpened():
        print("Error opening video file")
    else:
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        frame_size = (frame_width, frame_height)
        print(frame_size)
        fps = int(cap.get(5))
        frame_count = cap.get(7)
        output = cv2.VideoWriter(
            "diving_analyzed.mov",
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            frame_size,
        )
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
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

                # joint_groups is a dict of key joint labels and value 3-tuples
                #   of the first, mid, and end points to measure a joint angle
                joint_groups = {
                    "Left Elbow Bend": ("LEFT_SHOULDER", "LEFT_ELBOW", "LEFT_WRIST"),
                    "Right Elbow Bend": (
                        "RIGHT_SHOULDER",
                        "RIGHT_ELBOW",
                        "RIGHT_WRIST",
                    ),
                    "Left Shoulder Bend": ("LEFT_ELBOW", "LEFT_SHOULDER", "LEFT_HIP"),
                    "Right Shoulder Bend": (
                        "RIGHT_ELBOW",
                        "RIGHT_SHOULDER",
                        "RIGHT_HIP",
                    ),
                    "Left Knee Bend": ("LEFT_HIP", "LEFT_KNEE", "LEFT_ANKLE"),
                    "Right Knee Bend": ("RIGHT_HIP", "RIGHT_KNEE", "RIGHT_ANKLE"),
                    "Left Hip Bend": ("LEFT_SHOULDER", "LEFT_HIP", "LEFT_KNEE"),
                    "Right Hip Bend": ("RIGHT_SHOULDER", "RIGHT_HIP", "RIGHT_KNEE"),
                }

                joint_angles = get_joint_angle_list(
                    landmarks, joint_groups, frame_width, frame_height
                )

                # Visualize angles
                text_coords = (10, 20)
                box_scale_x = 250 / 586
                box_scale_y = 21 / 826
                box_coords = (
                    (0, 0),
                    (
                        int(box_scale_x * frame_width),
                        int(box_scale_y * frame_height * len(joint_angles)),
                    ),
                )
                cv2.rectangle(image, box_coords[0], box_coords[1], (0, 0, 0), -1)

                for joint_label, joint_angle in joint_angles.items():
                    print(joint_label)
                    # Draw joint angle
                    cv2.putText(
                        image,
                        joint_label + ": " + str(int(joint_angle[0])) + " deg",
                        text_coords,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA,
                    )
                    text_coords = (text_coords[0], text_coords[1] + line_height)

            except:
                pass

            # Render detections
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(
                    color=(245, 117, 66), thickness=2, circle_radius=2
                ),
                mp_drawing.DrawingSpec(
                    color=(245, 66, 230), thickness=2, circle_radius=2
                ),
            )

            output.write(image)
        else:
            break

    cap.release()
    output.release()
