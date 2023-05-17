public class Grid {
    private Cell[][] cells;
    private int width;
    private int height;
    public Grid(int width, int height) {

      this.width = width;
      this.height = height;
      Grid grid = new Grid(200, 200);
      Cell[][] cells = grid.getCells();
      cells = new Cell[width][height];
      initialize();
    }

    private void initialize() {
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                cells[x][y] = new Cell(Math.random() < 0.5);
            }
        }
    }

    public void print() {
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                System.out.print(cells[x][y].isAlive() ? "X " : ". ");
            }
            System.out.println();
        }
    }

    public void update() {
        Cell[][] nextGeneration = new Cell[width][height];
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                int neighbors = countNeighbors(x, y);
                boolean alive = cells[x][y].isAlive();
                if (alive && (neighbors < 2 || neighbors > 3)) {
                    nextGeneration[x][y] = new Cell(false);
                } else if (!alive && neighbors == 3) {
                    nextGeneration[x][y] = new Cell(true);
                } else {
                    nextGeneration[x][y] = cells[x][y];
                }
            }
        }
        cells = nextGeneration;
    }

    private int countNeighbors(int x, int y) {
        int count = 0;
        for (int i = -1; i <= 1; i++) {
            for (int j = -1; j <= 1; j++) {
                if (i == 0 && j == 0) {
                    continue;
                }
                int neighborX = x + i;
                int neighborY = y + j;
                if (neighborX < 0) {
                    neighborX = width - 1;
                } else if (neighborX >= width) {
                    neighborX = 0;
                }
                if (neighborY < 0) {
                    neighborY = height - 1;
                } else if (neighborY >= height) {
                    neighborY = 0;
                }
                if (cells[neighborX][neighborY].isAlive()) {
                    count++;
                }
            }
        }
        return count;
    }
    
    public Cell[][] getCells() {
        return cells;
    }
}
