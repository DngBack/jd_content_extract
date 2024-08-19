from enum import Enum
import json
from utils.aws_sonet import AwsSonet35
from utils.groups import classify_entities

import ast
import json
from pathlib import Path
import pprint

import os
from dotenv import load_dotenv
load_dotenv(".env")

ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

# Set up llm 
llm = AwsSonet35()
llm.setup(ACCESS_KEY, SECRET_KEY, model_id)

list_name_dict = {
    "salary_fixed_allowances_attributes": "m_fixed_allowance",
    "salary_variable_allowances_attributes": "m_variable_allowance",
    "salary_type_id": "m_salary_type",
    "overtime_salary_id": "m_overtime_salary",
    "exceeding_overtime_id": "m_exceeding_overtime",
    "overtime_excluded_object_id": "m_overtime_excluded_object",
    "salary_payment_method_id": "m_salary_payment_method",
    "working_hours_type_id": "m_working_hours_type",
    "discretionary_labor_system_type_id": "m_discretionary_labor_system_type",
    "office_work_id": "m_office_work",
    "variable_working_hours_type_id": "m_variable_working_hours_type",
    "contract_working_hours_system_id": "m_contract_working_hours_system",
    "occupational_category_ids": "m_occupational_category",
    "prefecture_ids": "m_prefecture",
    "future_workplace_id": "m_future_workplace",
    "transfer_id": "m_transfer",
    "remote_type_ids": "m_remote_type",
    "smoking_prevention_content_id": "m_smoking_prevention_content",
    "ids": "m_future_job_description",
    "allowance_commute_money_type_id": "m_allowance_commute_money_type",
    "salary_raise_id": "m_salary_raise",
    "holidays_system_id": "m_holidays_system",
    "holidays_breakdown_ids": "m_holiday",
    "english_ids": "m_language_level",
    "insurance_ids": "m_insurance",
    "employment_type_ids": "m_employment_type",
    "employment_period_type_id": "m_employment_period_type",
    "trial_period_id": "m_trial_period",
    "job_charm_details1": "m_job_charm",
    "job_charm_details2": "m_job_charm",
    "job_charm_details3": "m_job_charm",
}

list_name = {
    "m_fixed_allowance": "The list of chosse: 家族手当, 住宅手当, 役職手当, 皆勤・精皆勤手当, \
        営業手当, 資格手当, 産休・育休手当, リー入力",
    "m_variable_allowance": "The list of chosse: 家族手当, 住宅手当, 役職手当, 皆勤・精皆勤手当, 営業手当, 資格手当, 産休・育休手当, フリー入力",
    "m_salary_type": "月給制, 年俸制, 日給制, 時給制, 完全歩合制, その他",
    "m_overtime_salary": "The list of chosse: 全額支給, 固定残業代制, 残業代支給対象外",
    "m_exceeding_overtime": "The list of chosse: 超過分は全額支給, みなし労働時間制のため記載なし",
    "m_overtime_excluded_object": "The list of chosse: 管理監督者, 裁量労働制（専門型）, 裁量労働制（企画型）, 事業場外みなし労働時間制,\
        高度プロフェッショナル制度対象者, 機密事務取扱者",
    "m_salary_payment_method": "The list of chosse: 年俸の1/12を毎月支給, その他",
    "m_working_hours_type": "The list of chosse: 固定労働時間制, 裁量労働制, 事業場外みなし労働時間制, \
        変形労働時間制, フレックスタイム制, シフト制, その他",
    "m_discretionary_labor_system_type": "The list of chosse: 専門業務型裁量労働制, 企画業務型裁量労働制",
    "m_office_work": "The list of chosse: 事業場内労働あり, 事業場内労働なし",
    "m_variable_working_hours_type": "The list of chosse: 完全週休2日制, 週休2日制, 隔週週休2日制, 週休制, その他",
    "m_contract_working_hours_system": "The list of chosse: The list of chosse: 固定労働時間制, 変形労働時間制",
    "m_occupational_category": "The list of chosse: 営業系, 企画・事務・マーケティング・管理系, 販売・サービス系（ファッション、フード、小売）,\
        専門サービス系（医療、福祉、教育、その他）, 専門職系（コンサルタント、金融、不動産）, \
        クリエイティブ系, エンジニア系（IT・Web・ゲーム・通信）, 技術系（電気、電子、機械）, \
        技術系（建築、土木）, 技術系（医薬、化学、素材、食品）, 施設・設備管理、技能工、運輸・物流系,\
        公務員、団体職員、その他",
    "m_prefecture": "The list of chosse: 北海道, 青森県, 岩手県, 宮城県, 秋田県, 山形県, 福島県, 茨城県, 栃木県, 群馬県,\
    埼玉県, 千葉県, 東京都, 神奈川県, 新潟県, 富山県, 石川県, 福井県, 山梨県, 長野県, 岐阜県, \
    静岡県, 愛知県, 三重県, 滋賀県, 京都府, 大阪府, 兵庫県, 奈良県, 和歌山県, 鳥取県, 島根県,\
    岡山県, 広島県, 山口県, 徳島県, 香川県, 愛媛県, 高知県, 福岡県, 佐賀県, 長崎県, 熊本県,\
    大分県, 宮崎県, 鹿児島県, 沖縄県, その他",
    "m_future_workplace": "The list of chosse: 本社および全ての支社、営業所, 条件範囲内の支社、営業所, 勤務地変更なし, その他",
    "m_transfer": "The list of chosse: tranfer1, tranfer2, tranfer3, tranfer4, tranfer5",
    "m_remote_type": "The list of chosse: フルリモートワーク（出社不要）, 一部リモートOK（出社要）",
    "m_smoking_prevention_content": "The list of chosse: 敷地内全面禁煙, 屋内全面禁煙、屋外に喫煙所を設置, 屋内に喫煙可能室設置, その他",
    "m_future_job_description": "The list of chosse: 同社業務全般, 条件付き同社業務全般, 仕事内容変更なし（限定職）, その他",
    "m_allowance_commute_money_type": "The list of chosse: 上限, 一律",
    "m_salary_raise": "The list of chosse: あり, なし",
    "m_holidays_system": "The list of chosse: 完全週休2日制, 週休2日制, 隔週週休2日制, 週休制, その他",
    "m_holiday": "あり, なし",
    "m_language_level": "The list of chosse: 上級（専門的な話題でも会話ができ、複雑な文章もスピーディに読み書きできる）, \
    中級（ビジネス場面での会話、文章は支障なくやりとりができる）, \
    初級（日常会話及び文章を読んで要点をつかむことができる）",
    "m_insurance": "The list of chosse: 健康保険, 厚生年金, 雇用保険, 労災保険",
    "m_employment_type": "The list of chosse: 正社員, 契約社員, その他",
    "m_employment_period_type": "The list of chosse: 雇用期間の定めなし, 期間指定",
    "m_trial_period": "The list of chosse: あり, 期間指定なし",
    "m_job_charm": ""
}

# list all categories
categories = [
    'location details', 'remote work details', 'smoking prevention details',
    'age and gender', 'employment type period', 'trial period',
    'contract renewal', 'job posting', 'salary information',
    'job working hour', 'recruiment and hiring', 'holidays and leaves',
    'welfare insurance'
]

target_categories = [
    'location_details', 'remote_work_details', 'smoking_prevention_details', 
    'age_and_gender', 'employment_type_period', 'trial_preiod', 
    'contract_renewal', 'job_posting', 'salary_informations', 
    'job_working_hours', 'recruiment_and_hiring', 'holidays_and_leaves', 
    'welfare_insurance'
]

# Open and read the JSON file
with open('entities.json', 'r', encoding="utf-8") as file:
    # Load the dictionary from the JSON file
    entities_dict = json.load(file)

# Replace 'data.json' with your file path
with open('1.json', 'r', encoding='utf-8') as file:
    info_extration = json.load(file)

result = {item['type']['en']: item['detail'] for item in info_extration["categories"]}

check = "employment_type_ids" in list_name_dict.keys()

output = {}
# for i in range(len(categories)):
i = 4
index_target = target_categories[i]
index_input = categories[i]

target = entities_dict[index_target]
content = result[index_input]

prompt_add = ""

for element in target.keys():
    if element in list_name_dict.keys():
        prompt_add = prompt_add + (element + ": " + 
                        list_name[list_name_dict[element]] + "\n")
    
output = {}

for i in range(len(categories)):
    index_target = target_categories[i]
    index_input = categories[i]

    target = entities_dict[index_target]
    content = result[index_input]

    prompt_add = ""

    for element in target.keys():
        if element in list_name_dict.keys():
            prompt_add = prompt_add + (element + ": " + 
                            list_name[list_name_dict[element]] + "\n")
    response = llm.chat(target=str(target),
                    content=str(content),
                prompt_add=str(prompt_add))

    print(response)
    response = eval(response)
    output[index_input] = response


# Convert and write JSON object to file

print(output)
with open('data.json', 'wb') as fp:
    fp.write(json.dumps(output, ensure_ascii=False).encode("utf8"))
# Check preprompt
# print(list_name_dict[index_target])
# print(list_name[list_name_dict[index_target]])
