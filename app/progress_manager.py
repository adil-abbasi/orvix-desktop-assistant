class ProgressManager:
    def __init__(self):
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback

    def update(self, message):
        print(f"PROGRESS: {message}")

        if self.callback:
            self.callback(message)


progress_manager = ProgressManager()