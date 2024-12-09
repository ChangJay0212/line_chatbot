from huggingface_hub import snapshot_download

repo_id = "yentinglin/Llama-3-Taiwan-8B-Instruct"
token = ""

snapshot_download(repo_id = repo_id, local_dir ="./model")