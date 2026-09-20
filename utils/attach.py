import os
import json
import allure
from allure_commons.types import AttachmentType


def add_screenshot(driver):
    png = driver.get_screenshot_as_png()
    allure.attach(body=png, name='screenshot', attachment_type=AttachmentType.PNG, extension='.png')


def add_logs(driver):
    if driver.capabilities.get("browserName") != "chrome":
        return

    try:
        log = "".join(f'{text}\n' for text in driver.get_log(log_type='browser'))
        allure.attach(log, 'browser_logs', AttachmentType.TEXT, '.log')
    except Exception as e:
        print(f"Не удалось получить browser logs: {e}")


def add_html(driver):
    html = driver.page_source
    allure.attach(html, 'page_source', AttachmentType.HTML, '.html')


def add_video(driver):
    selenoid_url = os.getenv("SELENOID_URL")
    video_url = f"https://{selenoid_url}/video/" + driver.session_id + ".mp4"
    html = "<html><body><video width='100%' height='100%' controls autoplay><source src='" \
           + video_url \
           + "' type='video/mp4'></video></body></html>"
    allure.attach(html, 'video_' + driver.session_id, AttachmentType.HTML, '.html')


def attach_api_response(response):
    request = response.request

    allure.attach(
        request.method,
        name="Request method",
        attachment_type=allure.attachment_type.TEXT
    )

    allure.attach(
        request.url,
        name="Request URL",
        attachment_type=allure.attachment_type.URI_LIST
    )

    if request.headers:
        allure.attach(
            json.dumps(
                dict(request.headers),
                indent=4,
                ensure_ascii=False
            ),
            name="Request headers",
            attachment_type=allure.attachment_type.JSON
        )

    if request.body:
        body = request.body

        if isinstance(body, bytes):
            body = body.decode("utf-8")

        allure.attach(
            body,
            name="Request body",
            attachment_type=allure.attachment_type.JSON
        )

    allure.attach(
        str(response.status_code),
        name="Response status code",
        attachment_type=allure.attachment_type.TEXT
    )

    try:
        allure.attach(
            json.dumps(
                response.json(),
                indent=4,
                ensure_ascii=False
            ),
            name="Response body",
            attachment_type=allure.attachment_type.JSON
        )
    except ValueError:
        allure.attach(
            response.text,
            name="Response body",
            attachment_type=allure.attachment_type.TEXT
        )