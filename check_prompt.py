from transformers import CLIPTokenizer
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14") 

def check_prompt_length(prompt):
	tokens = tokenizer(prompt, truncation=False, return_tensors="pt")
	tokens_len = tokens.input_ids.shape[-1]

	if tokens_len > tokenizer.model_max_length:
		return (False, tokens_len, tokenizer.model_max_length)
	else:
		return (True, tokens_len, tokenizer.model_max_length)