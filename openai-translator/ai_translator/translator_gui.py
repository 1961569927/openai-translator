from nicegui import ui
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import ArgumentParser, ConfigLoader
from model import  OpenAIModel
from translator import PDFTranslator

def handle_submit():
    """提交按钮回调函数"""
    # 逐个获取输入值

    openai_model = openai_model_input.value
    openai_api_key = openai_api_key_input.value
    book = book_input.value
    file_format = file_format_input.value
    target_language = language_input.value

    config_loader = ConfigLoader("/root/tmp/pycharmProject/openai-translator/config.yaml")
    config = config_loader.load_config()
    model_name = openai_model if openai_model else config['OpenAIModel']['model']
    api_key = openai_api_key if openai_api_key else config['OpenAIModel']['api_key']
    model = OpenAIModel(model=model_name, api_key=api_key)

    pdf_file_path = book if book else config['common']['book']
    file_format = file_format if file_format else config['common']['file_format']

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(pdf_file_path, file_format,target_language)

    # 显示成功提示
    ui.notify("参数已提交，开始处理翻译任务！", type='positive')


# 创建界面
with ui.column().classes('w-full max-w-2xl mx-auto gap-4'):
    # 标题
    ui.label('Translate English PDF book to Chinese').classes('text-2xl font-bold text-center mb-8')

    # 输入区域
    with ui.card().classes('w-full p-4 gap-4'):

        with ui.row().classes('w-full items-center'):
            ui.label('openai_model').classes('w-32 font-medium')
            openai_model_input = ui.input(placeholder='请输入openai_model').classes('flex-grow')

        with ui.row().classes('w-full items-center'):
            ui.label('openai_api_key').classes('w-32 font-medium')
            openai_api_key_input = ui.input(placeholder='请输入openai_api_key').classes('flex-grow')

        with ui.row().classes('w-full items-center'):
            ui.label('book').classes('w-32 font-medium')
            book_input = ui.input(placeholder='请输入book').classes('flex-grow')

        with ui.row().classes('w-full items-center'):
            ui.label('file_format').classes('w-32 font-medium')
            file_format_input = ui.input(placeholder='请输入file_format').classes('flex-grow')

        with ui.row().classes('w-full items-center'):
            ui.label('language').classes('w-32 font-medium')
            language_input = ui.input(placeholder='请输入language').classes('flex-grow')

    # 提交按钮
    ui.button('提交', on_click=handle_submit).classes('w-32 h-10 mx-auto')

# 运行配置
ui.run(
    title='PDF翻译器',
    host='0.0.0.0',
    port=8080,
    reload=False
)