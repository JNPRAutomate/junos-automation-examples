## PoE Port Bounce Utility

Have you ever needed to reset a PoE device that you couldn't (or just didn't want to) physically touch to pop the cable out and plug back in?

You could disable poe on a port, commit and then roll back, and that's essentially what this script does. After disabling and committing, the script executes a "rollback 1" and commits a 2nd time.

# Compatibility

I've tested this on my EX2300-C VC at home, as well as a couple of other models, like EX3400 and EX4300. The Junos syntax hasn't changed on other similar platforms like EX4100/4400, so this shouldn't have any issue working on those as well.

# Examples

Example: bounce port ge-0/0/29 on the switch closet13.mycompany.net, using the username jdoe, with SSH key authentication.

```
poe-port-bounce.py --sys closet13.mycompany.net --port ge-0/0/29 --user jdoe
```

Example: bounce port ge-0/0/1 on labsw1.mycompany.net, using the username/password jdoe/abc123.

```
poe-port-bounce.py --sys labsw1.mycompany.net --port ge-0/0/1 \
    --user jdoe --password abc123
```
