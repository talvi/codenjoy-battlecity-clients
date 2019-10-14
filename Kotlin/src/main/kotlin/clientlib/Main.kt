package clientlib

const val URL = "https://dojorena.io/codenjoy-contest/board/player/0?code=000000000000&gameName=battlecity"

fun main(args: Array<String>) {
    WebSocketRunner(SampleSolver()).run(URL, SampleSolver())
}

