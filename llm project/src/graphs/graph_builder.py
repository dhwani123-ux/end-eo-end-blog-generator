from langgraph.graph import StateGraph,END,START
from src.llms.groqllm import GroqLLM
from src.states.blogstate import BlogState
from src.nodes.blog_node import BlogNode
class GraphBuilder:
    def __init__(self,llm):
        self.llm=llm
        self.graph=StateGraph(BlogState)
    def build_topic_graph(self):
        """Build a graph to generate blogs bbased on topic"""  
        blog_node_obj=BlogNode(self.llm)
        print(self.llm)
        ##nodes
        self.graph.add_node("title_creation",blog_node_obj.title_creation)
        self.graph.add_node("content_generation",blog_node_obj.content_generation)
        ##edges
        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation","content_generation") 
        self.graph.add_edge("content_generation",END)   
        return self.graph
    def build_language_graph(self):
        """Build a graph for blog generation with inputs topics and language"""
        self.blog_node_obj=BlogNode(self.llm)
        print(self.llm)
        ##nodes
        self.graph.add_node("title_creation",self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation",self.blog_node_obj.content_generation)
        self.graph.add_node("english_translation",lambda state: self.blog_node_obj.translation({**state,"current_language":"english"}))
        self.graph.add_node("french_translation",lambda state: self.blog_node_obj.translation({**state,"current_language":"french"}))
        self.graph.add_node("spanish_translation",lambda state: self.blog_node_obj.translation({**state,"current_language":"spanish"}))
        self.graph.add_node("german_translation",lambda state: self.blog_node_obj.translation({**state,"current_language":"german"}))
        self.graph.add_node("route", self.blog_node_obj.route)
        #edges and conditional edges
        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation","content_generation")
        self.graph.add_edge("content_generation","route") 
        #conditional edge
        self.graph.add_conditional_edges(
            "route",
            self.blog_node_obj.route_decision,
            {
                "english":"english_translation",
                "french":"french_translation",
                "spanish":"spanish_translation",
                "german":"german_translation",
            }
        )
        self.graph.add_edge("english_translation",END)
        self.graph.add_edge("french_translation",END)
        self.graph.add_edge("spanish_translation",END)
        self.graph.add_edge("german_translation",END)
        return self.graph

        
    def setup_graph(self,usecase):
        if usecase=="topic":
            self.build_topic_graph()
        if usecase=="language":
            self.build_language_graph()
        return self.graph.compile()

    
        ##edges
# Below code is for langsmith studio
llm=GroqLLM().get_llm()
#get the graph
graph_builder=GraphBuilder(llm)
graph=graph_builder.build_topic_graph().compile()
# 👇 ye add karo file ke end me

groqllm = GroqLLM()
llm = groqllm.get_llm()

graph_builder = GraphBuilder(llm)
graph = graph_builder.setup_graph(usecase="topic")
