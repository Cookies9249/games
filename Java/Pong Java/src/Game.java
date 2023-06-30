import java.awt.event.*;
import javax.swing.*;
import java.awt.*;

public class Game extends JPanel implements KeyListener, ActionListener {
	// Initialize variables
	private boolean play = false;
	
	private Timer timer;
	private int delay = 8;
	
	private int playerA = 310;
	private int playerB = 310;
	
	private int ballposX = 120;
	private int ballposY = 350;
	private float ballXdir = -1;
	private float ballYdir = -2;
	
	private static final String FONT = "serif";
	
	public Game() {		
		// Initialize map and timer
        timer = new Timer(delay, this);
		timer.start();

		// Add listeners
		addKeyListener(this);
		setFocusable(true);
		setFocusTraversalKeysEnabled(false);
	}
	
	@Override
	public void paint(Graphics graphics) {
		// Background
		graphics.setColor(Color.black);
		graphics.fillRect(0, 0, 700, 600);
				
		// Borders
		graphics.setColor(Color.green);
		graphics.fillRect(0, 0, 3, 600);
		graphics.fillRect(0, 0, 700, 3);
		graphics.fillRect(697, 0, 3, 600);
		graphics.fillRect(0, 597, 700, 3);
		
		// Paddle (A)
		graphics.setColor(Color.red);
		graphics.fillRect(playerA, 550, 100, 8);

		// Paddle (B)
		graphics.setColor(Color.blue);
		graphics.fillRect(playerB, 50, 100, 8);
		
		// Ball
		graphics.setColor(Color.yellow);
		graphics.fillOval(ballposX, ballposY, 20, 20);
		
		// Game over (Red wins)
		if (ballposY < 30) {
			// Reset variables
			play = false;
            ballXdir = 0;
     		ballYdir = 0;

			// Add text
            graphics.setColor(Color.RED);
            graphics.setFont(new Font(FONT, Font.BOLD, 30));
			graphics.drawString("Red Wins!", 260, 300);  

			graphics.setColor(Color.RED);
            graphics.setFont(new Font(FONT, Font.BOLD, 20));           
            graphics.drawString("Press Enter to Play Again", 230, 350);        
        }
		// Game over (Blue wins)
		else if (ballposY > 570) {
			// Reset variables
			play = false;
            ballXdir = 0;
     		ballYdir = 0;

			// Add text
            graphics.setColor(Color.BLUE);
            graphics.setFont(new Font(FONT, Font.BOLD, 30));
			graphics.drawString("Blue Wins!", 255, 300); 
			
			graphics.setColor(Color.BLUE);
            graphics.setFont(new Font(FONT, Font.BOLD, 20));           
            graphics.drawString("Press Enter to Play Again", 230, 350);        
        }
		
		graphics.dispose();
	}

	public void keyReleased(KeyEvent e) {
		// Game must implement the inherited method KeyListener.keyReleased(KeyEvent)
	}
	public void keyTyped(KeyEvent e) {
		// Game must implement the inherited method KeyListener.keyTyped(KeyEvent)
	}

	public void keyPressed(KeyEvent e) {
		// Move player A
		if (e.getKeyCode() == KeyEvent.VK_RIGHT) {
			// Move right
			play = true; 
			playerA += 20;

			if (playerA >= 600) {
				playerA = 600;
			}
        }
		else if (e.getKeyCode() == KeyEvent.VK_LEFT) {     
			// Move left
			play = true;
			playerA -= 20;

			if (playerA < 10) {
				playerA = 10;
			}
        }

		// Move player B
		else if (e.getKeyCode() == KeyEvent.VK_D) {
			// Move right
			play = true;
			playerB += 20;

			if (playerB >= 600) {
				playerB = 600;
			}
        }
		else if (e.getKeyCode() == KeyEvent.VK_A) {
			// Move left
			play = true;
			playerB -= 20;

			if (playerB < 10) {
				playerB = 10;
			}
        }

		// Start game
		else if (e.getKeyCode() == KeyEvent.VK_ENTER && !play) {
			// Reset variables
			play = true;
			ballposX = 120;
			ballposY = 350;
			ballXdir = -1;
			ballYdir = -2;
			playerA = 310;
			playerB = 310;
			repaint();
        }
	}
	
	public void actionPerformed(ActionEvent e) 
	{
		// Validate play
		timer.start();
		if (!play) {
			return;
		}

		// Ball collisions with player
		Rectangle ballRect = new Rectangle(ballposX, ballposY, 20, 20);
		Rectangle playerARect = new Rectangle(playerA, 550, 100, 8);
		Rectangle playerBRect = new Rectangle(playerB, 50, 100, 8);

		if (ballRect.intersects(playerARect) || ballRect.intersects(playerBRect)) {
			ballYdir = -ballYdir;
		}

		// Move ball
		ballposX += ballXdir;
		ballposY += ballYdir;
		
		// Ball collisions with wall
		if (ballposX < 0 || ballposX > 670) {
			ballXdir = -ballXdir;
		}

		repaint();
	}
}
