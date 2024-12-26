import json
import os


class JsonDB:
    def __init__(self, filename="db.json"):
        # Create .cache directory if it doesn't exist
        cache_dir = os.path.join(os.path.dirname(__file__), ".cache")
        os.makedirs(cache_dir, exist_ok=True)

        # Store file in .cache directory
        self.filename = os.path.join(cache_dir, filename)
        self.data = {}
        self._load()

    def _load(self):
        """Load the JSON file if it exists, create it if it doesn't"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                self.data = {}
        else:
            self._save()

    def _save(self):
        """Save the current data to JSON file"""
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def set(self, key, value):
        """Set a key-value pair"""
        if not isinstance(value, str):
            raise ValueError("Only string values are accepted")
        self.data[key] = value
        self._save()

    def get(self, key, default=None):
        """Get value by key"""
        return self.data.get(key, default)

    def delete(self, key):
        """Delete a key-value pair"""
        if key in self.data:
            del self.data[key]
            self._save()

    def clear(self):
        """Clear all data"""
        self.data = {}
        self._save()

    def all(self):
        """Get all data"""
        return self.data
