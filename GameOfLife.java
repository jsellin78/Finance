import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Scanner;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.Timer;

public class GameOfLife extends JPanel implements ActionListener {
    private boolean[][] cells;
    private int width;
    private int height;
    private int generations;
    private int cellSize = 10;
    private Timer timer;

    
    public GameOfLife(int width, int height, int generations) {
        this.width = width;
        this.height = height;
        this.generations = generations;
        this.cells = new boolean[width][height];
        
        // Initialize random starting state
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                cells[x][y] = Math.random() < 0.5;
            }
        }
        
        // Set up timer for animation
        timer = new Timer(100, this);
        timer.setRepeats(true);
        timer.start();
    }
    
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        
        // Paint background
        g.setColor(Color.WHITE);
        g.fillRect(0, 0, getWidth(), getHeight());
        
        // Paint cells
        g.setColor(Color.BLACK);
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                if (cells[x][y]) {
                    g.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
                }
            }
        }
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Enter the width of the grid: ");
        int width = scanner.nextInt();
        System.out.print("Enter the height of the grid: ");
        int height = scanner.nextInt();
        System.out.print("Enter the number of generations: ");
        int generations = scanner.nextInt();
        
        // Set up window and panel
        JFrame frame = new JFrame("Game of Life");
        GameOfLife panel = new GameOfLife(width, height, generations);
        panel.setPreferredSize(new Dimension(width * panel.cellSize, height * panel.cellSize));
        frame.setContentPane(panel);
        frame.pack();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
        
        scanner.close();
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (generations == 0) {
            timer.stop();
            return;
        }       
        // Calculate next generation
        boolean[][] nextGeneration = new boolean[width][height];
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                int neighbors = countNeighbors(cells, x, y);
                boolean alive = cells[x][y];
                if (alive && (neighbors < 2 || neighbors > 3)) {
                    nextGeneration[x][y] = false;
                } else if (!alive && neighbors == 3) {
                    nextGeneration[x][y] = true;
                } else {
                    nextGeneration[x][y] = alive;
                }
            }
        }
        cells = nextGeneration;
        generations--;
        
        // Repaint panel
        repaint();
    }

private static int countNeighbors(boolean[][] cells, int x, int y) {
    int count = 0;
    int width = cells.length;
    int height = cells[0].length;

    for (int i = -1; i <= 1; i++) {
        for (int j = -1; j <= 1; j++) {
            if (i == 0 && j == 0) {
                continue;
            }
            int neighborX = x + i;
            int neighborY = y + j;
            if (neighborX < 0 || neighborX >= width || neighborY < 0 || neighborY >= height) {
                continue;
            }
            if (cells[neighborX][neighborY]) {
                count++;
            }
        }
    }

    return count;
}
}
