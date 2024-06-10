#include <Bounce2.h>

class LimitSwitch {
  public:
    // Constructeur
    LimitSwitch(int pin, unsigned long debounceInterval) : pin(pin), debounceInterval(debounceInterval) {
      // Initialiser le bouton avec la bibliothèque Bounce2
      debouncer = Bounce();
      debouncer.attach(pin, INPUT_PULLUP);
      debouncer.interval(debounceInterval);
      begin();
    }

    // Initialiser la broche
    void begin() {
      pinMode(pin, INPUT_PULLUP);
      debouncer.attach(pin);
      debouncer.interval(debounceInterval);
    }

    // Mettre à jour l'état du limit switch
    void update() {
      debouncer.update();
    }

    // Vérifier si le limit switch est activé (pression détectée)
    bool isPressed() {
      return debouncer.fell();
    }

    // Vérifier si le limit switch est relâché
    bool isReleased() {
      return debouncer.rose();
    }

  private:
    int pin;
    unsigned long debounceInterval;
    Bounce debouncer;
};


#define BUTTON_PIN 12
#define LIMITSWITCH_TOP 35
#define LIMITSWITCH_BOTTOM 36

LimitSwitch limitSwitchTop(35, 10);
LimitSwitch limitSwitchBottom(36, 10);



void setup() {
  Serial.begin(115200);

  limitSwitchTop.begin();
  limitSwitchBottom.begin();
}

void loop() {
  // Mettez à jour l'état du limit switch

  static unsigned long previousMillis = 0;
  const unsigned long interval = 3000;

  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    Serial.println("looping each 3 sec");
  }

  limitSwitchTop.update();
  limitSwitchBottom.update();

  // Vérifiez si le limit switch est pressé
  if (limitSwitchBottom.isPressed()) {
    Serial.println("Limit switch activated bottom.");
    // Code pour initialiser la position du robot
  }

  if (limitSwitchTop.isPressed()) {
    Serial.println("Limit switch activated top.");
    // Code pour initialiser la position du robot
  }

  // Vérifiez si le limit switch est relâché
  if (limitSwitchBottom.isReleased()) {
    Serial.println("Limit switch released bottom.");
  }

  if (limitSwitchTop.isReleased()) {
    Serial.println("Limit switch released top.");
  }

  delay(100);  // Délai pour éviter de surcharger le port série
}
