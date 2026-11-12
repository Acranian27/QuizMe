import json
from pathlib import Path

import random

class Question:
    def __init__(self, question):
        self.Question: str       = question['Question']
        self.ModelAnswer: str    = question['ModelAnswer']
        self.Keywords: list[str] = question['Keywords']
        self.Context: str | None = question.get("Context", None)
        self.HintsUsed: int      = 0

    def GiveContext(self):
        print('Give context or smth')
        pass

    def GiveHint(self) -> str:
        """ Returns one of the keywords required for to answer the question. """
        if self.HintsUsed >= len(self.Keywords):
            return self.ModelAnswer

        Hint = self.Keywords[self.HintsUsed]
        self.HintsUsed += 1
        return Hint

    def MarkAnswer(self, answer: str, advanced: bool):
        """
        Returns a grade for the given answer using the question's config data.

        A non-advanced marking involves counting the number of keywords found in the given answer.

        An advanced marking is more complex involving the format of the answer and whether it is comprehensible and not just a list of the keywords.
        """

        if not advanced:
            NumKeywords = len(self.Keywords)
            KeywordsIncluded = 0

            for word in self.Keywords:
                if word in answer:
                    KeywordsIncluded += 1

            return f'{KeywordsIncluded} / {NumKeywords}'

        else:
            return f'Not made yet (function kinda empty lmao)'

class Subject:
    def __init__(self, config):
        print(config)
        self.Name = config['SubjectName']
        self.Questions = config['Questions']
        self.Content = config['Content']

    def GetQuestion(self, contextual: bool) -> Question:
        """ Works by adding up all the possible questions and returning a randomly selected position in one of the tables of questions. """

        NumNonContextQ = len(self.Questions['NonContextual'])
        NumContextQ = len(self.Questions['Contextual'])

        # Only pick Non-Contextual questions
        if not contextual:
            SelectedPos = random.randint(0, NumNonContextQ - 1)
            SelectedQuestion = self.Questions['NonContextual'][SelectedPos]

        # Can be either -> First portion belongs to Contextual and second portion to Non-Contextual
        else:
            SelectedPos = random.randint(0, NumNonContextQ + NumContextQ - 1)
            if SelectedPos < NumContextQ:
                SelectedQuestion = self.Questions['Contextual'][SelectedPos]

            else:
                SelectedQuestion = self.Questions['NonContextual'][SelectedPos - NumContextQ]

        return Question(SelectedQuestion)

SubjectsPath = Path('Subjects')
Subjects: dict[str, Subject] = {}

for configFile in SubjectsPath.glob('*.json'):
    with open(configFile, 'r') as File:
        Config = json.load(File)

        if not Config.get('SubjectName', None): continue

        Subjects[Config['SubjectName']] = Subject(Config)

RandomQuestion = Subjects['Computer Science ATAR'].GetQuestion(False)
print(RandomQuestion.Question)