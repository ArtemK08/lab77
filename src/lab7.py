# Місце для вашого коду
import os

#Шлях до поточної папки (src), щоб файли завжди створювались і шукались поруч із скриптом
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_file_path(filename):
    #Повертає повний шлях до файлу в папці src.
    return os.path.join(BASE_DIR, filename)


def parse_grades(filepath):
   
    #Зчитує дані з файлу формату 'Прізвище,Ім’я,Оцінка'.
    #Повертає список кортежів: [(прізвище, ім'я, оцінка), ...]
    
    students = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line_num, line in enumerate(file, start=1):
            clean_line = line.strip()
            if not clean_line:
                continue  # Пропуск порожних рядків

            parts = clean_line.split(",")
            if len(parts) != 3:
                raise ValueError(f"Некоректний формат даних у рядку {line_num}: '{clean_line}'")

            surname = parts[0].strip()
            name = parts[1].strip()
            grade = float(parts[2].strip())  # Може викликати ValueError, якщо оцінка не число
            students.append((surname, name, grade))

    return students


def main():
    grades_filepath = get_file_path("grades.txt")

    # Читання grades.txt, виведення вмісту та обчислення середнього балу ===
    try:
        with open(grades_filepath, "r", encoding="utf-8") as file:
            print("=== Вміст файлу grades.txt ===")
            print(file.read().strip())
            print("=" * 30)

        students_data = parse_grades(grades_filepath)

        if not students_data:
            print("Файл порожній, немає даних для обчислення.")
            return

        total_score = sum(student[2] for student in students_data)
        average_score = total_score / len(students_data)
        print(f"\nСередній бал групи: {average_score:.2f}")

    except FileNotFoundError:
        print("Помилка: Файл 'grades.txt' не знайдено!")
        return
    except ValueError as e:
        print(f"Помилка обробки числових даних: {e}")
        return
    except IOError as e:
        print(f"Помилка введення-виведення при читанні файлу: {e}")
        return

    # Запит прізвища та запис оцінки у student_grade.txt ===
    target_surname = input("\nВведіть прізвище студента для пошуку (наприклад, Бойко): ").strip()
    output_filepath = get_file_path("student_grade.txt")

    found_students = [s for s in students_data if s[0].lower() == target_surname.lower()]

    try:
        with open(output_filepath, "w", encoding="utf-8") as out_file:
            if found_students:
                for surname, name, grade in found_students:
                    result_str = f"Студент: {surname} {name}, Оцінка: {grade}\n"
                    out_file.write(result_str)
                print(f"Дані успішно записано у файл 'student_grade.txt'.")
            else:
                out_file.write(f"Студента з прізвищем '{target_surname}' не знайдено.\n")
                print(f"Студента '{target_surname}' не знайдено. Відповідний запис зроблено у 'student_grade.txt'.")
    except IOError as e:
        print(f"Помилка запису у файл 'student_grade.txt': {e}")

    # Запит імені файлу та пошук студента з найвищою оцінкою ===
    user_filename = input("\nВведіть ім'я файлу для пошуку найкращого студента (наприклад, grades.txt): ").strip()
    user_filepath = get_file_path(user_filename)

    try:
        # Виводиться вміст вказаного користувачем файлу
        with open(user_filepath, "r", encoding="utf-8") as u_file:
            print(f"\n--- Вміст файлу '{user_filename}' ---")
            print(u_file.read().strip())
            print("-" * 30)

        # Шукається студент з найвищою оцінкою
        parsed_user_data = parse_grades(user_filepath)
        if parsed_user_data:
            best_student = max(parsed_user_data, key=lambda item: item[2])
            print(f"Студент з найвищою оцінкою: {best_student[0]} {best_student[1]} — {best_student[2]} балів.")
        else:
            print("У вказаному файлі відсутні записи про студентів.")

    except FileNotFoundError:
        print(f"Помилка: Файл '{user_filename}' не знайдено!")
    except ValueError as e:
        print(f"Помилка формату даних у файлі '{user_filename}': {e}")
    except IOError as e:
        print(f"Помилка читання файлу '{user_filename}': {e}")


if __name__ == "__main__":
    main()
