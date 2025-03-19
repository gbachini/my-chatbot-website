#!/usr/bin/env python3
from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

app = Flask(__name__)

# Load GPT-2 model and tokenizer (using the small model for this example)
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
model.eval()  # Set the model to evaluation mode

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    
    if not question:
        return jsonify({"error": "No question provided."}), 400

    # Create a prompt for the model
    prompt = f"Q: {question}\nA:"
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    
    # Generate the response from GPT-2
    with torch.no_grad():
        outputs = model.generate(inputs, max_length=150, num_return_sequences=1,
                                   no_repeat_ngram_size=2, early_stopping=True)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = generated_text.split("A:")[-1].strip()
    
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)