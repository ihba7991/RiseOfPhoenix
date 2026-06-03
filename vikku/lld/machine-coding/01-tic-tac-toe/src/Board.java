public class Board {
    private String[][] grid;

    public Board() {
        grid = new String[3][3];
    }

    public boolean makeMove(int row, int col, String symbol) {
        if (grid[row][col] == null) {
            grid[row][col] = symbol;
            return true;
        }
        return false;
    }

    public String[][] getGrid() {
        return grid;
    }
}