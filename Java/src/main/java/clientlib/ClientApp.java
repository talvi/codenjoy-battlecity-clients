package clientlib;



public class ClientApp {

    private final static String URL = "https://dojorena.io/codenjoy-contest/board/player/0?code=000000000000&gameName=battlecity";

    public static void main(String[] args) {
        try {
            WebSocketRunner.run(URL, new SampleSolver());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
