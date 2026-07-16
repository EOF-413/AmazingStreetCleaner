import os
import glob
import cv2
from config import TEMPLATE_KEYS, MATCH_THRESHOLD, MODIFIER_THRESHOLD


class Matcher:
    def __init__(self, folder='templates'):
        self.templates = {}
        self.load_templates(folder)

    def load_templates(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
            return

        keys = TEMPLATE_KEYS.copy()
        keys.sort(key=len, reverse=True)

        for f in glob.glob(f'{folder}/*.png'):
            name = os.path.splitext(os.path.basename(f))[0].upper()
            matched = next((k for k in keys if name.startswith(k)), name)

            img = cv2.imread(f, 0)
            if img is not None:
                _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                self.templates.setdefault(matched, []).append(img)

        print(f"[TEMPLATES] Загружено: {sum(len(v) for v in self.templates.values())}")

    def match(self, gray):
        best_score, best_key = -1, None

        for key, tlist in self.templates.items():
            for t in tlist:
                if gray.shape[0] < t.shape[0] or gray.shape[1] < t.shape[1]:
                    continue

                _, mx, _, _ = cv2.minMaxLoc(
                    cv2.matchTemplate(gray, t, cv2.TM_CCOEFF_NORMED)
                )

                if mx > best_score:
                    best_score, best_key = mx, key

        threshold = MODIFIER_THRESHOLD if best_key in ('L_ALT', 'L_SHIFT', 'L_CTRL') else MATCH_THRESHOLD

        return (best_key, best_score) if best_score >= threshold else (None, best_score)
