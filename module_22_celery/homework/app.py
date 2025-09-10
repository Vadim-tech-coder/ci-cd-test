"""
В этом файле будет ваше Flask-приложение
"""

import os
import zipfile

from celery import group
from flask import Flask, render_template, request, jsonify

from mail import send_email

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads/images"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/blur', methods = ['GET', 'POST'])
def upload_and_blur_images():
    if request.method == 'POST':
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        images = request.files.getlist('files')
        file_names = []
        if images:
            for image in images:
                image.save(os.path.join(UPLOAD_FOLDER, image.filename))
                file_names.append(f"{UPLOAD_FOLDER}/{image.filename}")
                print("Image path is:", f"{UPLOAD_FOLDER}/{image.filename}")
            from celery_tasks import process_images
            task_group = group(process_images.s(img_filename) for img_filename in file_names)
            result = task_group.apply_async()
            result.save()
            return render_template('status_page.html', group_id=result.id)
        return render_template('status_page.html')
    return render_template('load_images.html')


@app.route('/status/<string:group_id>', methods = ['GET'])
def get_status(group_id):
    from celery_tasks import celery_ap
    result = celery_ap.GroupResult.restore(group_id)

    if result:
        status = result.completed_count() / len(result)

        if int(status) == 1:
            zip_file_name = "blurred_photos.zip"
            zip_object = zipfile.ZipFile(zip_file_name, 'w')
            for file in result:
                print(file, file.info)
                zip_object.write(file.info, compress_type=zipfile.ZIP_DEFLATED)
            zip_object.close()

        else:
            return f"Не все задачи обработаны! {result.completed_count()} из {len(result)}"

        info = {
            "task_count": len(result),
            "completed": result.completed_count(),
            "message": f"На ваш email было отправлено письмо с архивом изображений - {zip_file_name}"
        }
        send_email(group_id, receiver='vadimbaz25@gmail.com', filename=zip_file_name)
        return render_template('status_page.html', info=info)
    return f"group_id: {group_id}"



import os
import zipfile
from flask import request, render_template
from celery.result import GroupResult

@app.route('/status', methods=['GET', 'POST'])
def submit_and_get_status():
    if request.method == 'POST':
        group_id = request.form.get('group_id')
        if not group_id:
            error = "Пожалуйста, введите идентификатор группы."
            return render_template('status_task.html', error=error)

        try:
            result = GroupResult.restore(group_id)
        except AttributeError as e:
            # Здесь ловим ошибку DisabledBackend
            error = ("Ошибка доступа к результатам задач.")
            return render_template('status_task.html', error=error)

        if not result or len(result) == 0:
            error = f"Группа с ID {group_id} не найдена."
            return render_template('status_task.html', error=error)

        result = GroupResult.restore(group_id)
        if not result:
            error = f"Группа с ID {group_id} не найдена."
            return render_template('status_task.html', error=error)

        total_tasks = len(result)
        completed = result.completed_count()
        status = completed / total_tasks if total_tasks > 0 else 0

        if status == 1.0:
            zip_file_name = "blurred_photos.zip"
            with zipfile.ZipFile(zip_file_name, 'w', compression=zipfile.ZIP_DEFLATED) as zip_object:
                for task_result in result.results:
                    file_path = task_result.result  # предполагается, что здесь путь к файлу
                    if file_path and os.path.exists(file_path):
                        zip_object.write(file_path, arcname=os.path.basename(file_path))

            # Отправляем email (проверьте реализацию send_email)
            send_email(group_id, receiver='vadimbaz25@gmail.com', filename=zip_file_name)

            info = {
                "task_count": total_tasks,
                "completed": completed,
                "message": f"На ваш email было отправлено письмо с архивом изображений - {zip_file_name}"
            }
            return render_template('status_task.html', info=info, group_id=group_id)

        else:
            message = f"Не все задачи обработаны! {completed} из {total_tasks}"
            return render_template('status_task.html', message=message, group_id=group_id)

    # GET-запрос — отображаем форму
    return render_template('status_task.html')

email_addresses = []

@app.route('/subscribe', methods = ['GET', 'POST'])
def subcribe():
    if request.method == 'POST':
        email = request.form.get('email')
        if email in email_addresses:
            error = 'Такой email уже подписан на рассылку'
            return  render_template('input_email.html', error = error)
        email_addresses.append(email)
        success = "Вы успешно подписались на рассылку!"
        return render_template('input_email.html', success = success)
    return render_template('input_email.html')

@app.route('/unsubscribe', methods = ['GET', 'POST'])
def unsubscribe():
    if request.method == 'POST':
        email = request.form.get('email')
        if email in email_addresses:
            email_addresses.remove(email)
            unsubscribe = "Вы отменили подсписку на email рассылку!"
            return render_template('unsubscribe.html', unsubscribe=unsubscribe)
        error_unsubscribe = f'Пользователь с таким email {email} не найден в списках рассылки!'
        return render_template('unsubscribe.html', error_unsubscribe=error_unsubscribe)
    return render_template('unsubscribe.html')


if __name__ == '__main__':
    app.run(debug=True)