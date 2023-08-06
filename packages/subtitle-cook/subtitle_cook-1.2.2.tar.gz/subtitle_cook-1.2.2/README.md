# Manual subtitle_cook

- Versión estable: 1.2.1

## Descripción
**subtitle_cook** es una herramienta para transformación de subtítulos. Fundamentalmente
permite:
    - Cambiar la segmentación de los subtítulos (es decir, la forma en que se
      divide el texto secuencialmente). Principalmente la herramienta intentará que los
      segmentos coincidan con la puntuación para lograr un flujo más natural del
      discurso.
    - Añadir de forma automática signos de puntuación a un archivo SRT que carezca de
      ellos.
    - Parametrizar algunos aspectos que afectan a la segmentación del subtítulo: tamaño
      máximo de línea o símbolos de puntuación a utilizar para marcar el cambio de
      segmento.

## ¿Es el mismo proyecto que *subtitle_resegmenter*?
Sí, pero evolucionado y más complejo.

Este proyecto se llamaba anteriormente **subtitle_resegmenter**, ya que estaba
dirigido exclusivamente a resegmentar o reestructurar subtítulos, es decir,
reordenar el texto de los segmentos para que cada uno de ellos cumpliese
ciertos criterios (acabar el segmento en un signo de puntuación, intentar
ajustarse a un nº determinado de caracteres por segmento...).

Con posterioridad se decidió fusionarlo con un proyecto con el que compartía
cierto ámbito de acción, llamado **automatic_punctuator**. Este proyecto
utilizaba la librería **rpunct** para añadido automatizado de signos de
puntuación a textos y la adaptaba para su aplicación a archivos de tipo SRT.

Al juntar los dos proyectos se obtiene uno mayor que permite aplicar la
puntuación automática como paso previo a la resegmentación, de tal modo que,
partiendo de un SRT sin ninguna puntuación, podemos acabar obteniendo un
archivo de subtítulos puntuado y en el que los segmentos intentarán coincidir
lo mejor posible con las frases delimitadas por dicha puntuación.

## Uso
La herramienta se utiliza llamando al script de arranque, **__main__.py**. Deberá
ejecutarse con un intérprete Python (preferiblemente entorno virtual) que cumpla los
requisitos del siguiente apartado

### Instalación
Para utilizar el proyecto se requiere:
- Python 3.7 (cualquier otra versión puede dar problemas)
- Instalar las dependencias indicadas en **./requirements/** (las mínimas necesarias son
  las descritas en **prod.txt**)
- Añadir a **./config/** los archivos **config.ini** necesarios. Cada uno de estos
  archivos incluye las claves para conectar con un servidor de TransLectures.
- Instalar un pequeño entorno Python2 dentro de **./cook/ttp_client/**:
    1. Crea un entorno virtual:

        `python2 -m virtualenv ./cook/ttp_client/python2_venv`

    2. Instala en el las dependencias:

    ```
    ./cook/ttp_client/python2_venv/bin/python ./cook/ttp_client/python2_requirements.txt
    ```

### Sintaxis

```
python ./main.py [-h] [-l LANGS] [--mock] [-v] [-p] [-m SPLITTING_MODE]
   [-ll LINE_LENGTH] id
```

Donde:
    - **-h**: mostrar la ayuda sintáctica
    - **-l/--langs**: pasar una lista de idiomas cuyos subtítulos se quieren resegmentar
      con códigos de 2 caracteres separados por comas. Por ejemplo: "ca,en,es"
    - **--mock**: activa el modo de prueba, que realiza las operaciones sobre un vídeo
      de test
    - **-v/--verbose**: aumenta la verbosidad. Acepta varios niveles incrementales según
      se van añadiendo "v"s
    - **-p/--punctuate**: activar la fase de adición automática de signos de puntuación.
      Solo funciona para el idioma inglés ("en")
    - **-m/--splitting-mode**: indicar el tipo de política a seguir para la segmentación
      de subtítulos. De momento está definida como sigue: 1-Separar segmentos solo por
      puntos, 2-Separar también por los siguientes signos: **!,?;:**, 3-Separar también
      por espacios en blanco.
    - **-ll/--line-length**: longitud de línea máxima deseada. No se aplica de forma
      absolutamente estricta, sino combinada con el *splitting mode*, intentando
      permanecer por debajo de este valor pero sin partir el texto allá donde no se
      permite.
    - **id**: el único parámetro obligatorio es el identificador de vídeo en PoliMedia

### Ejemplos
1. Resegmentar los subtítulos en catalán y castellano:

    `python main.py -l ca,es 07370e30-cf98-11ec-8320-41acd79e78c3`

2. Repuntuar los subtítulos en inglés y después resegmentar inglés, catalán y castellano

    `python main.py -p -l en,ca,es 07370e30-cf98-11ec-8320-41acd79e78c3`

3. Misma operación anterior pero intentando que los segmentos de texto no superen los
   60 caracteres y permitiendo la ruptura por símbolos de puntuación y espacios (lo cual
   dará lugar a segmentos bastante cortos de forma generalizada)

    `python main.py -p -l en,ca,es -ll 60 -m 3 07370e30-cf98-11ec-8320-41acd79e78c3`
