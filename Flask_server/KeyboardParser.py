class KeyboardParser:
    def __init__(self):
        # מילון למצבי מקלדת
        self.special_keys = {
            'ctrl_l': 'Ctrl',
            'ctrl_r': 'Ctrl',
            'shift_l': 'Shift',
            'shift_r': 'Shift',
            'alt_l': 'Alt',
            'alt_r': 'Alt',
            'backspace': '←',
            'enter': '↵',
            'space': ' ',
            'tab': '↹',
            'caps_lock': 'Caps Lock',
            'esc': 'Esc',
            'up': '↑',
            'down': '↓',
            'left': '←',
            'right': '→',
            'f1': 'F1', 'f2': 'F2', 'f3': 'F3', 'f4': 'F4', 'f5': 'F5',
            'f6': 'F6', 'f7': 'F7', 'f8': 'F8', 'f9': 'F9', 'f10': 'F10',
            'f11': 'F11', 'f12': 'F12'
        }

    def parse_text_input(self, text_input):
        """המרת מחרוזת טקסט לרשימת הקשות"""
        if isinstance(text_input, str):
            # המרת המחרוזת לרשימה
            keys = text_input[1:-1].split(', ')
            # הסרת הגרשיים מכל מפתח
            keys = [key[1:-1] for key in keys]
            return keys
        return text_input

    def format_as_text(self, keys):
        """הצגת ההקשות בצורה קריאה עם רווחים והורדות שורה"""
        formatted = []
        for key in keys:
            if key is None:
                continue
            if key in self.special_keys:
                formatted.append(self.special_keys[key])
            else:
                formatted.append(key)
        return ' '.join(formatted)

    def format_special_keys_only(self, keys):
        """הצגת רק הקשות מיודות"""
        formatted = []
        for key in keys:
            if key is None:
                continue
            if key in self.special_keys:
                formatted.append(self.special_keys[key])
            elif key.startswith('\\x'):
                formatted.append(f'[Special: {key}]')
        return ' '.join(formatted)

    def format_with_timestamps(self, keys):
        """הצגת ההקשות עם חותמות זמן"""
        formatted = []
        for key in keys:
            if key is None:
                continue
            if key in self.special_keys:
                formatted.append(self.special_keys[key])
            else:
                formatted.append(key)
        return '\n'.join(f"[{i:03d}] {key}" for i, key in enumerate(formatted))


def process_keyboard_input(text_input, format_type='text'):
    """
    עיבוד והצגת הקשות מקלדת

    פרמטרים:
        text_input: מחרוזת טקסט המכילה את ההקשות
        format_type: סוג ההצגה ('text', 'special', 'timestamp')

    טיפוסי הצגה:
        'text': הצגה קריאה עם רווחים
        'special': רק הקשות מיוחדות
        'timestamp': הצגה עם חותמות זמן
    """
    parser = KeyboardParser()
    keys = parser.parse_text_input(text_input)

    if format_type == 'text':
        return parser.format_as_text(keys)
    elif format_type == 'special':
        return parser.format_special_keys_only(keys)
    elif format_type == 'timestamp':
        return parser.format_with_timestamps(keys)
    else:
        raise ValueError(f"סוג הצגה לא תקין: {format_type}")