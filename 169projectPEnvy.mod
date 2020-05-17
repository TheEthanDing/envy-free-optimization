set ITEMS;
set PEOPLE;

param values{i in PEOPLE, j in ITEMS};
param normalized_values{i in PEOPLE, j in ITEMS} = values[i,j] / sum{k in ITEMS}(values[i,k]);

var allocated{i in PEOPLE, j in ITEMS}, binary;
var p >= 0, <= 1;

minimize p_envy: p;

subject to

allocation_requirement{j in ITEMS}: sum{i in PEOPLE}(allocated[i, j]) = 1;
p_envy_free{i in PEOPLE, k in PEOPLE}: sum{j in ITEMS}((allocated[i,j] - allocated[k,j])*normalized_values[i,j]) >= -p;
 


