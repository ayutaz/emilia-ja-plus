import os
import json
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from sudachipy import dictionary, Tokenizer

# JSONファイルが存在するディレクトリのパス
DATA_DIR = 'JA'

# カタカナをひらがなに変換する関数
def katakana_to_hiragana(text):
    """カタカナをひらがなに変換する関数"""
    hiragana = ''
    for char in text:
        code = ord(char)
        # カタカナの範囲内の文字をひらがなに変換
        if 0x30A1 <= code <= 0x30F4:
            hiragana += chr(code - 0x60)
        elif code == 0x30FC:  # 長音符「ー」の処理（そのまま追加）
            hiragana += char
        elif 0x30FD <= code <= 0x30FF:  # 「ヽ」「ヾ」「ヿ」
            hiragana += chr(code - 0x60)
        else:
            hiragana += char
    return hiragana

# SudachiPyのトークナイザーを初期化（full辞書を使用）
tokenizer_obj = dictionary.Dictionary(dict="full").create()
split_mode = Tokenizer.SplitMode.C  # 分割モードを指定

# 単一のJSONファイルを処理する関数
def process_json(file_name):
    try:
        file_path = os.path.join(DATA_DIR, file_name)
        # JSONファイルであることを確認
        if not file_name.endswith('.json'):
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 'text'フィールドを取得
        text = data.get('text', '')
        if not text:
            return

        # テキストをかなに変換
        kana_text = ''
        for m in tokenizer_obj.tokenize(text, split_mode):
            kana = m.reading_form()
            kana_text += kana

        # カタカナをひらがなに変換
        hiragana_text = katakana_to_hiragana(kana_text)

        # 'kana_text'と'hiragana_text'フィールドを追加
        data['kana_text'] = kana_text
        data['hiragana_text'] = hiragana_text

        # 更新されたJSONデータを書き戻す（indentを追加）
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"{file_name}の処理中にエラーが発生しました: {e}")

# メイン関数で並列処理を実行
def main():
    # ディレクトリ内のすべてのファイルをリストアップ
    file_list = os.listdir(DATA_DIR)

    # マルチプロセッシングのプールを使用
    cpu_cores = cpu_count()
    with Pool(cpu_cores) as p:
        list(tqdm(p.imap_unordered(process_json, file_list), total=len(file_list)))

if __name__ == '__main__':
    main()