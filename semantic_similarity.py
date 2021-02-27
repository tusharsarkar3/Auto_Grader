from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-distilroberta-base-v1')

def semantic_similarity_roberta(sentences):
    sentence_embeddings = model.encode(sentences)
    li = []
    for sentence, embedding in zip(sentences, sentence_embeddings):
        print("Sentence:", sentence)
        li.append(embedding)
        print("Embedding:", embedding.shape)

    dot = sum(a*b for a, b in zip(li[0], li[1]))
    norm_a = sum(a*a for a in li[0]) ** 0.5
    norm_b = sum(b*b for b in li[1]) ** 0.5

    cos_sim = dot / (norm_a*norm_b)

    print(cos_sim)

