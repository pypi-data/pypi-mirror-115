from typing import Optional
from abc import ABC, abstractmethod

import tensorflow as tf
import numpy as np

class AbstractModel(ABC):
    
    def __init__(self, name:Optional[str]=None, 
                 random_state:Optional[int]=None, 
                 checkpoint_path:Optional[str]:None,
                 *args, **kwargs):
        self.name = name
        self.random_state = random_state
        self.checkpoint_path = checkpoint_path
        
        self.validate_init()
        
    @abstractmethod
    def _create_checkpoint(self):
        pass
    
    
    def validate_init(self):
        pass