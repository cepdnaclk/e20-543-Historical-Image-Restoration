import cv2

# Load original and mask images
original = cv2.imread('base.jpg')
mask = cv2.imread('mask.png', 0)

# Apply Telea inpainting algorithm with 3x3 kernel
repaired_image = cv2.inpaint(original, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

# Resize images to reduce display size
scale_percent = 50  
width = int(original.shape[1] * scale_percent / 100)
height = int(original.shape[0] * scale_percent / 100)
dim = (width, height)

# Resize images
original_resized = cv2.resize(original, dim, interpolation=cv2.INTER_AREA)
repaired_resized = cv2.resize(repaired_image, dim, interpolation=cv2.INTER_AREA)

# Show resized original image and repaired one
cv2.imshow('Original image', original_resized)
cv2.imshow('Repaired image', repaired_resized)

# Save the repaired image
cv2.imwrite('repaired.png', repaired_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
