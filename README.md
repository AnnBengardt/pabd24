# Предиктивная аналитика больших данных

Учебный проект для демонстрации основных этапов жизненного цикла проекта предиктивной аналитики.  

## Installation 

Клонируйте репозиторий, создайте виртуальное окружение, активируйте и установите зависимости:  

```sh
git clone https://github.com/yourgit/pabd24
cd pabd24
python -m venv venv

source venv/bin/activate  # mac or linux
.\venv\Scripts\activate   # windows

pip install -r requirements.txt
```

## Usage

### 1. Сбор данных о ценах на недвижимость на однокомнатные, двухкомнатные и трехкомнатные квартиры в Москве 
```sh
python parse_cian.py
```  

### 2. Выгрузка данных в хранилище S3. 
Принимает на вход наименования файлов, которые необходимо выгрузить 
Для доступа к хранилищу скопируйте файл `.env` в корень проекта.  

```sh
python upload_to_s3.py
```   
Или
```sh
python upload_to_s3.py -i data/raw/1_2024-05-14_20-14.csv
```   

### 3. Загрузка данных из S3 на локальную машину.
Принимает на вход наименования файлов, которые необходимо скачать 

```sh
python download_from_s3.py
```   
Или
```sh
python download_from_s3.py -i data/raw/1_2024-05-14_20-14.csv
```   

### 4. Предварительная обработка данных.
Сохраняет файлы с train и val выборками в data/proc. Принимает на вход размер train выборки (float), наименования файлов, которые необходимо предобработать

```sh
python preprocess_data.py
```   
Или
```sh
python preprocess_data.py -s 0.8 -i data/raw/1_2024-05-14_20-14.csv
``` 

### 5. Обучение модели 
Запуск обучения модели (также проводит и валидацию из скрипта test_model.py при локальном запуске). На вход можно передать путь для сохранения весов обученной модели.

```sh
python train_model.py
```   
Или
```sh
python train_model.py -m models/linear_regression_v02.joblib
```

Запуск валидации модели. На вход можно передать путь, где хранится обученная модель.

```sh
python test_model.py
```   
Или
```sh
python test_model.py -m models/linear_regression_v02.joblib
``` 

### 6. Запуск приложения flask 
Запуск приложения локально

```sh
python predict_app.py
```

Запуск приложения при деплое на сервере gunicorn на виртуальной машине

```sh
gunicorn -b 0.0.0.0 src.predict_app:app --daemon
```

Адрес задеплоенного приложения (Endpoint)
http://192.144.13.190:8000/predict

### 7. Использование сервиса через веб интерфейс 
Для использования сервиса используйте файл `app/index.html`.  index.html обращается к Endpoint на сервере, указанному в п.6
