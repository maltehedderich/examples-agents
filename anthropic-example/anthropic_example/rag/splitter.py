from typing import List

import nltk


class TextSplitter:
    def __init__(
        self,
        chunk_size: int,
        chunk_overlap: int,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        nltk.download("punkt", quiet=True)

    def split_text(self, text: str) -> list[str]:
        """Splits a text into chunks of up to `chunk_size` characters. This splitter will split by sentences, and create
        chunks that are as close to `chunk_size` as possible, while also adding overlap between chunks.

        Parameters
        ----------
        text : str
            The text to split.

        Returns
        -------
        List[str]
            A list of chunks.
        """
        sentences = nltk.sent_tokenize(text)
        chunks: list[list[str]] = []
        current_chunk: list[str] = []
        current_chunk_tokens: int = 0

        for sentence in sentences:
            sentence_tokens = len(sentence)

            if current_chunk_tokens + sentence_tokens > self.chunk_size:
                # Start a new chunk
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = [sentence]
                current_chunk_tokens = sentence_tokens
            else:
                # Add sentence to current chunk
                current_chunk.append(sentence)
                current_chunk_tokens += sentence_tokens

        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk)

        # Add overlap between chunks
        chunks_with_overlap = self._add_overlap(chunks)

        return [" ".join(chunk) for chunk in chunks_with_overlap]

    def _add_overlap(self, chunks: list[list[str]]) -> list[list[str]]:
        """Adds sentences from the previous chunk to the beginning of each chunk.

        Parameters
        ----------
        chunks : List[List[str]]
            A list of chunks, where each chunk is a list of sentences.

        Returns
        -------
        List[List[str]]
            A list of chunks as list of sentences with overlap between them.
        """
        overlapped_chunks = [chunks[0]]  # Add the first chunk as is
        for i, chunk in enumerate(chunks[1:], start=1):
            previous_chunk = chunks[i - 1]
            overlap_length: int = 0
            overlap_sentences: list[str] = []
            for sentence in reversed(previous_chunk):
                if overlap_length + len(sentence) > self.chunk_overlap:
                    break
                overlap_sentences.append(sentence)
                overlap_length += len(sentence)
            overlapped_chunks.append(overlap_sentences + chunk)
        return overlapped_chunks
