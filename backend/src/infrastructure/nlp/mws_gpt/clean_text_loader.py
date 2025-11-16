import re
from langchain_community.document_loaders import TextLoader


class CleanTextLoader(TextLoader):
    def load(self):
        docs = super().load()
        for doc in docs:
            doc.page_content = re.sub(r'\n{3,}', '\n', doc.page_content)
            # doc.page_content = re.sub(r'\*+', '', doc.page_content)
            # doc.page_content = re.sub(r'\s+', ' ', doc.page_content)
        return docs
