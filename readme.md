# CHatBot La Maxima

Parcial para la materia de inteligencia artificial
## Requerimiento 

Estaremos utilizan [anaconda] (https://www.anaconda.com/products/individual) y [python] (https://www.python.org/downloads/)

## Instalacion

Creamos el entorno de anaconda, este proyecto utilza la version 3.6 de python
```sh
conda create -n chat python=3.6
```
Despues de instalada activamos el entorno
```sh
conda activate chat
```
Los paquete que vamos a instalar son:

```sh
pip install nltk
pip install tensorflow==1.14.0
pip install numpy
pip install tflearn==0.3.2
```

Si el paquete nltk le da problemas con el punkt utilizar el siguiente comando
```python
nltk.download('punkt')
```
Si quiere utilizar la API de discor intalar este paquete en su ambiente anaconda
```sh
pip install discord
```




