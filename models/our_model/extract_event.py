def extract_events_from_conllu(conllu_str: str):
    """
    Lấy events từ conllu string.
    Quy tắc:
    - VERB root → giữ nguyên, trừ khi có VERB compound gắn với root → gộp, root không lấy riêng lẻ
    - VERB mà deprel chứa 'compound' và head là root → gộp token với root
    - Các VERB khác (conj) → giữ nguyên token
    """
    tokens_info = []  # lưu thông tin token: id, token, pos, deprel, head

    for line in conllu_str.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cols = line.split("\t")
        if len(cols) > 7:
            tid = int(cols[0])
            token = cols[1].replace(" ", "_").lower()
            pos = cols[3]
            deprel = cols[7]
            head = int(cols[6])
            tokens_info.append({
                "id": tid,
                "token": token,
                "pos": pos,
                "deprel": deprel,
                "head": head
            })

    # Tìm token root
    root_tokens = {t["id"]: t for t in tokens_info if t["deprel"] == "root"}
    events = []
    used_ids = set()  # đánh dấu các token đã dùng

    # 1️⃣ Xử lý VERB compound gắn root trước
    for t in tokens_info:
        if t["pos"] == "VERB" and "compound" in t["deprel"]:
            head_token = root_tokens.get(t["head"])
            if head_token and head_token["id"] not in used_ids:
                combined = f"{head_token['token']} {t['token']}"
                events.append(combined)
                used_ids.add(t["id"])
                used_ids.add(head_token["id"])  # đánh dấu root đã dùng

    # 2️⃣ Xử lý root chưa được gộp và các VERB khác
    for t in tokens_info:
        if t["id"] in used_ids:
            continue
        if t["id"] in root_tokens:
            events.append(t["token"])
            used_ids.add(t["id"])
        elif t["pos"] == "VERB":
            events.append(t["token"])
            used_ids.add(t["id"])

    return events
