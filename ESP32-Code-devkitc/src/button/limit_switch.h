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