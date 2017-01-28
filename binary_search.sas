/********************************************************************
********************** BINARY SEARCH ALGO ***************************
* Developer: Srujan Surapaneni                                      *
* Reference: Ray, Craig, 'A Comparison of Table Lookup Techniques', *
* Purpose: Solves for searching a range containing non-unique keys  *
********************************************************************/

%MACRO BINARY_SEARCH (table =, keys =, unique = YES, lowvalue =, hivalue =, order = A, first = 1, last =);
%let unique = %upcase(&unique);
%let order =  %upcase(&order);
_found = 0;
_bottom = &first;
%if &Iast = %then
%do;
if 0 then set &table nobs = _top;
%end;
%else
%do;
_top = &last;
%end;
%if &order eq D %then
%do;
%let lt = gt;
%let gt = lt;
%let firstval = &hivalue;
%let lastval = &lowvalue;
%end;
%else
%do;
%let lt = lt;
%let gt = gt;
%let firstval = &lowvalue;
%let lastval = &hivalue;
%end;
length _text $ 80;
do while (not _stop);
_mid = int((_bottom + _top)/2);
set &table point = _mid;
_key = &keys;
if _key &lt &firstval then
_bottom = _mid + 1;
else if _key &gt &lastval then
_top =_mid -1;
else
do;
_found = 1;
_stop = 1;
end;
if _top < _bottom then
_stop = 1;
end;
%if &unique ne NO %then
%goto exit;
if not _found then
goto endsrch;
_holdb = _mid;
_holdt = _top;
_top = _mid;
_stop = 0;
do while (not _stop);
_mid = int((_bottom + _top)/ 2);
set &table point = _mid;
_key = &keys;
if _key &lt &firstval then
_bottom = _mid + 1;
else d _mid eq _bottom then
_stop = 1;
else
do;
_top =_mid -1;
set &table point = _top;
_key = &keys;
if _key &lt &firstval then
_stop = 1;
end;
end;
_first = mid;
_bottom = _holdb;
_top = _holdt;
_stop = 0;
do while (not _stop);
_mid = int((_bottom + _top) 12);
set &table point = _mid;
_key = &keys;
if _key &gt &lastval then
_top =_mid -1;
else if _mid eq _top then
_stop = 1;
else
do;
_bottom = _mid + 1;
set &table point = _bottom;
_key = &keys;
if _key &gt &lastval then
_stop = 1;
end;
end;
_last = _mid;
endsrch : _stop = 1;
%exit: %put end of BINARY_SEARCH macro;
%MEND BINARY_SEARCH; 