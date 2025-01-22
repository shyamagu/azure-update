# Azure Update Deck

このプロジェクトは、Azureの更新情報を取得して処理し、PowerPoint形式のプレゼンテーションデッキを生成する2つのPythonスクリプトで構成されています。

## 前提条件

- Python 3.7以上
- pip (Pythonパッケージインストーラー)
- Azure OpenAIアカウントとAPIキー、エンドポイント

## セットアップ

1. リポジトリをクローンします:
    ```sh
    git clone https://github.com/shyamagu/azure-update.git
    cd azure-update
    ```

2. 仮想環境を作成してアクティブにします:
    ```sh
    python -m venv venv
    source venv/bin/activate  # Windowsの場合は `venv\Scripts\activate`
    ```

3. 必要なパッケージをインストールします:
    ```sh
    pip install -r requirements.txt
    ```

4. プロジェクトのルートディレクトリに `.env` ファイルを作成し、Azure OpenAIの認証情報を追加します:
    ```env
    AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
    AZURE_OPENAI_API_KEY=your_azure_openai_api_key
    MODEL_DEPLOYMENT_NAME=your_azure_openai_model
    ```
    ※動作検証にはgpt-4oを利用しました。

## 使用方法

### ステップ1: Azure更新情報の取得

`1_get_azure_update.py` スクリプトを実行して最新のAzure更新情報を取得します。日付を `YYYY-MM-DD` 形式で引数として指定する必要があります。
指定された日付**以降**の更新情報を取得しています。

```sh
python 1_get_azure_update.py 2025-01-01
```

このコマンドは、更新情報を含むMarkdownファイルを作成します。

### ステップ2: プレゼンテーションデッキの生成

`2_make_jp_update_pptx.py` スクリプトを実行して、取得した更新情報を生成AIをつかって処理し、PowerPoint形式のプレゼンテーションデッキを生成します。

```sh
python 2_make_jp_update_pptx.py
```

デフォルトでは、最新の `azure_update*.md` ファイルを使用します。特定のファイルを指定することもできます:

```sh
python 2_make_jp_update_pptx.py azure_update_20250101_20250122.md
```

出力は `pptx_azure_update_*.pptx` ファイルとなります。

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。