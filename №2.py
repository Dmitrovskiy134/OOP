class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        # Проверяем, что это лектор и курс подходит
        if not isinstance(lecturer, Lecturer):
            return 'Ошибка: это не лектор'
        if course not in self.courses_in_progress:
            return 'Ошибка: студент не изучает этот курс'
        if course not in lecturer.courses_attached:
            return 'Ошибка: лектор не читает этот курс'
        if not (0 <= grade <= 10):
            return 'Ошибка: оценка должна быть от 0 до 10'

        # Добавляем оценку лектору
        if hasattr(lecturer, 'grades'):
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            # Если у лектора нет атрибута grades, создаём его
            lecturer.grades = {course: [grade]}

        return None


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}  # Оценки за лекции


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
            return None
        else:
            return 'Ошибка'


# Тестирование
if __name__ == "__main__":
    lecturer = Lecturer('Иван', 'Иванов')
    reviewer = Reviewer('Пётр', 'Петров')
    student = Student('Алёхина', 'Ольга', 'Ж')

    student.courses_in_progress += ['Python', 'Java']
    lecturer.courses_attached += ['Python', 'C++']
    reviewer.courses_attached += ['Python', 'C++']

    print(student.rate_lecture(lecturer, 'Python', 7))  # None
    print(student.rate_lecture(lecturer, 'Java', 8))  # Ошибка
    print(student.rate_lecture(lecturer, 'С++', 8))  # Ошибка
    print(student.rate_lecture(reviewer, 'Python', 6))  # Ошибка

    print(lecturer.grades)  # {'Python': [7]}