import re

from config import CHUNK_LENGTH


def semantic_chunk(text: str, chunk_length: int = CHUNK_LENGTH):
    """
    Split text into sentence-aware chunks.

    The function attempts to keep complete sentences together
    until the configured chunk length is reached.
    """

    if not text.strip():
        return []

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Split into sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        # Add sentence if it still fits
        if len(current_chunk) + len(sentence) + 1 <= chunk_length:

            if current_chunk:
                current_chunk += " "

            current_chunk += sentence

        else:

            # Save completed chunk
            if current_chunk:
                chunks.append(current_chunk)

            # Handle very long sentences
            if len(sentence) > chunk_length:

                start = 0

                while start < len(sentence):

                    end = start + chunk_length

                    chunks.append(sentence[start:end])

                    start = end

                current_chunk = ""

            else:

                current_chunk = sentence

    if current_chunk:

        chunks.append(current_chunk)

    return chunks
