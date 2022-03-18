import nlpaug
import nlpaug.augmenter.word as naw
import transformers
import torch

with open('emotion_sentences.txt') as f:
    lines = f.readlines()

clean_text = lines[0:3]
clean_text = [sent.strip() for sent in clean_text]

TOPK=20 #default=100
ACT = 'insert' #"substitute"

aug_bert = naw.ContextualWordEmbsAug(
    model_path='distilbert-base-uncased', 
    action=ACT, top_k=TOPK)

print("Original:")
print(clean_text)

print("Augmented Text:")
for i in range(3):
    augmented_text = aug_bert.augment(clean_text)
    print(augmented_text)
