import os
import numpy as np

from glob import glob
from sys import platform

import soundfile as sf

import torch
from scipy.io import wavfile

from .models import Generator
from .utils import config_setup, load_checkpoint


def save_wav(wav, path, hparams, norm=False):
    if norm:
        wav *= 32767 / max(0.01, np.max(np.abs(wav)))
        wavfile.write(path, hparams.sample_rate, wav.astype(np.int16))
    else:
        sf.write(path, wav, hparams.sample_rate)


def inference(input_mel_folder, vocoder_path, vocoder_config_path, sampling_method, sampling_steps):

    hparams = config_setup(vocoder_config_path)
    print(hparams)

    vocoder = Generator(hparams).cuda()
    # vocoder = Generator(hparams)
    load_checkpoint(vocoder_path, vocoder)
    vocoder.eval()

    with torch.no_grad():
        files_all = []
        for input_mel_file in glob(input_mel_folder +'/*.mel'):
            x = torch.load(input_mel_file)
            mel = x.float().cuda()
            if mel.shape[1] != hparams.mel_dim:
                mel = mel.transpose(1, 2)

            predicted_audio, noise = vocoder.inference(mel, sampling_method, sampling_steps)
            predicted_audio, noise = predicted_audio.squeeze().cpu().numpy(), noise.squeeze().cpu().numpy()

            # form a filename
            output_file = input_mel_file.replace('.mel','.wav')

            # save
            save_wav(predicted_audio, output_file, hparams, norm=True)

            print('<<--',output_file)

            files_all.append(output_file)

            os.remove(input_mel_file)

        s = '/'
        if platform == "win32":
            s = 'results\\'

        names = []
        for k in files_all:
            names.append(int(k.replace(input_mel_folder, '').replace(s, '').replace('.wav', '')))

        names_w = [f'{it}.wav' for it in sorted(names)]

        print('To combine all files into one, use this command:')
        print('')
        print('sox ' + ' '.join(names_w) + ' all.wav')


def process_folder(input_mel_folder, vocoder_path, vocoder_config_path, sampling_method, sampling_steps):
    inference(input_mel_folder, vocoder_path, vocoder_config_path, sampling_method, sampling_steps)
