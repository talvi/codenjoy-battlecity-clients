package clientlib;


import org.eclipse.jetty.websocket.WebSocket;
import org.eclipse.jetty.websocket.WebSocketClient;
import org.eclipse.jetty.websocket.WebSocketClientFactory;

import java.net.URI;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class WebSocketRunner {
    private static boolean printToConsole = true;
    private static Map<String, WebSocketRunner> clients = new ConcurrentHashMap<>();

    private WebSocket.Connection connection;
    private Solver solver;
    private WebSocketClientFactory factory;
    private Runnable onClose;

    private WebSocketRunner(Solver solver) {
        this.solver = solver;
    }


    public static WebSocketRunner run(String url, Solver solver) {
        String serverLocation = url.replace("http", "ws").replace("board/player/", "ws?user=").replace("?code=", "&code=");

        try {
            if (clients.containsKey(serverLocation)) {
                return clients.get(serverLocation);
            }
            final WebSocketRunner client = new WebSocketRunner(solver);
            client.start(serverLocation);
            Runtime.getRuntime().addShutdownHook(new Thread(){
                @Override
                public void run() {
                    client.stop();
                }
            });

            clients.put(serverLocation, client);
            return client;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private void stop() {
        try {
            connection.close();
            factory.stop();
        } catch (Exception e) {
            print(e);
        }
    }

    private void start(final String server) throws Exception {
        final Pattern urlPattern = Pattern.compile("^board=(.*)$");

        factory = new WebSocketClientFactory();
        factory.start();

        final WebSocketClient client = factory.newWebSocketClient();

        onClose = new Runnable() {
            @Override
            public void run() {
                printReconnect();
                connectLoop(server, urlPattern, client);
            }
        };

        connectLoop(server, urlPattern, client);
    }

    private void connectLoop(String server, Pattern urlPattern, WebSocketClient client) {
        while (true) {
            try {
                tryToConnect(server, urlPattern, client);
                break;
            } catch (Exception e) {
                print(e);
                printReconnect();
            }
        }
    }

    private void printReconnect() {
        print("Waiting before reconnect...");
        printBreak();
        sleep(5000);
    }

    private void tryToConnect(String server, final Pattern urlPattern, WebSocketClient client) throws Exception {
        URI uri = new URI(server);
        print(String.format("Connecting '%s'...", uri));

        if (connection != null) {
            connection.close();
        }

        connection = client.open(uri, new WebSocket.OnTextMessage() {
            public void onOpen(Connection connection) {
                print("Opened connection " + connection.toString());
            }

            public void onClose(int closeCode, String message) {
                if (onClose != null) {
                    onClose.run();
                }
                print("Closed with message: '" + message + "' and code: " + closeCode);
            }

            public void onMessage(String data) {
                print("Data from server: " + data);
                try {
                    Matcher matcher = urlPattern.matcher(data);
                    if (!matcher.matches()) {
                        throw new RuntimeException("Error parsing data: " + data);
                    }

                    solver.parseField(matcher.group(1));
                    String answer = solver.move();
                    print("Sending step: " + answer);
                    connection.sendMessage(answer);
                } catch (Exception e) {
                    print(e);
                }
                printBreak();
            }
        }).get(5000, TimeUnit.MILLISECONDS);
    }

    private void sleep(int mills) {
        try {
            Thread.sleep(mills);
        } catch (InterruptedException e) {
            print(e);
        }
    }

    private void printBreak() {
        print("-------------------------------------------------------------");
    }

    public static void print(String message) {
        if (printToConsole) {
            System.out.println(message);
        }
    }

    private void print(Exception e) {
        if (printToConsole) {
            e.printStackTrace(System.out);
        }
    }
}
