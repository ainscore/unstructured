import typing as t
from abc import ABC, abstractmethod
from dataclasses import dataclass

from unstructured.ingest.interfaces import (
    BaseDestinationConnector,
    BaseSourceConnector,
    ChunkingConfig,
    EmbeddingConfig,
    PartitionConfig,
    ProcessorConfig,
    ReadConfig,
)
from unstructured.ingest.processor import process_documents
from unstructured.ingest.runner.writers import writer_map


@dataclass
class Runner(ABC):
    processor_config: ProcessorConfig
    read_config: ReadConfig
    partition_config: PartitionConfig
    writer_type: t.Optional[str] = None
    writer_kwargs: t.Optional[dict] = None
    embedding_config: t.Optional[EmbeddingConfig] = None
    chunking_config: t.Optional[ChunkingConfig] = None

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    def get_dest_doc_connector(self) -> t.Optional[BaseDestinationConnector]:
        writer_kwargs = self.writer_kwargs if self.writer_kwargs else {}
        if self.writer_type:
            writer = writer_map[self.writer_type]
            return writer(**writer_kwargs)
        return None

    def process_documents(self, source_doc_connector: BaseSourceConnector):
        process_documents(
            processor_config=self.processor_config,
            source_doc_connector=source_doc_connector,
            partition_config=self.partition_config,
            dest_doc_connector=self.get_dest_doc_connector(),
            embedder_config=self.embedding_config,
            chunking_config=self.chunking_config,
        )
