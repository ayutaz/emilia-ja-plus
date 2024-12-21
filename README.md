# Emilia-JA-Plus: A Comprehensive Japanese Speech Dataset for Large-Scale Speech Generation

## Overview

**Emilia-JA-Plus** is a dataset that extracts only the Japanese portion of the Emilia dataset and adds the following information:

- **Transcriptions using Parakeet**: All audio data has been transcribed using the Parakeet toolkit.
- **Kana Conversion using Sudachi**: The transcribed text has been converted to kana notation using Sudachi.

This dataset provides a high-quality resource that is useful for Japanese speech recognition, speech synthesis, and related research.

### Dataset Features

- **Japanese Speech Data Only**: Extracted Japanese speech data from the Emilia dataset.
- **Diverse Speakers and Speaking Styles**: Collected from various video platforms and podcasts on the internet, covering various content genres such as talk shows, interviews, debates, sports commentary, and audiobooks.
- **High-Quality Annotations**: Provides transcriptions using Parakeet and kana notation using Sudachi.

### Data Volume

| Language | Duration (hours) |
|----------|------------------|
| Japanese | 1,715            |

## How to Use the Dataset

Emilia-JA-Plus is publicly available on [HuggingFace](https://huggingface.co/datasets/yourusername/Emilia-JA-Plus).

### Loading the Dataset

You can load the dataset using the following code:

```python
from datasets import load_dataset
dataset = load_dataset("yourusername/Emilia-JA-Plus", streaming=True)
print(dataset)
print(next(iter(dataset['train'])))
Use Cases
The transcribed text and kana-converted text can be utilized as training data for Japanese speech recognition models or speech synthesis models.
```

## Dataset Structure

The dataset has the following structure:

- **id**: Unique identifier for each audio sample.
- **wav**: Path to the audio file.
- **text**: Transcribed text using Parakeet.
- **kana_text**: Kana-converted text using Sudachi.
- **duration**: Length of the audio file in seconds.
- **speaker**: Speaker identifier.
- **language**: Language code (`ja`).
- **dnsmos**: DNSMOS score of the audio sample.

### Data Sample

```json
{
    "id": "JA_B00002_S06268_W000002",
    "wav": "JA_B00002/JA_B00002_S06268/mp3/JA_B00002_S06268_W000002.mp3",
    "text": "あると思うけど、調べてみないとね、お昼過ぎにもう一度来てくれる?",
    "duration": 6.621,
    "speaker": "JA_B00002_S06268",
    "language": "ja",
    "dnsmos": 3.4955,
    "kana_text": "アルトオモウケド、シラベテミナイトネ、オヒルスギニモウイチドキテクレル?",
    "hiragana_text": "あるとおもうけど、しらべてみないとね、おひるすぎにもういちどきてくれる?"
}
```

## References
If you use this dataset, please cite the following paper:

```bibtex
@inproceedings{emilia,
    author={He, Haorui and Shang, Zengqiang and Wang, Chaoren and Li, Xuyuan and Gu, Yicheng and Hua, Hua and Liu, Liwei and Yang, Chen and Li, Jiaqi and Shi, Peiyang and Wang, Yuancheng and Chen, Kai and Zhang, Pengyuan and Wu, Zhizheng},
    title={{Emilia}: An Extensive, Multilingual, and Diverse Speech Dataset for Large-Scale Speech Generation},
    booktitle={Proc.~of SLT},
    year={2024}
}
```

## License

This dataset is released under the CC BY-NC-4.0 license. For detailed terms of use, please refer to the [Emilia Dataset](https://huggingface.co/datasets/amphion/Emilia-Dataset).

## Notes

- **Non-Commercial Use Only**: This dataset is intended for non-commercial purposes only.
- **About Copyright**: The copyrights of the audio files remain with their original owners. When using this dataset, please comply with all relevant laws and regulations.

## Contact

If you have any questions or requests regarding the dataset, please feel free to contact us.

---

Thank you for your interest in the Emilia-JA-Plus dataset. We hope it will be a valuable resource for your research and projects.