from langchain_text_splitters import RecursiveCharacterTextSplitter


class Splitter:
    split_text = RecursiveCharacterTextSplitter(
        chunk_size=8000,     # Максимальный размер чанка (в символах или токенах)
        chunk_overlap=500,    # Перекрытие между чанками (для контекста)
        length_function=len, # Функция для измерения длины (можно использовать токенизатор)
    ).split_text
