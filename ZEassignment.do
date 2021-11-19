clear all
clear results
set mem 50m
set more off
capture log close
cd "C:\Users\eser\Desktop\ZubeyirEser"
log using ZubeyirEser.log, replace
****DATA managing and DESCRIPTON STATISTICS
*here I am importing the data
import delimited C:\Users\eser\Desktop\ZubeyirEser\ZubeyirEser.csv, delimiter(";") 

*here I am labeling the progress
*partyname refers to sponsor's party
encode demorrep, gen(partyname)
label define p 1 D 2 R
drop partyname
encode demorrep, gen(partyname) label(p)
drop demorrep
rename partyname demorrep
*here I am creating new variable which is total cosponsor number
**Now I will create date in billname
gen rloc = billname
split rloc, parse("(") gen(billdate)
*bro
drop billdate1
* Now I have dates but each dates represent the year not the congress \*
*\so I will label them
encode billdate2, gen(billdate)
label define d 110 "2007-2008)" 111 "2009-2010)" 112 "2011-2012)" 113 "2013-2014)" 114 "2015-2016)" 115 "2017-2018)" 116 "2019-2020)"
drop billdate 
encode billdate2, gen(billdate) label(d) 
gen cosponsors = noofdemcos + noofrepcos
tab noofothercos
sum noofothercos
drop rloc billdate2
*I checked the number of other co-sponsors except Dem. or Rep \*
*\ 2 type of cosponsor so I can drop the noofothercos
*Here I need to use tab and sum in order to analyse the descriptive statistics
tab demorrep
sum demorrep
sum cosponsor
graph bar (count), over(demorrep)
****here I will create number of democrats support the republican
gen zeros = 0
gen a = zeros + demorrep
recode a 2=0
gen demsuprep =a*noofrepcos
****here I will create number of democrats support the republican
gen zero = 0
gen b = zero + demorrep
recode b 1=0
recode b 2 =1
gen repsupdem = b*noofdemcos
gen demsupdem = a*noofdemcos
gen repsuprep = b*noofrepcos
drop a b zero zeros

tabstat demorrep cosponsors demsuprep repsupdem , by(billdate) stat(mean sd min max)

***** Greaphical Analysis**********
**I find one good function that will draw the CI by congress
ssc install ciplot
ciplot cosponsor, by(billdate)
***here I will show the 4 diffrent variable in one graph****
***In the above I create demsupdem,repsupdem,demsuprep, and repsuprep***
***dem and rep Represent the party name dem = Democrat and rep = Republican***
ciplot demsuprep repsupdem demsupdem repsuprep , by(billdate)
************DETERMINANCY OF THE COSPONSOR*****************
*** need to substract district number form bill name
gen zeross = 0
gen a =zeross+demorrep
recode a 2= 0
rename a democrat
gen a = zeross+demorrep
recode a 1=0
recode a 2 =1
rename a republican
****** extract the strict no*******
gen s = congressman
split s, parse("[") gen(k)
split k2, parse("-") gen(k1)
split k2, parse("]") gen(k4)
split k13, parse("]") gen(k5)
tab k51
*** we need to encode k51****
sort k51
encode k51, gen(districtno)
label define g 0 "At Large"
drop districtno
encode k51, gen(districtno) label(g)
drop zeross  s k1 k2 k11 k13 k41 k51
rename k12 statename
****************Regress****************
eststo: reg cosponsor republican districtno, robust
esttab using olsreg1.tex,replace


*****Linear Probability Model******
label define l 1 "Agreed" 1 "Became" 1 "Failed" 0 "Introduced" 1 "Passed" 1 "Resolving" 1 "To" 1 "Vetoed"
encode progress, gen(rrr) label(l) 
gen zer = 0
gen a1 = zer + rrr
**here somehow stata didnt labeled my string as I defined above so I did it here manually
tab a1
replace a1 = 10 if (a1<1)
replace a1 = 1 if  (a1<10)
replace a1 = 0 if (a1>2)
rename a1 progsituation
eststo: reg progsituation cosponsor republican districtno, robust
esttab using olsreg2.tex, replace

******* IV*************
**here I am creacting my instrument// I have information cosponsorship the number of same party representatives from the sponsor’s state of election
//gen instrument = numberofsamepartysamestatecospon* republican

eststo: ivregress 2sls  progsituation republican districtno ( cosponsor = numberofsamepartysamestatecospon ) , robust

esttab using OLS1IV.tex, replace
*****end*****
// I used the eststo and esttab in order the import table to Latex.
