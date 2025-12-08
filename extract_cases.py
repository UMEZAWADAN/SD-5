#!/usr/bin/env python3
"""
PDF事例集からテキストマイニング用のデータを抽出するスクリプト
"""

import os
import re
import json
import pdfplumber
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    """PDFからテキストを抽出"""
    text_pages = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_pages.append(text)
    except Exception as e:
        print(f"Error extracting {pdf_path}: {e}")
    return text_pages

def parse_osaka_cases(text_pages):
    """大阪大学の困難事例集（PDF1）をパース"""
    cases = []
    full_text = "\n".join(text_pages)
    
    # 事例パターンを検出
    case_pattern = r'事例[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳\d]+\s*(.+?)(?=事例[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳\d]+|$)'
    
    # カテゴリパターン
    category_pattern = r'■■\s*([A-Z]\..+?)(?=■■|事例)'
    
    current_category = ""
    
    for i, page_text in enumerate(text_pages):
        # カテゴリを検出
        cat_match = re.search(r'■■\s*([A-Z]\..+)', page_text)
        if cat_match:
            current_category = cat_match.group(1).strip()
        
        # 困難キーワードと支援キーワードを抽出
        difficulty_match = re.search(r'困難キーワード[：:]\s*(.+?)(?=支援キーワード|$)', page_text, re.DOTALL)
        support_match = re.search(r'支援キーワード[：:]\s*(.+?)(?=事例|$)', page_text, re.DOTALL)
        
        if difficulty_match or support_match:
            case = {
                "source": "大阪大学困難事例集",
                "category": current_category,
                "difficulty_keywords": [],
                "support_keywords": [],
                "content": page_text[:2000],
                "page": i + 1
            }
            
            if difficulty_match:
                keywords = difficulty_match.group(1).strip()
                case["difficulty_keywords"] = [k.strip() for k in re.split(r'[、,，]', keywords) if k.strip()]
            
            if support_match:
                keywords = support_match.group(1).strip()
                case["support_keywords"] = [k.strip() for k in re.split(r'[、,，]', keywords) if k.strip()]
            
            if case["difficulty_keywords"] or case["support_keywords"]:
                cases.append(case)
    
    return cases

def parse_saitama_cases(text_pages):
    """さいたま市の事例集（PDF2）をパース"""
    cases = []
    full_text = "\n".join(text_pages)
    
    # 事例を検出（事例1、事例2など）
    case_sections = re.split(r'事例\s*(\d+)', full_text)
    
    for i in range(1, len(case_sections), 2):
        if i + 1 < len(case_sections):
            case_num = case_sections[i]
            case_content = case_sections[i + 1][:3000]
            
            # 支援内容や結果を抽出
            support_match = re.search(r'支援[内容の概要]*[：:]\s*(.+?)(?=結果|経過|$)', case_content, re.DOTALL)
            result_match = re.search(r'(?:結果|経過)[：:]\s*(.+?)(?=事例|$)', case_content, re.DOTALL)
            
            case = {
                "source": "さいたま市事例集",
                "case_number": case_num,
                "content": case_content,
                "support_content": support_match.group(1).strip()[:500] if support_match else "",
                "result": result_match.group(1).strip()[:500] if result_match else "",
                "difficulty_keywords": [],
                "support_keywords": []
            }
            
            # キーワードを抽出（テキストから推測）
            if "独居" in case_content or "一人暮らし" in case_content:
                case["difficulty_keywords"].append("独居")
            if "拒否" in case_content:
                case["difficulty_keywords"].append("支援拒否")
            if "妄想" in case_content:
                case["difficulty_keywords"].append("妄想")
            if "徘徊" in case_content:
                case["difficulty_keywords"].append("徘徊")
            if "介護" in case_content and "負担" in case_content:
                case["difficulty_keywords"].append("介護負担")
            
            if "デイサービス" in case_content:
                case["support_keywords"].append("デイサービス導入")
            if "訪問" in case_content:
                case["support_keywords"].append("訪問支援")
            if "受診" in case_content:
                case["support_keywords"].append("医療機関受診")
            if "入院" in case_content or "施設" in case_content:
                case["support_keywords"].append("入院/施設利用")
            
            cases.append(case)
    
    return cases

def parse_ncgg_cases(text_pages):
    """国立長寿医療研究センターの事例集（PDF3）をパース"""
    cases = []
    full_text = "\n".join(text_pages)
    
    # 事例パターンを検出
    for i, page_text in enumerate(text_pages):
        # ポイント欄を検出
        point_match = re.search(r'ポイント[：:]*\s*(.+?)(?=事例|$)', page_text, re.DOTALL)
        
        if point_match or len(page_text) > 200:
            case = {
                "source": "国立長寿医療研究センター事例集",
                "content": page_text[:2000],
                "point": point_match.group(1).strip()[:500] if point_match else "",
                "page": i + 1,
                "difficulty_keywords": [],
                "support_keywords": []
            }
            
            # キーワードを抽出
            if "独居" in page_text or "一人暮らし" in page_text:
                case["difficulty_keywords"].append("独居")
            if "拒否" in page_text:
                case["difficulty_keywords"].append("支援拒否")
            if "妄想" in page_text or "幻覚" in page_text:
                case["difficulty_keywords"].append("幻覚・妄想")
            if "徘徊" in page_text:
                case["difficulty_keywords"].append("徘徊")
            if "老老" in page_text:
                case["difficulty_keywords"].append("老老介護")
            if "認認" in page_text:
                case["difficulty_keywords"].append("認認介護")
            
            if "連携" in page_text:
                case["support_keywords"].append("多職種連携")
            if "地域" in page_text and "資源" in page_text:
                case["support_keywords"].append("地域資源活用")
            if "家族" in page_text and "支援" in page_text:
                case["support_keywords"].append("家族支援")
            
            if case["difficulty_keywords"] or case["support_keywords"] or case["point"]:
                cases.append(case)
    
    return cases

def parse_kanagawa_cases(text_pages):
    """神奈川県の事例集（PDF4）をパース"""
    cases = []
    full_text = "\n".join(text_pages)
    
    # 世帯タイプごとのセクションを検出
    section_types = ["夫婦世帯", "親と子世帯", "単身世帯", "未受診ケース", "家族関係悪化ケース", "被害妄想のあるケース"]
    
    for i, page_text in enumerate(text_pages):
        case = {
            "source": "神奈川県事例集",
            "content": page_text[:2000],
            "page": i + 1,
            "household_type": "",
            "difficulty_keywords": [],
            "support_keywords": []
        }
        
        # 世帯タイプを検出
        for section_type in section_types:
            if section_type in page_text:
                case["household_type"] = section_type
                break
        
        # キーワードを抽出
        if "独居" in page_text or "単身" in page_text:
            case["difficulty_keywords"].append("独居")
        if "拒否" in page_text:
            case["difficulty_keywords"].append("支援拒否")
        if "妄想" in page_text:
            case["difficulty_keywords"].append("妄想")
        if "未受診" in page_text:
            case["difficulty_keywords"].append("未受診")
        if "家族関係" in page_text and "悪化" in page_text:
            case["difficulty_keywords"].append("家族関係悪化")
        if "介護負担" in page_text:
            case["difficulty_keywords"].append("介護負担")
        
        if "デイサービス" in page_text:
            case["support_keywords"].append("デイサービス")
        if "訪問" in page_text:
            case["support_keywords"].append("訪問支援")
        if "受診" in page_text and "つなげ" in page_text:
            case["support_keywords"].append("受診支援")
        if "入院" in page_text:
            case["support_keywords"].append("入院支援")
        if "施設" in page_text:
            case["support_keywords"].append("施設入所")
        
        if case["difficulty_keywords"] or case["support_keywords"]:
            cases.append(case)
    
    return cases

def create_tfidf_corpus(cases):
    """TF-IDF用のコーパスを作成"""
    corpus = []
    for case in cases:
        # テキストを結合
        text_parts = [
            case.get("content", ""),
            " ".join(case.get("difficulty_keywords", [])),
            " ".join(case.get("support_keywords", [])),
            case.get("support_content", ""),
            case.get("result", ""),
            case.get("point", "")
        ]
        combined_text = " ".join(text_parts)
        
        corpus.append({
            "id": f"{case.get('source', 'unknown')}_{len(corpus)}",
            "source": case.get("source", ""),
            "text": combined_text,
            "difficulty_keywords": case.get("difficulty_keywords", []),
            "support_keywords": case.get("support_keywords", []),
            "policy": case.get("support_content", "") or case.get("point", "") or case.get("result", "")
        })
    
    return corpus

def main():
    """メイン処理"""
    pdf_files = [
        {
            "path": os.path.expanduser("~/attachments/21fe92e6-c579-4d37-a50f-3d9f233f567b/ea998a7fa25280ed6946db5d03e64df7456bf9ed.pdf"),
            "name": "大阪大学困難事例集",
            "parser": parse_osaka_cases
        },
        {
            "path": os.path.expanduser("~/attachments/b578cdd2-fde5-46a1-9cf0-f2409e54367c/jirei-shu.pdf"),
            "name": "さいたま市事例集",
            "parser": parse_saitama_cases
        },
        {
            "path": os.path.expanduser("~/attachments/53ff2a47-50d8-4477-a6a3-9a2d8eb6e591/R3_Casestudies2.pdf"),
            "name": "国立長寿医療研究センター事例集",
            "parser": parse_ncgg_cases
        },
        {
            "path": os.path.expanduser("~/attachments/03f1c28b-b159-4bf4-ad62-0a8ba53ec6ae/syokisyuutyuujireisyuu.pdf"),
            "name": "神奈川県事例集",
            "parser": parse_kanagawa_cases
        }
    ]
    
    all_cases = []
    
    for pdf_info in pdf_files:
        print(f"\n処理中: {pdf_info['name']}")
        
        if not os.path.exists(pdf_info["path"]):
            print(f"  ファイルが見つかりません: {pdf_info['path']}")
            continue
        
        text_pages = extract_text_from_pdf(pdf_info["path"])
        print(f"  ページ数: {len(text_pages)}")
        
        cases = pdf_info["parser"](text_pages)
        print(f"  抽出事例数: {len(cases)}")
        
        all_cases.extend(cases)
    
    # TF-IDF用コーパスを作成
    corpus = create_tfidf_corpus(all_cases)
    
    # JSONファイルに保存
    output_path = os.path.join(os.path.dirname(__file__), "data", "case_studies", "cases.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    output_data = {
        "extracted_at": datetime.now().isoformat(),
        "total_cases": len(corpus),
        "sources": [pdf["name"] for pdf in pdf_files],
        "cases": corpus
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n完了: {len(corpus)}件の事例を {output_path} に保存しました")
    
    # 統計情報を表示
    print("\n=== 統計情報 ===")
    sources = {}
    for case in corpus:
        source = case.get("source", "unknown")
        sources[source] = sources.get(source, 0) + 1
    
    for source, count in sources.items():
        print(f"  {source}: {count}件")
    
    return output_data

if __name__ == "__main__":
    main()
