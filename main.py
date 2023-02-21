import cv2
import mediapipe as mp
from tqdm import tqdm

import utils

# VIDEO REFERENCE: https://www.youtube.com/watch?v=06TE_U21FK4

if __name__ == "__main__":
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    path = "diving.mov"
    cap = cv2.VideoCapture(path)
    line_height = 20

    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        if cap.isOpened():
            # Get capture data from video
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))
            frame_size = (frame_width, frame_height)
            # print(frame_size)
            fps = int(cap.get(5))
            frame_count = int(cap.get(7))
            output = cv2.VideoWriter(
                "diving_analyzed.mov", cv2.VideoWriter_fourcc(*"mp4v"), fps, frame_size
            )
            with tqdm(total=frame_count) as pbar:
                # Iterate through each frame from the video capture
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
                            joint_angles = utils.get_joint_angle_list(
                                landmarks, utils.JOINT_GROUPS, frame_width, frame_height
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
                            cv2.rectangle(
                                image, box_coords[0], box_coords[1], (0, 0, 0), -1
                            )

                            for joint_label, joint_angle in joint_angles.items():
                                # print(joint_label)
                                # Draw joint angle
                                cv2.putText(
                                    image,
                                    joint_label
                                    + ": "
                                    + str(int(joint_angle[0]))
                                    + " deg",
                                    text_coords,
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5,
                                    (255, 255, 255),
                                    2,
                                    cv2.LINE_AA,
                                )
                                text_coords = (
                                    text_coords[0],
                                    text_coords[1] + line_height,
                                )

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
                        pbar.update()
                    else:
                        break
        else:
            print("Error opening video file")

        cap.release()
        output.release()
