#!/usr/bin/env python
#  Author        : Jimmy Jimenez Salas - jjsalas@juniper.net
#  Version       : 1.0
#  Platform      : JunOS JET MGD API
#  Release       : Tested in 22.2R3-S2.8
#
#  Copyright (c) 2016  Juniper Networks. All Rights Reserved.
#
#  YOU MUST ACCEPT THE TERMS OF THIS DISCLAIMER TO USE THIS SOFTWARE
#
#  JUNIPER IS WILLING TO MAKE THE INCLUDED SCRIPTING SOFTWARE AVAILABLE TO YOU
#  ONLY UPON THE CONDITION THAT YOU ACCEPT ALL OF THE TERMS CONTAINED IN THIS
#  DISCLAIMER. PLEASE READ THE TERMS AND CONDITIONS OF THIS DISCLAIMER
#  CAREFULLY.
#
#  THE SOFTWARE CONTAINED IN THIS FILE IS PROVIDED "AS IS." JUNIPER MAKES NO
#  WARRANTIES OF ANY KIND WHATSOEVER WITH RESPECT TO SOFTWARE. ALL EXPRESS OR
#  IMPLIED CONDITIONS, REPRESENTATIONS AND WARRANTIES, INCLUDING ANY WARRANTY
#  OF NON-INFRINGEMENT OR WARRANTY OF MERCHANTABILITY OR FITNESS FOR A
#  PARTICULAR PURPOSE, ARE HEREBY DISCLAIMED AND EXCLUDED TO THE EXTENT
#  ALLOWED BY APPLICABLE LAW.
#
#  IN NO EVENT WILL JUNIPER BE LIABLE FOR ANY LOST REVENUE, PROFIT OR DATA, OR
#  FOR DIRECT, SPECIAL, INDIRECT, CONSEQUENTIAL, INCIDENTAL OR PUNITIVE
#  DAMAGES HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY ARISING
#  OUT OF THE USE OF OR INABILITY TO USE THE SOFTWARE, EVEN IF JUNIPER HAS
#  BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
#
##
# Routes pushed to a Junos device using the JET RPD API dissapear after some time if the Client disconnects. Configuration changes to the ephemeral DB using the management API
# remain until a reboot or JSD restart. This script presents an example to emulate the purge on disconnect behavior. It is not meant to be a full application, but it works as a POC.
# Step by step:
# 1. The script connects and creates an eph DB instance in the static config and a deactivated time event 
# 2. Loads two event policies to the eph DB:
#   a.  DELETE-"<controller_name>" is set to execute once a timed event COUNTDOWN-"<controller_name>" goes off for the first time and deletes both the eph DB instance and the timer.
#       Since the periodic event is deactivated in config, it will never run until condition b is met.
#   b. The second policy ACTIVATE_TIMER_"<controller_name>" triggers upon controller disconnection and activates the periodic event (COUNTDOWN-"<controller_name>").
#
# 3. When the client(controller) disconnects:
#   - The ACTIVATE_TIMER_"<controller_name>" runs and activates the timer COUNTDOWN-"<controller_name>"
#   - The counter goes off 60 seconds later, If the client re-connects before the timer goes off, it just needs to deactivate COUNTDOWN-"<controller_name>" on the static configuration 
#       to prevent the first policy from running. The logic to reconnect is not included here
#   - The counter triggers the DELETE-"<controller_name>" policy and things get cleaned up
# 
#  Usage example:
#   - python jet_eph_mgd_api_purge_on_disconnect.py -d "<Target_IP>" -t 100 -p 50051 -u <user> -pw <password> -c <controller name>
#

import argparse
import grpc
import os
import stat
import sys
import time

import jnx_authentication_service_pb2
import jnx_authentication_service_pb2_grpc
import jnx_management_service_pb2
import jnx_management_service_pb2_grpc
import jnx_common_base_types_pb2
import jnx_routing_bgp_service_pb2
import jnx_routing_bgp_service_pb2_grpc
import jnx_routing_base_types_pb2
import jnx_routing_base_types_pb2_grpc
import jnx_common_addr_types_pb2
import jnx_common_addr_types_pb2_grpc


_HOST_OVERRIDE = 'router'

def Main():
    try:
        parser = argparse.ArgumentParser()

        parser.add_argument('-d','--device', help='Input hostname',
            required=True)
        parser.add_argument('-t','--timeout', help='Input time_out value',
            required=True,type=int)
        parser.add_argument('-p', '--port', help='gRPC port',
            required=True)
        parser.add_argument('-u', '--user', help='Input username',
            required=True)
        parser.add_argument('-pw', '--password', help='Input password',
            required=True)
        parser.add_argument('-c', '--controller', help='Controller instance, this is used to name the eph DB instance, counter and policies',
            required=True)

        args = parser.parse_args()

        #Establish grpc channel to jet router
        channel = grpc.insecure_channel(target=args.device + ":50051")
        controller_name = args.controller.upper()
        #create stub for authentication services
        stub = jnx_authentication_service_pb2_grpc.AuthenticationStub(channel)
        #Authenticate
        login_request = jnx_authentication_service_pb2.LoginRequest(
            username=args.user, password=args.password, client_id=controller_name)
        login_response = stub.Login(login_request, args.timeout)
        #Check if authentication is successful
        if login_response.status.code == jnx_common_base_types_pb2.SUCCESS:
            print("[INFO] Connected to gRPC Server")
        else:
            print("[ERROR] gRPC Server Connection failed:")
            print(login_response.status.message)
       
        #Create stub for management services
        stub = jnx_management_service_pb2_grpc.ManagementStub(channel)
        print("[INFO] Connected to management service")

#1. Once connected, create a unique Eph database Instance

        comm_merge=jnx_management_service_pb2.ConfigCommit(type=jnx_management_service_pb2.ConfigCommitType.CONFIG_COMMIT, comment='testing')
        config_xml_inst = "<configuration><system><configuration-database><ephemeral><instance><name>"+controller_name+"</name></instance></ephemeral></configuration-database></system><event-options><generate-event inactive=\"inactive\"><name>COUNTDOWN-"+controller_name+"</name><time-interval>60</time-interval></generate-event></event-options></configuration>"
        op = jnx_management_service_pb2.ConfigSetRequest(xml_config=config_xml_inst, load_type=jnx_management_service_pb2.ConfigLoadType.CONFIG_LOAD_MERGE, commit=comm_merge)
        op_response = stub.ConfigSet(op)
        if op_response.status.code == jnx_common_base_types_pb2.SUCCESS:
            print("[INFO] Commit OK, Eph DB instance created")
#2. Once created, make some commits to eph DB
            config_evt_script = "<configuration><event-options><policy><name>DELETE-"+controller_name+"</name><events>COUNTDOWN-"+controller_name+"</events><then><change-configuration><commands><name>delete system configuration-database ephemeral instance "+controller_name+"</name></commands> \
                                    <commands><name>delete event-options generate-event COUNTDOWN-"+controller_name+"</name></commands> \
                                        <commit-options><log>instance "+controller_name+" gone</log></commit-options></change-configuration></then></policy><policy><name>ACTIVATE_TIMER_"+controller_name+"</name><events>mgd_api_application_disconnect</events><attributes-match> \
                                            <from-event-attribute>mgd_api_application_disconnect.message</from-event-attribute><condition>matches</condition><to-event-attribute-value>"+controller_name+"</to-event-attribute-value></attributes-match><then><change-configuration> \
                                                <commands><name>activate event-options generate-event COUNTDOWN-"+controller_name+"</name></commands><commit-options><log>instance "+controller_name+" gone, start timer</log></commit-options></change-configuration></then></policy></event-options> \
                                                    </event-options></configuration>"
            config_xml_eph = "<configuration><policy-options><policy-statement><name>TEST-EPH</name><term><name>1</name><from><protocol>bgp</protocol><route-filter><address>10.0.2.0/24</address><exact/></route-filter></from> \
                                    <then><accept/></then></term></policy-statement></policy-options></configuration>"
            eph_conf_op_evt = jnx_management_service_pb2.EphemeralConfigSetRequest.ConfigOperation(id=controller_name, operation=jnx_management_service_pb2.ConfigOperationType.CONFIG_OPERATION_UPDATE, path="/", xml_config=config_evt_script)
            eph_conf_op = jnx_management_service_pb2.EphemeralConfigSetRequest.ConfigOperation(id=controller_name, operation=jnx_management_service_pb2.ConfigOperationType.CONFIG_OPERATION_UPDATE, path="/", xml_config=config_xml_eph)
            conf_operations = []
            conf_operations.append(eph_conf_op_evt)
            conf_operations.append(eph_conf_op)
            eph_op = jnx_management_service_pb2.EphemeralConfigSetRequest(config_operations=conf_operations, instance_name=controller_name, validate_config=True)
            eph_op_response = stub.EphemeralConfigSet(eph_op)
            if eph_op_response.status.code == jnx_common_base_types_pb2.SUCCESS:
                print("[INFO] Commit to eph DB OK")
#3 Seems like we need to reload event-scripts
                op_xml_command = "<reload-event-scripts></reload-event-scripts>"
                op = jnx_management_service_pb2.OpCommandGetRequest(
                xml_command=op_xml_command, out_format=2)
                # Invoke API
                op_response = stub.OpCommandGet(op, args.timeout)
                for resp in op_response:
                    if resp.status.code == jnx_common_base_types_pb2.SUCCESS:
                        print("[INFO] Invoked OpCommandGetRequest succeeded")
                        print("[INFO] Return output in CLI format = ")
                        print(resp.data)
                        input_s = input("Press a key to exit")
                    else:
                        print("[ERROR] Invoked OpCommandGetRequest failed")
                        print("[ERROR] " + resp.status.message)
            else: 
                print("[ERROR] Commit to eph failed")
        else:
            print("[ERROR] Commit failed")
            print("[ERROR] " + op_response.status.message) 

    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    Main()
