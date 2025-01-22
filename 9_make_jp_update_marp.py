import os
import sys
from openai import AzureOpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) 

client = AzureOpenAI(
    azure_endpoint = os.getenv("AOAI_GO_ENDPOINT"), 
    api_key=os.getenv("AOAI_GO_API_KEY"),  
    api_version="2024-12-01-preview",
    )

def get_completion_from_messages(messages,temperature=0):
    response = client.chat.completions.create(
        model=os.getenv('AOAI_GO_MODEL'),
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

def callGPT(system_prompt, user_prompt):
    messages =  [
        {'role':'system', 'content':system_prompt},
        {'role':'user', 'content':user_prompt}
        ]
    
    return get_completion_from_messages(messages)

def get_latest_update_file():
    files = [f for f in os.listdir() if f.startswith("azure_update") and f.endswith(".md")]
    if not files:
        raise FileNotFoundError("No azure_update*.md files found.")
    latest_file = max(files, key=os.path.getctime)
    return latest_file

def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if not os.path.exists(input_file):
            print(f"Error: Specified file '{input_file}' not found.")
            return
        print(f"Using specified file: {input_file}")
    else:
        try:
            input_file = get_latest_update_file()
            print(f"Using latest file: {input_file}")
        except FileNotFoundError as e:
            print(e)
            return

    # ファイルを読み込む
    with open(input_file, "r", encoding="utf-8") as f:
        update_text = f.read()

    # update_textは =*50で区切られているため分割してループする
    slides = update_text.split("="*50)

    system_prompt = """\
    入力された情報はあるAzureの機能更新情報です。この情報を以下のルールで更新してください。

    # ルール
    - タイトル(先頭行): なるべくそのままの表現で日本語に翻訳する
    - 更新対象機能 : 元の情報のまま
    - 更新日付: 元の情報のまま
    - 更新内容: 日本語で３行程度に要約する
    - 参考リンク: 元の情報のまま
    """

    all_update_deck = """\
---
marp: true
style: |
    section {
        justify-content: start;
        font-size: 20px;
        margin:0px;
        padding-top:20px;
        font-family: "Meiryo UI"
    }
    h1 {
        font-size:32px;
        color: #0078D4
    }
    h2 {
        font-size: 20px;
        margin:0px;
        color: #444;
        margin-top: 10px;
    }
---

"""
    for slide in slides:
        user_prompt = slide
        if not user_prompt.strip():
            continue
        one_update_deck = callGPT(system_prompt, user_prompt)
        print(one_update_deck)
        all_update_deck += one_update_deck
        all_update_deck += "\n\n---\n\n"

    # 生成されたマークダウンをファイルに出力
    output_file = f"marp_{os.path.basename(input_file)}"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(all_update_deck)

if __name__ == "__main__":
    main()
