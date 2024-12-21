# whisper_language_detector.py

import os
import json
import torch
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import whisper
from whisper.audio import N_FRAMES, log_mel_spectrogram, pad_or_trim

# 処理を開始するディレクトリ（JSONファイルが格納されているディレクトリ）
DATA_DIR = 'JA'  # 必要に応じて変更してください

# 各プロセスでモデルを初期化する関数
def init_process(model_name='large-v3-turbo', device='cuda'):
    global model
    model = whisper.load_model(model_name, device=device)

# 単一のJSONファイルを処理する関数
def process_json(file_name):
    try:
        file_path = os.path.join(DATA_DIR, file_name)
        # JSONファイルであることを確認
        if not file_name.endswith('.json'):
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 音声ファイルのパスをJSONファイルの名前から取得
        audio_file_name = os.path.splitext(file_name)[0] + '.mp3'
        audio_file_path = os.path.join(DATA_DIR, audio_file_name)

        if not os.path.exists(audio_file_path):
            print(f"音声ファイルが見つかりません: {audio_file_path}")
            return

        # 音声ファイルの読み込みと処理
        try:
            mel = log_mel_spectrogram(audio_file_path)
        except Exception as e:
            print(f"音声ファイルの読み込み中にエラーが発生しました ({audio_file_path}): {e}")
            return
        
        # 30秒データに整形
        # モデルのデバイスがFP16をサポートしているか確認
        if model.device.type == 'cpu':
            dtype = torch.float32
        else:
            dtype = torch.float16

        segment = pad_or_trim(mel, N_FRAMES).to(model.device).to(dtype)

        # 言語を検出
        _, probs = model.detect_language(segment)
        detected_language = max(probs, key=probs.get)

        # 確率を取得し、小数点以下6桁に丸める
        detected_language_prob = round(float(probs[detected_language]), 6)

        # 'detected_language'とその確率'language_prob'を追加
        data['detected_language'] = detected_language
        data['language_prob'] = detected_language_prob

        # 更新されたJSONデータを書き戻す（インデントを追加）
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"{relative_file_path}の処理中にエラーが発生しました: {e}")

# メイン関数で並列処理を実行
def main():
    # DATA_DIR内のすべてのJSONファイルをリストアップ
    file_list = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]

    # GPUメモリを考慮してプロセス数を制限
    max_processes = 1  # 使用するモデルとGPUメモリに応じて適切に設定してください
    cpu_cores = min(cpu_count(), max_processes)

    # マルチプロセッシングのプールを使用
    with Pool(cpu_cores, initializer=init_process, initargs=('large-v3-turbo', 'cuda')) as p:
        list(tqdm(p.imap_unordered(process_json, file_list), total=len(file_list)))

if __name__ == '__main__':
    main()