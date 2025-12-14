"""
Configuration system for interactive editor.

Loads user preferences from YAML file with fallback to sensible defaults.
Config file location: ~/.whenmathprays/editor_config.yaml

If config file doesn't exist, uses built-in defaults. This ensures zero breakage
for existing installations while allowing customization for power users.
"""

import json
from pathlib import Path
from typing import Dict, Any


# Observability settings
DEBUG_OBSERVER_ENABLED = True  # Toggle observer logging on/off

# Default configuration - matches current hardcoded LAYOUT values
DEFAULT_CONFIG = {
    'layout': {
        'margin_left': 0.14,
        'margin_right': 0.02,
        'margin_top': 0.08,
        'margin_bottom': 0.06,
        'panel_gap': 0.35,
        'subplot_gap': 0.3,
        'primitive_gauge_x': -0.18,
        'primitive_gauge_y': 0.5,
        'trajectory_readout_x': -0.15,
        'trajectory_readout_y': 0.95,
        'save_button_left': 0.16,
        'save_button_bottom': 0.96,
        'save_button_width': 0.06,
        'save_button_height': 0.035,
        'save_info_x': 0.92,
        'save_info_y': 0.965
    },
    'weights': {
        'w_v': 1.0,
        'w_r': 1.0,
        'w_f': 1.0,
        'w_a': 1.0,
        'w_S_real': 0.5,
        'w_S_imag': 0.5
    },
    'appearance': {
        'marker_size': 8,
        'line_width': 1.5,
        'grid_alpha': 0.3
    }
}


class EditorConfig:
    """Manages editor configuration with file persistence."""
    
    def __init__(self, config_path: Path = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Optional custom config file path.
                        Defaults to ~/.whenmathprays/editor_config.json
        """
        if config_path is None:
            config_dir = Path.home() / '.whenmathprays'
            config_path = config_dir / 'editor_config.json'
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load config from file or return defaults."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                # Merge user config with defaults (user values override)
                return self._merge_configs(DEFAULT_CONFIG, user_config)
            except Exception as e:
                print(f"[CONFIG] Warning: Could not load {self.config_path}: {e}")
                print("[CONFIG] Using default configuration")
                return self._deep_copy(DEFAULT_CONFIG)
        else:
            return self._deep_copy(DEFAULT_CONFIG)
    
    def _merge_configs(self, defaults: Dict, user: Dict) -> Dict:
        """Recursively merge user config into defaults."""
        result = self._deep_copy(defaults)
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def _deep_copy(self, d: Dict) -> Dict:
        """Deep copy a dictionary."""
        import copy
        return copy.deepcopy(d)
    
    def save(self):
        """Save current configuration to file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"[CONFIG] Saved configuration to {self.config_path}")
        except Exception as e:
            print(f"[CONFIG] Error saving configuration: {e}")
    
    def get(self, section: str, key: str = None, default=None):
        """
        Get configuration value.
        
        Args:
            section: Config section (e.g., 'layout', 'weights')
            key: Optional key within section
            default: Fallback value if not found
        
        Returns:
            Config value or default
        """
        if key is None:
            return self.config.get(section, default)
        return self.config.get(section, {}).get(key, default)
    
    def set(self, section: str, key: str, value):
        """Set configuration value."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
    
    def get_layout(self) -> Dict[str, float]:
        """Get layout configuration as dictionary."""
        return self.config.get('layout', {})
    
    def get_weights(self) -> Dict[str, float]:
        """Get trajectory computation weights."""
        return self.config.get('weights', {})
    
    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self.config = self._deep_copy(DEFAULT_CONFIG)


# Global config instance (lazy loaded)
_global_config = None


def get_config() -> EditorConfig:
    """Get global configuration instance."""
    global _global_config
    if _global_config is None:
        _global_config = EditorConfig()
    return _global_config
