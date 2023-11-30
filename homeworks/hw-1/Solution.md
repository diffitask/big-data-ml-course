# Домашнее задание 1

## Блок 1. Развертывание локального кластера Hadoop

**Задание**:

1. Развернуть локальный кластер в конфигурации 1 NN, 1-3 DN (в зависимости от доступных мощностей ноутбука), 1-2 NM, 1
   RM.
   Можно использовать готовый docker-compose/ делать по инструкции.
2. Изучить настройки и состояние NM и RM в веб-интерфейсе. Сделать скриншоты NN и RM. Скриншоты добавить в репозиторий.
3. Развернуть юпитер. Создать ноутбук.
4. Из него с помощью питон кода (pyarrow), либо с помощью команд “hadoop fs” загрузить любой файл с данными на hdfs.
5. В отдельных ячейках выполнить команду !hadoop fs -ls (путь до файла) + !hadoop fs -cat
6. Запустить команду !hadoop jar /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 15 1800
7. Ноутбук с результатами, а также скриншоты запуска с RM добавить в репозиторий

**Решение**:

Был развернут кластер в конфигурации 1 NN, 1 DN, 1 NM, 1 RM.

Name node info: http://localhost:9870/dfshealth.html#tab-overview
<img src="block-1/screenshots/name-node-p1.png">
<img src="block-1/screenshots/name-node-p2.png">
<img src="block-1/screenshots/name-node-p3.png">

Node manager: http://localhost:8042/node/node
<img src="block-1/screenshots/node-manager.png">

Resource manager: http://localhost:8088/cluster/cluster
<img src="block-1/screenshots/resource-manager.png">

С помощью библиотеки pyarrow был создан файл, содержащий текст песни.
Ноутбук с
результатами: [block-1.ipynb](https://github.com/diffitask/big-data-ml-course/blob/hw-1/homeworks/hw-1/block-1/block-1.ipynb)

## Блок 2

Требуется написать несколько map-reduce задач. 
Для написания использовать питон и (по желанию) фреймворк mrjob.

Задачи следует протестировать как локально, так и на кластере.

В качестве результатов к каждой задаче нужно добавить в ваш репозиторий (результаты каждой задачи в отдельной папке):
- Скриншоты запуска из RM.
- Ноутбук с кодом mapred, командами запуска и диаграммами (если требуются).
- Результаты запуска в виде файлов.


### Задача 1: Болтун - находка для шпиона империи

**Задание**:

Требуется найти топ самых разговорчивых персонажей - посчитать количество реплик у каждого, и выбрать 20 с самым большим
значением.
Результаты отсортировать по количеству реплик (по убыванию).
Предоставить результаты для каждого эпизода, и отдельно по всем трем.

Результаты из hdfs должны быть прочитаны в ноутбуке и выведены на диаграмму.
Стоит посмотреть в доке методы
mapper_init
mapper_final
reducer_init
reducer_final

**Решение**:

- Ноутбук: [block-2.ipynb](https://github.com/diffitask/big-data-ml-course/blob/hw-1/homeworks/hw-1/block-2/block-2.ipynb)
- MapRed .py файл: [most_talkative_characters.py](https://github.com/diffitask/big-data-ml-course/blob/hw-1/homeworks/hw-1/block-2/most_talkative_characters.py)
- Результаты выполнения: [task-1](https://github.com/diffitask/big-data-ml-course/tree/hw-1/homeworks/hw-1/block-2/results/task-1)

### Задача 2: Воодушевляющая речь

**Задание**:

Требуется найти самую длинную фразу каждого персонажа. Результат должен содержать пары (имя персонажа: его самая длинная фраза), а так же должен быть обратно отсортирован по длине фразы.

Предоставить результаты для каждого эпизода, и отдельно по всем трем.

**Решение**:

- Ноутбук: [block-2.ipynb](https://github.com/diffitask/big-data-ml-course/blob/hw-1/homeworks/hw-1/block-2/block-2.ipynb)
- MapRed .py файл: [longest_character_phrase.py](https://github.com/diffitask/big-data-ml-course/blob/hw-1/homeworks/hw-1/block-2/longest_character_phrase.py)
- Результаты выполнения: [task-2](https://github.com/diffitask/big-data-ml-course/tree/hw-1/homeworks/hw-1/block-2/results/task-2)

### Задача 3: Кто о чем, а ситх об абсолюте

**Задание**:

В данной задаче мы будем проводить статистический анализ текста эпизодов. 

Каждое предложение в тексте должно пройти предварительную очистку: быть приведено к lowercase-у, быть очищено от грамматики и пунктуации. После очистки предложение должно быть разбито на bigram-ы.
Ответ должен содержать в себе 20 самых частых биграм.

Предоставить результаты для каждого эпизода, и отдельно по всем трем.

Очистка должна быть произведена в коде mapper-а, на reducer должны приходить уже готовые bigram-ы. 

Результат данной части может отличаться в зависимости от качества предварительной очистки, это норма. 

 Результаты каждого запуска прочитать и вывести на диаграмму любым удобным способом.

Для обработки текста обязательно использовать библиотеку nltk. https://www.nltk.org/

Внимание!

Помните, что мы в распределенной системе. Вам необходимо установить зависимость nltk не только в юпитере, но так же на nodemanager!

На стороне маппера возможно потребуется произвести доп. инициализацию библиотеки:

def mapper_init(self):
     nltk.download('punkt')
     nltk.download('stopwords')

**Решение**:

- Ноутбук: [block-2.ipynb](https://github.com/diffitask/big-data-ml-course/blob/hw-1/homeworks/hw-1/block-2/block-2.ipynb)
- MapRed .py файл: [top_frequent_bigrams.py](https://github.com/diffitask/big-data-ml-course/blob/hw-1/homeworks/hw-1/block-2/top_frequent_bigrams.py)
- Результаты выполнения: [task-3](https://github.com/diffitask/big-data-ml-course/tree/hw-1/homeworks/hw-1/block-2/results/task-3)






