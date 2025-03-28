#include <VBCoreG4_arduino_system.h>
#include "communication.h"
#include "physics.h"
#include "utils.h"



//User defined settings -------------------------------
#define INFOMSG "Готово к работе|Левитатор ECP-730|Магнитная левитация|www.github.com/vlafder/sfive|Чемякин В.C.|"
#define PLOT_TEMPALTES "{ \"plots\": {  \"0\": {   \"name\": \"Высота от времени\",   \"upper_limit\": 150,   \"lower_limit\": -10,   \"width\": 5000,   \"graphs\": {    \"0\": {     \"name\": \"Высота с датчика\",     \"color\": [255, 0, 0, 0.5],     \"width\": 1    },    \"1\": {     \"name\": \"Высота после фильтра\",     \"color\": [0, 0, 255, 1],     \"width\": 1    },    \"2\": {     \"name\": \"Целевая высота\",     \"color\": [0, 0, 255, 1],     \"width\": 1    }   }  },  \"1\": {   \"name\": \"Ток от времени\",   \"upper_limit\": 150,   \"lower_limit\": -10,   \"width\": 5000,   \"graphs\": {    \"3\": {     \"name\": \"Ток в нижней катушке\",     \"color\": [0, 0, 0, 1],     \"width\": 1    }   }  } }}"

void setup() 
{
	params = {3, 0.4, 5, 20};
	initCom();
  initPhysics();
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

int get_idle_val()
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
  
  return (int)(idle_pos*params.amp + params.origin);
}

float get_real_val()
{
	//Return string aca "<real_val_1>|<real_val_2>|<...>|<real_val_last>"
	return lff_filter(get_height());
}

String get_model_info(void)
{
  return String(INFOMSG) + String(PLOT_TEMPALTES);
}


//Main loop
void loop()
{
}