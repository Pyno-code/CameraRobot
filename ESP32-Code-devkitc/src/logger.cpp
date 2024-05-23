#include "logger.h"


namespace logger {
    String levelToString(LogLevel level) {
        switch(level) {
            case TRACE: return "TRACE";
            case DEBUG: return "DEBUG";
            case INFO: return "INFO";
            case WARNING: return "WARNING";
            case ERROR: return "ERROR";
            case FATAL: return "FATAL";
            default: return "UNKNOWN";
        }
    }

    void print(LogLevel level, const String& message, bool ln) {
        String content = format(level, message);
        if (ln) {
            Serial.println(content);
        } else {
            Serial.print(content);
        }
    }

    String format(LogLevel level, const String& content) {
        unsigned long timestamp = millis();
        unsigned long minutes = (timestamp / 60000) % 60;
        unsigned long seconds = (timestamp / 1000) % 60;
        unsigned long milliseconds = timestamp % 1000;
        String logLevel = levelToString(level);
        String formattedContent = "[" + logLevel + "]" + "[" + String(minutes) + ":" + String(seconds) + ":" + String(milliseconds) + "] -- " + content;
        return formattedContent;
    }
}