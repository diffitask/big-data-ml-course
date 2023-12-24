## Kafka

### Поднимаем окружение

Сборка:

```commandline
docker-compose build
```

Поднимаем наши компоненты: jobmanager, taskmanager, kafka, zookeper

```commandline
docker-compose up -d
```

Смотрим процесс:

```commandline
docker-compose ps
```
Проверим в браузерном UI:
```
http://localhost:8081/#/overview

```

Чтобы все погасить:

```commandline
docker-compose down -v
```

---

### Создание очереди

- Указываем адрес брокера: 'kafka' + порт -- это внутри сети докера.
- Создать новый топик + имя топика -- это просто название очереди. Очереди обычно разделяем по топикам, чтобы не замешивать все данные в одном месте. Разные топики отчевают за хранение данных под разные задачи.
- Задать параметры 'partitions' и 'replication_factor'

```commandline
docker-compose exec kafka kafka-topics.sh --bootstrap-server kafka:9092 --create --topic itmo --partitions 1 --replication-factor 1
```

Проверим, правильно ли создалась наша очередь в kafka:

```commandline
docker-compose exec kafka kafka-topics.sh --bootstrap-server kafka:9092 --describe itmo  
```

Можем изменить число партиций нашей очереди:
```commandline
 docker-compose exec kafka kafka-topics.sh --bootstrap-server kafka:9092 --alter --topic itmo --partitions 2

```

```commandline
docker-compose exec jobmanager ./bin/flink run -py /opt/pyflink/device_job.py -d  
```
