package clientlib

import org.eclipse.jetty.websocket.WebSocket
import org.eclipse.jetty.websocket.WebSocketClient
import org.eclipse.jetty.websocket.WebSocketClientFactory
import java.net.URI
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.TimeUnit
import java.util.regex.Pattern

private const val EXTRA_CHAR_OF_BOARD = 6
var board: String = ""

class WebSocketRunner(val solver: Solver) {


    private val printToConsole = true
    private val clients = ConcurrentHashMap<String, WebSocketRunner>()
    private var connection: WebSocket.Connection? = null
    private var factory: WebSocketClientFactory? = null
    private var onClose: Runnable? = null


    fun run(url: String, solver: Solver): WebSocketRunner? {
        val serverLocationWS = url.replace("http", "ws").replace("board/player/", "ws?user=").replace("?code=", "&code=")
        try {
            if (clients.containsKey(serverLocationWS)) {
                return clients[serverLocationWS]
            }
            val client = WebSocketRunner(solver)
            client.start(serverLocationWS)
            Runtime.getRuntime().addShutdownHook(object : Thread() {
                override fun run() {
                    client.stop()
                }
            })
            clients[serverLocationWS] = client
            return client
        } catch (e: Exception) {
            throw RuntimeException(e)
        }
    }

    private fun stop() {
        try {
            connection!!.close()
            factory!!.stop()
        } catch (e: Exception) {
            print(e)
        }
    }

    @Throws(Exception::class)
    private fun start(server: String) {
        val urlPattern = Pattern.compile("^board=(.*)$")
        factory = WebSocketClientFactory()
        factory!!.start()
        val client = factory!!.newWebSocketClient()
        onClose = Runnable {
            printReconnect()
            connectLoop(server, urlPattern, client)
        }
        connectLoop(server, urlPattern, client)
    }

    private fun connectLoop(server: String, urlPattern: Pattern, client: WebSocketClient) {
        while (true) {
            try {
                tryToConnect(server, urlPattern, client)
                break
            } catch (e: Exception) {
                print(e)
                printReconnect()
            }
        }
    }

    private fun printReconnect() {
        print("Waiting before reconnect...")
        printBreak()
        sleep(5000)
    }

    @Throws(Exception::class)
    private fun tryToConnect(server: String, urlPattern: Pattern, client: WebSocketClient) {
        val uri = URI(server)
        print(String.format("Connecting '%s'...", uri))
        if (connection != null) {
            connection!!.close()
        }
        connection = client.open(uri, object : WebSocket.OnTextMessage {
            override fun onOpen(connection: WebSocket.Connection) {
                print("Opened connection " + connection.toString())
            }

            override fun onClose(closeCode: Int, message: String) {
                if (onClose != null) {
                    onClose!!.run()
                }
                print("Closed with message: '$message' and code: $closeCode")
            }

            override fun onMessage(data: String) {
                board = data.takeLast(data.length - EXTRA_CHAR_OF_BOARD)
                print("Data from server: $data")
                try {
                    val matcher = urlPattern.matcher(data)
                    if (!matcher.matches()) {
                        throw RuntimeException("Error parsing data: $data")
                    }
                    solver.parseField(matcher.group(1))
                    val answer = solver.move()
                    print("Sending step: $answer")
                    connection!!.sendMessage(answer)
                } catch (e: Exception) {
                    print(e)
                }
                printBreak()
            }
        }).get(5000, TimeUnit.MILLISECONDS)
    }

    private fun sleep(mills: Int) {
        try {
            Thread.sleep(mills.toLong())
        } catch (e: InterruptedException) {
            print(e)
        }
    }

    private fun printBreak() {
        print("-------------------------------------------------------------")
    }

    fun print(message: String) {
        if (printToConsole) {
            println(message)
        }
    }

    private fun print(e: Exception) {
        if (printToConsole) {
            e.printStackTrace(System.out)
        }
    }
}