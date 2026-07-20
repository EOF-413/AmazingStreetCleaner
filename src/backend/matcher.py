import os
import sys
import cv2

from src.config import KEYS, load_config


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Matcher:
    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self):
        templates = {}
        for key in KEYS:
            try:
                fpath = resource_path(os.path.join('templates', f'{key}.png'))
                img = cv2.imread(fpath, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    templates[key] = img
            except Exception as e:
                print(e)
        return templates

    def process(self, gray):
        config = load_config()
        best_key = None
        best_score = 0.0

        for key, tmpl in self.templates.items():
            try:
                # Проверяем, что шаблон не больше изображения
                if tmpl.shape[0] > gray.shape[0] or tmpl.shape[1] > gray.shape[1]:
                    continue

                result = cv2.matchTemplate(gray, tmpl, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                score = max_val

                if score > best_score:
                    best_score = score
                    best_key = key
            except Exception:
                continue

        if best_key is None:
            return None, round(best_score * 100, 1)

        threshold = config.get("MIN_MATCH", 0.7)

        if best_score >= threshold:
            return best_key, round(best_score * 100, 1)
        return None, round(best_score * 100, 1)
