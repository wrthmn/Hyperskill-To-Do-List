from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from datetime import timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):

    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default="default_value")
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def format_date(date):

    date_string = datetime.strftime(date, '%d %b')

    if date.day < 10:

        date_string = date_string.replace('0', '')

    return date_string


def add_task():

    new_task = input("Enter task\n")
    new_row = Table(task=new_task)

    task_deadline = input("Enter deadline\n")

    try:

        new_row.deadline = datetime.strptime(task_deadline, "%Y-%m-%d")

    except ValueError:

        print("\nWrong date format. Must be: YYYY-MM-DD. The current date is set.")

    session.add(new_row)
    session.commit()
    print("\nThe task has been added!\n")


def delete_task():

    print("Choose the number of the task you want to delete:")
    rows = session.query(Table).order_by(Table.deadline).all()

    if rows:

        for row in rows:

            print(f"{row.id}. {row}. {format_date(row.deadline)}")

        task_id = input()

        session.query(Table).filter(Table.id == task_id).delete()
        session.commit()

        print("The task has been deleted!\n")

    else:

        print("No tasks to delete!\n")


def show_day_tasks(day, today=False):

    print(f"Today {format_date(day)}:" if today else f"{datetime.strftime(day, '%A')} {format_date(day)}:")
    rows = session.query(Table).filter(Table.deadline == day.date()).all()

    if rows:

        for row in rows:

            print(f"{row.id}. {row}.")

        print()

    else:

        print("Nothing to do!\n")


def show_week_tasks():

    day = datetime.today()

    print("Week's tasks:")

    for i in range(7):

        show_day_tasks(day)

        day += timedelta(days=1)


def show_all_tasks():

    print("All tasks:")
    rows = session.query(Table).order_by(Table.deadline).all()

    if rows:

        for row in rows:

            print(f"{row.id}. {row}. {format_date(row.deadline)}")

        print()

    else:

        print("Nothing to do!\n")


def show_missed_tasks():

    missed_tasks = session.query(Table).filter(Table.deadline < datetime.today()).all()

    print("Missed tasks:")

    if missed_tasks:

        for task in missed_tasks:

            print(f"{task.id}. {task}. {format_date(task.deadline)}")

        print()

    else:

        print("Nothing is missed!\n")


while True:

    command = input("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit\n""")

    print()

    if command == "1":

        today = datetime.today()
        show_day_tasks(today, today=True)

    elif command == "2":

        show_week_tasks()

    elif command == "3":

        show_all_tasks()

    elif command == "4":

        show_missed_tasks()

    elif command == "5":

        add_task()

    elif command == "6":

        delete_task()

    elif command == "0":

        print("Bye!")
        break

    else:

        print("Unknown command.\n")
