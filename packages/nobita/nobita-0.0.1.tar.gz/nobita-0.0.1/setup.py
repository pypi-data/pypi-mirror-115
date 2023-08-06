# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modules']

package_data = \
{'': ['*'], 'modules': ['models/*']}

modules = \
['__init__', 'nobita_vision']
install_requires = \
['depthai>=2.8.0,<3.0.0', 'numpy>=1.21.1,<2.0.0', 'opencv-python>=4.5.3,<5.0.0']

setup_kwargs = {
    'name': 'nobita',
    'version': '0.0.1',
    'description': '',
    'long_description': '# nobita\nA non-verbal communication library for robot development using OAK-D\n\n**Japanese readme is [here](docs/README_JA.md).**\n\n## Preparing\nTo use this library, you need a Python environment running [OAK-D](https://store.opencv.ai/) and [depthai](https://github.com/luxonis/depthai).\n\n### Install by the repository\n```\npip install https://github.com/wbawakate/nobita\n```\n\n## Overview\nSince Nobita wraps the tedious process of DepthAI, two-step inference such as face detection and emotion estimation can be done with few lines of code. \n\n![fig1](docs/images/2step_estimation_depthai.png)\n\nThis figure shows the data flow when using DepthAI and OAK-D to handle multiple neural networks. First, the first neural network is used to infer the image obtained from the RGB of OAK-D. Then you need to convert the data into the input format of that second neural network. Therefore, it is necessary to transfer data between the OAK-D and the host computer many times. When using depthai without any wrappers, the amount of code to write tends to increase because all data transfer needs to be defined. With Nobita, you can more easily deploy multiple neural networks to OAK-D.\n\nThere are two main elements to Nobita; `nobita.modules` and `nobita.VisionPipeline`. `nobita.modules` is a set of neural network modules that handle typical tasks related to non-verbal communication, such as face detection and emotion inference. For more information, see [Modules](##Modules). `nobita.VisionPipeline` deploys `nobita.modules` as a pipeline to OAK-D and performs continuous inference.  \n\nNow, let\'s start emotion estimation from face images using nobita. The following is the code for face detection and emotion estimation.\n```\nimport cv2\nimport numpy as np\nfrom nobita import VisionPipeline\nfrom nobita.modules import FaceDetection, EmotionEstimation\n\nemotions = ["neutral", "happy", "sad", "surprise", "anger"]\n# prepare VisionPipeline of nobita\n#    pass `nobita.modules` to modules as a list\n#    if you use OAK-D, set `use_oak=True`\nwith VisionPipeline(modules=[FaceDetection(), EmotionEstimation()], use_oak=True) as pipeline:\n    while True:\n        # get result of estimation and camera preview as dict\n        #     key of the dict is name of `nobita.modules`.\n        #     value of the dict is list of numpy.array, which is prediction values of estimation of the `nobita.module`.\n        out_frame = pipeline.get()\n        if out_frame["FaceDetection"] :\n            # facial image by cropped by face detection \n            face_cv2_frame = cv2.UMat(out_frame["FaceDetection"][0] ) \n            if out_frame["EmotionEstimation"]:\n                    id_emo = np.argmax(out_frame["EmotionEstimation"][0])\n                    max_prob = np.max(out_frame["FaceDetection"][0])\n                    # put estimated emotion on a facial image as text\n                    cv2.putText(face_cv2_frame, f"{emotions[id_emo]}",(5, 15),cv2.FONT_HERSHEY_TRIPLEX,0.6,(255,0,0))\n            # show the facial image\n            cv2.imshow(f"face 0", face_cv2_frame)\n        if cv2.waitKey(1) == ord("q"):\n            cv2.destroyAllWindows()\n            break\n```\nJust pass `nobita.modules` such as `FaceDetection` and `EmotionEstimation` to `nobita.VisionPipeline` to perform two-step inference easily. The result of the inference can be retrieved as a dictionary with `pipeline.get()`. In the demo, the emotion text inferred by `EmotionEstimation` is pasted on the face image detected by `FaceDetection` and shown on the display.\n\n## Demo\nThere is demo code for each module in `demo/`.\nRun the code as follows in the `demo/` directory.\n```\npython face_emotion.py\n```\nEach demo has an option `--device`. This option allows you to specify the device to capture the video. If you are using OAK-D, specify -1 (default). When using other webcams, specify the same device ID as when specifying the device in OpenCV.\n\n## Module\n| module | discription | source | blob file | \n|-------|-------------|--------|----|\n|FaceDetection | face detection |[OpenVINO Toolkit](https://docs.openvinotoolkit.org/2020.1/_models_intel_face_detection_retail_0004_description_face_detection_retail_0004.html)  |face-detection-retail-0004_openvino_2021.2_6shave.blob |\n|PoseEstimation | human pose estimation| [depthai_movenet](https://github.com/geaxgx/depthai_movenet)|movenet_singlepose_lightning_U8_transpose.blob|\n|EmotionEstimation | emotion estimation by facial imases |[OpenVINO Toolkit](https://docs.openvinotoolkit.org/2019_R1/_emotions_recognition_retail_0003_description_emotions_recognition_retail_0003.html)| emotions-recognition-retail-0003.blob|\n|AgeGender | age and gender estimation facial imases|[OpenVINO Toolkit](https://docs.openvinotoolkit.org/2019_R1/_age_gender_recognition_retail_0013_description_age_gender_recognition_retail_0013.html) | age-gender-recognition-retail-0013_openvino_2021.2_6shave.blob|\n|FaceLandmark | facial landmark detection by facial images |[OpenVINO Toolkit](https://docs.openvinotoolkit.org/2019_R1/_facial_landmarks_35_adas_0002_description_facial_landmarks_35_adas_0002.html) | facial-landmarks-35-adas-0002-shaves6.blob|\n|HeadPose | head pose estimation by facial images | [OpenVINE](https://docs.openvinotoolkit.org/2019_R1/_head_pose_estimation_adas_0001_description_head_pose_estimation_adas_0001.html)| head-pose-estimation-adas-0001-shaves4.blob |\n\n\n\n# Credit\n- WBA Future Leaders ( https://wbawakate.jp )\n',
    'author': 'all-in-one library for non-verbal communication of robots',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wbawakate/nobita',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
