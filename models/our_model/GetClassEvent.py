import numpy as np

from models.our_model.get_vecto import get_embed_all_word


def normalize(vecs):
    return vecs / (np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-9)


def cosine_similarity(vec, centroids):
    vec = vec / (np.linalg.norm(vec) + 1e-9)
    return np.dot(centroids, vec)


def main(list_event, sentence):
    # Lấy embedding cho tất cả từ trong list_event
    flat_events = [w if isinstance(w, str) else "_".join(w) for w in list_event]
    word_vectors = get_embed_all_word(flat_events)

    # load lại centroids và labels
    class_centroids = np.load("/home/ducpt/Code/models/our_model/class_centroids.npy")
    with open("/home/ducpt/Code/models/our_model/class_labels.txt", "r", encoding="utf-8") as f:
        class_labels = [line.strip() for line in f]

    # chuẩn hóa centroids trước
    class_centroids = normalize(class_centroids)

    # Threshold
    threshold = 0.5

    # mapping từ event -> class
    event_annotations = []

    for i, word in enumerate(flat_events):
        sims = cosine_similarity(word_vectors[i], class_centroids)
        best_idx = np.argmax(sims)
        best_score = sims[best_idx]

        if best_score >= threshold:  # chỉ lấy khi similarity đủ cao
            best_class = class_labels[best_idx]
        else:
            best_class = 'OCCURRENCE'

        event_annotations.append((word.strip(), best_class))

    # Gán nhãn EVENT vào câu
    annotated_sentence = sentence
    eid_counter = 1

    for word, cls in event_annotations:
        eid = f"e{eid_counter}"
        eid_counter += 1
        tag = f'<EVENT eid="{eid}" class="{cls}">{word}</EVENT>'
        # thay thế từ gốc bằng từ đã chèn tag
        annotated_sentence = annotated_sentence.replace(word, tag, 1)

    return annotated_sentence


# print(main(["đi học", "khóc"], "Hôm nay tôi đi học vào thứ 2 và tôi đã khóc"))
