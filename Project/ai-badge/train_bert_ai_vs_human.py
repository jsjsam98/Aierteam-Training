import torch
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, classification_report
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from datasets import load_dataset
from tqdm import tqdm


def main():
    # Load the dataset
    dataset = load_dataset("openai_humaneval", split="test")

    # Simulate binary classification labels
    # Human-written: Use 'prompt' column
    # AI-generated: Use 'canonical_solution' column as a proxy for AI-like output
    human_texts = dataset["prompt"][:200]  # Human-written
    ai_texts = dataset["canonical_solution"][:200]  # Simulated AI-generated
    texts = human_texts + ai_texts
    labels = [0] * len(human_texts) + [1] * len(ai_texts)  # 0: Human, 1: AI

    # Train/test split
    train_texts = texts[:320]
    test_texts = texts[320:]
    train_labels = labels[:320]
    test_labels = labels[320:]

    # Tokenize the text
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    train_encodings = tokenizer(
        train_texts, truncation=True, padding=True, max_length=512
    )
    test_encodings = tokenizer(
        test_texts, truncation=True, padding=True, max_length=512
    )

    # Create a PyTorch dataset
    class TextDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels

        def __len__(self):
            return len(self.labels)

        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            item["labels"] = torch.tensor(self.labels[idx])
            return item

    train_dataset = TextDataset(train_encodings, train_labels)
    test_dataset = TextDataset(test_encodings, test_labels)

    # Load the BERT model
    model = BertForSequenceClassification.from_pretrained(
        "bert-base-uncased", num_labels=2
    )
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    model.to(device)

    # Optimizer and DataLoader
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)
    optimizer = AdamW(model.parameters(), lr=5e-5)

    # Training loop
    for epoch in range(3):  # Adjust epochs as needed
        model.train()
        loop = tqdm(train_loader, leave=True)
        for batch in loop:
            batch = {key: val.to(device) for key, val in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            loop.set_description(f"Epoch {epoch}")
            loop.set_postfix(loss=loss.item())

    # Evaluate the model
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in test_loader:
            batch = {key: val.to(device) for key, val in batch.items()}
            outputs = model(**batch)
            preds = torch.argmax(outputs.logits, dim=-1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(batch["labels"].cpu().numpy())

    print("Accuracy:", accuracy_score(all_labels, all_preds))
    print("Classification Report:\n", classification_report(all_labels, all_preds))


if __name__ == "__main__":
    main()
