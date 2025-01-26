import asyncio
from time import time
from typing import Dict, List, Tuple

import numpy as np
from langchain_core.vectorstores import VectorStoreRetriever
# from FlagEmbedding import LightWeightFlagLLMReranker

from db import CustomChroma, CustomMilvus
from utils import BGEM3EmbeddingFunction


class BasicRetriever:
    def __init__(self):
        chroma = CustomChroma()
        vectorstore = chroma.get_vector_store()
        self.retriever : VectorStoreRetriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

class MatryshkaHybridRetriever:
    def __init__(
        self,
        collection_name: str = "word_700_hybrid",
    ):
        """
        Initialize staged hybrid searcher with separate sparse and dense vectors
        
        Args:
            collection_name: Base name for collections
            sparse_model_name: Model name for sparse embeddings (KLUE-BERT)
            dense_model_name: Model name for dense embeddings (BGE-M3)
        """        
        self.milvus = CustomMilvus()
        self.collection_name = collection_name

        self.sparse_emb_fn = self.milvus.sparse_emb_fn
        self.dense_emb_fn = BGEM3EmbeddingFunction()
        # self.reranker = LightWeightFlagLLMReranker('BAAI/bge-reranker-v2.5-gemma2-lightweight', use_fp16=True)
    
    async def search(
        self,
        query: str,
        initial_k: int = 100,
        final_k: int = 10,
        lexical_weight: float = 0.3
    ) -> List[Dict]:
        """
        Perform staged hybrid search
        
        Args:
            query: Search query
            initial_k: Number of results to retrieve in initial search
            final_k: Number of final results after reranking
            lexical_weight: Weight for lexical search results
        """
        # Generate query embeddings
        sparse_query = self.sparse_emb_fn.embed_query(query)
        
        # Perform initial searches in parallel
        initial_results = await self._initial_search(
            query,
            sparse_query,
            initial_k,
            lexical_weight
        )
        
        # Perform reranking
        final_results = await self._rerank_results_dense(
            query,
            initial_results,
            final_k
        )
        
        return final_results
    
    async def _initial_search(
        self,
        query: str,
        sparse_query: np.ndarray,
        k: int,
        lexical_weight: float
    ) -> List[Dict]:
        """Perform parallel lexical and similarity search using sparse vectors"""
        client = self.milvus.get_milvus_client()

        async def lexical_search():
            # Use Milvus's match operator for lexical search
            return client.search(
                collection_name=self.collection_name,
                data=[sparse_query],
                anns_field="sparse_vector",
                param={"metric_type": "L2", "params": {"nprobe": 10}},
                limit=k,
                filter=f"text like '%{query}%'"  # Lexical matching
            )
        
        async def similarity_search():
            return client.search(
                collection_name=self.collection_name,
                data=[sparse_query],
                anns_field="sparse_vector",
                param={"metric_type": "L2", "params": {"nprobe": 10}},
                limit=k
            )
        start = time()
        # Execute searches in parallel
        lexical_results, similarity_results = await asyncio.gather(
            lexical_search(),
            similarity_search()
        )
        self.initial_search_latency = time() - start
        
        # Combine results with weights
        combined_results = {}
        
        for hit in lexical_results[0]:
            combined_results[hit.id] = lexical_weight * (1 - hit.score)
            
        for hit in similarity_results[0]:
            if hit.id in combined_results:
                combined_results[hit.id] += (1 - lexical_weight) * (1 - hit.score)
            else:
                combined_results[hit.id] = (1 - lexical_weight) * (1 - hit.score)
        
        return sorted(combined_results.items(), key=lambda x: x[1], reverse=True)
    
    async def _rerank_results_dense(
        self,
        query: str,
        initial_results: List[Tuple[int, float]],
        k: int
    ) -> List[Dict]:
        """Rerank results using dense vectors"""
        client = self.milvus.get_milvus_client()

        # Get dense query embedding
        dense_query = self.dense_embg_fn.embed_query(query)
        
        # Get candidate IDs from initial results
        candidate_ids = [str(result[0]) for result in initial_results]

        # Rerank using dense vectors
        reranked_results = client.search(
            collection_name=self.collection_name,
            data=[dense_query],
            anns_field="dense_vector",
            param={"metric_type": "L2", "params": {"ef": 200}},
            limit=k,
            filter=f"id in {candidate_ids}"
        )
        
        return reranked_results
    
    # async def _rerank_results_reranker(
    #     self,
    #     query: str,
    #     initial_results: List[Tuple[int, float]],
    #     k: int
    # ) -> List[Dict]:
    #     """Rerank results using dense vectors"""        
    #     # Get candidate IDs from initial results
    #     candidates = [str(result[0]) for result in initial_results] # text 가져오도록 바꾸기기
    #     scores = [self.reranker.compute_score([query, canditate], cutoff_layers=[28], compress_ratio=2, compress_layer=[24, 40]) for canditate in candidates] # Adjusting 'cutoff_layers' to pick which layers are used for computing the score.

    #     # Rerank using scores
    #     # TODO
    #     reranked_results = []

    #     return reranked_results

tools = {
    "basic_retriever": BasicRetriever().retriever,
    "matryshka_hybrid_retriever": MatryshkaHybridRetriever()
}