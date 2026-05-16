# # from src.states.blogstate import BlogState
# # # class BlogNode:
# # #     """a class to represent the blog node"""
# # #     def __init__(self,llm):
# # #         self.llm=llm
# # #     def title_creation(self,state:BlogState):
# # #          """create the title for the blog"""
# # #          if "topic" in state and state["topic"]:
# # #             prompt="""you are an expert blog content writer. use markdown formatting. generate a blog title for the {topic}.this title shiuld be creative and SEO friendly. I just want only one best title among all titles"""
# # #             system_message= prompt.format(topic=state["topic"])   
# # #             response=self.llm.invoke(system_message) 
# # #             return{"blog":{"title":response.content}} 
# # #     def content_generation(self,state:BlogState):
# # #         """create the content for the blog"""
# # #         if "blog" in state and state["blog"] and "title" in state["blog"]:
# # #             prompt="""you are an expert blog content writer. use markdown formatting. generate a detailed blog content and detailed breakdown for the {title}"""
# # #             system_message= prompt.format(title=state["blog"]["title"])   
# # #             response=self.llm.invoke(system_message) 
# # #             return{"blog":{"title":state["blog"]["title"], "content":response.content}}
# # class BlogNode:
# #     def __init__(self, llm):
# #         self.llm = llm

# #     def title_creation(self, state: BlogState):
# #         if "topic" in state and state["topic"]:
# #             prompt = """
# #             Generate ONLY ONE blog title for: {topic}
# #             - One line only
# #             - Max 10 words
# #             - No extra text
# #             """
# #             system_message = prompt.format(topic=state["topic"])
# #             response = self.llm.invoke(system_message)

# #             title = response.content.strip().split("\n")[0]

# #             return {
# #                 "blog": {
# #                     **state.get("blog", {}),
# #                     "title": title
# #                 }
# #             }

# #     def content_generation(self, state: BlogState):
# #         if "blog" in state and "title" in state["blog"]:
# #             prompt = """
# #             Write a detailed blog on: {title}

# #             Structure:
# #             - Introduction
# #             - Headings
# #             - Conclusion

# #             Use markdown.
# #             Do not repeat title.
# #             """
# #             system_message = prompt.format(title=state["blog"]["title"])
# #             response = self.llm.invoke(system_message)

# #             return {
# #                 "blog": {
# #                     **state.get("blog", {}),
# #                     "content": response.content
# #                 }
# #             }

# class BlogNode:
#     def __init__(self, llm):
#         self.llm = llm

#     def title_creation(self, state):
#         if "topic" in state and state["topic"]:
#             prompt = """
#             Generate ONLY ONE blog title for: {topic}
#             - One line only
#             - Max 10 words
#             - No extra text
#             """

#             response = self.llm.invoke(
#                 prompt.format(topic=state["topic"])
#             )

#             title = response.content.strip().split("\n")[0]

#             return {
#                 "blog": {
#                     **state.get("blog", {}),
#                     "title": title
#                 }
#             }

#     def content_generation(self, state):
#         if "blog" in state and "title" in state["blog"]:
#             prompt = """
#             Write a detailed blog on: {title}

#             Structure:
#             - Introduction
#             - Headings
#             - Bullet points
#             - Conclusion

#             Use markdown.
#             Do NOT repeat title.
#             """

#             response = self.llm.invoke(
#                 prompt.format(title=state["blog"]["title"])
#             )

#             return {
#                 "blog": {
#                     **state.get("blog", {}),
#                     "content": response.content
#                 }
#             }
from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog

class BlogNode:
    """
    A class to represent he blog node
    """

    def __init__(self,llm):
        self.llm=llm

    
    def title_creation(self,state:BlogState):
        """
        create the title for the blog
        """

        if "topic" in state and state["topic"]:
            prompt="""
                   You are an expert blog content writer. Use Markdown formatting. Generate
                   a blog title for the {topic}. This title should be creative and SEO friendly

                   """
            
            sytem_message=prompt.format(topic=state["topic"])
            print(sytem_message)
            response=self.llm.invoke(sytem_message)
            print(response)
            return {"blog":{"title":response.content}}
        
    def content_generation(self,state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}
        
    def translation(self,state:BlogState):
        """
        Translate the content to the specified language.
        """
        translation_prompt="""
        Translate the following title and content into {current_language}.
        - Maintain the original tone, style, and formatting.
        - Adapt cultural references and idioms to be appropriate for {current_language}.

        ORIGINAL TITLE:
        {blog_title}

        ORIGINAL CONTENT:
        {blog_content}

        """
        print(state["current_language"])
        blog_title=state["blog"].get("title", "")
        blog_content=state["blog"].get("content", "")
        messages=[
            HumanMessage(content=translation_prompt.format(current_language=state["current_language"], blog_title=blog_title, blog_content=blog_content))
        ]
        translation_obj = self.llm.with_structured_output(Blog).invoke(messages)
        return {"blog": {"title": translation_obj.title, "content": translation_obj.content}}

    def route(self, state: BlogState):
        return {"current_language": state['current_language'] }
    

    def route_decision(self, state: BlogState):
        """
        Route the content to the respective translation function.
        """
        if state["current_language"] == "french":
            return "french"
        elif state["current_language"] == "english":
            return "english"
        elif state["current_language"] == "spanish":
            return "spanish"
        elif state["current_language"] == "german":
            return "german"
        else:
            return state['current_language']

         