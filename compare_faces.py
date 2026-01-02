from services.face_service import FaceService
import cv2

# Initialize FaceService with threshold (0.6 is standard for VGG-Face)
face_service = FaceService()

# Paths for registered and voting faces
img1_path = r"D:\SecureVote\SecureVote\static\uploads\faces\auth_12345_20251004_203651.jpg"      # Registered voter face
img2_path = r"D:\SecureVote\SecureVote\static\uploads\fraud_attempts\auth_12345_20251004_201021.jpg"  # Captured face during voting

# Load images
img1 = cv2.imread(img1_path)
img2 = cv2.imread(img2_path)

# Encode faces using FaceService
encoding1 = face_service.encode_face_deepface(img1)
encoding2 = face_service.encode_face_deepface(img2)

# Check if encodings were successful
if encoding1 is None:
    print("❌ Could not encode face from Image 1 (Registration face). Try again with better lighting.")
elif encoding2 is None:
    print("❌ Could not encode face from Image 2 (Voting face). Try again.")
else:
    # Compare using FaceService's built-in method
    is_match, distance = face_service.verify_face([encoding1], encoding2)

    if is_match:
        print(f"✅ Faces Match! (Distance: {distance:.4f})")
    else:
        print(f"❌ Faces Do Not Match. (Distance: {distance:.4f})")

