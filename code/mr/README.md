# Для того, чтобы запустить проект локально под Windows нужно:

1. Скачать содержимое https://github.com/steveloughran/winutils/tree/master/hadoop-2.8.1 и распаковать это в директорию вида: С:\tmp\winutils\bin\ . Папку bin создаем обязательно.
2. Скачиваем IDEA Community Edition
3. File -> New... -> Project from Exiting Sources
3. Выбираем корень проекта, ставим галочку на Gradle -> Next
4. Ставим галочку на "Use auto-import"
5. Run -> Edit Configurations -> + -> Applications
  Main class: ru.spbu.apmath.pt.mr.WordCountExample
  VM options: -Dhadoop.home.dir={путь до winutils без bin}
  Program arguments: {полный путь}\code\mr\src\main\resources\texts.txt {полный путь}\code\mr\src\main\resources\res
  Environment variables: PATH=c:\gnu\winutils\bin
  Use classpath of module: mt-intro_main
  
6. Запускаем.

Запуск из hadoop sandbox:
> yarn jar mt-intro-1.0-SNAPSHOT.jar ru.spbu.apmath.pt.mr.WordCountExample texts.txt out

Файл `texts.txt` должен быть в корне HDFS.