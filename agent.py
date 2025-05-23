import asyncio
from prompts import INSTRUCTIONS, ASKING_QUESTION_MESSAGE, INFORM_USER_MESSAGE
from livekit.agents.llm import function_tool
from livekit.agents import Agent

class Assistant(Agent):
    
    def __init__(self) -> None:
        super().__init__(instructions=INSTRUCTIONS)

    @function_tool
    async def ask_question(self, question: str):
        print(f"ask_question - question: {question}")
        self.session.generate_reply(instructions=ASKING_QUESTION_MESSAGE(question))
        
        task = asyncio.create_task(self.raise_events())
        result = await self.query_for_answer(question)
        task.cancel()
        await self.session.generate_reply(instructions="Give the user the following answer :" + result)
         


    async def query_for_answer(self, question):
        await asyncio.sleep(60)
        return "Cannot find an answer for the question: " + question

    async def raise_events(self):
        print("Raising events")
        ix = 1
        while ix < 10:
            await asyncio.sleep(10)
            print("Raising event: " + str(ix))
            self.on_ai_question_update("This is the test message number " + str(ix))
            ix += 1

    def on_ai_question_update(self, message):  
        self.session._loop.create_task(self.generate_reply(message))
    
    async def generate_reply(self, message):
        print ("generating reply: " + message)   
        #await self.session.say(message)
        await self.session.generate_reply(instructions=INFORM_USER_MESSAGE(message))
        