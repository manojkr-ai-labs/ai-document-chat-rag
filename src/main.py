# from src.services.index_manifest import load_manifest
# from src.services.index_manifest import save_manifest

# manifest = load_manifest()

# manifest["Docker.pdf"] = {
#     "hash": "123456789"
# }

# save_manifest(manifest)

# print("✅ Manifest saved successfully")
# print(manifest)

from src.services.indexing_service import build_vector_database

build_vector_database()