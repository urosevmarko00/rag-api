class ChunkingService:

    def chunk(self, text: str) -> list[str]:
        chunks = text.split("\n\n")
        return [chunk.strip() for chunk in chunks if chunk.strip()]
