Title: IPSEC VPN Up or Down Email Notification\
Author: Jessica Garrison\
Type of Junos Script: Op\
Language: SLAX\
XML Version: 1.2\
Minimum Junos Version: 14?

Description:\
Step 1: We have two events configured under the event policy: [ike_vpn_down_alarm_user](https://apps.juniper.net/syslog-explorer/?msg=IKE_VPN_DOWN_ALARM_USER&sw=Junos%20OS&rel=22.4R3) and [ike_vpn_up_alarm_user](https://apps.juniper.net/syslog-explorer/?msg=IKE_VPN_UP_ALARM_USER&sw=Junos%20OS&rel=22.4R3). 
\
Step 2: When these events occur, they trigger their own [event scripts](https://www.juniper.net/documentation/us/en/software/junos/automation-scripting/topics/concept/junos-script-automation-event-script-overview.html): email-down.slax and email-up.slax. \
Step 3: The SLAX script uses the [curl extension](https://www.juniper.net/documentation/us/en/software/junos/automation-scripting/topics/topic-map/junos-script-automation-libslax-default-extension-libraries.html#id-libslax-curl-extension-library) to communicate with the SMTP server. 
