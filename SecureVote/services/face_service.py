import cv2
import numpy as np
import os
import base64
from PIL import Image
import io
from typing import List, Tuple, Optional, Dict
import json

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("WARNING: DeepFace not installed. Using fallback face encoding method.")

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

class FaceService:
    def __init__(self, threshold: float = 0.6):
        self.threshold = threshold
        # Initialize OpenCV face detector
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        # Initialize AI models if API keys are available
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        self.gemini_key = os.environ.get('GEMINI_API_KEY')

        if self.openai_key and OPENAI_AVAILABLE:
            openai.api_key = self.openai_key

        if self.gemini_key and GENAI_AVAILABLE:
            genai.configure(api_key=self.gemini_key)

    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect faces in an image using OpenCV"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if isinstance(faces, tuple):
            return []
        return [tuple(face) for face in faces]

    def assess_face_quality(self, image: np.ndarray) -> Tuple[bool, str, float]:
        """Assess face image quality before encoding"""
        try:
            # Check image brightness
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)

            if brightness < 40:
                return False, "Image too dark. Please ensure good lighting.", 0.0
            if brightness > 220:
                return False, "Image overexposed. Reduce lighting.", 0.0

            # Check image sharpness using Laplacian variance
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

            if laplacian_var < 15:
                return False, "Image too blurry. Hold camera steady.", 0.0

            # Check if face is detected and properly sized
            faces = self.detect_faces(image)
            if not faces:
                return False, "No face detected. Position face in center.", 0.0

            # Get largest face
            largest_face = max(faces, key=lambda f: f[2] * f[3])
            x, y, w, h = largest_face

            # Face should be at least 120x120 pixels for good quality
            if w < 120 or h < 120:
                return False, "Face too small. Move closer to camera.", 0.0

            # Calculate quality score (0-1)
            brightness_score = 1.0 - abs(brightness - 128) / 128.0
            sharpness_score = min(laplacian_var / 500.0, 1.0)
            size_score = min(w * h / (300 * 300), 1.0)

            quality_score = (brightness_score + sharpness_score + size_score) / 3.0

            if quality_score < 0.25:
                return False, f"Image quality too low ({quality_score:.2f}). Improve lighting and focus.", quality_score

            return True, "Good quality", quality_score

        except Exception as e:
            print(f"Quality assessment error: {e}")
            return True, "Unable to assess quality", 0.5

    def preprocess_face(self, image: np.ndarray) -> np.ndarray:
        """Enhanced face preprocessing with alignment and normalization"""
        try:
            # Detect face
            faces = self.detect_faces(image)
            if not faces:
                return image

            # Get largest face
            largest_face = max(faces, key=lambda f: f[2] * f[3])
            x, y, w, h = largest_face

            # Extract face with margin
            margin = int(0.2 * min(w, h))
            x1 = max(0, x - margin)
            y1 = max(0, y - margin)
            x2 = min(image.shape[1], x + w + margin)
            y2 = min(image.shape[0], y + h + margin)

            face_img = image[y1:y2, x1:x2]

            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
            lab = cv2.cvtColor(face_img, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            enhanced = cv2.merge([l, a, b])
            face_img = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

            # Denoise
            face_img = cv2.fastNlMeansDenoisingColored(face_img, None, 10, 10, 7, 21)

            return face_img

        except Exception as e:
            print(f"Preprocessing error: {e}")
            return image

    def encode_face_deepface(self, image: np.ndarray) -> Optional[np.ndarray]:
        """Extract face encoding using DeepFace with VGG-Face (ResNet-34 based) model"""
        if not DEEPFACE_AVAILABLE:
            print("ERROR: DeepFace not available. Cannot encode face without deep learning model.")
            return None

        try:
            # Quality check before encoding
            is_good_quality, message, quality_score = self.assess_face_quality(image)
            if not is_good_quality:
                print(f"Quality check failed: {message}")
                return None

            # Preprocess face for better encoding
            preprocessed_image = self.preprocess_face(image)

            # DeepFace expects BGR image from OpenCV
            # Use VGG-Face model which is based on ResNet-34 architecture for accurate embeddings
            # VGG-Face produces 4096-D embeddings with superior accuracy
            embedding_objs = DeepFace.represent(
                img_path=preprocessed_image,
                model_name="VGG-Face",
                enforce_detection=True,
                detector_backend="opencv",
                align=True
            )

            if embedding_objs and len(embedding_objs) > 0:
                # Get the first face embedding
                embedding = np.array(embedding_objs[0]["embedding"])
                print(f"Successfully encoded face with VGG-Face (ResNet-34 based). Quality: {quality_score:.2f}, Embedding dims: {embedding.shape}")
                return embedding

            print("No face embeddings generated by VGG-Face")
            return None

        except Exception as e:
            print(f"DeepFace encoding error: {e}")
            # Do NOT fall back to custom encoding - it's not accurate enough
            # Return None to reject the face
            return None

    def _extract_custom_encoding(self, image: np.ndarray) -> Optional[np.ndarray]:
        """Fallback custom face encoding method"""
        try:
            faces = self.detect_faces(image)
            if not faces:
                return None

            # Use the largest face
            largest_face = max(faces, key=lambda f: f[2] * f[3])
            return self.extract_face_features(image, largest_face)
        except Exception as e:
            print(f"Custom encoding error: {e}")
            return None

    def extract_face_features(self, image: np.ndarray, face_box: Tuple[int, int, int, int]) -> np.ndarray:
        """Extract enhanced face features to create 128-D encoding"""
        x, y, w, h = face_box
        face_roi = image[y:y+h, x:x+w]

        # Convert to grayscale for feature extraction
        gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

        # Resize to standard size (larger for better features)
        resized_face = cv2.resize(gray_face, (128, 128))

        # Normalize lighting
        normalized_face = cv2.equalizeHist(resized_face)

        # Extract multiple features to create 128-D encoding
        all_features = []

        # 1. Regional Histogram features (32 features: 4x4 grid, 2 bins each)
        for i in range(4):
            for j in range(4):
                region = normalized_face[i*32:(i+1)*32, j*32:(j+1)*32]
                hist = cv2.calcHist([region], [0], None, [2], [0, 256])
                all_features.extend(hist.flatten().tolist())

        # 2. Enhanced LBP features (64 features)
        lbp_features = self._compute_enhanced_lbp(normalized_face)
        all_features.extend(lbp_features)

        # 3. HOG-like gradient features (32 features: 4x4 grid, 2 bins each)
        sobelx = cv2.Sobel(normalized_face, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(normalized_face, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(sobelx**2 + sobely**2)

        for i in range(4):
            for j in range(4):
                region = magnitude[i*32:(i+1)*32, j*32:(j+1)*32]
                all_features.append(np.mean(region))
                all_features.append(np.std(region))

        # Convert to numpy array and ensure exactly 128 features
        feature_array = np.array(all_features[:128])
        if len(feature_array) < 128:
            feature_array = np.pad(feature_array, (0, 128 - len(feature_array)))

        # Normalize the feature vector
        norm = np.linalg.norm(feature_array)
        if norm > 0:
            feature_array = feature_array / norm

        return feature_array

    def _compute_enhanced_lbp(self, image: np.ndarray) -> List[float]:
        """Compute enhanced Local Binary Pattern features"""
        h, w = image.shape
        features = []

        # Sample 64 points for better discrimination
        step = 8
        for i in range(step, h-step, step):
            for j in range(step, w-step, step):
                center = int(image[i, j])
                # Check 8 neighbors
                pattern = 0
                for idx, (di, dj) in enumerate([(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]):
                    if int(image[i+di, j+dj]) >= center:
                        pattern |= (1 << idx)
                features.append(pattern / 255.0)
                if len(features) >= 64:
                    return features

        # Pad if needed
        while len(features) < 64:
            features.append(0.0)

        return features[:64]

    def encode_face_from_base64(self, base64_image: str) -> Optional[np.ndarray]:
        """Convert base64 image to face encoding using DeepFace"""
        try:
            # Remove data URL prefix if present
            if ',' in base64_image:
                base64_image = base64_image.split(',')[1]

            # Decode base64 image
            image_data = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(image_data))

            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

            # Use DeepFace for encoding
            encoding = self.encode_face_deepface(cv_image)

            return encoding

        except Exception as e:
            print(f"Error encoding face: {e}")
            return None

    def compare_encodings(self, encoding1: np.ndarray, encoding2: np.ndarray) -> float:
        """Compare two face encodings using cosine similarity (more accurate for VGG-Face)"""
        try:
            # Normalize encodings
            enc1_norm = encoding1 / np.linalg.norm(encoding1)
            enc2_norm = encoding2 / np.linalg.norm(encoding2)

            # Compute cosine similarity
            cosine_similarity = np.dot(enc1_norm, enc2_norm)

            # Convert to distance (0 = identical, 1 = completely different)
            # Cosine similarity ranges from -1 to 1, we convert to 0-1 distance
            distance = (1 - cosine_similarity) / 2.0

            # Also compute Euclidean distance for additional verification
            euclidean_distance = np.linalg.norm(encoding1 - encoding2)

            # For VGG-Face, typical Euclidean distance for same person is 0.3-0.6
            # Different persons typically have distance > 0.7
            # We'll use cosine distance as primary metric

            print(f"Cosine distance: {distance:.4f}, Euclidean distance: {euclidean_distance:.4f}")

            return float(distance)

        except Exception as e:
            print(f"Error comparing encodings: {e}")
            return 1.0  # Return maximum distance on error

    def verify_face(self, known_encodings: List[np.ndarray], test_encoding: np.ndarray) -> Tuple[bool, float]:
        """Verify if test encoding matches any known encodings"""
        if not known_encodings or test_encoding is None:
            print("Verification failed: No known encodings or test encoding is None")
            return False, 1.0

        # Validate encoding dimensions
        test_dims = test_encoding.shape[0] if len(test_encoding.shape) > 0 else 0
        print(f"Test encoding dimensions: {test_dims}")

        min_distance = float('inf')
        best_match_idx = -1

        for idx, known_encoding in enumerate(known_encodings):
            known_dims = known_encoding.shape[0] if len(known_encoding.shape) > 0 else 0

            # Ensure encodings have compatible dimensions
            if known_dims != test_dims:
                print(f"WARNING: Encoding dimension mismatch! Known: {known_dims}, Test: {test_dims}")
                continue

            distance = self.compare_encodings(known_encoding, test_encoding)
            if distance < min_distance:
                min_distance = distance
                best_match_idx = idx

        # Use threshold for matching
        is_match = min_distance < self.threshold

        print(f"Verification result: {'MATCH' if is_match else 'NO MATCH'}")
        print(f"  - Best distance: {min_distance:.4f} (threshold: {self.threshold:.4f})")
        print(f"  - Best match index: {best_match_idx}")
        print(f"  - Compared against {len(known_encodings)} enrolled face(s)")

        return is_match, min_distance

    def ai_liveness_detection(self, base64_image: str) -> Dict[str, any]:
        """Use AI (OpenAI or Gemini) to detect if image is a real person (liveness detection)"""
        try:
            # Try OpenAI first
            if self.openai_key and OPENAI_AVAILABLE:
                return self._openai_liveness_check(base64_image)
            # Fallback to Gemini
            elif self.gemini_key and GENAI_AVAILABLE:
                return self._gemini_liveness_check(base64_image)
            else:
                # No AI available, return basic check (allow all)
                return {"is_live": True, "confidence": 0.5, "reason": "No AI liveness detection available - allowing all faces"}
        except Exception as e:
            print(f"AI liveness detection error: {e}")
            return {"is_live": True, "confidence": 0.5, "reason": f"Error: {str(e)}"}

    def _openai_liveness_check(self, base64_image: str) -> Dict[str, any]:
        """Use OpenAI Vision to check for liveness"""
        if not OPENAI_AVAILABLE:
            return {"is_live": True, "confidence": 0.5, "reason": "OpenAI not available"}

        try:
            # Remove data URL prefix if present
            if ',' in base64_image:
                base64_image = base64_image.split(',')[1]

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this image carefully. Is this a real human face (live person) or a fake/spoofed image (photo, screen, printed image, mask)? Answer with ONLY 'REAL' or 'FAKE' followed by a brief reason."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=100
            )

            result = response.choices[0].message.content.strip()
            is_live = "REAL" in result.upper()

            return {
                "is_live": is_live,
                "confidence": 0.9 if is_live else 0.1,
                "reason": result
            }
        except Exception as e:
            print(f"OpenAI liveness check error: {e}")
            return {"is_live": True, "confidence": 0.5, "reason": f"Error: {str(e)}"}

    def _gemini_liveness_check(self, base64_image: str) -> Dict[str, any]:
        """Use Gemini Vision to check for liveness"""
        if not GENAI_AVAILABLE:
            return {"is_live": True, "confidence": 0.5, "reason": "Gemini not available"}

        try:
            # Remove data URL prefix if present
            if ',' in base64_image:
                base64_image = base64_image.split(',')[1]

            # Decode base64 to bytes
            image_data = base64.b64decode(base64_image)

            model = genai.GenerativeModel('gemini-1.5-flash')

            response = model.generate_content([
                "Analyze this image carefully. Is this a real human face (live person) or a fake/spoofed image (photo, screen, printed image, mask)? Answer with ONLY 'REAL' or 'FAKE' followed by a brief reason.",
                {"mime_type": "image/jpeg", "data": base64_image}
            ])

            result = response.text.strip()
            is_live = "REAL" in result.upper()

            return {
                "is_live": is_live,
                "confidence": 0.9 if is_live else 0.1,
                "reason": result
            }
        except Exception as e:
            print(f"Gemini liveness check error: {e}")
            return {"is_live": True, "confidence": 0.5, "reason": f"Error: {str(e)}"}

    def save_image_from_base64(self, base64_image: str, filepath: str) -> bool:
        """Save base64 image to file"""
        try:
            # Remove data URL prefix if present
            if ',' in base64_image:
                base64_image = base64_image.split(',')[1]

            # Decode and save
            image_data = base64.b64decode(base64_image)

            with open(filepath, 'wb') as f:
                f.write(image_data)

            return True

        except Exception as e:
            print(f"Error saving image: {e}")
            return False

    def detect_blink(self, image1: np.ndarray, image2: np.ndarray) -> bool:
        """Simple blink detection by comparing eye regions"""
        try:
            gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

            eyes1 = self.eye_cascade.detectMultiScale(gray1)
            eyes2 = self.eye_cascade.detectMultiScale(gray2)

            # Simple heuristic: significant change in number of detected eyes
            return len(eyes1) != len(eyes2) and abs(len(eyes1) - len(eyes2)) >= 2

        except Exception:
            return False