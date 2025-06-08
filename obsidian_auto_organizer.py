#!/usr/bin/env python3
"""
Obsidian自動整理システム - vault-organizerプラグインの代替実装
CLAUDE.md Simple First原則に基づく実装
"""

import os
import shutil
import re
from pathlib import Path
import json
from datetime import datetime

class ObsidianAutoOrganizer:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.rules = {
            # ファイル拡張子による分類
            'images': ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'],
            'attachments': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'],
            'audio': ['.mp3', '.wav', '.m4a', '.flac'],
            'video': ['.mp4', '.avi', '.mov', '.mkv'],
            # タグによる分類
            'daily': ['#daily', '#日記'],
            'projects': ['#project', '#プロジェクト'],
            'research': ['#research', '#リサーチ', '#調査'],
            'ai': ['#AI', '#claude', '#chatgpt', '#機械学習'],
            'tech': ['#tech', '#技術', '#プログラミング', '#coding']
        }
        
    def analyze_vault(self):
        """Vaultの現状分析"""
        print("📊 Obsidian Vault分析中...")
        
        files_by_type = {
            'markdown': [],
            'images': [],
            'attachments': [],
            'other': []
        }
        
        for file_path in self.vault_path.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                if file_path.suffix == '.md':
                    files_by_type['markdown'].append(file_path)
                elif file_path.suffix.lower() in self.rules['images']:
                    files_by_type['images'].append(file_path)
                elif file_path.suffix.lower() in self.rules['attachments']:
                    files_by_type['attachments'].append(file_path)
                else:
                    files_by_type['other'].append(file_path)
        
        print(f"📝 Markdownファイル: {len(files_by_type['markdown'])}個")
        print(f"🖼️ 画像ファイル: {len(files_by_type['images'])}個")
        print(f"📎 添付ファイル: {len(files_by_type['attachments'])}個")
        print(f"📁 その他: {len(files_by_type['other'])}個")
        
        return files_by_type
        
    def organize_by_type(self, dry_run=True):
        """ファイルタイプ別整理"""
        print("🗂️ ファイルタイプ別整理開始...")
        
        files = self.analyze_vault()
        organized = []
        
        # 画像ファイルの整理
        images_dir = self.vault_path / "Assets" / "Images"
        if files['images'] and not dry_run:
            images_dir.mkdir(parents=True, exist_ok=True)
            
        for img_file in files['images']:
            new_path = images_dir / img_file.name
            if dry_run:
                print(f"📷 移動予定: {img_file.relative_to(self.vault_path)} → {new_path.relative_to(self.vault_path)}")
            else:
                if not new_path.exists():
                    shutil.move(str(img_file), str(new_path))
                    organized.append(f"画像移動: {img_file.name}")
                    
        # 添付ファイルの整理
        attachments_dir = self.vault_path / "Assets" / "Attachments"
        if files['attachments'] and not dry_run:
            attachments_dir.mkdir(parents=True, exist_ok=True)
            
        for att_file in files['attachments']:
            new_path = attachments_dir / att_file.name
            if dry_run:
                print(f"📎 移動予定: {att_file.relative_to(self.vault_path)} → {new_path.relative_to(self.vault_path)}")
            else:
                if not new_path.exists():
                    shutil.move(str(att_file), str(new_path))
                    organized.append(f"添付ファイル移動: {att_file.name}")
                    
        return organized
        
    def organize_by_tags(self, dry_run=True):
        """タグ別整理"""
        print("🏷️ タグ別整理開始...")
        
        files = self.analyze_vault()
        organized = []
        
        for md_file in files['markdown']:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # タグ抽出
                tags = re.findall(r'#\w+', content)
                
                # 分類判定
                target_folder = None
                for category, category_tags in self.rules.items():
                    if category in ['images', 'attachments', 'audio', 'video']:
                        continue
                        
                    for tag in tags:
                        if tag in category_tags:
                            target_folder = category
                            break
                    if target_folder:
                        break
                
                if target_folder:
                    category_dir = self.vault_path / target_folder.title()
                    new_path = category_dir / md_file.name
                    
                    if dry_run:
                        print(f"📝 移動予定: {md_file.relative_to(self.vault_path)} → {new_path.relative_to(self.vault_path)} (タグ: {', '.join(tags)})")
                    else:
                        category_dir.mkdir(exist_ok=True)
                        if not new_path.exists():
                            shutil.move(str(md_file), str(new_path))
                            organized.append(f"ノート移動: {md_file.name} → {target_folder}")
                            
            except Exception as e:
                print(f"❌ ファイル処理エラー: {md_file.name} - {e}")
                
        return organized
        
    def organize_daily_notes(self, dry_run=True):
        """デイリーノート整理"""
        print("📅 デイリーノート整理開始...")
        
        files = self.analyze_vault()
        organized = []
        
        # 日付パターン (YYYY-MM-DD, YYYY年MM月DD日 等)
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',
            r'\d{4}年\d{1,2}月\d{1,2}日',
            r'\d{4}\d{2}\d{2}'
        ]
        
        daily_dir = self.vault_path / "Daily Notes"
        
        for md_file in files['markdown']:
            is_daily = False
            
            # ファイル名から日付判定
            for pattern in date_patterns:
                if re.search(pattern, md_file.name):
                    is_daily = True
                    break
                    
            # ファイル内容から判定
            if not is_daily:
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if any(tag in content for tag in self.rules['daily']):
                            is_daily = True
                except:
                    pass
                    
            if is_daily:
                new_path = daily_dir / md_file.name
                if dry_run:
                    print(f"📅 移動予定: {md_file.relative_to(self.vault_path)} → {new_path.relative_to(self.vault_path)}")
                else:
                    daily_dir.mkdir(exist_ok=True)
                    if not new_path.exists():
                        shutil.move(str(md_file), str(new_path))
                        organized.append(f"デイリーノート移動: {md_file.name}")
                        
        return organized
        
    def create_organization_report(self, organized_items):
        """整理レポート作成"""
        report_path = self.vault_path / f"Organization_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        report_content = f"""# 📋 Obsidian自動整理レポート

**実行日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## ✅ 整理完了項目

"""
        for item in organized_items:
            report_content += f"- {item}\n"
            
        report_content += f"""

## 📊 整理結果

- **処理ファイル数**: {len(organized_items)}個
- **整理カテゴリ**: ファイルタイプ別、タグ別、デイリーノート
- **作成フォルダ**: Assets/Images, Assets/Attachments, Daily Notes, Projects, Research, Tech, AI

## 🔄 次回実行

自動整理を再実行する場合:
```bash
python3 obsidian_auto_organizer.py organize
```

---
*自動生成レポート by Obsidian Auto Organizer*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        print(f"📋 整理レポート作成: {report_path.name}")
        
    def run_full_organization(self, dry_run=True):
        """完全自動整理実行"""
        print("🚀 Obsidian自動整理システム開始")
        print(f"📁 対象Vault: {self.vault_path}")
        print(f"🔍 モード: {'ドライラン(確認のみ)' if dry_run else '実際に整理実行'}")
        print("-" * 50)
        
        all_organized = []
        
        # 各整理実行
        all_organized.extend(self.organize_by_type(dry_run))
        all_organized.extend(self.organize_daily_notes(dry_run))
        all_organized.extend(self.organize_by_tags(dry_run))
        
        if not dry_run and all_organized:
            self.create_organization_report(all_organized)
            
        print("-" * 50)
        print(f"✅ 整理完了: {len(all_organized)}項目")
        
        if dry_run:
            print("\n💡 実際に整理を実行するには:")
            print("python3 obsidian_auto_organizer.py organize")
            
        return all_organized

def main():
    import sys
    
    vault_path = r"G:\マイドライブ\Obsidian Vault"
    organizer = ObsidianAutoOrganizer(vault_path)
    
    if len(sys.argv) > 1 and sys.argv[1] == "organize":
        # 実際に整理実行
        organizer.run_full_organization(dry_run=False)
    else:
        # ドライラン(確認のみ)
        organizer.run_full_organization(dry_run=True)

if __name__ == "__main__":
    main()