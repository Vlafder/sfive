#include <VBCoreG4_arduino_system.h>
#include "communication.h"
#include "physics.h"
#include "utils.h"



//User defined settings -------------------------------
#define INFOMSG "Готово к работе|Левитатор ECP-730|Магнитная левитация|www.github.com/vlafder/sfive|Чемякин В.C.|"
#define PLOT_TEMPALTES "{\"plots\": {\"0\": {\"name\": \"Высота от времени\", \"upper_limit\": 150, \"lower_limit\": -10, \"width\": 5000, \"left_label\": \"миллиМетры\", \"bottom_label\": \"миллиСекунды\", \"graphs\": {\"0\": {\"name\": \"Высота с датчика\", \"color\": [255, 0, 0], \"width\": 1}, \"1\": {\"name\": \"Высота после фильтра\", \"color\": [0, 0, 255], \"width\": 1}, \"2\": {\"name\": \"Целевая высота\", \"color\": [0, 255, 0], \"width\": 1}}}}, \"etc\": {\"k1\": {\"max\": -10, \"min\": 10, \"default\": 0, \"step\": 1, \"factor\": -10}, \"k2\": {\"max\": -10, \"min\": 10, \"default\": 0, \"step\": -10, \"factor\": -10}}}"

void setup() 
{
	params = {3, 0.4, 5, 20};
	initCom();
  initPhysics();
}


int get_idle_height() 
{
  double idle_pos;
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



//User callbacks ----------------------------------------

void parse_params(String new_params)
{
	//new_params[0] is <command> type
	/*params.signal = CHAR_TO_INT(new_params[1]);
	params.freq   = to_uint(new_params, 2, 3);
	params.amp    = to_uint(new_params, 5, 3); //String, indent, length in bytes
	params.origin = to_uint(new_params, 8, 3);
  */
}

String get_val()
{
  String answer;
  int height = 0;
  
  height = get_height();

  answer = String(height) + "|";

  answer += String(lff_filter(height)) + "|";

  answer += String(get_idle_height());

  return answer;
}



String get_model_info(void)
{
  return String(INFOMSG) + String(PLOT_TEMPALTES);
}


//Main loop
void loop()
{
  set_height(get_idle_height());
}