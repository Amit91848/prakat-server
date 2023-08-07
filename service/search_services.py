from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import pandas as pd
from typing import List
from model.DTO.search_result import SearchResult
from sklearn.metrics.pairwise import linear_kernel
import json
# from models.CrawledSites import crawled_sites

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

def rank_documents(query: str, vectorizer: TfidfVectorizer, vector_tfidf: TfidfTransformer, df, page: int, pageCount: int) -> List[SearchResult]:
    query_vec = vectorizer.transform([query])
    cosine_similarities = linear_kernel(query_vec, vector_tfidf).flatten()
    ranking = cosine_similarities.argsort()[::-1]
    print(ranking)

    start_index = (page - 1) * pageCount
    end_index = start_index + pageCount
    
    results = []
    count = 1
    for i in ranking[start_index:end_index]:
        tags_list = df['tags'][i]

        # If tags_list is not a list, set it to an empty list
        if not isinstance(tags_list, list):
            tags_list = []
        result = SearchResult(title=df['title'][i], url=df['url'][i], score=ranking[i], id=str(df['_id'][i]), tags=tags_list)

        results.append(result)
        count+=1

    return results
