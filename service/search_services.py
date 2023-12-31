from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import pandas as pd
from typing import List
from model.DTO.search_result import SearchResult
from sklearn.metrics.pairwise import linear_kernel
import json
from pymongo import MongoClient
from bson import ObjectId
# from models.CrawledSites import crawled_sites

client = MongoClient(
    'mongodb+srv://yash23malode:9dtb8MGh5aCZ5KHN@cluster.u0gqrzk.mongodb.net/')
db = client['prakat23']
crawled_sites = db['crawled_sites']

report_collection = db['report_collection']


def get_lines(file_obj):
    json_list = []
    for line in file_obj:
        json_line = json.loads(line.strip())
        json_list.append(json_line)

    return json_list


def load_and_vectorize_data(collection):
    df = pd.DataFrame(collection)
    vectorizer = TfidfVectorizer()
    vectorizer.fit(df['body'])
    vector_tfidf = vectorizer.transform(df['body'])

    return df, vectorizer, vector_tfidf


def rank_documents(query: str, vectorizer: TfidfVectorizer, vector_tfidf: TfidfTransformer, df, page: int, pageCount: int, tags: str) -> List[SearchResult]:
    query_vec = vectorizer.transform([query])
    cosine_similarities = linear_kernel(query_vec, vector_tfidf).flatten()
    ranking = cosine_similarities.argsort()[::-1]

    start_index = (page - 1) * pageCount
    end_index = start_index + pageCount

    results = []
    start_index = (page - 1) * pageCount
    end_index = start_index + pageCount

    results = []
    count = 1
    for i in ranking[start_index:end_index]:
        tags_list = df['tags'][i]

        # If tags_list is not a list, set it to an empty list
        if not isinstance(tags_list, list):
            tags_list = []

        if tags:
            # Check if the filter is present in tags_list
            # if tags in tags_list:
            #     result = SearchResult(title=df['title'][i], url=df['url'][i], score=ranking[i], id=str(df['_id'][i]), tags=tags_list)
            #     results.append(result)
            # else:
            #     end_index+=1
            #     continue
            # Convert comma-separated string to a list
            tags_to_check = tags.split(',')

            # Check if any tag in tags_to_check is present in tags_list
            if all(tag in tags_list for tag in tags_to_check):
                # print(list(report_collection.find_one({"url_id": df['_id'][i]})))

                # print(list(report_collection.find_one(
                #     {"url_id": str(df['_id'][i])})))

                result = SearchResult(title=df['title'][i], url=df['url'][i], score=ranking[i], id=str(
                    df['_id'][i]), tags=tags_list, report_generated=df['report_generated'][i])
                results.append(result)
            else:
                end_index += 1
                continue
        else:
            # No filter specified, include the document in the results
            doc = report_collection.find_one(
                {"url_id": str(df['_id'][i])})
            if doc is not None:
                print(doc['name'])
                # print(listdoc.get('report_generated'))
                result = SearchResult(title=df['title'][i], url=df['url'][i], score=ranking[i], id=str(
                    df['_id'][i]), tags=tags_list, report_generated=doc['report_generated'])
            else:
                print('doc not found')
                result = SearchResult(title=df['title'][i], url=df['url'][i], score=ranking[i], id=str(
                    df['_id'][i]), tags=tags_list, report_generated=0)

            results.append(result)

        # Increment end_index by one regardless of the filter being present or not
        count += 1

    return results

# count = 1
# for i in ranking[start_index:end_index]:
#     tags_list = df['tags'][i]

#     if not isinstance(tags_list, list):
#         tags_list = []
#     result = SearchResult(title=df['title'][i], url=df['url'][i], score=ranking[i], id=str(df['_id'][i]), tags=tags_list)
#     results.append(result)
#     count+=1
