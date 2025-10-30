from typing import Iterable

class IO:
    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r') as file:
            return file.read()

    @staticmethod
    def write_file(file_path, content):
        with open(file_path, 'w') as file:
            file.write(content)

    @staticmethod
    def save_stream(stream: Iterable[bytes], dest_path: str, chunk_size: int = 8192) -> None:
        with open(dest_path, "wb") as f:
            for chunk in stream:
                if not chunk:
                    continue  # skip keep-alive chunks
                f.write(chunk)

    @staticmethod
    def read_stream(file_path: str, chunk_size: int = 8192) -> Iterable[bytes]:
        with open(file_path, "rb") as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data