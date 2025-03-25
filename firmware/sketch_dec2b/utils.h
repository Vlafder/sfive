#define sgn(x) ((x) < 0 ? -1 : ((x) > 0 ? 1 : 0))

//signal form functions ---------------------------------------
double sine_form(int time)
{
  double radian = 2*M_PI * params.freq * (float(time)/1000);
  return sin(radian);
}

double sign_form(int time) 
{
  return sgn(sine_form());
}

double sawlike_form(int time)
{
  if(params.freq == 0)
    return -1;

  double T = 1.f/params.freq;

  return -1.f + 2.f/T * fmod((float(time)/1000), T);
}

double triang_form(int time)
{
  if(params.freq == 0)
    return -1;

  double T = 1.f/params.freq;

  return (-1 + 4.f/T * fmod((float(time)/1000), T/2))*sgn(sine_form());
}