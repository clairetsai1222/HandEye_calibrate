'''
记录所有和Realsense相机相关的函数
包含：
1. 定义类RealSenseCamera，包含初始化、获取帧、获取内参、获取深度比例等函数
2. 示例用法
'''

import pyrealsense2 as rs
import numpy as np
import cv2


class RealSenseCamera:
    def __init__(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        # self.config.enable_stream(rs.stream.depth, 720, 1280, rs.format.z16, 30)
        # self.config.enable_stream(rs.stream.color, 720, 1280, rs.format.rgb8, 30)
        self.pipeline.start(self.config)
        self.align = rs.align(rs.stream.color)  # 创建align对象用于深度-颜色对齐

    def get_frames(self):
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        if not aligned_frames:
            print("Frames not aligned")
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
        else:
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()

        if not depth_frame or not color_frame:
            raise RuntimeError("Could not acquire depth or color frames")
        return depth_frame, color_frame

    def get_intrinsics_coefficients(self, depth_frame):
        intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics

        intrinsics_coefficients = np.array(intrinsics.coeffs)

        intrinsic_matrix = np.array([
            [intrinsics.fx, 0, intrinsics.ppx],
            [0, intrinsics.fy, intrinsics.ppy],
            [0, 0, 1]
        ])

        return intrinsic_matrix, intrinsics_coefficients
    

    def get_depth_scale(self):
        depth_scale = self.pipeline.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
        return 1 / depth_scale

    def print_intrinsics_and_scale(self):
        depth_frame, color_frame = self.get_frames()
        intrinsic_matrix, intrinsics_coefficients = self.get_intrinsics_coefficients(depth_frame)
        depth_scale_patch = self.get_depth_scale()

        print("Intrinsic Matrix:")
        print(intrinsic_matrix)
        print("Depth Scale (factor_depth):", depth_scale_patch)
        print("Color Coefficients:", intrinsics_coefficients)
        return intrinsic_matrix, depth_scale_patch, intrinsics_coefficients

    def capture_frames(self):
        try:
            while True:
                # 等待一对同步的帧：颜色和深度
                frames = self.pipeline.wait_for_frames()
                aligned_frames = self.align.process(frames)
                if not aligned_frames:
                    continue  # 如果对齐失败，回到循环开始

                color_frame = aligned_frames.get_color_frame()
                aligned_depth_frame = aligned_frames.get_depth_frame()

                if not color_frame or not aligned_depth_frame:
                    continue

                # 将aligned_depth_frame和color_frame转换为numpy数组
                aligned_depth_image = np.asanyarray(aligned_depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())

                # 显示对齐的深度图像
                aligned_depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(aligned_depth_image, alpha=0.03),
                                                           cv2.COLORMAP_JET)
                cv2.imshow("Aligned Depth colormap", aligned_depth_colormap)

                cv2.imshow("Aligned Depth Image", aligned_depth_image)
                cv2.imwrite('./doc/rs_visual_data/depth.png', aligned_depth_image)

                # 显示颜色图像
                cv2.imshow("Color Image", color_image)
                cv2.imwrite('./doc/rs_visual_data/color.png', color_image)

                # 按'q'退出
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            # 停止pipeline并关闭所有窗口
            self.pipeline.stop()
            cv2.destroyAllWindows()
    
    def stop(self):
        self.pipeline.stop()

# 示例用法
if __name__ == "__main__":
    camera = RealSenseCamera()
    try:
        camera.print_intrinsics_and_scale()
    finally:
        camera.stop()
