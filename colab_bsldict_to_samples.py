# === BSLDict videos -> samples file for the BSL Translator website ===
# Paste this whole file into ONE Google Colab cell and run it.
#
# Before running: put BSLDict videos in Google Drive like this
#   MyDrive/bsl_hackathon/data/videos/hello/clip1.mp4
#   MyDrive/bsl_hackathon/data/videos/hello/clip2.mp4
#   MyDrive/bsl_hackathon/data/videos/thank you/clip1.mp4
# (one folder per English word; the folder name becomes the label)
#
# Output: MyDrive/bsl_hackathon/bsldict_samples.json
# Then on the website: Train tab -> Import samples -> choose that file.

!pip install -q mediapipe opencv-python-headless
!wget -q -O /content/hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task

import glob, json, os
import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
from google.colab import drive

drive.mount('/content/drive')

VIDEO_DIR = '/content/drive/MyDrive/bsl_hackathon/data/videos'
OUT_FILE = '/content/drive/MyDrive/bsl_hackathon/bsldict_samples.json'
MAX_FRAMES = 120  # BSLDict clips are short; this caps very long ones


def make_detector():
    options = vision.HandLandmarkerOptions(
        base_options=mp_python.BaseOptions(model_asset_path='/content/hand_landmarker.task'),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,  # BSL is two-handed
    )
    return vision.HandLandmarker.create_from_options(options)


def to_slots(result, aspect):
    """Same format as the website: [hand_slot_0, hand_slot_1], each 63 numbers or None."""
    slots = [None, None]
    for lms, handed in zip(result.hand_landmarks, result.handedness):
        idx = 0 if handed[0].category_name == 'Left' else 1
        if slots[idx] is not None:
            idx = 1 - idx
        if slots[idx] is not None:
            continue
        flat = []
        for p in lms:
            flat += [round(p.x * aspect, 4), round(p.y, 4), round(p.z * aspect, 4)]
        slots[idx] = flat
    return slots


def extract(path):
    detector = make_detector()  # fresh detector per video (timestamps must restart)
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    frames, i = [], 0
    while i < MAX_FRAMES:
        ok, bgr = cap.read()
        if not ok:
            break
        h, w = bgr.shape[:2]
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = detector.detect_for_video(image, int(i * 1000 / fps))
        frames.append(to_slots(result, w / h))
        i += 1
    cap.release()
    detector.close()
    return frames


samples, failed = [], 0
word_dirs = sorted(d for d in glob.glob(os.path.join(VIDEO_DIR, '*')) if os.path.isdir(d))
print(f'Found {len(word_dirs)} word folders')

for word_dir in word_dirs:
    label = os.path.basename(word_dir).strip().lower()
    videos = sorted(glob.glob(os.path.join(word_dir, '*.mp4')))
    for v in videos:
        try:
            frames = extract(v)
            if sum(1 for f in frames if f[0] or f[1]) >= 3:
                samples.append({'label': label, 'source': 'bsldict', 'frames': frames})
            else:
                failed += 1
        except Exception as e:
            print('  skipped', v, '-', e)
            failed += 1
    print(f'{label}: {len(videos)} videos')

with open(OUT_FILE, 'w') as f:
    json.dump({'format': 'bsl-landmarks-v1', 'samples': samples}, f)

print(f'\nDone: {len(samples)} samples saved to {OUT_FILE} ({failed} skipped, no hands found)')
