# -*- coding: utf-8 -*-
import time
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from model import TextRCNN_Bert
from load_data import traindataloader
from transformers import AdamW
from transformers import get_linear_schedule_with_warmup
from tqdm import tqdm

EPOCHS = 3
CLS = 2
BERT_PATH = './bert-base-chinese'

def my_plot(epochs, loss):
    plt.plot(epochs, loss)

device = "cpu"
if torch.cuda.is_available():
    device = "cuda"
print(f'Use {device}')

model = TextRCNN_Bert(BERT_PATH, CLS)
model.to(device)

total_steps = len(traindataloader) * EPOCHS
optimizer = AdamW(model.parameters(), lr=5e-5)
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps = 0, num_training_steps = total_steps)
criterion = nn.NLLLoss()

start = time.time()
loss_vals = []
for epoch in range(EPOCHS):
    model.train()
    epoch_loss= []
    pbar = tqdm(traindataloader)
    pbar.set_description("[Epoch {}]".format(epoch)) 
    for tokens_ids, mask, label in pbar:
        tokens_ids, mask, label = tokens_ids.to(device), mask.to(device), label.to(device)
        model.zero_grad()
        out = model(tokens_ids, mask)
        loss = criterion(out, label)
        loss.backward()
        epoch_loss.append(loss.item())
        optimizer.step()
        scheduler.step()
        pbar.set_postfix(loss=loss.item())
    loss_vals.append(np.mean(epoch_loss))    
end = time.time()
print(f'Training costs:{end-start} seconds')

torch.save(model.state_dict(), "model.pth") 
my_plot(np.linspace(1, EPOCHS, EPOCHS).astype(int), loss_vals)