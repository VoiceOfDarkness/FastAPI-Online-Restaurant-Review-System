from typing import Any, Dict

from models.data.orrs import Question


class QuestionRepository:
    
    def __init__(self, engine) -> None:
        self.engine = engine
    
    async def insert_question(self, details: Dict[str, Any]):
        try:
            question = Question(**details)
            print(question)
            await self.engine.save(question)
        
        except Exception as e:
            print(e)
            return False
        return True
    
    async def update_question(self, id: int, details: Dict[str, Any]):
        try:
            question = await self.engine.find_one(Question, Question.question_id == id)
            
            for key, val in details.items():
                setattr(question, key, val)
            
            await self.engine.save(question)
        except Exception as e:
            print(e)
            return False
        return True
    
    async def delete_question(self, id: int):
        try:
            question = await self.engine.find_one(Question, Question.question_id == id)
            await self.engine.delete(question)
        except:
            return False
        return True
    
    async def get_all_question(self):
        questions = await self.engine.find(Question)
        return questions
    
    async def get_question(self, id: int):
        question = await self.engine.find_one(Question, Question.question_id == id)
        return question
