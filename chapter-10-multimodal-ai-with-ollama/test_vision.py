# test_vision.py
from vision_tools import describe_image, ask_about_image

print(describe_image("sample.jpg"))
print()
print(ask_about_image("sample.jpg", "What is the dominant color in this image?"))
