# image_knowledge_base.py
# Indexes a folder of images by generating a text description for each
# one, then storing those descriptions in a Chroma collection for
# semantic search   letting you find relevant images with a text query.

from pathlib import Path
from chroma_store import DocumentStore
from vision_tools import describe_image


class ImageKnowledgeBase:
    def __init__(self, path: str = "./image_kb_db"):
        self.store = DocumentStore(path=path, collection_name="images")

    def index_folder(self, folder: str):
        folder_path = Path(folder)
        image_files = list(folder_path.glob("*.jpg")) + list(folder_path.glob("*.png"))

        for image_path in image_files:
            print(f"Describing {image_path.name}...")
            description = describe_image(str(image_path))
            # We store the *description* as searchable text, tagged with
            # the original image path in metadata so we can look the
            # actual image back up after a text-based match.
            self.store.add_chunks([description], source=str(image_path))

        print(f"Indexed {len(image_files)} images.")

    def find_image(self, query: str) -> dict | None:
        results = self.store.search(query, top_k=1)
        return results[0] if results else None


if __name__ == "__main__":
    kb = ImageKnowledgeBase()
    kb.index_folder("./photos")

    match = kb.find_image("a photo with a dog in it")
    if match:
        print(f"Best match: {match['source']}")
        print(f"Description: {match['text']}")
    else:
        print("No matching image found.")
