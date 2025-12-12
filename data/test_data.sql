-- テスト用対象者データ（20ケース）
-- 認知症初期集中支援チームのテスト用データ

-- クライアント1: 独居高齢者、軽度認知症
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (101, '山田 太郎', 'ヤマダ タロウ', '1940-03-15', '男', '茅ヶ崎市東海岸北1-1-1', '0467-11-1111', '山田 花子（長女）', '090-1111-1111', '茅ヶ崎中央病院 田中医師', '高血圧、糖尿病', '要支援1', '独居。物忘れが増えてきた。');

-- クライアント2: 老老介護、中等度認知症
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (102, '佐藤 花子', 'サトウ ハナコ', '1938-07-22', '女', '茅ヶ崎市浜竹2-2-2', '0467-22-2222', '佐藤 一郎（夫）', '0467-22-2222', '湘南病院 鈴木医師', '骨粗鬆症、白内障', '要介護1', '夫と二人暮らし。夫も高齢で介護負担大。');

-- クライアント3: 支援拒否、妄想あり
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (103, '鈴木 一郎', 'スズキ イチロウ', '1942-11-08', '男', '茅ヶ崎市松が丘3-3-3', '0467-33-3333', '鈴木 美智子（妻）', '0467-33-3333', '茅ヶ崎市立病院 山本医師', '心疾患', '未申請', '物盗られ妄想あり。介護サービス拒否。');

-- クライアント4: 若年性認知症
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (104, '高橋 健二', 'タカハシ ケンジ', '1965-04-12', '男', '茅ヶ崎市円蔵4-4-4', '0467-44-4444', '高橋 由美（妻）', '090-4444-4444', '神奈川県立病院 佐々木医師', '特になし', '要介護2', '58歳で若年性アルツハイマー型認知症と診断。');

-- クライアント5: 徘徊あり
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (105, '伊藤 幸子', 'イトウ サチコ', '1936-09-30', '女', '茅ヶ崎市香川5-5-5', '0467-55-5555', '伊藤 正男（長男）', '090-5555-5555', '茅ヶ崎中央病院 中村医師', '高血圧、変形性膝関節症', '要介護2', '夕方になると外出しようとする。徘徊の既往あり。');

-- クライアント6: セルフネグレクト
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (106, '渡辺 正夫', 'ワタナベ マサオ', '1939-01-25', '男', '茅ヶ崎市萩園6-6-6', '0467-66-6666', '渡辺 明美（姪）', '090-6666-6666', '未受診', '不明', '未申請', '独居。ゴミ屋敷状態。近隣から苦情あり。');

-- クライアント7: 認認介護
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (107, '中村 美代子', 'ナカムラ ミヨコ', '1941-06-18', '女', '茅ヶ崎市下町屋7-7-7', '0467-77-7777', '中村 健一（長男）', '090-7777-7777', '湘南病院 高橋医師', '糖尿病、高血圧', '要介護1', '夫も認知症。二人とも服薬管理ができていない。');

-- クライアント8: 介護者の負担大
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (108, '小林 勝', 'コバヤシ マサル', '1937-12-05', '男', '茅ヶ崎市浜之郷8-8-8', '0467-88-8888', '小林 恵子（妻）', '0467-88-8888', '茅ヶ崎市立病院 伊藤医師', '脳梗塞後遺症、高血圧', '要介護3', '妻が介護。妻の疲労が著しい。');

-- クライアント9: 金銭管理困難
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (109, '加藤 静江', 'カトウ シズエ', '1943-08-14', '女', '茅ヶ崎市赤羽根9-9-9', '0467-99-9999', '加藤 誠（長男）', '090-9999-9999', '茅ヶ崎中央病院 渡辺医師', '骨粗鬆症', '要支援2', '独居。訪問販売で高額商品を購入してしまう。');

-- クライアント10: 幻覚・妄想
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (110, '吉田 武', 'ヨシダ タケシ', '1940-02-28', '男', '茅ヶ崎市小和田10-10-10', '0467-10-1010', '吉田 和子（妻）', '0467-10-1010', '神奈川県立病院 小林医師', 'パーキンソン病', '要介護2', 'レビー小体型認知症。幻視あり。');

-- クライアント11: 独居・未受診
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (111, '松本 節子', 'マツモト セツコ', '1944-05-20', '女', '茅ヶ崎市今宿11-11-11', '0467-11-1112', '松本 健太（甥）', '090-1111-1112', '未受診', '高血圧（自己申告）', '未申請', '独居。認知症の疑いあるが受診拒否。');

-- クライアント12: 入院後の在宅復帰
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (112, '井上 正雄', 'イノウエ マサオ', '1939-10-10', '男', '茅ヶ崎市矢畑12-12-12', '0467-12-1212', '井上 美智子（妻）', '0467-12-1212', '茅ヶ崎市立病院 加藤医師', '大腿骨骨折術後、高血圧', '要介護2', '入院中に認知機能低下。在宅復帰に向けた支援が必要。');

-- クライアント13: 服薬管理困難
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (113, '木村 トメ', 'キムラ トメ', '1935-03-03', '女', '茅ヶ崎市堤13-13-13', '0467-13-1313', '木村 太郎（長男）', '090-1313-1313', '湘南病院 井上医師', '糖尿病、高血圧、心不全', '要介護1', '独居。薬の飲み忘れ・重複服用あり。');

-- クライアント14: 家族間の意見相違
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (114, '斎藤 清', 'サイトウ キヨシ', '1941-07-07', '男', '茅ヶ崎市室田14-14-14', '0467-14-1414', '斎藤 幸子（長女）', '090-1414-1414', '茅ヶ崎中央病院 木村医師', '慢性腎臓病', '要介護1', '長男と長女で介護方針が異なる。施設入所の是非で対立。');

-- クライアント15: 日中独居
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (115, '山本 ミツ', 'ヤマモト ミツ', '1942-04-15', '女', '茅ヶ崎市西久保15-15-15', '0467-15-1515', '山本 健一（長男）', '090-1515-1515', '茅ヶ崎市立病院 斎藤医師', '変形性腰椎症', '要支援2', '長男夫婦と同居だが日中は独居。火の不始末あり。');

-- クライアント16: 前頭側頭型認知症
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (116, '田中 義男', 'タナカ ヨシオ', '1955-11-11', '男', '茅ヶ崎市柳島16-16-16', '0467-16-1616', '田中 美恵子（妻）', '0467-16-1616', '神奈川県立病院 山本医師', '特になし', '要介護2', '前頭側頭型認知症。脱抑制行動あり。万引きで警察沙汰に。');

-- クライアント17: 遠距離介護
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (117, '藤田 ハル', 'フジタ ハル', '1938-08-08', '女', '茅ヶ崎市南湖17-17-17', '0467-17-1717', '藤田 正（長男・東京在住）', '090-1717-1717', '湘南病院 田中医師', '高血圧、白内障術後', '要支援1', '独居。長男は東京在住で月1回しか来られない。');

-- クライアント18: 虐待疑い
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (118, '清水 キヨ', 'シミズ キヨ', '1936-02-14', '女', '茅ヶ崎市中海岸18-18-18', '0467-18-1818', '清水 勝（長男）', '0467-18-1818', '茅ヶ崎中央病院 藤田医師', '骨粗鬆症、圧迫骨折', '要介護2', '長男と同居。あざが見られる。経済的虐待の疑いも。');

-- クライアント19: アルコール問題
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (119, '後藤 三郎', 'ゴトウ サブロウ', '1945-09-09', '男', '茅ヶ崎市菱沼19-19-19', '0467-19-1919', '後藤 洋子（妻）', '0467-19-1919', '茅ヶ崎市立病院 清水医師', 'アルコール性肝障害', '未申請', 'アルコール依存と認知症の合併。妻が疲弊。');

-- クライアント20: 多問題世帯
INSERT INTO client (client_id, name, furigana, birth_date, gender, address, phone, emergency_contact, emergency_phone, primary_doctor, medical_history, care_level, notes)
VALUES (120, '岡田 ヨシ', 'オカダ ヨシ', '1940-12-25', '女', '茅ヶ崎市共恵20-20-20', '0467-20-2020', '岡田 隆（長男）', '090-2020-2020', '未受診', '不明', '未申請', '独居。長男は精神疾患あり。経済的困窮。ライフライン停止の恐れ。');

-- =====================================================
-- 訪問記録データ（全20クライアント用・現場で使われる詳細な内容）
-- =====================================================

-- クライアント101: 独居高齢者、軽度認知症
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (101, '2025-01-15 10:00:00', '包括支援センター 佐藤', '初回訪問・状況確認', '在宅・本人のみ',
'訪問を快く受け入れ、笑顔で対応された。会話も楽しそうにされ、昔の話を詳しく語られた。ただし、同じ話を繰り返す場面が見られた。',
'短期記憶の低下が顕著。5分前の話を覚えていない。長期記憶は比較的保たれており、昔の仕事の話は詳細に語れる。見当識は日付の認識に曖昧さあり。',
'IIa',
'特に問題行動は見られない。穏やかな性格で、近隣との関係も良好。',
'歩行は自立。血圧管理のため降圧剤を服用中。糖尿病のコントロールは良好とのこと。',
'J1',
'独居だが基本的なADLは自立。買い物は近所のスーパーまで徒歩で行ける。調理は簡単なものは可能だが、最近は惣菜を購入することが増えた。',
'25', '5', '8',
'今の生活を続けたい。施設には入りたくない。娘には迷惑をかけたくない。',
'できるだけ自宅で生活させたい。週1回は様子を見に来ている。何かあったらすぐ連絡してほしい。',
'郵便物の管理ができていない様子。重要書類が未開封のまま放置されていた。',
'軽度認知症の疑い。かかりつけ医への受診勧奨と、介護予防サービスの利用検討が必要。',
'1.かかりつけ医に認知機能について相談するよう促す 2.地域の介護予防教室への参加を提案 3.見守りサービスの導入を検討 4.2週間後に再訪問し状況確認');

-- クライアント102: 老老介護、中等度認知症
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (102, '2025-01-16 14:00:00', '包括支援センター 田中', '定期訪問・介護者支援', '在宅・夫同席',
'初めは警戒した様子で「どなたですか」と繰り返し尋ねられた。夫が説明すると徐々に打ち解け、お茶を出してくださった。',
'中等度の認知機能低下。自分の年齢や生年月日が言えない。季節の認識も曖昧。夫の名前は認識できるが、訪問者の顔は覚えられない。',
'IIb',
'夜間の不穏あり。夜中に起き出して「仕事に行かなきゃ」と言うことがある。昼夜逆転傾向。',
'骨粗鬆症のため転倒リスクあり。白内障術後で視力は改善したが、段差の認識が難しい。',
'A1',
'夫と二人暮らし。家事は夫が全て担当。本人は日中テレビを見て過ごすことが多い。入浴は夫の介助が必要。',
'32', '12', '22',
'夫と一緒にいたい。家にいたい。',
'できる限り自宅で介護したいが、自分も腰が痛くて限界を感じている。デイサービスを利用させたい。',
'夫の介護負担が大きい。夫自身も高血圧で通院中。レスパイトケアの必要性あり。',
'老老介護の典型的なケース。介護者支援と本人へのサービス導入が急務。',
'1.デイサービスの体験利用を調整 2.夫の介護負担軽減のためショートステイの利用を提案 3.介護保険申請の支援 4.1週間後に再訪問');

-- クライアント103: 支援拒否、妄想あり
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (103, '2025-01-17 11:00:00', '包括支援センター 鈴木', '初回訪問・状況確認', '在宅・妻同席',
'訪問を強く拒否。「何しに来た」「帰れ」と怒鳴られた。妻の説得で玄関先での短時間の対応となった。',
'妻からの聞き取りによると、中等度の認知機能低下。最近の出来事を覚えていない。「財布を盗まれた」と頻繁に訴える。',
'IIb',
'物盗られ妄想が顕著。妻を泥棒扱いすることがある。興奮すると大声を出す。',
'心疾患があり、興奮時の血圧上昇が心配。歩行は自立しているが、やや不安定。',
'J2',
'妻と二人暮らし。室内は妻が整頓しており清潔。本人は一日中テレビを見ているか、財布を探している。',
'35', '18', '28',
'何も困っていない。余計なお世話だ。',
'夫の妄想に疲弊している。どこかに相談したかったが、夫が拒否するので困っていた。薬で落ち着かせてほしい。',
'妻の精神的負担が非常に大きい。妻自身のケアも必要。',
'支援拒否ケース。まずは妻への支援から開始し、信頼関係構築を優先。',
'1.妻への傾聴と精神的サポート 2.認知症疾患医療センターへの相談を提案 3.妻の了解を得て、短時間の訪問を継続 4.家族会の紹介');

-- クライアント104: 若年性認知症
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (104, '2025-01-18 13:00:00', '包括支援センター 高橋', '定期訪問・就労支援相談', '在宅・妻同席',
'穏やかに対応。自分の病気について「仕方ない」と受け入れている様子。ただし、時々涙ぐむ場面あり。',
'若年性アルツハイマー型認知症。58歳で発症。記憶障害が進行中。仕事でのミスが増え、退職を余儀なくされた。',
'IIa',
'特に問題行動なし。むしろ抑うつ傾向が心配。「自分は役立たずだ」という発言あり。',
'身体的には健康。運動習慣があり、毎朝散歩をしている。',
'J1',
'妻と二人暮らし。子どもは独立。退職後は自宅で過ごすことが多く、社会的孤立が心配。',
'28', '8', '18',
'何か役に立つことがしたい。社会とのつながりを持ちたい。',
'夫の気持ちを大切にしたい。働ける場所があれば働かせてあげたい。経済的な不安もある。',
'若年性認知症特有の課題。就労支援、経済的支援、本人の居場所づくりが必要。',
'若年性認知症の専門的支援が必要。本人の意欲を活かした支援計画を立てる。',
'1.若年性認知症支援コーディネーターにつなぐ 2.障害年金の申請支援 3.認知症カフェへの参加を提案 4.就労継続支援B型事業所の見学を調整');

-- クライアント105: 徘徊あり
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (105, '2025-01-19 15:00:00', '包括支援センター 伊藤', '緊急訪問・徘徊対応', '在宅・長男の妻同席',
'穏やかに対応されたが、「家に帰りたい」と繰り返し訴えられた。ここが自宅であることを説明しても理解されない。',
'中等度～重度の認知機能低下。見当識障害が顕著。自宅を実家と混同している。',
'III',
'夕方になると外出しようとする（夕暮れ症候群）。先週、警察に保護された。帰宅願望が強い。',
'高血圧あり。変形性膝関節症で歩行時に痛みあり。それでも歩いて出かけようとする。',
'A2',
'長男家族と同居。日中は長男夫婦が仕事で不在。デイサービスを週3回利用中だが、帰宅後に外出してしまう。',
'38', '15', '25',
'家に帰りたい（実家のことを指している）。お母さんに会いたい。',
'仕事があるので日中は見られない。GPSを持たせているが、外すことがある。施設入所も考えている。',
'徘徊による事故リスクが高い。見守り体制の強化が急務。',
'徘徊対策と家族支援が必要。デイサービスの増回と見守りサービスの導入を検討。',
'1.デイサービスを週5回に増回 2.GPS付き見守りサービスの導入 3.近隣への協力依頼（見守りネットワーク） 4.ショートステイの定期利用を提案');

-- クライアント106: セルフネグレクト
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (106, '2025-01-20 10:30:00', '包括支援センター 山田', '近隣からの通報による訪問', '在宅・本人のみ',
'ドア越しの対応。「用はない」「帰ってくれ」と拒否的。粘り強く説明し、玄関先で短時間話を聞けた。',
'評価困難。会話は成立するが、質問に対する回答が曖昧。認知機能低下の疑いあり。',
'評価困難',
'セルフネグレクト状態。入浴していない様子。衣類も汚れている。',
'栄養状態不良の疑い。痩せている。医療機関未受診のため詳細不明。',
'評価困難',
'独居。室内はゴミが堆積し、悪臭あり。近隣から苦情が出ている。電気・ガスは通っているが、水道が止まりかけている。',
'', '', '',
'一人で大丈夫。放っておいてくれ。',
'姪が遠方（大阪）に在住。年に1回程度しか会えない。できることがあれば協力したい。',
'緊急性の高いケース。生命の危険あり。多機関連携が必要。',
'セルフネグレクトの緊急ケース。関係機関と連携し、介入を継続。',
'1.保健師と連携し、健康状態の確認 2.社会福祉協議会と連携し、生活支援を検討 3.姪に状況を報告し、協力を依頼 4.週1回の訪問を継続し、信頼関係構築');

-- クライアント107: 認認介護
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (107, '2025-01-21 14:00:00', '包括支援センター 佐藤', '定期訪問・服薬管理確認', '在宅・夫婦同席',
'二人とも穏やかに対応。ただし、訪問の目的を何度も尋ねられた。',
'夫婦ともに軽度～中等度の認知機能低下。お互いの認知症を認識していない。',
'IIa（本人）、IIa（夫）',
'特に問題行動なし。ただし、二人とも服薬管理ができておらず、薬が大量に余っている。',
'本人は糖尿病と高血圧あり。夫も高血圧あり。二人とも服薬が不規則。',
'J2（本人）、J2（夫）',
'夫婦二人暮らし。長男は県外在住で月1回程度訪問。食事は惣菜や弁当が中心。',
'30', '10', '',
'二人で仲良く暮らしたい。子どもには迷惑をかけたくない。',
'両親のことが心配だが、仕事があり頻繁には来られない。サービスを利用してほしい。',
'認認介護の典型的なケース。服薬管理と栄養管理が課題。',
'夫婦への包括的支援が必要。服薬管理サービスと配食サービスの導入を優先。',
'1.訪問薬剤管理指導の導入 2.配食サービスの利用開始 3.デイサービスの体験利用（夫婦で） 4.長男への定期的な状況報告');

-- クライアント108: 介護者の負担大
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (108, '2025-01-22 11:00:00', '包括支援センター 田中', '介護者支援・レスパイト相談', '在宅・妻同席',
'本人は車椅子で対応。言葉は出にくいが、うなずきで意思表示。妻は疲労の色が濃い。',
'脳梗塞後遺症による血管性認知症。言語障害あり。理解力は比較的保たれている。',
'III',
'夜間の頻尿あり。妻が毎晩2-3回起きて対応。昼夜逆転傾向。',
'右片麻痺あり。車椅子使用。移乗には介助が必要。嚥下機能低下あり。',
'B2',
'妻と二人暮らし。妻が24時間介護。入浴は訪問入浴を週2回利用。デイサービス週3回。',
'42', '20', '32',
'（言葉で表現困難だが、自宅にいたい様子）',
'限界を感じている。夜眠れない。自分が倒れたらどうなるか不安。でも施設には入れたくない。',
'妻の介護負担が限界に達している。妻自身の健康状態も心配。',
'介護者支援が最優先。レスパイトケアの充実と妻の健康管理が必要。',
'1.ショートステイの定期利用（月2回）を提案 2.デイサービスを週5回に増回 3.妻の健康診断受診を勧奨 4.介護者の会への参加を提案');

-- クライアント109: 金銭管理困難
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (109, '2025-01-23 10:00:00', '包括支援センター 鈴木', '消費者被害相談', '在宅・本人のみ',
'にこやかに対応。「お客さんが来てくれて嬉しい」と歓迎された。',
'軽度の認知機能低下。判断力の低下が顕著。契約内容を理解できていない。',
'IIa',
'訪問販売員を家に上げてしまう。高額な布団や健康食品を購入。',
'骨粗鬆症あり。歩行は自立しているが、腰痛あり。',
'J1',
'独居。基本的なADLは自立。買い物は近所のスーパーで可能。ただし、金銭管理ができていない。',
'26', '6', '12',
'良いものを買っただけ。騙されてなんかいない。',
'母が高額な買い物をしていて困っている。通帳を預かりたいが、母が拒否する。',
'消費者被害のリスクが高い。成年後見制度の利用を検討。',
'金銭管理支援と消費者被害防止が必要。日常生活自立支援事業の利用を検討。',
'1.消費生活センターに相談 2.日常生活自立支援事業の利用を提案 3.クーリングオフの手続き支援 4.長男と連携し、見守り体制を強化');

-- クライアント110: 幻覚・妄想（レビー小体型認知症）
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (110, '2025-01-24 14:00:00', '包括支援センター 高橋', '定期訪問・症状確認', '在宅・妻同席',
'穏やかに対応。ただし、訪問中に「あそこに子どもがいる」と幻視を訴えられた。',
'レビー小体型認知症。認知機能の変動あり。調子の良い時と悪い時の差が大きい。',
'IIb',
'幻視が頻繁にある。「知らない人が家にいる」と訴える。パーキンソン症状あり。',
'パーキンソン病を合併。小刻み歩行、すくみ足あり。転倒リスク高い。',
'A2',
'妻と二人暮らし。日中は比較的穏やかだが、夕方から夜にかけて幻視が増える。',
'34', '16', '24',
'（幻視について）あの人たちは誰？怖くはないけど気になる。',
'幻視への対応に困っている。否定すると怒るし、肯定するのも良くないと聞いた。どうすればいいか。',
'レビー小体型認知症特有の症状への対応が必要。転倒予防も重要。',
'専門医との連携を強化。幻視への対応方法を家族に指導。',
'1.認知症疾患医療センターへの定期受診を継続 2.妻への幻視対応の指導 3.転倒予防のための住環境整備 4.デイサービスの利用を検討');

-- クライアント111: 独居・未受診
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (111, '2025-01-25 10:00:00', '包括支援センター 伊藤', '民生委員からの相談対応', '在宅・本人のみ',
'最初は警戒していたが、民生委員の紹介と伝えると態度が軟化。ただし、医療の話になると拒否的。',
'軽度～中等度の認知機能低下の疑い。同じ質問を繰り返す。日付の認識が曖昧。',
'評価困難（受診拒否のため）',
'特に問題行動なし。ただし、社会的に孤立している。近所付き合いもほとんどない。',
'高血圧の自己申告あり。しかし、医療機関を10年以上受診していない。',
'J2',
'独居。基本的なADLは自立。買い物は週1回、バスで大型スーパーへ。調理は自分で行っている。',
'', '', '',
'病院は嫌い。薬を飲むと体に悪い。自然に治る。',
'甥が遠方に在住。年に1回程度電話で話す程度。叔母のことは心配しているが、関わりは薄い。',
'未受診のため健康状態が不明。認知症の早期発見・早期対応が困難。',
'受診拒否ケース。信頼関係構築を優先し、徐々に受診につなげる。',
'1.定期的な訪問で信頼関係を構築 2.健康相談という形で保健師の訪問を調整 3.民生委員と連携した見守り 4.甥への状況報告と協力依頼');

-- クライアント112: 入院後の在宅復帰
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (112, '2025-01-26 14:00:00', '包括支援センター 山田', '退院前カンファレンス後の訪問', '在宅・妻同席',
'退院直後で疲労の様子。ベッドで横になりながら対応。妻が主に話をされた。',
'入院前は軽度の物忘れ程度だったが、入院中に認知機能が著しく低下。見当識障害あり。',
'IIb',
'入院中にせん妄があった。現在は落ち着いているが、夜間の混乱が時々ある。',
'大腿骨骨折術後。リハビリ中。歩行器使用で短距離歩行可能。転倒リスク高い。',
'A2',
'妻と二人暮らし。退院後、訪問リハビリと訪問看護を利用開始。妻が主介護者。',
'33', '12', '20',
'早く元気になりたい。歩けるようになりたい。',
'入院中に急に認知症が進んでショック。でも自宅で看たい。リハビリを頑張ってほしい。',
'入院による認知機能低下（廃用症候群）。リハビリと生活リズムの回復が重要。',
'在宅復帰支援。リハビリの継続と生活リズムの回復を支援。',
'1.訪問リハビリの継続（週2回） 2.デイケアの利用を検討 3.住環境の整備（手すり設置等） 4.妻への介護指導');

-- クライアント113: 服薬管理困難
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (113, '2025-01-27 11:00:00', '包括支援センター 佐藤', '薬剤師からの相談対応', '在宅・本人のみ',
'穏やかに対応。「薬はちゃんと飲んでいる」と言うが、実際は飲み忘れや重複服用がある。',
'軽度～中等度の認知機能低下。服薬の自己管理が困難。飲んだかどうか覚えていない。',
'IIa',
'特に問題行動なし。ただし、薬の管理ができず、血糖コントロールが悪化。',
'糖尿病、高血圧、心不全あり。複数の薬を服用中。最近、低血糖発作があった。',
'J2',
'独居。長男が週1回訪問して薬をセットしているが、それでも飲み忘れがある。',
'29', '8', '15',
'薬は飲んでいる。忘れてなんかいない。',
'薬の管理が心配。毎日は来られないので、何か良い方法はないか。',
'服薬管理の失敗が健康状態に直結。緊急性の高いケース。',
'服薬管理支援が最優先。訪問薬剤管理指導と見守りサービスの導入。',
'1.訪問薬剤管理指導の導入（週2回） 2.服薬カレンダーの設置 3.配食サービス利用時に服薬確認 4.かかりつけ医と連携し、処方の簡素化を相談');

-- クライアント114: 家族間の意見相違
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (114, '2025-01-28 13:00:00', '包括支援センター 田中', '家族調整・サービス担当者会議', '在宅・長女同席',
'穏やかに対応。家族の話し合いには参加せず、テレビを見ていた。',
'中等度の認知機能低下。自分の状況を正確に理解できていない。',
'IIb',
'特に問題行動なし。ただし、夜間のトイレ介助が必要で、長女の負担が大きい。',
'慢性腎臓病あり。週3回の透析が必要。透析後は疲労が強い。',
'A1',
'長女と同居。長男は別居で月1回訪問。長男は施設入所を希望、長女は在宅継続を希望。',
'35', '14', '26',
'（自分の意見を明確に表現できない状態）',
'長女：父を施設に入れたくない。私が看る。 長男：姉の負担が心配。施設の方が安心。',
'家族間の意見対立がサービス利用の障壁になっている。',
'家族調整が必要。中立的な立場で両者の意見を聞き、本人にとって最善の方法を検討。',
'1.家族会議の開催（長男・長女・ケアマネ・包括） 2.本人の意思確認（可能な範囲で） 3.ショートステイの体験利用を提案 4.長女の介護負担軽減策を検討');

-- クライアント115: 日中独居
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (115, '2025-01-29 10:30:00', '包括支援センター 鈴木', '火の不始末の相談対応', '在宅・本人のみ',
'穏やかに対応。「火の不始末なんてしていない」と否定。',
'軽度の認知機能低下。短期記憶の低下あり。自分の行動を覚えていない。',
'IIa',
'ガスコンロの消し忘れが複数回あり。鍋を焦がしたことも。本人は覚えていない。',
'変形性腰椎症で腰痛あり。歩行は自立しているが、長時間の立位は困難。',
'J2',
'長男夫婦と同居だが、日中は仕事で不在。一人で昼食を作ろうとして火の不始末が発生。',
'27', '9', '18',
'自分で料理くらいできる。心配しすぎ。',
'火事が心配。IHに変えたいが、母が使い方を覚えられるか不安。デイサービスで昼食を食べてほしい。',
'火災リスクが高い。日中の見守りと火の使用制限が必要。',
'火災予防と日中の見守り体制構築が必要。',
'1.IHクッキングヒーターへの変更を提案 2.デイサービスの利用（昼食提供）を検討 3.自動消火装置の設置 4.配食サービスの利用を提案');

-- クライアント116: 前頭側頭型認知症
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (116, '2025-01-30 14:00:00', '包括支援センター 高橋', '警察からの連絡対応', '在宅・妻同席',
'無表情で対応。質問に対して短い返答のみ。妻が代わりに説明。',
'前頭側頭型認知症。社会的認知の低下が顕著。善悪の判断が困難。',
'IIb',
'脱抑制行動あり。スーパーで商品を無断で持ち出し、警察沙汰に。本人は悪いことをした認識がない。',
'身体的には健康。68歳と比較的若い。',
'J1',
'妻と二人暮らし。子どもは独立。妻が常に付き添わないと外出できない状態。',
'36', '22', '30',
'（自分の行動の問題を認識できていない）',
'夫の行動に振り回されている。外出するたびにヒヤヒヤする。でも施設は嫌がる。',
'前頭側頭型認知症特有の行動障害。法的問題のリスクあり。',
'専門医との連携強化。行動障害への対応と妻の支援が必要。',
'1.認知症疾患医療センターへの相談 2.行動障害に対する薬物療法の検討 3.妻への心理的サポート 4.デイサービスの利用（構造化されたプログラム）');

-- クライアント117: 遠距離介護
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (117, '2025-01-31 10:00:00', '包括支援センター 伊藤', '定期訪問・状況確認', '在宅・本人のみ',
'穏やかに対応。「息子が来てくれないから寂しい」と訴え。',
'軽度の認知機能低下。日常生活は概ね自立しているが、複雑な判断は困難。',
'IIa',
'特に問題行動なし。ただし、孤独感が強く、抑うつ傾向あり。',
'高血圧あり。白内障術後で視力は改善。歩行は自立。',
'J1',
'独居。長男は東京在住で月1回程度訪問。近所付き合いは少ない。',
'25', '7', '',
'息子の近くに住みたいが、迷惑をかけたくない。ここで頑張る。',
'母のことは心配だが、仕事があり頻繁には帰れない。サービスを利用してほしい。電話は毎日している。',
'遠距離介護のケース。孤独感への対応と見守り体制の構築が必要。',
'社会的孤立の防止と見守り体制の強化。',
'1.デイサービスの利用を提案（社会参加） 2.見守りサービスの導入 3.長男との定期的な情報共有 4.地域のサロン活動への参加を促す');

-- クライアント118: 虐待疑い
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (118, '2025-02-01 11:00:00', '包括支援センター 山田', '虐待通報対応', '在宅・長男同席',
'おびえた様子。長男の顔色をうかがいながら話す。長男は「転んだだけ」と説明。',
'中等度の認知機能低下。自分の状況を正確に説明できない。',
'IIb',
'特に問題行動なし。むしろ、長男に対して従順すぎる印象。',
'左腕にあざあり。圧迫骨折の既往。栄養状態不良の疑い。',
'A1',
'長男と二人暮らし。長男は無職。本人の年金で生活している様子。',
'34', '10', '',
'（長男の前では本音を言えない様子）',
'母の世話は自分がしている。余計なお世話だ。',
'身体的虐待および経済的虐待の疑い。緊急性の高いケース。',
'虐待対応。本人の安全確保を最優先。関係機関との連携が必要。',
'1.高齢者虐待対応会議の開催 2.本人との個別面談の機会を作る 3.医療機関での診察（あざの確認） 4.緊急時の一時保護先の確保');

-- クライアント119: アルコール問題
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (119, '2025-02-02 14:00:00', '包括支援センター 佐藤', '妻からの相談対応', '在宅・妻同席',
'酒臭あり。ろれつが回らない状態。「何の用だ」と不機嫌。',
'アルコール性認知症の疑い。認知機能の評価が困難（飲酒の影響）。',
'評価困難',
'飲酒時に暴言あり。妻に対して怒鳴ることがある。物を投げることも。',
'アルコール性肝障害あり。栄養状態不良。歩行時のふらつきあり。',
'J2',
'妻と二人暮らし。朝から飲酒。妻は精神的に疲弊している。',
'', '', '35',
'酒は百薬の長。やめる必要はない。',
'夫の飲酒をやめさせたい。暴言が怖い。離婚も考えている。',
'アルコール依存と認知症の合併。DV（精神的虐待）の疑いもあり。',
'アルコール問題への対応と妻の安全確保が必要。',
'1.アルコール専門医療機関への相談 2.妻への支援（DV相談窓口の紹介） 3.断酒会などの自助グループの紹介 4.妻の避難先の確保');

-- クライアント120: 多問題世帯
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, visit_purpose, visit_condition, vr_reaction, vr_cognition, vr_dementia_adl, vr_behavior, vr_physical, vr_disability_adl, vr_living, vr_dasc, vr_dbd, vr_jzbi, vr_person_intent, vr_family_intent, vr_other, support_decision, future_plan)
VALUES (120, '2025-02-03 10:00:00', '包括支援センター 田中', '民生委員・社協からの相談対応', '在宅・本人のみ',
'疲れた様子。「どうしていいかわからない」と涙ぐむ。',
'軽度～中等度の認知機能低下の疑い。ストレスで認知機能が低下している可能性も。',
'評価困難',
'特に問題行動なし。むしろ、長男の世話で疲弊している。',
'健康状態不明。医療機関未受診。栄養状態不良の疑い。',
'J2',
'独居だが、精神疾患のある長男が頻繁に来て金銭を要求。電気代が払えず、停止の危機。',
'', '', '',
'息子を見捨てられない。でも、もう限界。',
'長男は精神疾患あり。母親に依存。金銭管理ができない。',
'多問題世帯。経済的困窮、長男の精神疾患、本人の認知症疑い。複合的な支援が必要。',
'多機関連携による包括的支援が必要。緊急性の高いケース。',
'1.生活保護の申請支援 2.長男の精神科受診支援 3.社会福祉協議会と連携し、緊急小口資金の利用 4.ライフライン停止防止のための調整 5.本人の医療機関受診');
