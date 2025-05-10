class KeybindManager:
    def __init__(self, root, bindings:dict):
        self.root = root
        for  key_combo, handler in bindings.items():
            root.bind(key_combo, handler)
