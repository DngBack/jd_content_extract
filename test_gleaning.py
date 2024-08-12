from dotenv import load_dotenv
from chunking.characters import character_chunking
from get_content.utils.scrape import scrape_html
from extraction.gleaning.graph import GraphExtractor
import os
import boto3
from botocore.exceptions import ClientError

load_dotenv('.env')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

DEFAULT_ENTITY_TYPES = ["emplyment_type_period_attributes", "trial_preiod_attributes", "contract_renewal_attributes"] 
DEFAULT_ENTITY_TYPES_v2 = ["recruiment_and_hiring_attributes", "holidays_and_leaves_attributes", "welfare_insurance_attributes"]
content_output = """
第三営業本部　第二新卒採用

【概要】
第二新卒を対象に当社第三営業本部内で幅広く選考を行う。
　
【選考フロー】
　・書類選考→一次面接→役員面接→最終面接
　※経験に親和性があれば面接2回の場合有
　　※応募前の企業説明は候補者から希望があれば対応
　・内定後、処遇待遇と共に配属部署（第三営業本部内のいずれか）を通知
　　配属部署は候補者の思考性や希望、経験の親和性にて判断

【第三営業本部内の部署】
　①ｴﾚｸﾄﾛﾆｸｽ材料ﾁｰﾑ
　　取り扱い商材：LED、電源、OA、照明、太陽電池
　②ﾒﾃﾞｨｶﾙ・ﾃﾞﾊﾞｲｽﾁｰﾑ
　　取り扱い商材：ｼﾘｺｰﾝ、医療機器接着剤、3Dﾓﾆﾀｰ用ｱｲｼｰﾙﾄﾞ、ﾌｪｲｽｼｰﾙﾄﾞ
　③ｵｰﾄﾓﾃｨﾌﾞｴﾚｸﾄﾛﾆｸｽﾁｰﾑ
　　取り扱い商材：自動車関連電子材料
　④ｴﾈﾙｷﾞｰﾃﾞﾊﾞｲｽﾁｰﾑ
　　取り扱い商材：ﾘﾁｳﾑｲｵﾝ電池

【勤務地】
　・東京のみ

【必須条件】
　・24～27歳
・有形商材の営業経験

【歓迎条件】
　・英語または中国語でのビジネス経験

【想定年収】
　・年収：3,600～4,500千円
"""

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client(
    service_name="bedrock-runtime",
    region_name="ap-northeast-1",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    )

# Set the model ID, e.g., Titan Text Premier.
model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"


extractor = GraphExtractor(
    llm_invoker=client,
    encoding_model= "cl100k_base",
    max_gleanings=1,
    entity_types=DEFAULT_ENTITY_TYPES_v2
    )

# Open the HTML file and read its content as a string
with open('test1.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# content_output = scrape_html(html_content)
chunk_list = character_chunking(content_output)
# print(chunk_list)

results = extractor(
    texts = chunk_list,
    model = model_id
)

print(results)
