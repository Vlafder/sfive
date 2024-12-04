

//User defined callbacks
void parse_params(String);
String get_idle_val(void);
String get_real_val(void);





//Commands
#define SET   0 
#define START 1
#define STOP  2
#define DROP  3
#define GET   4

String answer, request;

#define CHAR_TO_INT(x) (x-'0')


//Request handle timer
HardwareTimer *timer_handle_request = new HardwareTimer(TIM3);
void handle_request();

size_t data_time   = 0;
char   data_status = 0;


void initCom()
{
	//Initialise serial commincation interface
	Serial.begin(500000);
	delay(100);

	//Set timer interrupts and asign functions executed on interrupt
	timer_handle_request->pause();
	timer_handle_request->setOverflow(10000, MICROSEC_FORMAT); //every 10 milliseconds
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
				data_status = 1;
				break;
			case STOP:
				data_status = 0;
				break;
			case DROP:
				data_time   = 0;
				break;
			case GET:
				answer = String(data_time) + " " + get_idle_val() + " " + get_real_val();
    		Serial.println(answer);
				break;
		}
    Serial.flush();
	}
	else 
	{
		if(data_status)
			data_time += 10;
	}
}