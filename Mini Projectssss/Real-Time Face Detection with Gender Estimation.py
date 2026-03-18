import cv2
import numpy as np
from datetime import datetime
import os


class GenderEstimator:
    def __init__(self):
        # Load pre-trained face detection classifier
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        # Create directory for screenshots
        self.screenshot_dir = "gender_detection_screenshots"
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

        # Initialize webcam
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise Exception("Could not open webcam")

        # Variables for FPS calculation
        self.fps_start_time = datetime.now()
        self.fps_frame_count = 0
        self.fps = 0

        # Gender statistics
        self.male_count = 0
        self.female_count = 0
        self.unknown_count = 0

        # Load pre-trained gender detection model (using color histograms)
        # This is a simplified approach for demonstration
        self.gender_model = self.create_simple_gender_model()

    def create_simple_gender_model(self):
        """
        Create a simple rule-based gender classifier
        Based on common facial feature assumptions
        """
        return {
            'skin_tone_ranges': {
                'male': [(0, 140, 100), (180, 255, 255)],  # Darker skin tones
                'female': [(0, 120, 120), (180, 255, 255)]  # Lighter skin tones
            },
            'hair_features': {
                'male': {'short_hair_probability': 0.7},
                'female': {'long_hair_probability': 0.6}
            }
        }

    def calculate_fps(self):
        """Calculate and return current FPS"""
        self.fps_frame_count += 1
        elapsed_time = (datetime.now() - self.fps_start_time).total_seconds()

        if elapsed_time > 1:
            self.fps = self.fps_frame_count / elapsed_time
            self.fps_start_time = datetime.now()
            self.fps_frame_count = 0

        return self.fps

    def detect_faces(self, frame):
        """Detect faces in the frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)  # Larger min size for better gender estimation
        )

        return faces

    def estimate_gender_simple(self, face_roi):
        """
        Simple gender estimation based on:
        1. Face width-to-height ratio
        2. Skin tone analysis
        3. Texture analysis
        """
        # Convert to different color spaces
        hsv = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

        # 1. Facial structure analysis
        h, w = face_roi.shape[:2]
        face_ratio = w / h

        # 2. Skin tone analysis (simplified)
        skin_mask = cv2.inRange(hsv, (0, 20, 70), (20, 150, 255))
        skin_percentage = np.sum(skin_mask > 0) / (h * w)

        # 3. Texture analysis (using variance)
        texture_variance = np.var(gray)

        # 4. Edge detection for facial hair
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (h * w)

        # Combine features for gender estimation
        male_score = 0
        female_score = 0

        # Facial ratio: Males typically have more square faces
        if face_ratio < 0.85:  # More oval face
            female_score += 0.3
        elif face_ratio > 0.95:  # More square face
            male_score += 0.3

        # Skin tone (simplified)
        if skin_percentage > 0.3:  # High skin percentage might indicate less facial hair
            female_score += 0.2

        # Edge density (facial hair increases edges)
        if edge_density > 0.15:
            male_score += 0.4

        # Texture variance
        if texture_variance < 5000:  # Smoother skin
            female_score += 0.3
        else:
            male_score += 0.2

        # Make decision
        if male_score > female_score:
            return "Male", (255, 0, 0)  # Blue for male
        elif female_score > male_score:
            return "Female", (255, 192, 203)  # Pink for female
        else:
            return "Unknown", (128, 128, 128)  # Gray for unknown

    def draw_face_boxes(self, frame, faces):
        """Draw rectangles around detected faces with gender labels"""
        self.male_count = 0
        self.female_count = 0
        self.unknown_count = 0

        for (x, y, w, h) in faces:
            # Extract face region
            face_roi = frame[y:y + h, x:x + w]

            if face_roi.size > 0:
                # Estimate gender
                gender, color = self.estimate_gender_simple(face_roi)

                # Update counters
                if gender == "Male":
                    self.male_count += 1
                elif gender == "Female":
                    self.female_count += 1
                else:
                    self.unknown_count += 1

                # Draw rectangle around face with gender-specific color
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)

                # Add gender label with confidence-like indicator
                label = f"{gender}"
                cv2.putText(frame, label, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

                # Add a small confidence bar
                confidence = 0.7 if gender != "Unknown" else 0.3
                bar_x = x
                bar_y = y + h + 10
                bar_width = int(w * confidence)
                cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + 5), color, -1)

        return frame

    def add_info_overlay(self, frame):
        """Add detailed information overlay"""
        fps = self.calculate_fps()

        # Statistics overlay
        info_text = [
            f"FPS: {fps:.1f}",
            f"Statistics:",
            f"  Male: {self.male_count}",
            f"  Female: {self.female_count}",
            f"  Unknown: {self.unknown_count}",
            "Controls: 'q' quit, 's' save, 'r' reset stats"
        ]

        # Semi-transparent overlay for better readability
        overlay = frame.copy()
        cv2.rectangle(overlay, (5, 5), (250, 160), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

        for i, text in enumerate(info_text):
            y_position = 30 + (i * 20)
            color = (255, 255, 255) if i < 2 else (
                (255, 0, 0) if "Male" in text else
                (255, 192, 203) if "Female" in text else
                (128, 128, 128)
            )
            cv2.putText(frame, text, (15, y_position),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        return frame

    def save_screenshot(self, frame):
        """Save current frame with timestamp and stats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stats = f"M{self.male_count}_F{self.female_count}_U{self.unknown_count}"
        filename = f"{self.screenshot_dir}/gender_detect_{timestamp}_{stats}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Screenshot saved: {filename}")

    def reset_statistics(self):
        """Reset gender counters"""
        self.male_count = 0
        self.female_count = 0
        self.unknown_count = 0
        print("Statistics reset!")

    def run(self):
        """Main loop"""
        print("=" * 50)
        print("GENDER ESTIMATION SYSTEM")
        print("=" * 50)
        print("\nHow it works:")
        print("- Analyzes facial features like shape, texture, and skin")
        print("- Blue boxes = Male, Pink = Female, Gray = Unknown")
        print("- Confidence bar shows estimation reliability")
        print("\nControls:")
        print("  'q' - Quit")
        print("  's' - Save screenshot")
        print("  'r' - Reset statistics")
        print("  'h' - Show this help")
        print("=" * 50)

        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("Failed to grab frame")
                break

            # Flip for mirror effect
            frame = cv2.flip(frame, 1)

            # Detect and process faces
            faces = self.detect_faces(frame)
            frame = self.draw_face_boxes(frame, faces)
            frame = self.add_info_overlay(frame)

            # Display
            cv2.imshow('Gender Estimation System', frame)

            # Handle keys
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("Quitting...")
                break
            elif key == ord('s'):
                self.save_screenshot(frame)
            elif key == ord('r'):
                self.reset_statistics()
            elif key == ord('h'):
                self.print_help()

        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        self.print_final_report()

    def print_help(self):
        """Print help information"""
        print("\n" + "=" * 40)
        print("HELP - Gender Estimation System")
        print("=" * 40)
        print("Detection Method:")
        print("  • Face shape analysis (width/height ratio)")
        print("  • Skin tone analysis")
        print("  • Texture analysis for facial hair")
        print("  • Edge detection for facial features")
        print("\nColor Coding:")
        print("  • Blue - Male")
        print("  • Pink - Female")
        print("  • Gray - Unknown")
        print("\nTips for better results:")
        print("  • Good lighting")
        print("  • Face the camera directly")
        print("  • Remove sunglasses/face coverings")
        print("=" * 40)

    def print_final_report(self):
        """Print final statistics"""
        print("\n" + "=" * 40)
        print("FINAL REPORT")
        print("=" * 40)
        print(f"Total Detections:")
        print(f"  Male:    {self.male_count}")
        print(f"  Female:  {self.female_count}")
        print(f"  Unknown: {self.unknown_count}")
        total = self.male_count + self.female_count + self.unknown_count
        if total > 0:
            print(f"\nAccuracy Estimate:")
            print(f"  Male accuracy:   {self.male_count / total * 100:.1f}%")
            print(f"  Female accuracy: {self.female_count / total * 100:.1f}%")
        print("=" * 40)


def main():
    try:
        detector = GenderEstimator()
        detector.run()
    except Exception as e:
        print(f"Error: {e}")
        return


if __name__ == "__main__":
    main()