import logging
import os
import sys

import cv2

from config import KEYS, load_config


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Matcher:
    def __init__(self):
        self.use_gpu = self._check_cuda()
        self.templates = self._load_templates()

    def _check_cuda(self):
        try:
            return cv2.cuda.getCudaEnabledDeviceCount() > 0
        except Exception:
            return False

    def _load_templates(self):
        templates = {}
        for key in KEYS:
            try:
                path = resource_path(f'templates/{key}.png')
                print(f"[MATCHER] Загрузка шаблона: {path}")
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    templates[key] = img
                    print(f"[MATCHER] ✅ {key} загружен")
                else:
                    print(f"[MATCHER] ❌ Не удалось загрузить {key} по пути {path}")
            except Exception as e:
                logging.exception(f"Ошибка загрузки шаблона {key}:", e)
        return templates

    def process(self, gray):
        config = load_config()
        best_key = None
        best_score = 0.0

        for key, tmpl in self.templates.items():
            try:
                if self.use_gpu:
                    gpu_gray = cv2.cuda_GpuMat()
                    gpu_gray.upload(gray)
                    gpu_tmpl = cv2.cuda_GpuMat()
                    gpu_tmpl.upload(tmpl)
                    result = cv2.cuda.matchTemplate(gpu_gray, gpu_tmpl, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.cuda.minMaxLoc(result)
                    score = max_val
                else:
                    result = cv2.matchTemplate(gray, tmpl, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(result)
                    score = max_val

                if score > best_score:
                    best_score = score
                    best_key = key
            except Exception as e:
                logging.exception(f"Ошибка обработки шаблона {key}:", e)

        if best_key is None:
            return None, round(best_score * 100, 1)

        threshold = config["MIN_DEF_KEYS"] if "L_" in best_key else config["MIN_DIG_KEYS"]
        if best_score >= threshold:
            return best_key, round(best_score * 100, 1)
        return None, round(best_score * 100, 1)

    def get_gpu_status(self):
        if self.use_gpu:
            return "✅ GPU (CUDA) доступен"
        return "❌ GPU не найден, используется CPU"
