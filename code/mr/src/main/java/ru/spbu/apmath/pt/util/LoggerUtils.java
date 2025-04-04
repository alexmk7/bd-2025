package ru.spbu.apmath.pt.util;

import org.apache.log4j.*;

public class LoggerUtils {
    public static void initLogger() {
        BasicConfigurator.resetConfiguration();
        BasicConfigurator.configure();
        Logger.getRootLogger().removeAllAppenders();

        final PatternLayout layout = new PatternLayout("%d{dd.MM.yy HH:mm:ss} %5p [%t] %c{1} - %m%n");
        Logger.getRootLogger().addAppender(new ConsoleAppender(layout));
        Logger.getRootLogger().setLevel(Level.INFO);
    }
}
