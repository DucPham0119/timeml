from models.our_model.ViNeuroNLP.application.vidp import ViDP

absolute_path = "/home/ducpt/Code/models/our_model/ViNeuroNLP"


def run_dp_with_vineuronlp(sentence: str):
    vi_parser = ViDP(absolute_path)
    return vi_parser.parse(sentence=sentence)


def extract_time_from_conllu(dp_conllu_str: str):
    """
    Lấy các candidate time từ Dependency Parsing.
    - obl:tmod: gộp với các phụ thuộc trực tiếp, bỏ qua flat:date
    - flat:date: lấy riêng, không gộp
    """
    tokens_info = {}  # id -> token info
    dependents = {}   # head id -> list các id phụ thuộc

    for line in dp_conllu_str.splitlines():
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
            tokens_info[tid] = {
                "token": token,
                "pos": pos,
                "deprel": deprel,
                "head": head
            }
            dependents.setdefault(head, []).append(tid)

    # Hàm lấy các token gộp cho obl:tmod, theo id tăng dần
    def get_time_tokens(tid):
        ids = [tid]
        for dep_id in sorted(dependents.get(tid, [])):
            dep_deprel = tokens_info[dep_id]["deprel"]
            if dep_deprel == "flat:date":
                continue  # bỏ qua
            # Đệ quy gộp các phụ thuộc của dep_id
            ids.extend(get_time_tokens(dep_id))
        return ids

    time_candidates = []

    for tid, info in sorted(tokens_info.items()):
        if info["deprel"] == "obl:tmod":
            all_ids = get_time_tokens(tid)
            # Lấy token theo thứ tự id
            tokens = [tokens_info[i]["token"] for i in sorted(all_ids)]
            time_candidates.append(" ".join(tokens).replace("_", " "))
        elif info["deprel"] == "flat:date":
            time_candidates.append(info["token"].replace("_", " "))

    return time_candidates


# conllu = run_dp_with_vineuronlp("Ngày mai (10/5/2015) tôi sẽ đi học sau khi tôi thức dậy")
# print(conllu)
# print(extract_time_from_conllu(conllu))
