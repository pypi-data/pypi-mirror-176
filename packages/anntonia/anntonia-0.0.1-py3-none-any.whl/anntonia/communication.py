from server.server import Server
import subprocess
import src.anntonia.globals as globals


def StartServer(visualizer, actions=[], host="", port=8765):
    globals.currentVisualizer = visualizer
    visualizer.state.flush()

    new_server = Server(visualizer.state)
    globals.currentServer = new_server
    new_server.actions = actions
    new_server.Run(host, port)


def StartClient(ip="127.0.0.1", port=8765):
    subprocess.Popen([r"../resources/WindowsNoEditor/ANNtoNIA_rendering.exe", "-ConnectTo=" + str(ip) + ":" + str(port)])


def Visualize(visualizer, actions=[], host="", port=8765, start_client=True):
    globals.currentVisualizer = visualizer
    visualizer.state.flush()

    new_server = Server(visualizer.state)
    globals.currentServer = new_server
    new_server.actions = actions
    if start_client:
        StartClient()
    new_server.Run(host, port)
