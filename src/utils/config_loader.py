import yaml
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def load_config(config_path: str = None) -> dict:
    """
    Load configuration from YAML file with error handling
    
    Args:
        config_path: Optional custom path to config file
    
    Returns:
        dict: Configuration parameters
    """
    default_path = Path(__file__).parent.parent.parent / "config" / "lab_config.yaml"
    
    try:
        with open(config_path or default_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Validate required fields
        required_sections = ['sensor_api', 'alert_thresholds']
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required config section: {section}")
                
        return config
        
    except FileNotFoundError:
        logger.error("Config file not found at %s", config_path or default_path)
        raise
    except yaml.YAMLError as e:
        logger.error("Invalid YAML format in config file: %s", str(e))
        raise
    except Exception as e:
        logger.error("Failed to load config: %s", str(e))
        raise
