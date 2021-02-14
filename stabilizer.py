from vidgear.gears import VideoGear
import numpy as np
import cv2
from vidgear.gears import WriteGear


class Stabilizer:

    @staticmethod
    def get_adjusted_image_size(image_width, image_height, crop_width, crop_height):
        if crop_width is None or (crop_width >= image_width):
            crop_width = image_width

        if crop_height is None or (crop_height >= image_height):
            crop_height = image_height
        return int(crop_width), int(crop_height)

    @staticmethod
    def center_crop(img, crop_width, crop_height):
        if img is None:
            return None

        width, height = img.shape[1], img.shape[0]
        mid_x, mid_y = int(width / 2), int(height / 2)
        cw2, ch2 = int(crop_width / 2), int(crop_height / 2)
        crop_img = img[mid_y - ch2:mid_y + ch2, mid_x - cw2:mid_x + cw2]
        return crop_img

    def __init__(self, input_video_path, crop_width, crop_height, output_video_path):
        self.input_video_path = input_video_path
        self.crop_width = crop_width
        self.crop_height = crop_height
        self.output_video_path = output_video_path

    def execute(self):
        stream_vg = VideoGear(source=self.input_video_path, stabilize=True).start()
        org_frame_width = stream_vg.stream.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        org_frame_height = stream_vg.stream.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)

        adjusted_crop_width, adjusted_crop_height = self.get_adjusted_image_size(image_width=org_frame_width,
                                                                                 image_height=org_frame_height,
                                                                                 crop_width=self.crop_width,
                                                                                 crop_height=self.crop_height)
        fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        writer = cv2.VideoWriter(self.output_video_path, fmt, 30, (adjusted_crop_width, adjusted_crop_height))

        while True:
            frame = stream_vg.read()

            if frame is None:
                break

            frame = self.center_crop(frame, crop_width=adjusted_crop_width, crop_height=adjusted_crop_height)
            writer.write(frame)

        writer.release()
