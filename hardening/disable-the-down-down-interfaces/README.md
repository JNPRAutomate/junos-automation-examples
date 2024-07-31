Title: Disable the down-down interfaces\
Author: Jessica Garrison\
Type of Junos Script: Event\
Language: SLAX\
XML Version: 1.2\
Model: ex3400-24p\
Family: junos\
Junos: 18.2R3-S2.9\
Level: Lab\
Description: This event script is confiigured to run on a weekly basis.  It grabs the "show interfaces terse" command and checks for the Admin and Link statuses to be down.  If they are both down, it disables the interfaces configuration. 