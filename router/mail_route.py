from fastapi import APIRouter, Query
from service.ses import SesMailSender
import boto3
from pymongo import MongoClient
from bson import ObjectId

ses_access_key = 'AKIAZFR6HXDKUADEPQYU'
ses_secret_access_key = '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'
region = 'ap-south-1'

client = MongoClient(
    'mongodb+srv://yash23malode:9dtb8MGh5aCZ5KHN@cluster.u0gqrzk.mongodb.net/')
db = client['prakat23']
report_collection = db['report_collection']
crawled_sites = db['crawled_sites']
# ses_client = boto3.client('ses', ses_access_key, ses_secret_access_key, region)
ses_client = boto3.client(
    "ses",
    region_name=region,
    aws_access_key_id=ses_access_key,
    aws_secret_access_key=ses_secret_access_key
)

# ses_client = boto3.resource('ses', ses_access_key,
#                             ses_secret_access_key, region)
ses_mail_send = SesMailSender(ses_client)

router = APIRouter()


@router.get('/send')
async def email_report(report_id: str = Query()):
    # ses.mail_report('samit091848@gmail.com', "some report")
    report = report_collection.find_one(ObjectId(report_id))

    if report is None:
        return "Incorrect report id"

    ses_mail_send.send_email('phoenixalphainfo@gmail.com', {'ToAddresses': ['samit091848@gmail.com']},
                             'AI Generated Report', report['report'])
