import cv2
import numpy as np
import os
import base64
from PIL import Image
import io
from typing import List, Tuple, Optional, Dict
import json
from deepface import DeepFace
import openai
import google.generativeai as genai

class FaceService:
    def __init__(self, threshold: float = 0.6):
        self.threshold = threshold
        # Initialize OpenCV face detector
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Initialize AI models if API keys are available
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        self.gemini_key = os.environ.get('GEMINI_API_KEY')
        
        if self.openai_key:
            openai.api_key = self.openai_key
        
        if self.gemini_key:
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
    
    def encode_face_deepface(self, image: np.ndarray) -> Optional[np.ndarray]:
        """Extract face encoding using DeepFace (128-D or higher dimensional encoding)"""
        try:
            # DeepFace expects BGR image from OpenCV
            # Use Facenet512 model for robust 512-D embeddings
            embedding_objs = DeepFace.represent(
                img_path=image,
                model_name="Facenet512",
                enforce_detection=False,
                detector_backend="opencv"
            )
            
            if embedding_objs and len(embedding_objs) > 0:
                # Get the first face embedding
                embedding = np.array(embedding_objs[0]["embedding"])
                return embedding
            return None
        except Exception as e:
            print(f"DeepFace encoding error: {e}")
            # Fallback to custom encoding method
            return self._extract_custom_encoding(image)
    
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
        """Compare two face encodings using Euclidean distance"""
        try:
            # Compute Euclidean distance
            distance = np.linalg.norm(encoding1 - encoding2)
            
            # Normalize distance to 0-1 range
            # For DeepFace Facenet512, typical distance is 0-40, we'll normalize to 0-1
            max_distance = 40.0  # Adjust based on model
            normalized_distance = min(distance / max_distance, 1.0)
            
            return float(normalized_distance)
            
        except Exception as e:
            print(f"Error comparing encodings: {e}")
            return 1.0  # Return maximum distance on error
    
    def verify_face(self, known_encodings: List[np.ndarray], test_encoding: np.ndarray) -> Tuple[bool, float]:
        """Verify if test encoding matches any known encodings"""
        if not known_encodings or test_encoding is None:
            return False, 1.0
        
        min_distance = float('inf')
        
        for known_encoding in known_encodings:
            distance = self.compare_encodings(known_encoding, test_encoding)
            min_distance = min(min_distance, distance)
        
        # Use threshold for matching
        is_match = min_distance < self.threshold
        return is_match, min_distance
    
    def ai_liveness_detection(self, base64_image: str) -> Dict[str, any]:
        """Use AI (OpenAI or Gemini) to detect if image is a real person (liveness detection)"""
        try:
            # Try OpenAI first
            if self.openai_key:
                return self._openai_liveness_check(base64_image)
            # Fallback to Gemini
            elif self.gemini_key:
                return self._gemini_liveness_check(base64_image)
            else:
                # No AI available, return basic check
                return {"is_live": True, "confidence": 0.5, "reason": "No AI liveness detection available"}
        except Exception as e:
            print(f"AI liveness detection error: {e}")
            return {"is_live": True, "confidence": 0.5, "reason": f"Error: {str(e)}"}
    
    def _openai_liveness_check(self, base64_image: str) -> Dict[str, any]:
        """Use OpenAI Vision to check for liveness"""
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
