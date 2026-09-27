from dataclasses import dataclass

@dataclass
class CleanerConfig:
    min_chars: int = 200
    shingle_size: int = 5
    minhash_permutations: int = 128
    lsh_threshold: float = 0.8
    common_line_threshold: int = 50
    doc_start_marker: str = "==="
