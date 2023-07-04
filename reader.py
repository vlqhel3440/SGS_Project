from llama_index.readers import ChatGPTRetrievalPluginReader
import os
import sys

os.environ["OPENAI_API_KEY"] = "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"
os.environ["BEARER_TOKEN"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InZscWhlbDMwODZAZ21haWwuY29tIiwibmFtZSI6IlNldW5nS3l1IExlZSIsInBhc3N3b3JkIjoiZG9uZ3lhbmcifQ.lZa62X2IVa-j4sGGoi1vQXKjiGle8Rki_fctf9KC4hg"

bearer_token = os.getenv("BEARER_TOKEN")

reader = ChatGPTRetrievalPluginReader(
    endpoint_url="http://127.0.0.1:8000",
    bearer_token=bearer_token
)

documents = reader.load_data("Tell me where the person whose name is Jung lives")
print(len(documents))

from llama_index import ListIndex

index = ListIndex(documents)

query_engine = index.as_query_engine(response_mode="compact")
response = query_engine.query(
    sys.argv[1],
)

print(response)