from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
from model.env import Env

get_HuggingFace_API_KEY = Env.get_HuggingFace_API_KEY()
login(token=get_HuggingFace_API_KEY)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")

# Example input
input_text = "Hello, how can I assist you today?"
inputs = tokenizer(input_text, return_tensors="pt")

# Generate a response
outputs = model.generate(inputs.input_ids, max_length=50, num_return_sequences=1)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(response)

from huggingface_hub import snapshot_download

snapshot_download(repo_id="meta-llama/Llama-3.2-3B-Instruct", repo_type="model")