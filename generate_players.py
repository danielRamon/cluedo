from typing import List
from langchain_ollama import OllamaLLM
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

llm = OllamaLLM(model="gemma2", temperature=0.8)


class Person(BaseModel):
    name: str = Field(description="Person's name")
    age: int = Field(description="Person's age")
    nationality: str = Field(description="Person's nationality")
    gender: str = Field(description="Person's gender")
    description: str = Field(description="Person's description")
    occupation: str = Field(description="Person's occupation")
    known_languages: str = Field(
        description="Person's known languages it could be one or more")


class Witness(Person):
    testimony: str = Field(description="Witness's testimony")


class Suspect(Person):
    guilty: bool = Field(description="Suspect's guilt")
    background: str = Field(
        description="Suspect's background during the crime")


class Crime(BaseModel):
    suspects: List[Suspect]
    witnesses: List[Witness]
    event: str = Field(
        description="A long description with all the details about the crime with date, aproximetly time and place")
    date: str = Field(description="Crime date")
    location: str = Field(description="Crime location")
    summary: str = Field(description="Brief description of the crime")
    motive: str = Field(description="Motive of the crime")


parser = PydanticOutputParser(pydantic_object=Crime)

prompt = PromptTemplate(
    template="Create a crime in {country} in all the text should be in the language of this country, and a list with {suspects} suspects and {witnesses} where only one of the suspects is guilty. \n {format_instructions}",
    input_variables=["suspects", "witnesses"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()},
)


def generate_crime(suspects, witnesses, country):
    chain = prompt | llm | parser
    output = chain.invoke(
        {"suspects": suspects, "witnesses": witnesses, "country": country})
    return output
