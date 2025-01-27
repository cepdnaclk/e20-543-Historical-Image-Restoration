import cv2
import numpy as np

# Initialize variables
drawing = False  # True if the mouse is being pressed
ix, iy = -1, -1  # Initial mouse coordinates
brush_size = 5

def draw_circle(event, x, y, flags, param):
    global drawing, ix, iy

    if event == cv2.EVENT_LBUTTONDOWN:  # Start drawing
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:  # Draw while moving
        if drawing:
            cv2.circle(img, (x, y), brush_size, (0, 0, 255), -1)  # Draw a red circle

    elif event == cv2.EVENT_LBUTTONUP:  # Stop drawing
        drawing = False
        cv2.circle(img, (x, y), brush_size, (0, 0, 255), -1)

# Load the image
img_path = "base.jpg"  # Ensure the image file is in the same directory as this script
img = cv2.imread(img_path)
if img is None:
    print("Error: Could not load the image. Ensure 'base.jpg' is in the current directory.")
    exit()

# Create a window and set the mouse callback function
cv2.namedWindow("Draw on the Image")
cv2.setMouseCallback("Draw on the Image", draw_circle)

print("Instructions:")
print(" - Draw red marks on the image using the left mouse button.")
print(" - Press 's' to save the image.")
print(" - Press 'q' to quit without saving.")
print(" - Use '+' and '-' to increase or decrease brush size.")

while True:
    cv2.imshow("Draw on the Image", img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):  # Save the painted image
        # Save the painted image
        output_path = "./base_red.jpg"
        cv2.imwrite(output_path, img)
        print(f"Painted image saved as {output_path}.")
        break

    elif key == ord("q"):  # Quit without saving
        print("Exiting without saving.")
        break
    
    elif key == ord("+"):  # Increase brush size
        brush_size = min(brush_size + 1, 50)  # Limit max size to 50
        print(f"Brush size increased to {brush_size}.")

    elif key == ord("-"):  # Decrease brush size
        brush_size = max(1, brush_size - 1)  # Limit min size to 1
        print(f"Brush size decreased to {brush_size}.")

# Clean up
cv2.destroyAllWindows()
