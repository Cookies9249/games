import java.util.Scanner;

public class App {
    public static void main(String[] args) throws Exception {
        int height = 0;

        do {
            // Get input
            Scanner input = new Scanner(System.in);
            System.out.print("Height: ");
            height = input.nextInt();
        }
        // Validate input
        while (height < 1 || height > 8);

        // For each row
        for (int row = 0; row < height; row++) {
            // Space before stairs
            for (int i = 0; i < height - row - 1; i++) {
                System.out.print(' ');
            }

            // First set of stairs
            for (int i = 0; i <= row; i++) {
                System.out.print("#");
            }

            // Gap between stairs
            System.out.print("  ");

            // Second set of stairs
            for (int i = 0; i <= row; i++) {
                System.out.print("#");
            }

            // New line
            System.out.print('\n');
        }
    }
}
