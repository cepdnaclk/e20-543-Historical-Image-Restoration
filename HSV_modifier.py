import cv2
import numpy as np
import os

class HSV_MODIFIER:

    def __init__(self, path):

        self.file = path

        # Validate the image path
        if not os.path.exists(self.file):
            print(f"Error: File '{self.file}' does not exist.")
            return

        # Load image
        image = cv2.imread(self.file)
        if image is None:
            print("Error: Could not load the image. Ensure the file is a valid image.")
            return
        
        
        original_width, original_height = image.shape[:2] # Store original width and height values.
        image = cv2.resize(image, (900,600)) # We'll resize the image if it's too big for the screen

        # Create a windows
        cv2.namedWindow('image')
        cv2.resizeWindow('image', 900, 500)

        # Create trackbars for HSV adjustment
        cv2.createTrackbar('HMin', 'image', 0, 179, self.nothing)
        cv2.createTrackbar('SMin', 'image', 0, 255, self.nothing)
        cv2.createTrackbar('VMin', 'image', 0, 255, self.nothing)
        cv2.createTrackbar('HMax', 'image', 179, 179, self.nothing)
        cv2.createTrackbar('SMax', 'image', 255, 255, self.nothing)
        cv2.createTrackbar('VMax', 'image', 255, 255, self.nothing)

        # Initialize HSV min/max values
        hMin = sMin = vMin = hMax = sMax = vMax = 0
        phMin = psMin = pvMin = phMax = psMax = pvMax = 0

        while(1):
            # Get current positions of all trackbars
            hMin = cv2.getTrackbarPos('HMin', 'image')
            sMin = cv2.getTrackbarPos('SMin', 'image')
            vMin = cv2.getTrackbarPos('VMin', 'image')
            hMax = cv2.getTrackbarPos('HMax', 'image')
            sMax = cv2.getTrackbarPos('SMax', 'image')
            vMax = cv2.getTrackbarPos('VMax', 'image')

            # Set minimum and maximum HSV values to display
            lower = np.array([hMin, sMin, vMin])
            upper = np.array([hMax, sMax, vMax])

            # Convert to HSV format and color threshold
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower, upper)
            result = cv2.bitwise_and(image, image, mask=mask)

            # Print if there is a change in HSV value
            if((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
                print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
                phMin = hMin
                psMin = sMin
                pvMin = vMin
                phMax = hMax
                psMax = sMax
                pvMax = vMax

            # Display result image
            cv2.imshow('result', result)
            
            # Key controls
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            elif cv2.waitKey(10) & 0xFF == ord('s'):
                # Save the mask by pressing "s" on the predefined path "new_path":
                new_path = 'mask.png'
                new_img = cv2.resize(mask, (original_height, original_width))
                cv2.imwrite(new_path, new_img)
                continue

        cv2.destroyAllWindows()

    def nothing(self, x):
        pass

# Run the HSV_MODIFIER with the image path
HSV_MODIFIER('./painted_image.jpg')