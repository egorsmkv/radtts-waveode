# RADTTS + WaveODE vocoder

🇺🇦 Join Ukrainian Text-to-Speech community: https://t.me/speech_synthesis_uk

<a target="_blank" href="https://colab.research.google.com/drive/116S9IgTV4hqU1jjeuq35jrz3dLSolWqr?usp=sharing">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

---

Clone the code:

```bash
git clone https://github.com/egorsmkv/radtts-waveode
cd radtts-waveode
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Download Ukrainian RADTTS and WaveODE models:

```bash
mkdir models
cd models

wget https://github.com/egorsmkv/radtts-waveode/releases/download/v1.0/M_40.pth
wget https://github.com/egorsmkv/radtts-istftnet/releases/download/v1.0/RADTTS-Lada.pt
```

Then you can inference own texts by the following command:

```bash
python3 inference.py -c config_ljs_dap.json -r models/RADTTS-Lada.pt -t test_sentences.txt --vocoder_path models/hifi_vocoder.pt --vocoder_config_path models/hifi_config.json -o results/
```
