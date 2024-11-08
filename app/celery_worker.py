from celery import Celery

celery = Celery(__name__, broker="redis://redis:6379/0")

@celery.task
def background_task(task_id: int, task_title: str):
    print(f"Задача с id={task_id} и name='{task_title}' была успешно создана")
