from pynput import keyboard, mouse


class ScopeInputListener:
    def __init__(self, scope):
        self.scope = scope

        self.k_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )

        self.m_listener = mouse.Listener(
            on_click=self.on_click
        )

        self.k_listener.start()
        self.m_listener.start()

    # -------------------
    # Matching helpers
    # -------------------
    def normalize_key(self, key):
        try:
            if key.char:
                return key.char.upper()
        except AttributeError:
            pass

        name = str(key).replace("Key.", "").upper()

        mapping = {
            "CTRL_L": "CTRL",
            "CTRL_R": "CTRL",
            "SHIFT_L": "SHIFT",
            "SHIFT_R": "SHIFT",
            "ALT_L": "ALT",
            "ALT_R": "ALT",
        }

        return mapping.get(name, name)

    def normalize_mouse(self, button):
        return str(button).replace("Button.", "").upper()

    # -------------------
    # Keyboard
    # -------------------
    def on_key_press(self, key):
        key_name = self.normalize_key(key)

        if key_name != self.scope.activation_input:
            return

        if self.scope.activation_type == "toggle":
            self.scope.toggle_visibility()

        elif self.scope.activation_type == "hold":
            self.scope.set_visible(True)

    def on_key_release(self, key):
        key_name = self.normalize_key(key)

        if key_name != self.scope.activation_input:
            return

        if self.scope.activation_type == "hold":
            self.scope.set_visible(False)

    # -------------------
    # Mouse
    # -------------------
    def on_click(self, x, y, button, pressed):
        btn_name = self.normalize_mouse(button)

        if btn_name != self.scope.activation_input:
            return

        if self.scope.activation_type == "toggle" and pressed:
            self.scope.toggle_visibility()

        elif self.scope.activation_type == "hold":
            self.scope.set_visible(pressed)
