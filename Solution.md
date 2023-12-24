# Домашнее задание 3: Flink

## Блок 1: Flink checkpoint

### Развертывание Flink + Kafka
Поднимаем окружение:
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
<img src="homework/screenshots/block-1/2-docker-compose-ps-res.png">

Проверяем, что во Flink UI, что все корректно создано:
```
http://localhost:8081/#/overview

```
<img src="homework/screenshots/block-1/1-docker-build-res.png">

Создаем очередь 'hse2023':
```commandline
docker-compose exec kafka kafka-topics.sh --bootstrap-server kafka:9092 --create --topic hse2023 --partitions 1 --replication-factor 1
```
<img src="homework/screenshots/block-1/3-create-topic.png">

Проверим, правильно ли создалась очередь -- смотрим описание очереди:
```commandline
docker-compose exec kafka kafka-topics.sh --bootstrap-server kafka:9092 --describe itmo  
```
<img src="homework/screenshots/block-1/4-topic-desc.png">


