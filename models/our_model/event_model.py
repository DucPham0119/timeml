
from models.our_model.ViNeuroNLP.application.vidp import ViDP
from models.our_model.extract_event import extract_events_from_conllu
from models.our_model.getClassEvent import main

absolute_path = "/home/ducpt/Code/models/our_model/ViNeuroNLP"


def run_dp_with_vineuronlp(sentence: str):
    vi_parser = ViDP(absolute_path)
    return vi_parser.parse(sentence=sentence)


def event_pipeline(sentence: str):
    conllu_str = run_dp_with_vineuronlp(sentence)
    print(conllu_str)

    event_candidates = extract_events_from_conllu(conllu_str)
    print(event_candidates)

    return main(event_candidates, sentence)


# if __name__ == "__main__":
#     sent = "Hôm nay tôi đi học vào thứ 2 và khóc"
#     result = event_pipeline(sent)
#     print(result)
