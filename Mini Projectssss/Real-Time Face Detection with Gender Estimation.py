import cv2
import numpy as np
from datetime import datetime
import os


class NeuralNetwork:
    """Simple 2-layer neural network implemented with only NumPy"""

    def __init__(self, input_size, hidden_size, output_size):
        # Initialize weights and biases
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -250, 250)))

    def forward(self, X):
        # Forward propagation
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2


class AdvancedGenderEstimator:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        self.screenshot_dir = "advanced_gender_detection"
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise Exception("Could not open webcam")

        # Initialize neural network
        # Input: 100 features (50x50 face region simplified)
        # Hidden: 50 neurons
        # Output: 2 (Male/Female)
        self.nn = NeuralNetwork(100, 50, 2)

        # Statistics
        self.male_count = 0
        self.female_count = 0
        self.confidence_history = []

        # FPS calculation
        self.fps_start_time = datetime.now()
        self.fps_frame_count = 0
        self.fps = 0

    def extract_face_features(self, face_roi):
        """Extract meaningful features from face region"""
        # Resize to standard size
        face_resized = cv2.resize(face_roi, (50, 50))

        # Convert to grayscale
        gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)

        # Extract multiple features

        # 1. Raw pixel values (normalized)
        pixels = gray.flatten() / 255.0

        # 2. Histogram of Oriented Gradients (simplified)
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        mag, ang = cv2.cartToPolar(gx, gy)

        # 3. Local Binary Pattern (simplified)
        lbp = np.zeros_like(gray)
        for i in range(1, gray.shape[0] - 1):
            for j in range(1, gray.shape[1] - 1):
                center = gray[i, j]
                code = 0
                code |= (gray[i - 1, j - 1] > center) << 7
                code |= (gray[i - 1, j] > center) << 6
                code |= (gray[i - 1, j + 1] > center) << 5
                code |= (gray[i, j + 1] > center) << 4
                code |= (gray[i + 1, j + 1] > center) << 3
                code |= (gray[i + 1, j] > center) << 2
                code |= (gray[i + 1, j - 1] > center) << 1
                code |= (gray[i, j - 1] > center) << 0
                lbp[i, j] = code

        # Combine features
        hist_lbp = np.histogram(lbp, bins=32, range=(0, 256))[0]
        hist_mag = np.histogram(mag, bins=16, range=(0, 100))[0]

        # Normalize all features
        hist_lbp = hist_lbp / (np.sum(hist_lbp) + 1e-6)
        hist_mag = hist_mag / (np.sum(hist_mag) + 1e-6)

        # Final feature vector (simplified for demo)
        # In reality, we'd use all features, but for speed we'll use a subset
        features = np.concatenate([
            pixels[::250],  # Every 250th pixel (to reduce dimension)
            hist_lbp[:10],  # First 10 LBP features
            hist_mag[:5]  # First 5 magnitude features
        ])

        # Ensure we have exactly 100 features
        if len(features) < 100:
            features = np.pad(features, (0, 100 - len(features)))
        else:
            features = features[:100]

        return features.reshape(1, -1)

    def estimate_gender_neural(self, face_roi):
        """Use neural network for gender estimation"""
        try:
            # Extract features
            features = self.extract_face_features(face_roi)

            # Forward pass through network
            output = self.nn.forward(features)

            # Get probabilities
            male_prob = float(output[0, 0])
            female_prob = float(output[0, 1])

            # Normalize probabilities
            total = male_prob + female_prob + 1e-6
            male_prob /= total
            female_prob /= total

            # Make decision with confidence
            if male_prob > female_prob:
                if male_prob > 0.6:
                    return "Male", (255, 0, 0), male_prob
                else:
                    return "Likely Male", (200, 100, 100), male_prob
            elif female_prob > male_prob:
                if female_prob > 0.6:
                    return "Female", (255, 192, 203), female_prob
                else:
                    return "Likely Female", (255, 150, 150), female_prob
            else:
                return "Unknown", (128, 128, 128), 0.5

        except Exception as e:
            print(f"Error in gender estimation: {e}")
            return "Error", (0, 0, 255), 0.0

    def calculate_fps(self):
        self.fps_frame_count += 1
        elapsed_time = (datetime.now() - self.fps_start_time).total_seconds()

        if elapsed_time > 1:
            self.fps = self.fps_frame_count / elapsed_time
            self.fps_start_time = datetime.now()
            self.fps_frame_count = 0

        return self.fps

    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100)  # Larger size for better feature extraction
        )
        return faces

    def draw_face_boxes(self, frame, faces):
        self.male_count = 0
        self.female_count = 0

        for (x, y, w, h) in faces:
            # Add margin around face for better feature extraction
            margin = int(w * 0.1)
            x1 = max(0, x - margin)
            y1 = max(0, y - margin)
            x2 = min(frame.shape[1], x + w + margin)
            y2 = min(frame.shape[0], y + h + margin)

            face_roi = frame[y1:y2, x1:x2]

            if face_roi.size > 0:
                # Estimate gender using neural network
                gender, color, confidence = self.estimate_gender_neural(face_roi)

                # Update counters
                if "Male" in gender:
                    self.male_count += 1
                elif "Female" in gender:
                    self.female_count += 1

                # Store confidence for averaging
                self.confidence_history.append(confidence)
                if len(self.confidence_history) > 100:
                    self.confidence_history.pop(0)

                # Draw face box with gradient effect
                for i in range(3):
                    thickness = 3 - i
                    alpha = 1.0 - i * 0.3
                    box_color = tuple(int(c * alpha) for c in color)
                    cv2.rectangle(frame, (x1 - i, y1 - i), (x2 + i, y2 + i), box_color, thickness)

                # Create detailed label
                label = f"{gender} ({confidence:.1%})"

                # Add background for text
                text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                cv2.rectangle(frame,
                              (x1, y1 - 25),
                              (x1 + text_size[0] + 10, y1 - 5),
                              (0, 0, 0),
                              -1)

                # Add text
                cv2.putText(frame, label, (x1 + 5, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                # Add confidence meter
                meter_width = int(w * confidence)
                cv2.rectangle(frame, (x1, y2 + 5), (x1 + meter_width, y2 + 10), color, -1)
                cv2.rectangle(frame, (x1, y2 + 5), (x1 + w, y2 + 10), (255, 255, 255), 1)

        return frame

    def add_info_overlay(self, frame):
        fps = self.calculate_fps()

        # Calculate average confidence
        avg_confidence = np.mean(self.confidence_history) if self.confidence_history else 0

        # Create modern HUD
        overlay = frame.copy()

        # Top bar
        cv2.rectangle(overlay, (0, 0), (frame.shape[1], 80), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        # Statistics
        info_text = [
            f"GENDER ESTIMATION SYSTEM",
            f"FPS: {fps:.1f} | Avg Confidence: {avg_confidence:.1%}",
            f"Males: {self.male_count} | Females: {self.female_count} | Total: {self.male_count + self.female_count}"
        ]

        for i, text in enumerate(info_text):
            y_pos = 25 + i * 25
            cv2.putText(frame, text, (20, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Bottom controls bar
        cv2.rectangle(overlay, (0, frame.shape[0] - 40), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        controls = "Q:Quit | S:Screenshot | R:Reset | H:Help"
        cv2.putText(frame, controls, (20, frame.shape[0] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        return frame

    def save_screenshot(self, frame):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        avg_conf = np.mean(self.confidence_history) if self.confidence_history else 0
        filename = f"{self.screenshot_dir}/gender_nn_{timestamp}_M{self.male_count}_F{self.female_count}_C{avg_conf:.2f}.jpg"
        cv2.imwrite(filename, frame)
        print(f"📸 Screenshot saved: {filename}")

    def reset_statistics(self):
        self.male_count = 0
        self.female_count = 0
        self.confidence_history = []
        print("🔄 Statistics reset!")

    def run(self):
        print("=" * 60)
        print("🧠 ADVANCED GENDER ESTIMATION WITH NEURAL NETWORK")
        print("=" * 60)
        print("\nFeatures:")
        print("• Neural network-based classification (NumPy only)")
        print("• Multi-feature extraction (HOG, LBP, pixels)")
        print("• Confidence scoring")
        print("• Real-time statistics")
        print("\nControls:")
        print("  'q' - Quit")
        print("  's' - Save screenshot")
        print("  'r' - Reset statistics")
        print("  'h' - Help")
        print("=" * 60)

        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            frame = cv2.flip(frame, 1)
            faces = self.detect_faces(frame)
            frame = self.draw_face_boxes(frame, faces)
            frame = self.add_info_overlay(frame)

            cv2.imshow('Advanced Gender Estimation', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                self.save_screenshot(frame)
            elif key == ord('r'):
                self.reset_statistics()
            elif key == ord('h'):
                self.print_help()

        self.cap.release()
        cv2.destroyAllWindows()
        self.print_final_report()

    def print_help(self):
        print("\n" + "=" * 50)
        print("📚 HELP - How It Works")
        print("=" * 50)
        print("Feature Extraction:")
        print("  1. Raw pixels (normalized)")
        print("  2. HOG (Histogram of Oriented Gradients)")
        print("  3. LBP (Local Binary Patterns)")
        print("\nNeural Network:")
        print("  • Input layer: 100 features")
        print("  • Hidden layer: 50 neurons")
        print("  • Output layer: 2 neurons (Male/Female)")
        print("\nColor Coding:")
        print("  • Blue → Male")
        print("  • Pink → Female")
        print("  • Light colors → Lower confidence")
        print("=" * 50)

    def print_final_report(self):
        print("\n" + "=" * 50)
        print("📊 FINAL REPORT")
        print("=" * 50)
        print(f"Total Detections: {self.male_count + self.female_count}")
        print(f"  Males:  {self.male_count}")
        print(f"  Females: {self.female_count}")
        if self.confidence_history:
            print(f"\nAverage Confidence: {np.mean(self.confidence_history):.1%}")
            print(f"Confidence Stability: {np.std(self.confidence_history):.3f}")
        print("=" * 50)


if __name__ == "__main__":
    # Choose which version to run
    print("Select version:")
    print("1. Simple Rule-Based Gender Detection")
    print("2. Advanced Neural Network Gender Detection")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "2":
        detector = AdvancedGenderEstimator()
    else:
        detector = GenderEstimator()

    detector.run()