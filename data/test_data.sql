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

-- 訪問記録データ（一部のクライアント用）
INSERT INTO visit_record (client_id, visit_datetime, visitor_name, vr_reaction, vr_cognition, vr_behavior, vr_life, vr_will, vr_family, vr_dasc, vr_dbd)
VALUES 
(101, '2025-01-15 10:00:00', '包括支援センター 佐藤', '訪問を快く受け入れ、会話も楽しそう', 'DASC-21：25点。軽度の記憶障害', '特に問題行動なし', '独居だが自立した生活を維持', '今の生活を続けたい', '長女が週1回訪問', '25', '5'),
(102, '2025-01-16 14:00:00', '包括支援センター 田中', '初めは警戒していたが徐々に打ち解けた', 'DASC-21：32点。中等度の認知機能低下', '夜間の不穏あり', '夫と二人暮らし。家事は夫が担当', '夫と一緒にいたい', '夫が主介護者。疲労が見られる', '32', '12'),
(103, '2025-01-17 11:00:00', '包括支援センター 鈴木', '訪問を拒否。玄関先での対応', 'DASC-21：35点。中等度の認知機能低下', '物盗られ妄想あり', '妻と二人暮らし。室内は整頓されている', '何も困っていない', '妻が対応に苦慮', '35', '18'),
(105, '2025-01-18 15:00:00', '包括支援センター 高橋', '穏やかに対応。会話は成立', 'DASC-21：38点。中等度～重度の認知機能低下', '夕方になると外出しようとする', '長男家族と同居', '家に帰りたい（実家のことを言っている）', '長男の妻が主介護者', '38', '15'),
(106, '2025-01-19 10:30:00', '包括支援センター 伊藤', '訪問を拒否。ドア越しの対応', '評価困難', 'セルフネグレクト状態', '独居。ゴミが堆積', '一人で大丈夫', '姪が遠方に在住', '', '');

-- DASC-21データ（一部のクライアント用）
INSERT INTO dasc21 (client_id, entry_date, respondent_name, assessment_item)
VALUES 
(101, '2025-01-15', '長女', '{"q1":"2","q2":"2","q3":"2","q4":"2","q5":"2","q6":"1","q7":"1","q8":"1","q9":"1","q10":"1","q11":"1","q12":"1","q13":"1","q14":"1","q15":"1","q16":"1","q17":"1","q18":"1","q19":"1","q20":"1","q21":"1"}'),
(102, '2025-01-16', '夫', '{"q1":"3","q2":"3","q3":"2","q4":"2","q5":"2","q6":"2","q7":"2","q8":"2","q9":"1","q10":"1","q11":"1","q12":"1","q13":"1","q14":"1","q15":"1","q16":"1","q17":"1","q18":"1","q19":"1","q20":"1","q21":"1"}'),
(103, '2025-01-17', '妻', '{"q1":"3","q2":"3","q3":"3","q4":"2","q5":"2","q6":"2","q7":"2","q8":"2","q9":"2","q10":"1","q11":"1","q12":"1","q13":"1","q14":"1","q15":"1","q16":"1","q17":"1","q18":"1","q19":"1","q20":"1","q21":"1"}'),
(105, '2025-01-18', '長男の妻', '{"q1":"3","q2":"3","q3":"3","q4":"3","q5":"3","q6":"2","q7":"2","q8":"2","q9":"2","q10":"2","q11":"1","q12":"1","q13":"1","q14":"1","q15":"1","q16":"1","q17":"1","q18":"1","q19":"1","q20":"1","q21":"1"}');

-- DBD-13データ（一部のクライアント用）
INSERT INTO dbd13 (client_id, entry_date, respondent_name, assessment_item)
VALUES 
(101, '2025-01-15', '長女', '{"d1":"1","d2":"0","d3":"0","d4":"1","d5":"0","d6":"0","d7":"0","d8":"1","d9":"0","d10":"1","d11":"0","d12":"1","d13":"0"}'),
(102, '2025-01-16', '夫', '{"d1":"2","d2":"1","d3":"1","d4":"2","d5":"1","d6":"0","d7":"1","d8":"1","d9":"0","d10":"1","d11":"1","d12":"1","d13":"0"}'),
(103, '2025-01-17', '妻', '{"d1":"3","d2":"2","d3":"2","d4":"3","d5":"1","d6":"1","d7":"1","d8":"2","d9":"1","d10":"2","d11":"1","d12":"1","d13":"0"}'),
(105, '2025-01-18', '長男の妻', '{"d1":"2","d2":"2","d3":"1","d4":"2","d5":"2","d6":"1","d7":"1","d8":"2","d9":"1","d10":"2","d11":"1","d12":"1","d13":"0"}');
