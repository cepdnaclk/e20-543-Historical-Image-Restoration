import cv2
import numpy as np

# Initialize variables
drawing = False  # True if the mouse is being pressed
ix, iy = -1, -1  # Initial mouse coordinates

def draw_circle(event, x, y, flags, param):
    global drawing, ix, iy

    if event == cv2.EVENT_LBUTTONDOWN:  # Start drawing
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:  # Draw while moving
        if drawing:
            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)  # Draw a red circle

    elif event == cv2.EVENT_LBUTTONUP:  # Stop drawing
        drawing = False
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

# Load the image
img_path = "base.jpg"  # Ensure the image file is in the same directory as this script
img = cv2.imread(img_path)
if img is None:
    print("Error: Could not load the image. Ensure 'base.jpg' is in the current directory.")
    exit()

# Create a window and set the mouse callback function
cv2.namedWindow("Draw on the Image")
cv2.setMouseCallback("Draw on the Image", draw_circle)

print("Draw the red marks on the image. Press 's' to save or 'q' to quit.")

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

# Clean up
cv2.destroyAllWindows()
