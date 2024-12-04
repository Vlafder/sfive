#include <VBCoreG4_arduino_system.h>

#include "communication.h"


//User defined settings -------------------------------
#define TRIANGULAR 0
#define SINE       1
#define SAWLIKE    2
#define SQUARE     3

struct {
	u_int signal;
	u_int freq;
	u_int amp;
	u_int origin;
} params;



void setup() 
{
	params = {0, 0, 0, 75};
	initCom();
}

void loop(){}




//User callbacks ----------------------------------------

void parse_params(String new_params)
{
	//new_params[0] is <command> type
	params.signal = CHAR_TO_INT(new_params[1]);
	params.freq   = to_uint(new_params, 2, 3);
	params.amp    = to_uint(new_params, 5, 3); //String, indent, length in bytes
	params.origin = to_uint(new_params, 8, 3);
}

String get_idle_val()
{
	//Return string aca "<idle_val_1> <idle_val_2> <...> <idle_val_last>"
  //radian = (1/2*PI)*FREQUANCY*TIME_IN_MILLIS*1000
  double radian = (1.f/(2*M_PI)*params.freq*data_time/10);
  int idle_pos = sin(radian)*params.amp + params.origin;
	return String(idle_pos);
}

String get_real_val()
{
	//Return string aca "<real_val_1> <real_val_2> <...> <real_val_last>"
  double radian = (1.f/(2*M_PI)*params.freq*data_time/10);
  int real_pos = sin(radian)*params.amp + params.origin + 20;
	return String(real_pos);
}


//other functions ---------------------------------------

u_int to_uint(String val, int indent, int size)
{
	u_int sum = 0;
	for(int i=0; i<size; ++i)
		sum = sum*10 + CHAR_TO_INT(val[i+indent]);
	return sum;
}