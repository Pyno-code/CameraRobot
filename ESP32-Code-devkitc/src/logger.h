#ifndef LOGGER_H
#define LOGGER_H

#include <HardwareSerial.h>

namespace logger {
    enum LogLevel {
        TRACE,
        DEBUG,
        INFO,
        WARNING,
        ERROR,
        FATAL
    };

    String levelToString(LogLevel level);

    void print(LogLevel level, const String& message, bool ln=true);
    String format(LogLevel level, const String& content);
}

#endif // LOGGER_H