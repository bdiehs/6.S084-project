%{
  #include "snazzle.tab.h"
  int line_num = 1;
%}
%%
[ \t]          ;
sNaZZle        { return SNAZZLE; }
type           { return TYPE; }
end            { return END; }
[0-9]+\.[0-9]+ { yylval.fval = atof(yytext); return FLOAT; }
[0-9]+         { yylval.ival = atoi(yytext); return INT; }
\?			   { return HOLE; }
[a-zA-Z0-9]+   {
  yylval.sval = strdup(yytext);
  return STRING;
}
\n             { ++line_num; return ENDL; }
.              ;
%%
