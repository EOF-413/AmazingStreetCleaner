from json import dump, load

X1_RATIO = 0.4427
Y1_RATIO = 0.6944
X2_RATIO = 0.5547
Y2_RATIO = 0.8102

KEYS = ['L_SHIFT', 'L_CTRL', 'L_ALT', 'A', 'C', 'D', 'E', 'J', 'K', 'L', 'N', 'Q', 'R', 'S', 'W']


def load_config(file="config.json"):
    with open(file, 'r', encoding='utf-8') as f:
        return load(f)


def save_config(data, file="config.json"):
    with open(file, 'w', encoding='utf-8') as f:
        dump(data, f, indent=4, ensure_ascii=False)
