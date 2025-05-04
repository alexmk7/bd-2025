# MRJob

В файле `job.py` простой код для подсчета количества слов в текстовых данных. Для того, чтобы запустить локально:
```bash
python3 job.py < ../../data/hive.txt
```


Для того, чтобы запустить в песочнице `Hadoop`:
1. Запустите bash в контексте контейнера
```bash
docker exec -it nodemanager bash
```

2. Скопируйте файл на `HDFS`
```bash 
hadoop fs -put /bd2024/data/hive.txt /hive.txt
```

3. Запустите `job.py` с нужным ключем
```bash
python3 /bd2024/code/mrjob/job.py -r hadoop  hdfs:///hive.txt -o hdfs:///hive_res
```

4. Можно посмотреть на результат
```bash
hadoop fs -cat "hdfs:///hive_res/*"
```