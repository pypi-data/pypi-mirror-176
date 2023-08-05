from setuptools import setup

setup(
    name="trackhand",
    version="2.0",
    description="This is a simple Hand tracking module",
    long_description="Track-Hand module is based on mediapipe & open-cv, having the landmark function inbuild so you can easily use this module in your computer vision projects for Hand Tracking purposes just simply install it using (pip install trackhand) it is having the function track_hand() just call it and you are good to go",
    author="Sudhanshu Yadav",
    author_email="sudhanshuy17@gmail.com",
    packages=['TrackHand'],
    install_requires=['opencv-python', 'mediapipe'],
)
