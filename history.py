import json

def load_history(path="history.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return []


def save_history(history_list, path="history.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history_list, f, ensure_ascii=False, indent=2)


class History:
    def __init__(self, path="history.json"):
        self.path = path
        self.history = load_history(self.path)
        self.expr = ""

    def show_history(self):
        if not self.history:
            print("No history available.")
            return []
        for entry in self.history:
            print(entry)
        return self.history.copy()

    def reset_history(self):
        cleared_count = len(self.history)
        self.history = []
        save_history(self.history, self.path)
        return cleared_count
    
    def add_entry(self, entry):
        self.history.append(entry)
        save_history(self.history, self.path)
        return len(self.history)

