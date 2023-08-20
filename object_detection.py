import torch
import ssl

# create ssl certificate
ssl._create_default_https_context = ssl._create_unverified_context

# load the model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# sample image
imgs = ['https://ultralytics.com/images/zidane.jpg']  # batch of images

# Inference
results = model(imgs)

# Results
results.print()
results.save()  # or .show()

results.xyxy[0]  # img1 predictions (tensor)
results.pandas().xyxy[0]  # img1 predictions (pandas)