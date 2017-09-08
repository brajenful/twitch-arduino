#include <Bounce2.h>
#include <LiquidCrystal.h>

Bounce bouncer = Bounce();
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
int enablePin = 8;
int enableButtonPin = 22;
int clearButtonPin = 23;
bool state;
String message;


void setup() {
	pinMode(enableButtonPin, INPUT_PULLUP);
	pinMode(clearButtonPin, INPUT_PULLUP);
	pinMode(enablePin, OUTPUT);
	lcd.begin(16, 2);
	Serial.begin(9600);
	bouncer.attach(enableButtonPin);
	bouncer.interval(20);
}

void loop() {
	bounce();
	if (Serial.available()) {
		message = Serial.readString();
		message.replace("'", "");
		lcd.clear();
		lcd.setCursor(0, 0);
		on();
		lcd.print(message);
		lcd.setCursor(0, 1);
		lcd.print("is live!");
	}
	if (digitalRead(clearButtonPin) == 0) {
		lcd.clear();
		off();
	}
}

void bounce() {
	bouncer.update();
	if (bouncer.fell() == 1) {
		state = !state;
		digitalWrite(enablePin, state);
	}
}

void on() {
	state = 1;
	digitalWrite(enablePin, state);
}

void off() {
	state = 0;
	digitalWrite(enablePin, state);
}
