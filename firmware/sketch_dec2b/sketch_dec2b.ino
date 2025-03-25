#include <VBCoreG4_arduino_system.h>
#include "communication.h"
#include "physics.h"
#include "utils.h"



//User defined settings -------------------------------
#define TRIANGULAR 0
#define SINE       1
#define SAWLIKE    2
#define SQUARE     3

#define INFOMSG "Готово к работе|Левитатор ECP-730|Магнитная левитация|www.github.com/vlafder/sfive|Чемякин В.C."


void setup() 
{
	params = {0, 0, 0, 75};
	initCom();
  initPhysics();
}

void loop()
{
  set_height(idle_val(data_time));
}





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
  //Return string aca "<idle_val_1>|<idle_val_2>|<...>|<idle_val_last>"
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
	//Return string aca "<real_val_1>|<real_val_2>|<...>|<real_val_last>"
	return get_height();
}

String get_model_info(void)
{
  return String(INFOMSG);
}