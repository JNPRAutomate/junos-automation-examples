#!/usr/bin/env python3
"""
Junos PyEZ script that displays all global parameters and variables from the 
Junos_Context dictionary with clear labels. 

Can also be done like this:
Junos_Context['user-context']['class-name']

https://www.juniper.net/documentation/us/en/software/junos/automation-scripting/topics/concept/junos-script-automation-junos-xsl-global-params-and-var.html
"""

from junos import Junos_Context

def display_junos_context():
    """Display all Junos_Context parameters and variables with descriptive labels."""
    
    print("=" * 70)
    print("PRINTING GLOBAL PARAMETERS AND VARIABLES USING JUNOS CONTEXT")
    print("=" * 70)
    print()
    
    # Device information
    print("-" * 70)
    print("DEVICE INFORMATION")
    print("-" * 70)
    print(f"The hostname of this device is: {Junos_Context.get('hostname')}")
    print(f"The product model of this device is: {Junos_Context.get('product')}")
    print(f"The chassis type is: {Junos_Context.get('chassis')}")
    print(f"The Routing Engine name is: {Junos_Context.get('routing-engine-name')}")
    
    # User context information
    print("-" * 70)
    print("USER CONTEXT INFORMATION")
    print("-" * 70)
    user_context = Junos_Context.get('user-context', {})
    
    if user_context:
        print(f"The login name is: {user_context.get('login-name')}")
        print(f"The local user name is: {user_context.get('user')}")
        print(f"The user class name is: {user_context.get('class-name')}")
        print(f"The user ID (UID) is: {user_context.get('uid')}")
    else:
        print("User context information is not available")
    
    print()

    # Check if this is the master RE
    if Junos_Context.get('re-master') is None:
        print("This script is executing on the master Routing Engine: Yes")
    else:
        print("This script is executing on the master Routing Engine: No")
    
    print()
    
    # Time information
    print("-" * 70)
    print("TIME INFORMATION")
    print("-" * 70)
    print(f"The local time is: {Junos_Context.get('localtime')}")
    print(f"The local time (ISO format) is: {Junos_Context.get('localtime-iso')}")
    print()
    
    # Script execution information
    print("-" * 70)
    print("SCRIPT EXECUTION INFORMATION")
    print("-" * 70)
    print(f"The script type is: {Junos_Context.get('script-type')}")
    print(f"The process ID (PID) is: {Junos_Context.get('pid')}")
    print(f"The TTY of the user's session is: {Junos_Context.get('tty')}")
    
    # Check for software upgrade
    sw_upgrade = Junos_Context.get('sw-upgrade-in-progress')
    if sw_upgrade == 'yes':
        print("Software upgrade in progress: Yes (first reboot after software install)")
    else:
        print("Software upgrade in progress: No")
    
    print()
    
    # op script context (if available)
    if 'op-context' in Junos_Context:
        print("-" * 70)
        print("OP SCRIPT CONTEXT")
        print("-" * 70)
        op_context = Junos_Context.get('op-context', {})
        
        if isinstance(op_context, dict) and op_context.get('via-url') is not None:
            print("This op script was executed via URL: Yes")
        else:
            print("This op script was executed locally")
        print()
    
    # Commit script  context (if available)
    if 'commit-context' in Junos_Context:
        print("-" * 70)
        print("COMMIT SCRIPT CONTEXT")
        print("-" * 70)
        commit_context = Junos_Context.get('commit-context', {})
        
        if commit_context:
            # Check commit boot
            if commit_context.get('commit-boot') is not None:
                print("Commit at boot time: Yes")
            else:
                print("Commit at boot time: No")
            
            # Check commit check
            if commit_context.get('commit-check') is not None:
                print("Commit check operation: Yes")
            else:
                print("Commit check operation: No")
            
            # Check commit synchronize
            if commit_context.get('commit-sync') is not None:
                print("Commit synchronize operation: Yes")
            else:
                print("Commit synchronize operation: No")
            
            # Check commit confirm
            if commit_context.get('commit-confirm') is not None:
                print("Commit confirm operation: Yes")
            else:
                print("Commit confirm operation: No")
            
            # Display commit comment (if available)
            commit_comment = commit_context.get('commit-comment')
            if commit_comment:
                print(f"Commit comment: {commit_comment}")
            else:
                print("Commit comment: None")
            
            # Display database path (if available)
            db_path = commit_context.get('database-path')
            if db_path:
                print(f"Database path: {db_path}")
        print()

if __name__ == "__main__":
    # Display formatted context information
    display_junos_context()
