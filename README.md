##  HandEye_calibrate：hand to eye calibration using OpenCV

**hand2eye_calibrate.py** is a Python implementation of hand to eye calibration using OpenCV. The code is based on [webpage](https://blog.csdn.net/qq_40016998/article/details/121099134) and designed to work with a kortex gen3 robotic arm with the Robotiq 2-Finger Grippers-85 and a realsense D435i camera.

The code takes in the images of a aruco board grabbed by the robotic arm's end-effector, and outputs the transformation matrix that maps the camera's coordinates to the robot base's coordinates and saves it as the calibration.txt file.

## Setup Instructions
Note that this codebase was tested on ubuntu 20.04 with Python 3.8 (must be 3.8 >= Python >= 3.5 for using kortex gen3).

- Create a conda environment:
```Shell
conda create -n calibrate python=3.8
conda activate calibrate
```

- Install other dependencies:
```Shell
pip install -r requirements.txt
```
 
- Install realsense and kortex sdk if needed:
```Shell
python3 -m pip install <whl relative fullpath name>.whl
```
[Realsense sdk](https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python)


- Connected to D435i camera and gen3 robotic arm (Physical wiring)
Refer to the respective official documentation and website

- Ulterate the intrinsics matrix of the camera 
User need to get the intrinsic parameters of the camera and modify the `get_camera_intrinsics()` function in `statical_cammera_info`

You may refer to `rs_intrinsics.py` if you are use realsense D435i camera.

- Clamp the calibration plate on the gripper

## Running Code

```Shell
python3 hand2eye_calibrate.py
```
Then user will be asked to input required number of saving images for calibration recommended from 20 to 30, and needs to adjust the robot arm pose to obtain the aruco board images with different positions and orientations.For each determing position, user needs to press 's' to capture a rgb image and save it in user-specified directory .

After capturing all the images, the code will automatically calculate the transformation matrix and save it as the calibration.txt file.

## Other Notices
- Pose trasformation for kortex gen3 robotic arm:
Because of the special return value of kortex gen3 api, if you are using kinove gen3 robotic arm, the outcome of the calibration will be on the gripper base's coordinate order and located in robot base's coordinate instead of just on the robot base's coordinate system as usual.
Therefore, the specific pose that was being transformated by the transformation matrix needs to be modified accordingly.
For example, refer to the code in `pose_trasform_example.py` to modify the pose accordingly.

- Board position ulteration:
Because user is using the central of the aruco board as the gripper's reference point, the transformated grasp position should be adjusted to be in the center of the gripper's fingers.
For example, refer to the code in `pose_trasform_example.py` to modify the pose accordingly.