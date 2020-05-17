set ITEMS;
set PEOPLE;

param values{i in PEOPLE, j in ITEMS}; 
param cash;
param normalized_values{i in PEOPLE, j in ITEMS} = values[i,j] / (sum{k in ITEMS}(values[i,k]) + cash);
param normalized_cash{i in PEOPLE} = 1/(sum{k in ITEMS}(values[i,k]) + cash);

var allocated{i in PEOPLE, j in ITEMS}, binary;
var cash_alloc{i in PEOPLE} >= 0, <= cash; 
var p >= 0, <= 1;

minimize p_envy: p;

subject to

allocation_requirement{j in ITEMS}: sum{i in PEOPLE}(allocated[i, j]) = 1;
p_envy_free{i in PEOPLE, k in PEOPLE}: (cash_alloc[i] - cash_alloc[k])*normalized_cash[i] + sum{j in ITEMS}((allocated[i,j] - allocated[k,j])*normalized_values[i,j]) >= -p;
cash_restriction: sum{i in PEOPLE}(cash_alloc[i]) = cash;