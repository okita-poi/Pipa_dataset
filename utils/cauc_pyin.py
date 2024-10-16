import pretty_midi
import numpy as np

standard_midi_file = 'midi/2671.mid'  # groundtruth
result_midi_file = 'utils/2671_pyin.mid'

standard_midi = pretty_midi.PrettyMIDI(standard_midi_file)
result_midi = pretty_midi.PrettyMIDI(result_midi_file)

def extract_notes(midi_data):
    notes = []
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            notes.append({
                'start': note.start,
                'end': note.end,
                'pitch': note.pitch
            })
    return notes

standard_notes = extract_notes(standard_midi)
result_notes = extract_notes(result_midi)

# 根据开始时间对音符进行排序
standard_notes.sort(key=lambda x: x['start'])
result_notes.sort(key=lambda x: x['start'])

# 匹配条件：音高相同，开始时间差异在阈值范围内
time_threshold = 0.05  # 时间容忍度
matched_standard_indices = set()
matched_result_indices = set()

for s_idx, s_note in enumerate(standard_notes):
    for r_idx, r_note in enumerate(result_notes):
        if r_idx in matched_result_indices:
            continue
        time_diff = abs(s_note['start'] - r_note['start'])
        if time_diff <= time_threshold and s_note['pitch'] == r_note['pitch']:
            matched_standard_indices.add(s_idx)
            matched_result_indices.add(r_idx)
            break 

# 计算评估指标
TP = len(matched_standard_indices)  # 真阳性：匹配的音符数
FP = len(result_notes) - len(matched_result_indices)  # 假阳性：未匹配的结果音符数
FN = len(standard_notes) - len(matched_standard_indices)  # 假阴性：未匹配的标准音符数

precision = TP / (TP + FP) if (TP + FP) > 0 else 0.0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0.0
f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

print(f"准确率Precision:{precision:.4f}")
print(f"召回率Recall:{recall:.4f}")
print(f"F1 Score:{f1_score:.4f}")
