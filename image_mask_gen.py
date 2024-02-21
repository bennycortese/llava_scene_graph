from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2

def show_anns(anns):
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    # Initialize the image with a blank canvas. No need for an alpha channel here.
    img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 3))
    
    for ann in sorted_anns:
        m = ann['segmentation']
        # Generate a solid color mask. No alpha channel needed.
        color_mask = np.random.random(3) * 255 # Multiply by 255 for color values in the range [0, 255]
        img[m] = color_mask
    ax.imshow(img.astype(np.uint8))

image = cv2.imread('./images/dog.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

device = "cuda"

sam = sam_model_registry["default"](checkpoint="./sam_vit_h_4b8939.pth")

sam.to(device=device)

mask_generator = SamAutomaticMaskGenerator(sam)

masks = mask_generator.generate(image)

print(len(masks))
print(masks[0].keys())

plt.figure(figsize=(20,20))
plt.imshow(image)
show_anns(masks)
plt.axis('off')
plt.show() 

# note - test clip here and see if the annotation file is similar to those required
