import hashlib
from typing import List, Set
from datasketch import MinHash, MinHashLSH
from tqdm import tqdm
from .config import CleanerConfig

def get_shingles(doc: str, size: int) -> Set[str]:
    words = doc.split()
    return set([' '.join(words[i:i + size]) for i in range(len(words) - size + 1)])

def deduplicate_documents(docs: List[str], config: CleanerConfig) -> List[str]:
    lsh = MinHashLSH(threshold=config.lsh_threshold, num_perm=config.minhash_permutations)
    unique_docs = []
    seen_hashes = set()

    for doc in tqdm(docs, desc="Дедупликация"):
        shingles = get_shingles(doc, config.shingle_size)
        m = MinHash(num_perm=config.minhash_permutations)
        for shingle in shingles:
            m.update(shingle.encode('utf-8'))
            
        duplicates = lsh.query(m)
        if not duplicates:
            doc_hash = hashlib.md5(doc.encode('utf-8')).hexdigest()
            lsh.insert(doc_hash, m)
            unique_docs.append(doc)
            seen_hashes.add(doc_hash)
            
    return unique_docs
