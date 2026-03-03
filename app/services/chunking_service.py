class ChunkingService:

    def __init__(self, chunk_size: int = 800, overlap: int = 150):
        if overlap >= chunk_size:
            raise ValueError("Overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        if not text.strip():
            return []

        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            if end >= len(text):
                chunk = text[start:len(text)]
                chunks.append(chunk.strip())
                break

            space_index = text.rfind(" ", start, end)
            if space_index != -1 and space_index > start:
                end = space_index

            chunk = text[start:end]
            chunks.append(chunk.strip())

            start = end - self.overlap

        return chunks
