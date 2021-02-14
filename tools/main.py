from vidgear.gears import VideoGear
import numpy as np
import cv2


def center_crop(img, dim):
    if img is None:
        return None

    width, height = img.shape[1], img.shape[0]
    crop_width = dim[0] if dim[0] < img.shape[1] else img.shape[1]
    crop_height = dim[1] if dim[1] < img.shape[0] else img.shape[0]
    mid_x, mid_y = int(width / 2), int(height / 2)
    cw2, ch2 = int(crop_width / 2), int(crop_height / 2)
    crop_img = img[mid_y - ch2:mid_y + ch2, mid_x - cw2:mid_x + cw2]
    return crop_img


if __name__ == '__main__':

    stream_stab = VideoGear(source='data/0.avi', stabilize=True).start()
    stream_org = VideoGear(source='data/0.avi').start()

    while True:

        frame_stab = stream_stab.read()
        frame_stab = center_crop(frame_stab,(300, 300))

        if frame_stab is None:
            break

        frame_org = stream_org.read()
        frame_org = center_crop(frame_org,(300, 300))

        output_frame = np.concatenate((frame_org, frame_stab), axis=1)

        cv2.putText(
            output_frame, "Before", (10, output_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 255, 0), 2,
        )
        cv2.putText(
            output_frame, "After", (output_frame.shape[1] // 2 + 10, output_frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 255, 0), 2,
        )

        cv2.imshow("Stabilized Frame", output_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()

    stream_org.stop()
    stream_stab.stop()
