

//User defined callbacks
void parse_params(String);
int get_idle_val();
float get_real_val();
String get_model_info(void);

//Commands
#define SET   0 
#define START 1
#define STOP  2
#define DROP  3
#define GET   4
#define INFO  5

//Signal forms
#define TRIANGULAR 0
#define SINE       1
#define SAWLIKE    2
#define SQUARE     3

String answer, request;

#define CHAR_TO_INT(x) (x-'0')


//Request handle timer
HardwareTimer *timer_handle_request = new HardwareTimer(TIM3);
void handle_request();


size_t data_time   = 0;
char   exchange    = 1;
struct {
	u_int signal;
	float freq;
	u_int amp;
	u_int origin;
} params;


void initCom()
{
	//Initialise serial commincation interface
	Serial.begin(500000);
	delay(100);

	//Set timer interrupts and asign functions executed on interrupt
	timer_handle_request->pause();
	timer_handle_request->setOverflow(1000, MICROSEC_FORMAT); //every 10 milliseconds
	timer_handle_request->attachInterrupt(handle_request);
	timer_handle_request->refresh();
	timer_handle_request->resume();
}

void handle_request()
{
	if(Serial.available()>0)
	{
		request = Serial.readStringUntil('\n');

		switch (CHAR_TO_INT(request[0])) 
		{
			case SET:
				parse_params(request);
				break;
			case START:
				exchange = 1;
				break;
			case STOP:
				exchange = 0;
				break;
			case DROP:
				data_time   = 0;
				break;
			case GET:
				answer = String(data_time) + "|" + String(get_idle_val()) + "|" + String(get_real_val());
    		Serial.println(answer);
				break;
      case INFO:
				Serial.println(get_model_info());
        break;
		}
    Serial.flush();
	}
	else 
	{
		if(exchange)
			data_time += 1;
	}
}

u_int to_uint(String val, int indent, int size)
{
	u_int sum = 0;
	for(int i=0; i<size; ++i)
		sum = sum*10 + CHAR_TO_INT(val[i+indent]);
	return sum;
}