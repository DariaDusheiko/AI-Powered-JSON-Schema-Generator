from langchain_core.prompts import ChatPromptTemplate


class Prompts:
    def type_request(request, llm):
        template = "Твоя задача определить, нужно ли по запросу создать json-схему или отредактировать json-схему. " \
        "Выведи одну цифру 1, если нужно создать. " \
        "Выведи 2, если нужно отредактировать. " \
        "0 В противном случае."

        prompt = ChatPromptTemplate(
            [("system", template), ("user", "Запрос: {request}")]
        )
        return (prompt | llm).invoke({"request": request}).content

    def descriptions(requst, llm, content):
        template = ""
    

class TypeRequest:
    create = "create"
    edit = "edit"

# print(Prompts.type_request(""))