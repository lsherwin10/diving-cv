import mediapipe as mp
import numpy as np

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

# joint_groups is a dict of key joint labels and value 3-tuples
#   of the first, mid, and end points to measure a joint angle
JOINT_GROUPS = {
    "Left Elbow Bend": (
        "LEFT_SHOULDER",
        "LEFT_ELBOW",
        "LEFT_WRIST",
    ),
    "Right Elbow Bend": (
        "RIGHT_SHOULDER",
        "RIGHT_ELBOW",
        "RIGHT_WRIST",
    ),
    "Left Shoulder Bend": (
        "LEFT_ELBOW",
        "LEFT_SHOULDER",
        "LEFT_HIP",
    ),
    "Right Shoulder Bend": (
        "RIGHT_ELBOW",
        "RIGHT_SHOULDER",
        "RIGHT_HIP",
    ),
    "Left Knee Bend": ("LEFT_HIP", "LEFT_KNEE", "LEFT_ANKLE"),
    "Right Knee Bend": (
        "RIGHT_HIP",
        "RIGHT_KNEE",
        "RIGHT_ANKLE",
    ),
    "Left Hip Bend": ("LEFT_SHOULDER", "LEFT_HIP", "LEFT_KNEE"),
    "Right Hip Bend": (
        "RIGHT_SHOULDER",
        "RIGHT_HIP",
        "RIGHT_KNEE",
    ),
}


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
