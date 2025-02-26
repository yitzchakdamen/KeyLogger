class KeyboardParser:

    def __init__(self, text_input):
        self.special_keys = {
            'ctrl_l': '_Ctrl_',
            'ctrl_r': '_Ctrl_',
            'shift_l': '_Shift_',
            'shift_r': '_Shift_',
            'alt_l': '_Alt_',
            'alt_r': '_Alt_',
            'backspace': '←',
            'enter': '\n',
            'space': ' ',
            'tab': '↹',
            'caps_lock': '_Caps Lock_',
            'esc': '_Esc_',
            'up': '↑',
            'down': '↓',
            'left': '←',
            'right': '→',
            'f1': 'F1', 'f2': 'F2', 'f3': 'F3', 'f4': 'F4', 'f5': 'F5',
            'f6': 'F6', 'f7': 'F7', 'f8': 'F8', 'f9': 'F9', 'f10': 'F10',
            'f11': 'F11', 'f12': 'F12'
        }
        self.keys_input = text_input[1:-1].split(', ') # המרת המחרוזת לרשימה
        self.keys = [key[1:-1] for key in self.keys_input]   # הסרת הגרשיים מכל מפתח

    def format_as_text(self):
        """
        הצגת ההקשות בצורה קריאה עם רווחים והורדות שורה
        """
        formatted = []
        for key in self.keys:
            if key is None or key.startswith('\\x'):
                continue
            if key in self.special_keys:
                formatted.append(f" {self.special_keys[key]} ")
            else:
                formatted.append(key)
        return ''.join(formatted)

    def format_as_text_only(self):
        """
        הצגת ההקשות בצורה קריאה עם רווחים והורדות שורה
        """
        formatted = []
        for key in self.keys:
            if key.isalnum() and len(key) == 1:
                formatted.append(key)
        return ''.join(formatted)

    def format_special_keys_only(self):
        """הצגת רק הקשות מיודות"""
        formatted = []
        for key in self.keys:
            if key is None:
                continue
            if key in self.special_keys:
                formatted.append(self.special_keys[key])
            elif key.startswith('\\x'):
                formatted.append(f'Special: {key}]')
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
