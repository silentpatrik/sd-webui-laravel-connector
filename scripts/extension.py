import gradio as gr
import mysql.connector
from mysql.connector import Error

import modules.scripts as scripts
from modules import script_callbacks, errors
from modules.shared import opts, OptionInfo
import os 
autoSave = False

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST', 'default_host'),  # Use 'default_host' if DB_HOST is not set
    'database': os.getenv('DB_DATABASE', 'default_database'),  # Default fallbacks are just examples
    'user': os.getenv('DB_USER', 'default_user'),
    'password': os.getenv('DB_PASSWORD', 'default_password')
}


def save_image_data(filename, text=""):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            db_cursor = connection.cursor()
            sql_insert_query = """INSERT INTO `image_data` (`filename`, `text`) VALUES (%s,%s)"""
            values = (filename, text)
            db_cursor.execute(sql_insert_query, values)
            connection.commit()
            print("Image data saved to MySQL database")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            db_cursor.close()
            connection.close()

def onChangeCheckbox(value):
    global autoSave
    autoSave = value

class AutoSaveScript(scripts.Script):
    def show(self, _):
        return scripts.AlwaysVisible

    def ui(self, _):
        autoSaveCheckbox = gr.Checkbox(False, label="Enable auto save")
        autoSaveCheckbox.change(onChangeCheckbox, inputs=autoSaveCheckbox)

def on_image_saved(imageSaveParams: script_callbacks.ImageSaveParams):
    global autoSave
    if autoSave == False or "grid" in imageSaveParams.filename:
        return
    try:
        save_image_data(imageSaveParams.filename)
    except Error as e:
        errors.report(f"Error saving image data to database: {e}", exc_info=True)

script_callbacks.on_image_saved(on_image_saved)

def on_after_component(component, **_):
    # This placeholder exists to demonstrate where additional component interactions could be added.
    pass

script_callbacks.on_after_component(on_after_component)

def on_ui_settings():
    # This placeholder demonstrates where UI settings could be implemented.
    pass

script_callbacks.on_ui_settings(on_ui_settings)
