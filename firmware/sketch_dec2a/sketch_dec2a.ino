#include <VBCoreG4_arduino_system.h>

#include "communication.h"

#define sgn(x) ((x) < 0 ? -1 : ((x) > 0 ? 1 : 0))


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
	double idle_pos = params.origin;

  switch (params.signal) 
  {
    case SINE:
      idle_pos = sine_form();
      break;
    case TRIANGULAR:
      idle_pos = triang_form();
      break;
    case SAWLIKE:
      idle_pos = sawlike_form();
      break;
    case SQUARE:
      idle_pos = sign_form();
      break;
  }
  
  return String(int(idle_pos*params.amp + params.origin));
}

String get_real_val()
{
	//Return string aca "<real_val_1> <real_val_2> <...> <real_val_last>"
	return get_idle_val();
}






//signal form functions ---------------------------------------


double sine_form()
{
  double radian = 2*M_PI * params.freq * (float(data_time)/1000);
  return sin(radian);
}

double sign_form() 
{
  return sgn(sine_form());
}

double sawlike_form()
{
  if(params.freq == 0)
    return -1;

  double T = 1.f/params.freq;

  return -1.f + 2.f/T * fmod((float(data_time)/1000), T);
}

double triang_form()
{
  if(params.freq == 0)
    return -1;

  double T = 1.f/params.freq;

  return (-1 + 4.f/T * fmod((float(data_time)/1000), T/2))*sgn(sine_form());
}





//other functions ---------------------------------------