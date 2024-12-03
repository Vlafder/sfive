
//Power and control pins
#define IN1 PA8
#define IN2 PA9
#define USR_BTN PC13



//Request & responce timers
HardwareTimer *timer_read_request = new HardwareTimer(TIM3);
//HardwareTimer *timer_move = new HardwareTimer(TIM5);
HardwareTimer *timer_send_response = new HardwareTimer(TIM7);


String answer, request;

void read_request();
void send_response();


void initCom(){
	//Initialise serial commincation interface
  Serial.begin(500000);
  delay(1000);

  //Set timer interrupts and asign functions executed on interrupt
  timer_read_request->pause();
  timer_send_response->pause();

  //set timer overflows
  timer_read_request->setOverflow(200, HERTZ_FORMAT); 
  timer_send_response->setOverflow(200, HERTZ_FORMAT);

  //attach function executed on interrupt
  timer_read_request->attachInterrupt(read_request);
  timer_send_response->attachInterrupt(send_response);

  //update tiner parameters
  timer_read_request->refresh();
  timer_send_response->refresh();

  //continue timer counts
  timer_read_request->resume();
  timer_send_response->resume();
}

void read_request()
{
  
}


void send_response()
{
   // answer = String("#OUT ")+time_dot + " "+ u_send +" "+ current_angle+" "+ vel_model ;
   // Serial.println(answer);
}

