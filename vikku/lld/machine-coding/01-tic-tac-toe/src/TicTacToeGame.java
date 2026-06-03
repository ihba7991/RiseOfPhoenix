public class TicTacToeGame {
    private Board board;
    private Player player1;
    private Player player2;
    private Player currentPlayer;

    public TicTacToeGame(Board board, Player player1, Player player2, Player currentPlayer) {
        this.board = board;
        this.player1 = player1;
        this.player2 = player2;
        this.currentPlayer = currentPlayer;
    }

    public boolean move();
    public boolean checkWin();
    public boolean checkDraw();
    void switchPlayer();
}