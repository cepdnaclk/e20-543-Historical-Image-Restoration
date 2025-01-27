import cv2
import numpy as np

# Initialize variables
drawing = False  # True if the mouse is being pressed
ix, iy = -1, -1  # Initial mouse coordinates
brush_size = 5
brush_color = (0, 0, 255)  # Default color: red
undo_stack = []  # Stack to store image states for undo functionality

def draw_circle(event, x, y, flags, param):
    global drawing, ix, iy,undo_stack

    if event == cv2.EVENT_LBUTTONDOWN:  # Start drawing
        drawing = True
        ix, iy = x, y
        # Save the current state for undo
        undo_stack.append(img.copy())

    elif event == cv2.EVENT_MOUSEMOVE:  # Draw while moving
        if drawing:
            cv2.circle(img, (x, y), brush_size, brush_color, -1)  # Draw a red circle

    elif event == cv2.EVENT_LBUTTONUP:  # Stop drawing
        drawing = False
        cv2.circle(img, (x, y), brush_size, brush_color, -1)

# Load the image
img_path = "base.jpg"  
img = cv2.imread(img_path)
if img is None:
    print(f"Error: Could not load the image. Ensure {img_path} is in the current directory.")
    exit()

# Create a window and set the mouse callback function
cv2.namedWindow("Draw on the Image")
cv2.setMouseCallback("Draw on the Image", draw_circle)

print("Instructions:")
print(" - Draw on the image using the left mouse button.")
print(" - Press 's' to save the image.")
print(" - Press 'q' to quit without saving.")
print(" - Use '+' and '-' to increase or decrease brush size.")
print(" - Use 'r', 'g', 'b' to change brush color to red, green, or blue.")
print(" - Press 'u' to undo the last action.")

# Map RGB values to color names
color_names = {
    (0, 0, 255): "Red",
    (0, 255, 0): "Green",
    (255, 0, 0): "Blue",
}

while True:
    color_name = color_names.get(brush_color, str(brush_color))
    #cv2.imshow("Draw on the Image", img)
    img_copy = img.copy()
    text = f"Brush Size: {brush_size} | Color: {color_name}"
    cv2.putText(img_copy, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Draw on the Image", img_copy)
    
    
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
        
    elif key == ord("r"):  # Change color to red
        brush_color = (0, 0, 255)
        print("Brush color changed to red.")

    elif key == ord("g"):  # Change color to green
        brush_color = (0, 255, 0)
        print("Brush color changed to green.")

    elif key == ord("b"):  # Change color to blue
        brush_color = (255, 0, 0)
        print("Brush color changed to blue.")
        
    elif key == ord("u"):  # Undo the last action
        if undo_stack:
            img = undo_stack.pop()
            print("Undo performed.")
        else:
            print("Nothing to undo.")
# Clean up
cv2.destroyAllWindows()
