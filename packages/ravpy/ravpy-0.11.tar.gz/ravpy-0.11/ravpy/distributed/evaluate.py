import json
import os
import sys
import socket
from terminaltables import AsciiTable
from zipfile import ZipFile

from .compute import compute_locally, emit_error
from ..config import FTP_DOWNLOAD_FILES_FOLDER
from ..globals import g
from ..utils import setTimeout, stopTimer

timeoutId = g.timeoutId
opTimeout = g.opTimeout
initialTimeout = g.initialTimeout
client = g.client


@g.client.on('subgraph', namespace="/client")
def compute_subgraph(d):
    global client, timeoutId

    os.system('clear')
    # print("Received Subgraph : ",d["subgraph_id"]," of Graph : ",d["graph_id"])
    print(AsciiTable([['Provider Dashboard']]).table)
    g.dashboard_data.append([d["subgraph_id"], d["graph_id"], "Computing"])
    print(AsciiTable(g.dashboard_data).table)

    g.has_subgraph = True
    subgraph_id = d["subgraph_id"]
    graph_id = d["graph_id"]
    data = d["payloads"]
    subgraph_zip_file_flag = d["subgraph_zip_file_flag"]
    results = []
    g.error = False

    if subgraph_zip_file_flag == "True":
        server_file_path = 'zip_{}_{}.zip'.format(subgraph_id, graph_id)

        download_path = os.path.join(FTP_DOWNLOAD_FILES_FOLDER, server_file_path)

        try:
            g.ftp_client.ftp.voidcmd('NOOP')
            g.ftp_client.download(download_path, os.path.basename(server_file_path))

        except Exception as error:
            os.system('clear')
            g.dashboard_data[-1][2] = "Failed"
            print(AsciiTable([['Provider Dashboard']]).table)
            print(AsciiTable(g.dashboard_data).table)
            g.has_subgraph = False
            stopTimer(timeoutId)
            timeoutId = setTimeout(waitInterval, opTimeout)

            delete_dir = FTP_DOWNLOAD_FILES_FOLDER
            for f in os.listdir(delete_dir):
                os.remove(os.path.join(delete_dir, f))

            g.delete_files_list = []
            g.outputs = {}

            print('Error: ', error)
            emit_error(data[0], error, subgraph_id, graph_id)
            if 'broken pipe' in str(error).lower() or '421' in str(error).lower():
                print(
                    '\n\nYou have encountered an IO based Broken Pipe Error. \nRestart terminal and try connecting again')
                sys.exit()

        if os.path.exists(download_path):
            extract_to_path = FTP_DOWNLOAD_FILES_FOLDER
            with ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to_path)

            os.remove(download_path)
            g.ftp_client.delete_file(server_file_path)

    for index in data:

        # Perform
        operation_type = index["op_type"]
        operator = index["operator"]
        if operation_type is not None and operator is not None:
            result_payload = compute_locally(index, subgraph_id, graph_id)

            if not g.error:
                results.append(result_payload)
            else:
                break

    if not g.error:

        # check if file exists
        zip_file_name = 'local_{}_{}.zip'.format(subgraph_id, graph_id)
        if os.path.exists(zip_file_name):
            g.ftp_client.upload(zip_file_name, zip_file_name)
            os.remove(zip_file_name)

        emit_result_data = {"subgraph_id": d["subgraph_id"], "graph_id": d["graph_id"], "token": g.ravenverse_token,
                            "results": results}
        client.emit("subgraph_completed", json.dumps(emit_result_data), namespace="/client")
        # print('Emitted subgraph_completed')

        os.system('clear')
        g.dashboard_data[-1][2] = "Computed"
        print(AsciiTable([['Provider Dashboard']]).table)
        print(AsciiTable(g.dashboard_data).table)

    g.has_subgraph = False

    stopTimer(timeoutId)
    timeoutId = setTimeout(waitInterval, opTimeout)

    delete_dir = FTP_DOWNLOAD_FILES_FOLDER
    for f in os.listdir(delete_dir):
        os.remove(os.path.join(delete_dir, f))

    g.delete_files_list = []
    g.outputs = {}


@g.client.on('ping', namespace="/client")
def ping(d):
    global client
    g.ping_timeout_counter = 0
    client.emit('pong', d, namespace='/client')

@g.client.on('redundant_subgraph', namespace="/client")
def redundant_subgraph(d):
    subgraph_id = d['subgraph_id']
    graph_id = d['graph_id']
    for i in range(len(g.dashboard_data)):
        if g.dashboard_data[i][0] == subgraph_id and g.dashboard_data[i][1] == graph_id:
            g.dashboard_data[i][2] = "redundant_computation"
    os.system('clear')
    print(AsciiTable([['Provider Dashboard']]).table)
    print(AsciiTable(g.dashboard_data).table)
    
def waitInterval():
    global client, timeoutId, opTimeout, initialTimeout
    client = g.client

    try:
        sock = socket.create_connection(('8.8.8.8',53))
        sock.close()
    except Exception as e:
        print('\n ----------- Device offline -----------')
        os._exit(1)

    if g.client.connected:
        if not g.has_subgraph:
            client.emit("get_op", json.dumps({
                "message": "Send me an aop"
            }), namespace="/client")

        stopTimer(timeoutId)
        timeoutId = setTimeout(waitInterval, opTimeout)

    if not g.is_downloading:
        if not g.is_uploading:
            if g.noop_counter % 17 == 0:
                try:
                    g.ftp_client.ftp.voidcmd('NOOP')
                    g.ping_timeout_counter += 1
                except Exception as e:
                    exit_handler()
                    os._exit(1)

    if g.ping_timeout_counter > 10:
        exit_handler()
        os._exit(1)
    
    g.noop_counter += 1

def exit_handler():
    g.logger.debug('Application is Closing!')
    if g.client is not None:
        g.logger.debug("Disconnecting...")
        if g.client.connected:
            g.client.emit("disconnect", namespace="/client")