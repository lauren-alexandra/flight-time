import sys

def main():

    course_schedule = {
        'CSC502': {
            'course_name': 'Ethical Leadership in Software Development',
            'term': '22SD',
            'instructor': 'Faculty',
            'credits': 3,
            'textbook': {
                'title': 'Ethical reasoning in big data: An exploratory analysis',
                'ISBN': 9783319284200
            }
        },
        'CSC505': {
            'course_name': 'Principles of Software Development',
            'term': '21WD',
            'instructor': 'Dr. Pubali Banerjee',
            'credits': 3,
            'textbook': {
                'title': 'Software Engineering: A Practitioner’s Approach',
                'ISBN': 9781259872976
            }
        },
        'CSC506': {
            'course_name': 'Design and Analysis of Algorithms',
            'term': '22SB',
            'instructor': 'Faculty',
            'credits': 3,
            'textbook': {
                'title': 'Design and Analysis of Algorithms',
                'ISBN': 9781394012268
            }
        },
        'CSC507': {
            'course_name': 'Foundations of Operating Systems',
            'term': '21WB',
            'instructor': 'Dr. Lori Farr',
            'credits': 3,
            'textbook': {
                'title': 'Operating Systems',
                'ISBN': 9780134670959
            }
        },
        'CSC510': {
            'course_name': 'Foundations of Artificial Intelligence',
            'term': '21WB',
            'instructor': 'Dr. Brian Holbert',
            'credits': 3,
            'textbook': {
                'title': 'Analytics, Data Science, & Artificial Intelligence',
                'ISBN': 9780135192016
            }
        },
        'CSC515': {
            'course_name': 'Foundations of Computer Vision',
            'term': '22SB',
            'instructor': 'Faculty',
            'credits': 3,
            'textbook': {
                'title': 'Computer vision and image processing: Fundamentals and applications',
                'ISBN': 9780815370840
            }
        },
        'CSC525': {
            'course_name': 'Principles of Machine Learning',
            'term': '21WD',
            'instructor': 'Dr. Brandon Bass',
            'credits': 3,
            'textbook': {
                'title': 'Machine learning with Python for everyone',
                'ISBN': 9780134845623
            }
        }
    }

    available_courses = ', '.join(course_schedule)

    def get_course():
        need_course = True

        while need_course:
            need_course = False
            print(f'Available courses: {available_courses}\n')
            course_no = input('Enter a course code from the available courses, e.g. CSC505: ')
            if course_no.strip() not in course_schedule.keys():
                print('Course code not found. Please try again.')
                need_course = True

        return course_no

    course = get_course()
    session_info = course_schedule[course]
    course_name = 'Name: ' + session_info['course_name']
    term = 'Term: ' + session_info['term']
    instructor = 'Instructor: ' + session_info['instructor']
    credits = 'Credits: ' + str(session_info['credits'])
    textbook = 'Textbook: ' + session_info['textbook']['title'] + '. ISBN: ' + str(session_info['textbook']['ISBN']) + '.'

    print(f'\n{course_name}\n{term}\n{instructor}\n{credits}\n{textbook}')

    sys.exit()

if __name__ == "__main__":
    main()