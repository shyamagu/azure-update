import requests  
from bs4 import BeautifulSoup  
from datetime import datetime, timezone  
from dateutil import parser  
import sys

def main():  
    if len(sys.argv) < 2:  
        print("エラー: 日付を引数として指定してください。形式: YYYY-MM-DD")  
        return  

    try:  
        filter_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").replace(tzinfo=timezone.utc)  
        filter_date_str = filter_date.strftime("%Y%m%d")  
    except ValueError:  
        print("エラー: 日付の形式が正しくありません。形式: YYYY-MM-DD")  
        return  

    url = "https://www.microsoft.com/releasecommunications/api/v2/azure?$count=true&includeFacets=true&top=50&skip=0&orderby=modified%20desc"  
    headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',  
        'Accept': 'application/json, text/plain, */*',  
        'Accept-Language': 'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',  
        'Referer': 'https://www.microsoft.com/ja-jp/releasecommunications/azure',  
        'Origin': 'https://www.microsoft.com'  
    }  
 
    response = requests.get(url, headers=headers)  
 
    if response.status_code != 200:  
        print(f"エラー: データを取得できませんでした。ステータスコード: {response.status_code}")  
        print(f"レスポンスの内容:\n{response.text}")  
        return  
 
    try:  
        data = response.json()  
    except ValueError:  
        print("エラー: レスポンスから JSON をデコードできませんでした。")  
        print(f"レスポンスの内容:\n{response.text}")  
        return  
 
    status_translations = {  
        "Launched": "一般提供",  
        "In preview": "パブリックプレビュー",  
        "Retirement": "リタイアメント",  
        "Private Preview": "プライベートプレビュー",  
        "General Availability": "一般提供",  
        "Public Preview": "パブリックプレビュー",  
    }  
 
    output_filename = f"azure_update_{filter_date_str}_{datetime.now().strftime('%Y%m%d')}.md"
    with open(output_filename, "w", encoding="utf-8") as f:  # ファイルを最初に開く
        for item in data["value"]:  
            modified_date = item.get("modified", "")  
            if modified_date:  
                try:  
                    date_obj = parser.isoparse(modified_date)
                    if date_obj < filter_date:  
                        continue  # フィルター日付より古い場合はスキップ  
                    date_str = date_obj.strftime("%Y-%m-%d")  
                except Exception as e:  
                    print(f"エラー: 日付のパースに失敗しました。詳細: {e}")  
                    date_str = "不明"  
            else:  
                date_str = "不明"  
     
            # ステータスの抽出  
            status = item.get("status", "")  
            if not status:  
                # ステータスがない場合は availabilities から取得  
                if item.get("availabilities"):  
                    status = item["availabilities"][0].get("ring", "")  
     
            # ステータスを日本語に翻訳  
            status_jp = status_translations.get(status, status)  
     
            # タイトルから不要なプレフィックスを除去  
            title = item.get("title", "").strip()  
            prefixes = ["Generally Available:", "Public Preview:", "Private Preview:", "Retirement:", "GA:", "New:"]  
            for prefix in prefixes:  
                if title.startswith(prefix):  
                    title = title[len(prefix):].strip()  
                    break  # 最初のマッチで停止  
     
            # スライドタイトルの作成  
            slide_title = f"# {status_jp}: {title}"  
     
            # 更新対象機能の抽出  
            products = item.get("products", [])  
            features = ", ".join(products)  
            features_text = f"Azure {features}"  
     
            # 更新内容の抽出（HTMLタグを除去）  
            description_html = item.get("description", "")  
            soup = BeautifulSoup(description_html, 'html.parser')  
            description_text = soup.get_text().strip()  
     
            # 参考リンクの抽出  
            reference_links = []  
            for link in soup.find_all('a', href=True):  
                reference_links.append(link['href'])  
     
            # スライドの内容を構築  
            slide_content = f"""{slide_title}  
     
    ## 更新対象機能  
    {features_text}  
     
    ## 更新日付  
    {date_str}  
     
    ## 更新内容  
    {description_text}  
     
    ## 参考リンク  
    """  
            if reference_links:  
                for link in reference_links:  
                    slide_content += f" - {link}\n"  
            else:  
                slide_content += " - なし\n"  
     
            # スライドを出力  
            print(slide_content)  
            print("="*50)  
     
            # 上記の内容をファイルに出力（引数日付_今日の日付つきファイル名）  
            f.write(slide_content)  
            f.write("="*50)  
            f.write("\n")  
  
if __name__ == "__main__":  
    main()
