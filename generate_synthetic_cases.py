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


def generate_visit_fields(age: int, gender: str, living_situation: str, 
                          dementia_type: str, dementia_adl: str, disability_adl: str,
                          difficulty_keywords: List[str], support_keywords: List[str],
                          bpsd: List[str], physical_conditions: List[str],
                          outcome: str) -> Dict[str, str]:
    """訪問記録表の7つのフィールドを個別に生成
    
    訪問記録表のフィールド:
    - vr_reaction (訪問に対する本人の反応・理解)
    - vr_cognition (認知機能・認知症日常生活自立度)
    - vr_behavior (精神症状・行動症状)
    - vr_physical (身体状況・障害高齢者の日常生活自立度)
    - vr_living (生活状況)
    - vr_person_intent (本人の意向・希望)
    - vr_family_intent (介護者の意向・希望)
    - support_decision (支援方針)
    
    Returns:
        Dict with individual field values and concatenated visit_like_text
    """
    
    # 反応・理解 - test_data.sqlの実際の表現を参考に多様なテンプレート
    reaction_templates_base = [
        "訪問を快く受け入れ、笑顔で対応された。会話も楽しそうにされ、昔の話を詳しく語られた。ただし、同じ話を繰り返す場面が見られた。",
        "初めは警戒した様子で「どなたですか」と繰り返し尋ねられた。家族が説明すると徐々に打ち解け、お茶を出してくださった。",
        "にこやかに対応。「お客さんが来てくれて嬉しい」と歓迎された。",
        "訪問者を認識できず、不安そうな表情を見せた。家族の説明で落ち着いた。",
        "穏やかに対応。自分の病気について「仕方ない」と受け入れている様子。ただし、時々涙ぐむ場面あり。",
        "穏やかに対応されたが、「家に帰りたい」と繰り返し訴えられた。ここが自宅であることを説明しても理解されない。",
        "本人は車椅子で対応。言葉は出にくいが、うなずきで意思表示。",
        "退院直後で疲労の様子。ベッドで横になりながら対応。",
        "穏やかに対応。「薬はちゃんと飲んでいる」と言うが、実際は飲み忘れや重複服用がある。",
        "穏やかに対応。家族の話し合いには参加せず、テレビを見ていた。",
        "穏やかに対応。「息子が来てくれないから寂しい」と訴え。",
        "二人とも穏やかに対応。ただし、訪問の目的を何度も尋ねられた。",
        "無表情で対応。質問に対して短い返答のみ。家族が代わりに説明。"
    ]
    
    reaction_templates_negative = [
        "訪問を強く拒否。「何しに来た」「帰れ」と怒鳴られた。家族の説得で玄関先での短時間の対応となった。",
        "「何しに来た」と警戒的な態度。時間をかけて説明し、徐々に受け入れてくれた。",
        "ドア越しの対応。「用はない」「帰ってくれ」と拒否的。粘り強く説明し、玄関先で短時間話を聞けた。",
        "最初は警戒していたが、民生委員の紹介と伝えると態度が軟化。ただし、医療の話になると拒否的。",
        "おびえた様子。家族の顔色をうかがいながら話す。"
    ]
    
    if "支援拒否" in difficulty_keywords:
        reaction = random.choice(reaction_templates_negative)
    elif "虐待疑い" in difficulty_keywords:
        reaction = "おびえた様子。家族の顔色をうかがいながら話す。家族は「転んだだけ」と説明。"
    else:
        reaction = random.choice(reaction_templates_base)
    
    # 認知機能 - 認知症タイプと自立度に応じた詳細な記述
    cognition_parts = []
    
    # 認知症タイプ別の記述
    if dementia_type == "レビー小体型認知症":
        cognition_parts.append(f"レビー小体型認知症。認知機能の変動あり。調子の良い時と悪い時の差が大きい。")
    elif dementia_type == "前頭側頭型認知症":
        cognition_parts.append(f"前頭側頭型認知症。社会的認知の低下が顕著。善悪の判断が困難。")
    elif dementia_type == "血管性認知症":
        cognition_parts.append(f"脳梗塞後遺症による血管性認知症。言語障害あり。理解力は比較的保たれている。")
    elif dementia_type == "軽度認知障害（MCI）":
        cognition_parts.append(f"軽度認知障害（MCI）の疑い。物忘れが目立つが、日常生活は概ね自立。")
    else:
        # アルツハイマー型・混合型
        if dementia_adl in ["I", "IIa"]:
            cognition_parts.append(f"軽度の認知機能低下。短期記憶の低下が顕著。5分前の話を覚えていない。長期記憶は比較的保たれており、昔の仕事の話は詳細に語れる。見当識は日付の認識に曖昧さあり。")
        elif dementia_adl in ["IIb", "IIIa"]:
            cognition_parts.append(f"中等度の認知機能低下。自分の年齢や生年月日が言えない。季節の認識も曖昧。訪問者の顔は覚えられない。")
        elif dementia_adl in ["IIIb", "IV", "M"]:
            cognition_parts.append(f"中等度～重度の認知機能低下。見当識障害が顕著。自宅を実家と混同している。家族の顔も認識できないことがある。")
        else:
            cognition_parts.append(f"認知機能は比較的保たれている。日常生活は概ね自立しているが、複雑な判断は困難。")
    
    # 認知症日常生活自立度を追加
    cognition_parts.append(f"認知症日常生活自立度：{dementia_adl}。")
    
    # 特定の症状に応じた追加記述
    if "幻覚・妄想" in difficulty_keywords:
        if dementia_type == "レビー小体型認知症":
            cognition_parts.append("幻視が頻繁にある。「知らない人が家にいる」と訴える。")
        else:
            cognition_parts.append("物盗られ妄想が顕著。「財布を盗まれた」と頻繁に訴える。")
    if "徘徊" in difficulty_keywords:
        cognition_parts.append("夜中に起き出して「仕事に行かなきゃ」と言うことがある。昼夜逆転傾向。")
    if "若年性認知症" in difficulty_keywords:
        cognition_parts.append("若年性アルツハイマー型認知症。記憶障害が進行中。仕事でのミスが増え、退職を余儀なくされた。")
    
    cognition = " ".join(cognition_parts)
    
    # 行動・心理症状 - BPSDに応じた詳細な記述
    behavior_parts = []
    
    if "前頭側頭型認知症" in difficulty_keywords or dementia_type == "前頭側頭型認知症":
        behavior_parts.append("脱抑制行動あり。スーパーで商品を無断で持ち出し、警察沙汰に。本人は悪いことをした認識がない。")
    elif "徘徊" in difficulty_keywords:
        behavior_parts.append("夕方になると外出しようとする（夕暮れ症候群）。警察に保護されたこともある。帰宅願望が強い。")
    elif "幻覚・妄想" in difficulty_keywords:
        if dementia_type == "レビー小体型認知症":
            behavior_parts.append("幻視が頻繁にある。「知らない人が家にいる」と訴える。パーキンソン症状あり。")
        else:
            behavior_parts.append("物盗られ妄想が顕著。家族を泥棒扱いすることがある。興奮すると大声を出す。")
    elif "易怒性・興奮" in difficulty_keywords or "暴力・暴言" in difficulty_keywords:
        behavior_parts.append("些細なことで怒りっぽくなり、家族に暴言を吐くことがある。興奮時の対応が困難。")
    elif "支援拒否" in difficulty_keywords:
        behavior_parts.append("介護サービスの利用を拒否。「自分でできる」と主張。支援の必要性を感じていない様子。")
    elif "セルフネグレクト・ごみ屋敷" in difficulty_keywords:
        behavior_parts.append("セルフネグレクト状態。入浴していない様子。衣類も汚れている。")
    elif bpsd:
        bpsd_details = []
        for symptom in bpsd[:3]:
            if symptom == "夜間不穏":
                bpsd_details.append("夜間の不穏あり")
            elif symptom == "昼夜逆転":
                bpsd_details.append("昼夜逆転傾向")
            elif symptom == "介護抵抗":
                bpsd_details.append("介護への抵抗あり")
            elif symptom == "抑うつ":
                bpsd_details.append("抑うつ傾向が心配。「自分は役立たずだ」という発言あり")
            elif symptom == "帰宅願望":
                bpsd_details.append("「家に帰りたい」と繰り返し訴える")
            else:
                bpsd_details.append(f"{symptom}あり")
        behavior_parts.append(f"{', '.join(bpsd_details)}。")
    else:
        behavior_parts.append("特に問題行動は見られない。穏やかな性格で、近隣との関係も良好。")
    
    # 老老介護の場合の追加
    if "老老介護" in difficulty_keywords:
        behavior_parts.append("夜間の頻尿あり。配偶者が毎晩2-3回起きて対応。")
    
    behavior = " ".join(behavior_parts)
    
    # 身体状況 - 障害高齢者の日常生活自立度と身体疾患
    physical_parts = []
    
    # 身体疾患の記述
    if physical_conditions:
        condition_details = []
        for cond in physical_conditions:
            if cond == "パーキンソン病":
                condition_details.append("パーキンソン病を合併。小刻み歩行、すくみ足あり。転倒リスク高い")
            elif cond == "脳梗塞後遺症":
                condition_details.append("脳梗塞後遺症。右片麻痺あり")
            elif cond == "大腿骨骨折術後":
                condition_details.append("大腿骨骨折術後。リハビリ中")
            elif cond == "心疾患":
                condition_details.append("心疾患があり、興奮時の血圧上昇が心配")
            elif cond == "慢性腎臓病":
                condition_details.append("慢性腎臓病あり。週3回の透析が必要")
            else:
                condition_details.append(f"{cond}あり")
        physical_parts.append(f"{', '.join(condition_details)}。")
    
    # 障害高齢者の日常生活自立度に応じた記述
    if disability_adl in ["J1", "J2"]:
        physical_parts.append(f"障害高齢者の日常生活自立度：{disability_adl}。歩行は自立。基本的なADLは自立。")
    elif disability_adl in ["A1", "A2"]:
        if "骨粗鬆症" in physical_conditions:
            physical_parts.append(f"障害高齢者の日常生活自立度：{disability_adl}。骨粗鬆症のため転倒リスクあり。歩行は自立しているが、やや不安定。")
        else:
            physical_parts.append(f"障害高齢者の日常生活自立度：{disability_adl}。歩行は自立しているが、腰痛あり。買い物は近所のスーパーまで徒歩で行ける。")
    elif disability_adl in ["B1", "B2"]:
        physical_parts.append(f"障害高齢者の日常生活自立度：{disability_adl}。車椅子使用。移乗には介助が必要。屋内での生活は概ね自立だが、外出には介助が必要。")
    elif disability_adl in ["C1", "C2"]:
        physical_parts.append(f"障害高齢者の日常生活自立度：{disability_adl}。ベッド上での生活が中心。全介助が必要。嚥下機能低下あり。")
    else:
        physical_parts.append(f"身体機能は年齢相応。歩行も安定している。")
    
    # セルフネグレクトの場合
    if "セルフネグレクト・ごみ屋敷" in difficulty_keywords:
        physical_parts.append("栄養状態不良の疑い。痩せている。医療機関未受診のため詳細不明。")
    
    physical = " ".join(physical_parts)
    
    # 生活状況 - 世帯状況と困難キーワードに応じた詳細
    living_parts = []
    
    # 世帯状況の詳細
    if living_situation == "独居":
        living_parts.append("独居。")
        if "セルフネグレクト・ごみ屋敷" in difficulty_keywords:
            living_parts.append("室内はゴミが堆積し、悪臭あり。近隣から苦情が出ている。電気・ガスは通っているが、水道が止まりかけている。")
        elif "金銭管理困難" in difficulty_keywords:
            living_parts.append("基本的なADLは自立。買い物は近所のスーパーで可能。ただし、金銭管理ができていない。")
        else:
            living_parts.append("基本的なADLは自立。買い物は近所のスーパーまで徒歩で行ける。調理は簡単なものは可能だが、最近は惣菜を購入することが増えた。")
    elif "配偶者と二人暮らし" in living_situation:
        living_parts.append("配偶者と二人暮らし。")
        if "老老介護" in difficulty_keywords:
            living_parts.append("家事は配偶者が全て担当。本人は日中テレビを見て過ごすことが多い。入浴は配偶者の介助が必要。")
        elif "認認介護" in difficulty_keywords:
            living_parts.append("夫婦ともに認知機能の低下あり。お互いの状況を正確に把握できていない。食事は惣菜や弁当が中心。")
        else:
            living_parts.append("日中は比較的穏やかに過ごしている。")
    elif "子ども家族と同居" in living_situation:
        living_parts.append("子ども家族と同居。")
        if "日中独居" in difficulty_keywords:
            living_parts.append("日中は家族が仕事で不在。一人で昼食を作ろうとして火の不始末が発生することがある。")
        else:
            living_parts.append("家族が主介護者。")
    else:
        living_parts.append(f"{living_situation}。")
    
    # 追加の生活状況
    if "火の不始末" in difficulty_keywords:
        living_parts.append("ガスコンロの消し忘れが複数回あり。鍋を焦がしたことも。本人は覚えていない。")
    if "服薬管理困難" in difficulty_keywords:
        living_parts.append("薬の飲み忘れや重複服用があり、血糖コントロールが悪化。最近、低血糖発作があった。")
    if "遠距離介護" in difficulty_keywords:
        living_parts.append("子どもは遠方在住で月1回程度訪問。近所付き合いは少ない。")
    
    living = " ".join(living_parts)
    
    # 本人の意向 - 困難状況に応じた多様なテンプレート
    person_intent_templates_base = [
        "今の生活を続けたい。施設には入りたくない。家族には迷惑をかけたくない。",
        "「このまま家で暮らしたい」と希望。施設入所には消極的。",
        "「家族に迷惑をかけたくない」と話す。サービス利用には前向き。",
        "配偶者と一緒にいたい。家にいたい。",
        "早く元気になりたい。歩けるようになりたい。",
        "何か役に立つことがしたい。社会とのつながりを持ちたい。",
        "子どもの近くに住みたいが、迷惑をかけたくない。ここで頑張る。"
    ]
    
    person_intent_templates_negative = [
        "何も困っていない。余計なお世話だ。",
        "「自分のことは自分でできる」と主張。支援の必要性を感じていない様子。",
        "一人で大丈夫。放っておいてくれ。",
        "病院は嫌い。薬を飲むと体に悪い。自然に治る。",
        "良いものを買っただけ。騙されてなんかいない。"
    ]
    
    person_intent_templates_passive = [
        "「どうなってもいい」と投げやりな発言。意欲の低下が見られる。",
        "（言葉で表現困難だが、自宅にいたい様子）",
        "（自分の意見を明確に表現できない状態）",
        "（自分の行動の問題を認識できていない）"
    ]
    
    if "支援拒否" in difficulty_keywords or "未受診" in difficulty_keywords:
        person_intent = random.choice(person_intent_templates_negative)
    elif dementia_adl in ["IIIb", "IV", "M"] or "虐待疑い" in difficulty_keywords:
        person_intent = random.choice(person_intent_templates_passive)
    elif "徘徊" in difficulty_keywords:
        person_intent = "家に帰りたい（実家のことを指している）。お母さんに会いたい。"
    elif "幻覚・妄想" in difficulty_keywords:
        person_intent = "（幻視について）あの人たちは誰？怖くはないけど気になる。"
    else:
        person_intent = random.choice(person_intent_templates_base)
    
    # 家族の意向 - 介護状況に応じた多様なテンプレート
    family_intent_templates_home = [
        "できるだけ自宅で生活させたい。週1回は様子を見に来ている。何かあったらすぐ連絡してほしい。",
        "「できるだけ在宅で」と希望。介護サービスの利用を検討中。",
        "「本人の意思を尊重したい」と話す。サービス導入に協力的。",
        "本人の気持ちを大切にしたい。働ける場所があれば働かせてあげたい。経済的な不安もある。"
    ]
    
    family_intent_templates_burden = [
        "できる限り自宅で介護したいが、自分も腰が痛くて限界を感じている。デイサービスを利用させたい。",
        "「介護が大変」と疲弊している様子。レスパイトケアを希望。",
        "限界を感じている。夜眠れない。自分が倒れたらどうなるか不安。でも施設には入れたくない。",
        "本人の妄想に疲弊している。どこかに相談したかったが、本人が拒否するので困っていた。薬で落ち着かせてほしい。",
        "本人の行動に振り回されている。外出するたびにヒヤヒヤする。でも施設は嫌がる。"
    ]
    
    family_intent_templates_facility = [
        "「施設入所も視野に」と話す。在宅介護の限界を感じている。",
        "仕事があるので日中は見られない。GPSを持たせているが、外すことがある。施設入所も考えている。",
        "入院中に急に認知症が進んでショック。でも自宅で看たい。リハビリを頑張ってほしい。"
    ]
    
    family_intent_templates_distant = [
        "遠方に住んでおり、頻繁な訪問は困難。見守りサービスを希望。",
        "親のことが心配だが、仕事があり頻繁には来られない。サービスを利用してほしい。",
        "遠方（県外）に在住。年に1回程度しか会えない。できることがあれば協力したい。",
        "本人のことは心配だが、仕事があり頻繁には帰れない。サービスを利用してほしい。電話は毎日している。"
    ]
    
    family_intent_templates_conflict = [
        "長女：父を施設に入れたくない。私が看る。 長男：姉の負担が心配。施設の方が安心。",
        "母が高額な買い物をしていて困っている。通帳を預かりたいが、母が拒否する。",
        "幻視への対応に困っている。否定すると怒るし、肯定するのも良くないと聞いた。どうすればいいか。",
        "薬の管理が心配。毎日は来られないので、何か良い方法はないか。",
        "火事が心配。IHに変えたいが、本人が使い方を覚えられるか不安。デイサービスで昼食を食べてほしい。"
    ]
    
    if "遠距離介護" in difficulty_keywords:
        family_intent = random.choice(family_intent_templates_distant)
    elif "家族間の意見相違" in difficulty_keywords:
        family_intent = random.choice(family_intent_templates_conflict)
    elif "介護者の負担" in difficulty_keywords or "老老介護" in difficulty_keywords:
        family_intent = random.choice(family_intent_templates_burden)
    elif "幻覚・妄想" in difficulty_keywords:
        family_intent = "幻視への対応に困っている。否定すると怒るし、肯定するのも良くないと聞いた。どうすればいいか。"
    elif "金銭管理困難" in difficulty_keywords:
        family_intent = "本人が高額な買い物をしていて困っている。通帳を預かりたいが、本人が拒否する。"
    elif "服薬管理困難" in difficulty_keywords:
        family_intent = "薬の管理が心配。毎日は来られないので、何か良い方法はないか。"
    elif "火の不始末" in difficulty_keywords:
        family_intent = "火事が心配。IHに変えたいが、本人が使い方を覚えられるか不安。デイサービスで昼食を食べてほしい。"
    elif "虐待疑い" in difficulty_keywords:
        family_intent = "本人の世話は自分がしている。余計なお世話だ。"
    elif living_situation == "独居":
        family_intent = random.choice(family_intent_templates_distant)
    else:
        family_intent = random.choice(family_intent_templates_home + family_intent_templates_burden)
    
    # 支援方針 - 困難状況に応じた具体的な支援方針
    support_parts = []
    
    # 困難状況に応じた支援方針
    if "支援拒否" in difficulty_keywords:
        support_parts.append("支援拒否ケース。まずは信頼関係構築を優先し、段階的な支援導入を目指す。")
    elif "虐待疑い" in difficulty_keywords:
        support_parts.append("虐待対応。本人の安全確保を最優先。関係機関との連携が必要。")
    elif "セルフネグレクト・ごみ屋敷" in difficulty_keywords:
        support_parts.append("セルフネグレクトの緊急ケース。関係機関と連携し、介入を継続。")
    elif "老老介護" in difficulty_keywords:
        support_parts.append("老老介護の典型的なケース。介護者支援と本人へのサービス導入が急務。")
    elif "認認介護" in difficulty_keywords:
        support_parts.append("認認介護の典型的なケース。夫婦への包括的支援が必要。服薬管理サービスと配食サービスの導入を優先。")
    elif "徘徊" in difficulty_keywords:
        support_parts.append("徘徊対策と家族支援が必要。デイサービスの増回と見守りサービスの導入を検討。")
    elif "幻覚・妄想" in difficulty_keywords:
        support_parts.append("専門医との連携を強化。幻視への対応方法を家族に指導。")
    elif "金銭管理困難" in difficulty_keywords:
        support_parts.append("金銭管理支援と消費者被害防止が必要。日常生活自立支援事業の利用を検討。")
    elif "服薬管理困難" in difficulty_keywords:
        support_parts.append("服薬管理支援が最優先。訪問薬剤管理指導と見守りサービスの導入。")
    elif "火の不始末" in difficulty_keywords:
        support_parts.append("火災予防と日中の見守り体制構築が必要。")
    elif "介護者の負担" in difficulty_keywords:
        support_parts.append("介護者支援が最優先。レスパイトケアの充実と介護者の健康管理が必要。")
    elif "遠距離介護" in difficulty_keywords:
        support_parts.append("社会的孤立の防止と見守り体制の強化。")
    elif "若年性認知症" in difficulty_keywords:
        support_parts.append("若年性認知症の専門的支援が必要。本人の意欲を活かした支援計画を立てる。")
    elif "前頭側頭型認知症" in difficulty_keywords:
        support_parts.append("専門医との連携強化。行動障害への対応と家族の支援が必要。")
    else:
        support_parts.append(f"{', '.join(difficulty_keywords[:2])}の課題に対応。")
    
    # 具体的な支援内容
    support_parts.append(f"{', '.join(support_keywords[:3])}等の支援を検討。")
    support_parts.append(f"目標: {outcome}")
    
    support_decision = " ".join(support_parts)
    
    # 訪問記録表と同じ形式でテキストを結合（ヘッダーなし、スペース区切り）
    visit_like_text = " ".join([
        reaction,
        cognition,
        behavior,
        physical,
        living,
        person_intent,
        family_intent,
        support_decision
    ])
    
    return {
        "vr_reaction": reaction,
        "vr_cognition": cognition,
        "vr_behavior": behavior,
        "vr_physical": physical,
        "vr_living": living,
        "vr_person_intent": person_intent,
        "vr_family_intent": family_intent,
        "support_decision": support_decision,
        "visit_like_text": visit_like_text
    }


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
    
    # 訪問記録表の7つのフィールドを個別に生成（TF-IDF用）
    visit_fields = generate_visit_fields(
        age, gender, living_situation, dementia_type, dementia_adl, disability_adl,
        difficulty_keywords, support_keywords, bpsd, physical_conditions, outcome
    )
    
    # 全体テキストの組み立て（表示用）
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
        "visit_like_text": visit_fields["visit_like_text"],  # TF-IDF用の訪問記録表形式テキスト
        "vr_reaction": visit_fields["vr_reaction"],  # 訪問に対する本人の反応・理解
        "vr_cognition": visit_fields["vr_cognition"],  # 認知機能・認知症日常生活自立度
        "vr_behavior": visit_fields["vr_behavior"],  # 精神症状・行動症状
        "vr_physical": visit_fields["vr_physical"],  # 身体状況・障害高齢者の日常生活自立度
        "vr_living": visit_fields["vr_living"],  # 生活状況
        "vr_person_intent": visit_fields["vr_person_intent"],  # 本人の意向・希望
        "vr_family_intent": visit_fields["vr_family_intent"],  # 介護者の意向・希望
        "support_decision": visit_fields["support_decision"],  # 支援方針
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
