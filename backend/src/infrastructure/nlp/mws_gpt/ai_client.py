from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import START, END, StateGraph
from langgraph.types import Command
from typing import Literal
from backend.src.infrastructure.nlp.mws_gpt.clean_text_loader import CleanTextLoader
from backend.src.infrastructure.nlp.mws_gpt.chat_mws import ChatMWS
from backend.src.infrastructure.nlp.mws_gpt.utils import Splitter
from backend.src.infrastructure.nlp.mws_gpt.states import State, InputState, OutputState
from backend.src.infrastructure.nlp.mws_gpt.prompts import Prompts, TypeRequest
from backend.src.utils.path import build_absolute_path
from pathlib import Path

class AiClient:
    def __init__(self, *, api_key, model, temperature=1, max_tokens=10**9):
        self.llm = ChatMWS(model=model, api_key=api_key, t=temperature, max_tokens=max_tokens)

        path = build_absolute_path(Path("backend") / "src" / "infrastructure" / "nlp" / "mws_gpt" / "doc_json_schema.txt")
        loader = CleanTextLoader(path, encoding='utf-8')
        document = loader.load()[0].page_content[2093:]
        self.content = document[:1100]
        self.split_document = Splitter.split_text(document[1100:])
    
    def generate_json_schema(self, request: str):
        def type_request(state: InputState) -> Command[Literal["get_descrtptions", END]]:
            text = "\n ".join([message.content for message in state["messages"]])
            print(text)
            response = Prompts.type_request(text, self.llm)
            print(response)

            request_step = None
            goto = END
            if "1" in response:
                request_step = TypeRequest.create
            elif "2" in response:
                request_step = TypeRequest.edit
            
            return Command(goto=goto, update={"request_step": request_step})
        
        def get_descrtptions(state: State):
            # print(state)
            return {"response": "верю"}
            

        graph = StateGraph(State, input=InputState, output=OutputState)
        graph.add_node(type_request, "type_request")
        graph.add_node(get_descrtptions, "get_descrtptions")

        graph.add_edge(START, "type_request")
        graph.add_edge("type_request", "get_descrtptions")
        graph.add_edge("get_descrtptions", END)
        graph = graph.compile()

        return graph.invoke({
            "messages": [("user", request)]
        })
        # display(Image(graph.get_graph().draw_mermaid_png()))



prompt = ChatPromptTemplate([
    ("system", "Скажи \"привет\" на {language}")
])

ai_client = AiClient(api_key="sk-KNo006G2a48UVE3IxFlQEQ", model="qwen2.5-72b-instruct", temperature=0.5)

print(ai_client.generate_json_schema("Хочу банан"))
# print(ai_client.llm.invoke(documents + "\n Сделай саммари на русском"))

# print(ai_client.content)
# print(ai_client.split_document)


# chain = prompt | ai_client.llm
# res = chain.invoke({"language": "английском"})
# print(res.content)
