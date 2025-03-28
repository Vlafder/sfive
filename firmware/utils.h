
#define K 0.3

#define sgn(x) ((x) < 0 ? -1 : ((x) > 0 ? 1 : 0))

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

float lff_filter(int raw_dist)
{
  static float prev_dist = 0;
  prev_dist = (1-K)*prev_dist + K*raw_dist;
  return prev_dist;
}