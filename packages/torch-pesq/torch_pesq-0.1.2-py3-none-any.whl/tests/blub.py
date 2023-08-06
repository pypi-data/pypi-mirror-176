import torchaudio
import scipy.io.wavfile
import numpy as np
import torch
from torch_pesq import PesqLoss

sample_rate, ref = scipy.io.wavfile.read("samples/speech.wav")
sample_rate, deg = scipy.io.wavfile.read("samples/degraded.wav")

max_val = max(np.max(np.abs(ref / 1.0)), np.max(np.abs(deg / 1.0)))
ref, deg = (
    (ref / max_val).astype(np.float32),
    (deg / max_val).astype(np.float32),
)
ref, deg = torch.from_numpy(ref), torch.from_numpy(deg)


loss = PesqLoss(1.0, sample_rate=16000)
print(loss.mos(ref, deg))
