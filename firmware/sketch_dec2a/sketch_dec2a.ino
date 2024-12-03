#include <VBCoreG4_arduino_system.h>
#include "communication.h"


//User defined settings -------------------------------
#define TRIANGULAR 0
#define SINE       1
#define SAWLIKE    2
#define SQUARE     3

struct {
	u_char signal;
	u_char freq;
	u_char amp;
	u_char origin;
	char   state;
	size_t time;
} params;



void setup() 
{
	params = {0, 0, 0, 0, 0};
	initCom();
}

void loop(){}




//User callbacks ----------------------------------------

void parse_params(String new_params)
{
	//request[0] is <command> type
	params.form   = request[1];
	params.freq   = request[2];
	params.amp    = to_uchar(request, 3, 3); //String, indent, length in bytes
	params.origin = to_uchar(request, 6, 3);
}

String get_idle_val()
{
	//Return string aca "<idle_val_1> <idle_val_2> <...> <idle_val_last>"
	return String(75);
}

String get_real_val()
{
	//Return string aca "<real_val_1> <real_val_2> <...> <real_val_last>"
	return String(75);
}


//other functions ---------------------------------------

unsigned char to_uchar(String val, int indent, int size)
{
	unsigned char sum = 0;
	for(int i=0; i<size; ++i)
		sum = sum*10 + val[i+indent];
	return sum;
}