import javax.swing.JFrame;

public class Main {
	public static void main(String[] args) {
		// Create window and game
		JFrame window = new JFrame();
		Game game = new Game();
		
		// Initialize window
		window.setBounds(10, 10, 713, 636);
		window.setTitle("Pong");	
		window.setVisible(true);
		window.setResizable(false);
		window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		// Initialize game
		window.add(game);
        window.setVisible(true);
	}
}
