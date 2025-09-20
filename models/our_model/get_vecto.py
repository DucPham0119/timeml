import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

# Chọn thiết bị
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model/tokenizer
tokenizer = AutoTokenizer.from_pretrained('keepitreal/vietnamese-sbert')
model = AutoModel.from_pretrained('keepitreal/vietnamese-sbert').to(device)


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # [batch, seq, hidden]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def get_embeding(text):
    encoded_input = tokenizer(text.strip(), padding=True, truncation=True, return_tensors='pt').to(device)
    with torch.no_grad():
        model_output = model(**encoded_input)
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    return sentence_embeddings[0].cpu().numpy()


def get_embed_all_word(words, batch_size=32):
    embeddings = []
    for i in range(0, len(words), batch_size):
        batch = [w.strip() for w in words[i:i+batch_size] if w.strip()]
        if not batch:
            continue
        encoded_input = tokenizer(batch, padding=True, truncation=True, return_tensors='pt').to(device)
        with torch.no_grad():
            model_output = model(**encoded_input)
        batch_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
        embeddings.extend(batch_embeddings.cpu().numpy())
    return embeddings


def get_embed_average(word_groups):
    embeding = []
    for group in word_groups:
        batch = [w.strip() for w in group if w.strip()]
        if batch:
            group_embs = get_embed_all_word(batch)
            embeding.append(np.mean(group_embs, axis=0))
        else:
            embeding.append(np.zeros(model.config.hidden_size))
    return embeding

