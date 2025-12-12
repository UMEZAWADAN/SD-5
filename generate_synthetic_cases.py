#!/usr/bin/env python3
"""
ルールベース合成データ生成スクリプト
"""

import json
import random
from datetime import datetime
from typing import List, Dict, Any

# 困難キーワード（認知症ケアで直面する課題）
DIFFICULTY_KEYWORDS = [
    "独居", "老老介護", "認認介護", "支援拒否", "幻覚・妄想", "徘徊",
    "セルフネグレクト・ごみ屋敷", "介護者の負担", "金銭管理困難", "服薬管理困難",
    "キーパーソンの協力不足", "家族間の意見相違", "易怒性・興奮", "暴力・暴言",
    "アルコール問題", "虐待疑い", "経済的困窮", "未受診", "日中独居",
    "遠距離介護", "若年性認知症", "前頭側頭型認知症", "レビー小体型認知症",
    "多問題世帯", "近隣トラブル", "火の不始末", "運転の問題", "入院後の在宅復帰"
]

# 支援キーワード（実施した支援内容）
SUPPORT_KEYWORDS = [
    "本人への説明", "キーパーソン/家族/住民への説明", "在宅サービスの導入",
    "デイサービス導入", "訪問介護導入", "訪問看護導入", "ショートステイ利用",
    "入院/施設の利用", "医療機関受診", "認知症疾患医療センター連携",
    "支援機関の連携", "チーム員会議の活用", "地域ケア会議", "成年後見制度",
    "日常生活自立支援事業", "介護保険申請支援", "障害福祉サービス",
    "生活保護申請", "見守りサービス", "配食サービス", "服薬管理支援",
    "家族会紹介", "認知症カフェ", "介護者支援", "レスパイトケア",
    "住環境整備", "GPS見守り", "緊急通報システム"
]

# 認知症の種類
DEMENTIA_TYPES = [
    "アルツハイマー型認知症",
    "血管性認知症",
    "レビー小体型認知症",
    "前頭側頭型認知症",
    "混合型認知症",
    "軽度認知障害（MCI）"
]

# 年齢層
AGE_RANGES = [
    (65, 74, "前期高齢者"),
    (75, 84, "後期高齢者"),
    (85, 94, "超高齢者"),
    (50, 64, "若年性")
]

# 性別
GENDERS = ["男性", "女性"]

# 世帯状況
LIVING_SITUATIONS = [
    "独居",
    "配偶者と二人暮らし",
    "子ども家族と同居",
    "配偶者と子ども家族と同居",
    "兄弟姉妹と同居",
    "施設入所中"
]

# 介護度
CARE_LEVELS = [
    "未申請",
    "非該当",
    "要支援1",
    "要支援2",
    "要介護1",
    "要介護2",
    "要介護3",
    "要介護4",
    "要介護5"
]

# 認知症高齢者の日常生活自立度
DEMENTIA_ADL_LEVELS = ["自立", "I", "IIa", "IIb", "IIIa", "IIIb", "IV", "M"]

# 障害高齢者の日常生活自立度
DISABILITY_ADL_LEVELS = ["自立", "J1", "J2", "A1", "A2", "B1", "B2", "C1", "C2"]

# 主訴・相談経緯のテンプレート
REFERRAL_SOURCES = [
    "家族からの相談",
    "民生委員からの通報",
    "近隣住民からの相談",
    "かかりつけ医からの紹介",
    "地域包括支援センターへの相談",
    "警察からの連絡",
    "病院の医療ソーシャルワーカーからの紹介",
    "介護支援専門員からの相談",
    "行政（高齢福祉課）からの依頼",
    "本人からの相談"
]

# 身体疾患
PHYSICAL_CONDITIONS = [
    "高血圧", "糖尿病", "心疾患", "脳梗塞後遺症", "骨粗鬆症",
    "変形性膝関節症", "変形性腰椎症", "慢性腎臓病", "パーキンソン病",
    "白内障", "難聴", "慢性閉塞性肺疾患", "がん", "肝疾患",
    "大腿骨骨折術後", "圧迫骨折", "関節リウマチ"
]

# 行動・心理症状（BPSD）
BPSD_SYMPTOMS = [
    "物盗られ妄想", "被害妄想", "幻視", "幻聴", "徘徊", "夜間不穏",
    "昼夜逆転", "易怒性", "暴言", "暴力", "介護抵抗", "不安・焦燥",
    "抑うつ", "アパシー", "異食", "収集癖", "帰宅願望", "作話",
    "繰り返し質問", "同じ話の繰り返し", "脱抑制", "常同行動"
]

# 支援結果
SUPPORT_OUTCOMES = [
    "在宅生活継続",
    "介護サービス導入により安定",
    "医療機関への定期受診開始",
    "グループホーム入所",
    "特別養護老人ホーム入所",
    "介護老人保健施設入所",
    "精神科病院入院",
    "一般病院入院",
    "サービス付き高齢者向け住宅へ転居",
    "家族の介護力向上により安定",
    "地域の見守り体制構築",
    "経過観察中",
    "支援終了（安定）",
    "他機関へ引継ぎ"
]


def generate_background(age: int, gender: str, living_situation: str, 
                        dementia_type: str, physical_conditions: List[str]) -> str:
    """対象者の背景情報を生成"""
    templates = [
        f"{age}歳{gender}。{living_situation}。{dementia_type}の診断あり。既往歴として{', '.join(physical_conditions)}がある。",
        f"{age}歳の{gender}で、{living_situation}の生活を送っている。{dementia_type}と診断されており、{', '.join(physical_conditions)}の治療中。",
        f"{gender}、{age}歳。{living_situation}。約{'1年' if random.random() > 0.5 else '2年'}前より物忘れが目立ち始め、{dementia_type}と診断された。{', '.join(physical_conditions)}の既往あり。",
    ]
    return random.choice(templates)


def generate_initial_situation(difficulty_keywords: List[str], bpsd: List[str],
                               living_situation: str, referral: str) -> str:
    """初回訪問時の状況を生成"""
    situation_parts = []
    
    # 相談経緯
    situation_parts.append(f"【相談経緯】{referral}により支援開始。")
    
    # 困難状況の詳細
    if "独居" in difficulty_keywords:
        situation_parts.append("独居生活を送っており、日常生活の管理が困難になってきている。")
    if "老老介護" in difficulty_keywords:
        situation_parts.append("配偶者も高齢で健康上の問題を抱えており、介護負担が大きい状況。")
    if "認認介護" in difficulty_keywords:
        situation_parts.append("配偶者も認知機能の低下が見られ、お互いの状況を正確に把握できていない。")
    if "支援拒否" in difficulty_keywords:
        situation_parts.append("本人は支援の必要性を感じておらず、介入に対して拒否的な態度を示している。")
    if "幻覚・妄想" in difficulty_keywords:
        situation_parts.append("幻覚や妄想が見られ、家族や周囲との関係に影響が出ている。")
    if "徘徊" in difficulty_keywords:
        situation_parts.append("外出して帰宅できなくなることがあり、警察に保護されたこともある。")
    if "セルフネグレクト・ごみ屋敷" in difficulty_keywords:
        situation_parts.append("自宅内にゴミが堆積し、衛生状態が悪化している。入浴や着替えも不十分。")
    if "金銭管理困難" in difficulty_keywords:
        situation_parts.append("金銭管理ができなくなり、訪問販売で高額商品を購入するなどの問題が発生。")
    if "服薬管理困難" in difficulty_keywords:
        situation_parts.append("薬の飲み忘れや重複服用があり、健康状態への影響が懸念される。")
    if "虐待疑い" in difficulty_keywords:
        situation_parts.append("身体にあざが見られるなど、虐待が疑われる状況。")
    if "アルコール問題" in difficulty_keywords:
        situation_parts.append("アルコール依存の問題があり、認知機能低下との関連が疑われる。")
    if "火の不始末" in difficulty_keywords:
        situation_parts.append("調理中に火を消し忘れることがあり、火災のリスクが高い状態。")
    
    # BPSDの記載
    if bpsd:
        situation_parts.append(f"【行動・心理症状】{', '.join(bpsd[:3])}が見られる。")
    
    return "\n".join(situation_parts)


def generate_assessment(dementia_adl: str, disability_adl: str, 
                        care_level: str, bpsd: List[str]) -> str:
    """アセスメント結果を生成"""
    assessment_parts = []
    
    assessment_parts.append(f"【認知機能】認知症高齢者の日常生活自立度：{dementia_adl}")
    assessment_parts.append(f"【身体機能】障害高齢者の日常生活自立度：{disability_adl}")
    assessment_parts.append(f"【介護度】{care_level}")
    
    # 認知機能の詳細
    if dementia_adl in ["IIa", "IIb"]:
        assessment_parts.append("日常生活に支障をきたすような症状・行動が見られるが、誰かが注意していれば自立できる。")
    elif dementia_adl in ["IIIa", "IIIb"]:
        assessment_parts.append("日常生活に支障をきたすような症状・行動が見られ、介護を必要とする。")
    elif dementia_adl in ["IV", "M"]:
        assessment_parts.append("日常生活に支障をきたすような症状・行動が頻繁に見られ、常に介護を必要とする。")
    
    return "\n".join(assessment_parts)


def generate_support_plan(support_keywords: List[str], difficulty_keywords: List[str]) -> str:
    """支援方針を生成"""
    plan_parts = []
    
    plan_parts.append("【支援方針】")
    
    # 困難状況に応じた支援方針
    if "独居" in difficulty_keywords:
        plan_parts.append("・見守り体制の構築と生活支援サービスの導入を検討")
    if "老老介護" in difficulty_keywords or "介護者の負担" in difficulty_keywords:
        plan_parts.append("・介護者の負担軽減のためレスパイトケアの導入を検討")
    if "支援拒否" in difficulty_keywords:
        plan_parts.append("・信頼関係の構築を優先し、段階的な支援導入を目指す")
    if "幻覚・妄想" in difficulty_keywords:
        plan_parts.append("・専門医療機関との連携を強化し、薬物療法の調整を検討")
    if "徘徊" in difficulty_keywords:
        plan_parts.append("・GPS見守りサービスの導入と地域の見守りネットワーク構築")
    if "セルフネグレクト・ごみ屋敷" in difficulty_keywords:
        plan_parts.append("・生活環境の改善と訪問支援の導入を段階的に進める")
    if "金銭管理困難" in difficulty_keywords:
        plan_parts.append("・日常生活自立支援事業や成年後見制度の利用を検討")
    if "服薬管理困難" in difficulty_keywords:
        plan_parts.append("・訪問薬剤管理指導の導入と服薬カレンダーの活用")
    if "虐待疑い" in difficulty_keywords:
        plan_parts.append("・本人の安全確保を最優先とし、関係機関と連携して対応")
    if "未受診" in difficulty_keywords:
        plan_parts.append("・かかりつけ医への受診勧奨と医療機関との連携")
    
    # 支援キーワードに基づく具体的支援
    plan_parts.append("\n【具体的支援内容】")
    for keyword in support_keywords[:5]:
        plan_parts.append(f"・{keyword}")
    
    return "\n".join(plan_parts)


def generate_support_process(support_keywords: List[str], months: int) -> str:
    """支援経過を生成"""
    process_parts = []
    
    process_parts.append(f"【支援経過】約{months}ヶ月間の支援を実施。")
    
    # 初期
    process_parts.append("\n＜初期（1-2ヶ月目）＞")
    initial_actions = [
        "初回訪問にて本人・家族と面談し、状況を詳細に把握。",
        "アセスメントを実施し、支援計画を策定。",
        "関係機関との情報共有を行い、支援体制を構築。"
    ]
    process_parts.extend(initial_actions)
    
    # 中期
    if months > 2:
        process_parts.append("\n＜中期（3-4ヶ月目）＞")
        if "デイサービス導入" in support_keywords:
            process_parts.append("デイサービスの体験利用を開始。当初は拒否的だったが、徐々に慣れてきた。")
        if "訪問介護導入" in support_keywords:
            process_parts.append("訪問介護を導入し、生活支援を開始。")
        if "医療機関受診" in support_keywords:
            process_parts.append("かかりつけ医への定期受診を開始。認知症の薬物療法を開始。")
        if "家族会紹介" in support_keywords:
            process_parts.append("家族を介護者の会に紹介。同じ立場の方との交流で精神的な支えを得られた。")
    
    # 後期
    if months > 4:
        process_parts.append("\n＜後期（5ヶ月目以降）＞")
        process_parts.append("支援体制が安定し、定期的なモニタリングを継続。")
        process_parts.append("サービス担当者会議を開催し、支援内容の見直しを実施。")
    
    return "\n".join(process_parts)


def generate_outcome(outcome: str, support_keywords: List[str]) -> str:
    """支援結果を生成"""
    outcome_parts = []
    
    outcome_parts.append(f"【支援結果】{outcome}")
    
    # 結果の詳細
    if outcome == "在宅生活継続":
        outcome_parts.append("介護サービスと地域の見守りにより、住み慣れた自宅での生活を継続できている。")
    elif outcome == "介護サービス導入により安定":
        outcome_parts.append("適切な介護サービスの導入により、本人の状態が安定し、介護者の負担も軽減された。")
    elif "入所" in outcome:
        outcome_parts.append("在宅生活の継続が困難となり、本人・家族と相談の上、施設入所となった。")
    elif "入院" in outcome:
        outcome_parts.append("症状の悪化により入院加療が必要となった。退院後の支援体制について検討中。")
    
    # 今後の課題
    outcome_parts.append("\n【今後の課題】")
    outcome_parts.append("・定期的なモニタリングの継続")
    outcome_parts.append("・状態変化時の迅速な対応体制の維持")
    if "介護者支援" in support_keywords:
        outcome_parts.append("・介護者の健康管理と負担軽減の継続")
    
    return "\n".join(outcome_parts)


def generate_case(case_id: int) -> Dict[str, Any]:
    """1件の事例を生成"""
    
    # 基本属性の決定
    age_range = random.choice(AGE_RANGES)
    age = random.randint(age_range[0], age_range[1])
    gender = random.choice(GENDERS)
    living_situation = random.choice(LIVING_SITUATIONS)
    dementia_type = random.choice(DEMENTIA_TYPES)
    
    # 困難キーワードの選択（1-4個）
    num_difficulties = random.randint(1, 4)
    difficulty_keywords = random.sample(DIFFICULTY_KEYWORDS, num_difficulties)
    
    # 世帯状況に応じた困難キーワードの調整
    if living_situation == "独居":
        if "独居" not in difficulty_keywords:
            difficulty_keywords.append("独居")
    if "配偶者" in living_situation and random.random() > 0.5:
        if "老老介護" not in difficulty_keywords:
            difficulty_keywords.append("老老介護")
    
    # 支援キーワードの選択（2-6個）
    num_supports = random.randint(2, 6)
    support_keywords = random.sample(SUPPORT_KEYWORDS, num_supports)
    
    # 身体疾患の選択（1-3個）
    num_conditions = random.randint(1, 3)
    physical_conditions = random.sample(PHYSICAL_CONDITIONS, num_conditions)
    
    # BPSDの選択（0-4個）
    num_bpsd = random.randint(0, 4)
    bpsd = random.sample(BPSD_SYMPTOMS, num_bpsd) if num_bpsd > 0 else []
    
    # 各種レベルの決定
    dementia_adl = random.choice(DEMENTIA_ADL_LEVELS)
    disability_adl = random.choice(DISABILITY_ADL_LEVELS)
    care_level = random.choice(CARE_LEVELS)
    
    # 相談経緯
    referral = random.choice(REFERRAL_SOURCES)
    
    # 支援期間（1-12ヶ月）
    support_months = random.randint(1, 12)
    
    # 支援結果
    outcome = random.choice(SUPPORT_OUTCOMES)
    
    # テキストの生成
    background = generate_background(age, gender, living_situation, dementia_type, physical_conditions)
    initial_situation = generate_initial_situation(difficulty_keywords, bpsd, living_situation, referral)
    assessment = generate_assessment(dementia_adl, disability_adl, care_level, bpsd)
    support_plan = generate_support_plan(support_keywords, difficulty_keywords)
    support_process = generate_support_process(support_keywords, support_months)
    outcome_text = generate_outcome(outcome, support_keywords)
    
    # 全体テキストの組み立て
    full_text = f"""【事例{case_id}】

【対象者の背景】
{background}

{initial_situation}

{assessment}

{support_plan}

{support_process}

{outcome_text}
"""
    
    # 支援方針の要約
    policy_summary = f"{', '.join(difficulty_keywords)}の課題に対し、{', '.join(support_keywords[:3])}等の支援を実施。{outcome}。"
    
    return {
        "id": f"synthetic_case_{case_id:05d}",
        "source": "合成データ",
        "text": full_text,
        "difficulty_keywords": difficulty_keywords,
        "support_keywords": support_keywords,
        "policy": policy_summary,
        "metadata": {
            "age": age,
            "gender": gender,
            "living_situation": living_situation,
            "dementia_type": dementia_type,
            "care_level": care_level,
            "dementia_adl": dementia_adl,
            "disability_adl": disability_adl,
            "support_months": support_months,
            "outcome": outcome
        }
    }


def generate_all_cases(num_cases: int = 5000) -> Dict[str, Any]:
    """指定件数の事例を生成"""
    print(f"Generating {num_cases} synthetic cases...")
    
    cases = []
    for i in range(1, num_cases + 1):
        case = generate_case(i)
        cases.append(case)
        
        if i % 500 == 0:
            print(f"  Generated {i} cases...")
    
    result = {
        "extracted_at": datetime.now().isoformat(),
        "total_cases": num_cases,
        "sources": ["合成データ"],
        "generation_method": "ルールベース合成データ生成",
        "cases": cases
    }
    
    print(f"Done! Generated {num_cases} cases.")
    return result


def main():
    """メイン関数"""
    # 5000件の事例を生成
    data = generate_all_cases(5000)
    
    # JSONファイルに保存
    output_path = "data/case_studies/cases.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved to {output_path}")
    
    # 統計情報の表示
    print("\n=== Statistics ===")
    print(f"Total cases: {data['total_cases']}")
    
    # 困難キーワードの分布
    difficulty_counts = {}
    for case in data["cases"]:
        for kw in case["difficulty_keywords"]:
            difficulty_counts[kw] = difficulty_counts.get(kw, 0) + 1
    
    print("\nTop 10 difficulty keywords:")
    for kw, count in sorted(difficulty_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {kw}: {count}")
    
    # 支援キーワードの分布
    support_counts = {}
    for case in data["cases"]:
        for kw in case["support_keywords"]:
            support_counts[kw] = support_counts.get(kw, 0) + 1
    
    print("\nTop 10 support keywords:")
    for kw, count in sorted(support_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {kw}: {count}")


if __name__ == "__main__":
    main()
