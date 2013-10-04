Time = timer.get_time(); 	
if ( (Time > LastTime) && (Time % 600 == 0) ) { //Write every 10 minutes
	LastTime = Time;
	#include "WriteOutputVars.inc"
}
