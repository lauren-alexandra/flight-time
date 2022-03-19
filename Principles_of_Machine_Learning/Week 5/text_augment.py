import nlpaug.augmenter.word as naw

data_path = input('Enter the complete path of your dataset: ')
data_path = data_path.strip()

with open(data_path) as f:
    lines = f.readlines()
    clean_text = [sent.strip() for sent in lines]

    # initialize new dataset
    aug_file = open("aug_data.txt", "a")
    aug_file.write(''.join(lines))

    """
    - ContextualWordEmbsAug is an augmenter that applys operation (word level) to textual input based on contextual word embeddings.
    - DistilBERT is a transformers model, smaller and faster than BERT, which was pretrained on the same corpus in a self-supervised fashion, 
      using the BERT base model as a teacher. Uncased: it does not make a difference between english and English.
    - action: a new word will be injected to random position according to contextual word embeddings calculation
    - top_k: controlling lucky draw pool
    """
    aug_bert = naw.ContextualWordEmbsAug(
        model_path='distilbert-base-uncased', 
        action='insert', top_k=20)

    print("Augmenting data...")
    for line in clean_text: 
        try: 
            aug_text = aug_bert.augment(line)
            aug_file.write(''.join(aug_text + '\n'))
        except UnicodeEncodeError as e:
            continue

    aug_file.close()
