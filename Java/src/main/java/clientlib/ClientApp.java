package clientlib;



public class ClientApp {

    private final static String URL = "http://dojorena.io/codenjoy-contest/board/player/d25xy533nr4bfllc92se?code=993246243064791035&gameName=battlecity";
//    private final static String URL = "http://dojorena.io/codenjoy-contest/board/game/battlecity/player/d25xy533nr4bfllc92se?code=993246243064791035";

    public static void main(String[] args) {
        try {
            WebSocketRunner.run(URL, new SampleSolver());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
