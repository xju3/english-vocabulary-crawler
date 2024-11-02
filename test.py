import cv2
from PIL import Image, ImageEnhance
# Load the image in grayscale
image = cv2.imread('/Users/tju/Workspace/24-insta-rpa/tmp/opus/DB0xsAiSSG-/Video 1.jpg', cv2.IMREAD_GRAYSCALE)

_, thresh_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)

# Convert to Pillow format
pil_image = Image.fromarray(thresh_image)

# Enhance contrast and sharpness with Pillow
contrast_enhancer = ImageEnhance.Contrast(pil_image)
pil_image = contrast_enhancer.enhance(2)

sharpness_enhancer = ImageEnhance.Sharpness(pil_image)
pil_image = sharpness_enhancer.enhance(2)

# Save or display the final image
pil_image.save('final_enhanced_text_image.jpg')
pil_image.show()

# Denoise the image
# denoised_image = cv2.fastNlMeansDenoising(image, None, 30, 7, 21)
#
# # Apply thresholding to make text more visible
# _, thresh_image = cv2.threshold(denoised_image, 150, 255, cv2.THRESH_BINARY)
#
# # Save or display the processed image
# cv2.imwrite('denoised_text_image.jpg', thresh_image)
# cv2.imshow('Denoised Text Image', thresh_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()