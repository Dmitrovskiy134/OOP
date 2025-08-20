class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):
            return 'Ошибка: это не лектор'
        if course not in self.courses_in_progress:
            return 'Ошибка: студент не изучает этот курс'
        if course not in lecturer.courses_attached:
            return 'Ошибка: лектор не читает этот курс'
        if not (0 <= grade <= 10):
            return 'Ошибка: оценка должна быть от 0 до 10'

        if course in lecturer.grades:
            lecturer.grades[course].append(grade)
        else:
            lecturer.grades[course] = [grade]
        return None

    def _calculate_avg_grade(self):
        if not self.grades:
            return 0
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        return (f"Имя: {self.name}\nФамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {self._calculate_avg_grade():.1f}\n"
                f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
                f"Завершенные курсы: {', '.join(self.finished_courses)}")

    def __lt__(self, other):
        return isinstance(other, Student) and self._calculate_avg_grade() < other._calculate_avg_grade()

    def __eq__(self, other):
        return isinstance(other, Student) and self._calculate_avg_grade() == other._calculate_avg_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _calculate_avg_grade(self):
        if not self.grades:
            return 0
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        return f"{super().__str__()}\nСредняя оценка за лекции: {self._calculate_avg_grade():.1f}"

    def __lt__(self, other):
        return isinstance(other, Lecturer) and self._calculate_avg_grade() < other._calculate_avg_grade()

    def __eq__(self, other):
        return isinstance(other, Lecturer) and self._calculate_avg_grade() == other._calculate_avg_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
            return None
        return 'Ошибка'



def calculate_avg_hw_grade(students, course):
    all_grades = []
    for student in students:
        if course in student.grades:
            all_grades.extend(student.grades[course])
    return sum(all_grades) / len(all_grades) if all_grades else 0


def calculate_avg_lecture_grade(lecturers, course):
    all_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            all_grades.extend(lecturer.grades[course])
    return sum(all_grades) / len(all_grades) if all_grades else 0



if __name__ == "__main__":
    # Создаем экземпляры
    student1 = Student('Ruoy', 'Eman', 'male')
    student2 = Student('Anna', 'Ivanova', 'female')
    lecturer1 = Lecturer('Some', 'Buddy')
    lecturer2 = Lecturer('Other', 'Lecturer')
    reviewer1 = Reviewer('First', 'Reviewer')
    reviewer2 = Reviewer('Second', 'Checker')


    student1.courses_in_progress = ['Python']
    student1.grades = {'Python': [9, 10]}
    student2.courses_in_progress = ['Python']
    student2.grades = {'Python': [8, 9]}

    lecturer1.courses_attached = ['Python']
    lecturer1.grades = {'Python': [10, 9]}
    lecturer2.courses_attached = ['Python']
    lecturer2.grades = {'Python': [8, 9]}

    reviewer1.courses_attached = ['Python']
    reviewer2.courses_attached = ['Python']


    print("Средняя оценка за ДЗ по Python:", calculate_avg_hw_grade([student1, student2], 'Python'))
    print("Средняя оценка за лекции по Python:", calculate_avg_lecture_grade([lecturer1, lecturer2], 'Python'))


    print("\nПроверка сравнения:")
    print("lecturer1 > lecturer2:", lecturer1 > lecturer2)
    print("student1 == student2:", student1 == student2)