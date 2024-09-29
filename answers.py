from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import time

# Preguntar cuantas veces quiere que se responda la encuesta
answers = int(input("N° de respuestas: "))

# Bucle de la cantidad de veces que se respondera la encuesta segun lo ingresado
for i in range(answers):
    print(f"RESPUESTA N° {i}")
    # Generar correo aleatorio
    def generar_correo():
        nombre = ''.join(random.choices(string.ascii_lowercase, k=7))
        dominio = random.choice(['gmail.com', 'hotmail.com', 'yahoo.com'])
        return f"{nombre}@{dominio}"

    # Configuración del navegador
    driver = webdriver.Chrome() # chromedriver

    # Abre el formulario
    driver.get("https://forms.office.com/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAMAADWvCtNUQzJSUVJSWkJQMjhKQUM0MzFMVlM0NVZCTC4u") # formulario de ejemplo

    # Esperar que cargue el formulario
    time.sleep(2)

    # Esperar hasta que el campo de correo esté disponible usando 'data-automation-id'
    correo_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@data-automation-id='textInput']"))
    )
    correo_input.send_keys(generar_correo())

    # Seleccionar opción aleatoria para cada pregunta de opción única
    for pregunta_index in range(1, 16):  # Asumiendo que hay 16 preguntas
        try:
            # Encontrar la pregunta actual basada en el index
            pregunta_xpath = f"(//div[@role='radiogroup'])[{pregunta_index}]"
            opciones = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, pregunta_xpath + "//input[@type='radio']"))
            )
            
            # Si hay opciones disponibles, seleccionar una aleatoria
            if opciones:
                opcion_aleatoria = random.choice(opciones)
                driver.execute_script("arguments[0].scrollIntoView(true);", opcion_aleatoria)  # Asegurarse de que sea visible
                opcion_aleatoria.click()
                time.sleep(0.5)
                print(f"Se respondió correctamente la pregunta {pregunta_index + 1}")
            else:
                print(f"No se encontraron opciones para la pregunta {pregunta_index + 1}")
                
        except Exception as e:
            print(f"Error al seleccionar la opción para la pregunta {pregunta_index + 1}: {e}")

    # Enviar el formulario
    submit_button = driver.find_element(By.XPATH, "//button[@data-automation-id='submitButton']")
    submit_button.click()

    # Esperar unos segundos antes de cerrar el navegador
    time.sleep(3)
    driver.quit()

print("\nFIN DEL PROGRAMA, GRACIAS :)")