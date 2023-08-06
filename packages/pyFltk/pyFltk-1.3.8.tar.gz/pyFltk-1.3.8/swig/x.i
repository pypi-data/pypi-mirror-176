/* File : x.i */
//%module x

%{
#include "FL/x.H"
%}

#if defined(WIN32)
%ignore Fl_X::mapraise;
#pragma SWIG cpperraswarn=1
%include "FL/win32.h"
#pragma SWIG cpperraswarn=0
#else
%include "FL/x.H"
#endif
