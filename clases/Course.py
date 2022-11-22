# To this end, say you need to code a factory class called CumulativePowerFactory
# https://realpython.com/python-multiple-constructors/

# class Evaluation_Factory:

# from typing import Final


class Evaluation:
    last_type: str = ""
    last_total_percentage: float = 0

    WORDS_TO_SKIP: list[str] = ["Evaluación", "Examen"]

    def __init__(self, string: str):
        string = string.replace(':', '')
        words = string.split()
        if words[0] in self.WORDS_TO_SKIP:
            words.pop(0)

        self.type: str = words[0]
        self.name: str = ' '.join(words[0:-2])

        if self.type == self.last_type:
            self.percentage: float = float(self.last_total_percentage) * (float(words[-2])/100)
        else:
            self.percentage: float = words[-2]

    # def update_virtual_variables(self):
    #     if self.type == self.name:
    #         Evaluation.last_type = self.type
    #         Evaluation.last_total_percentage = self.percentage

    @classmethod
    def get_type_of_string(cls, string: str):
        string = string.replace(':', '')
        words = string.split()
        if words[0] in cls.WORDS_TO_SKIP:
            return words[1]
        return words[0]

    @classmethod
    def get_percentage_of_string(cls, string: str):
        string = string.replace(':', '')
        words = string.split()
        return words[-2]

    @classmethod
    def get_name_of_string(cls, string: str):
        string = string.replace(':', '')
        words = string.split()
        if words[0] in cls.WORDS_TO_SKIP:
            words.pop(0)
        return ' '.join(words[0:-2])


class Course:
    def __init__(self, name: str, evaluations: list[Evaluation], credits: int):
        self.name = name
        self.evaluations = evaluations
        self.credits = credits


# def make_list_of_evaluations():
    # pass
