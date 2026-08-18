import os
import json
from datetime import datetime

def main():
    # 1. 保存先の data ディレクトリがなければ自動作成する
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    
    # 2. 保存するデータの内容（必要に応じて書き換えてください）
    usage_data = {
        "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "status": "active",
        "details": "LINE Rangers usage data updated."
    }
    
    # 3. data/current.json として保存する
    file_path = os.path.join(output_dir, 'current.json')
    json_text = json.dumps(usage_data, ensure_ascii=False, indent=2)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json_text)
        
    # Actionsのログで確認するための出力
    print(f"Updated {len(json_text)} characters")

if __name__ == '__main__':
    main()

