import pandas as pd
import os
from config.settings import BASE_DIR

class Classification():
    def __init__(self) -> None:
        self._load_dataset(os.path.join(BASE_DIR, "core/data"))
        pass

    def _load_dataset(self, corpus_path):
        self.dataset = pd.read_csv(corpus_path+"/PreProcessing.csv")