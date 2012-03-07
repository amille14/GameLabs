import pygame, sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_START_X = 10
PADDLE2_START_X = SCREEN_WIDTH-20
PADDLE_START_Y = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Load sound
try:
	sound_name = "explosion.wav"
	sound = pygame.mixer.Sound(sound_name)
except pygame.error, message:
	print "Cannot load sound: " + sound_name
	raise SystemExit, message
	sound = None

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your paddle vertically centered on the left side
paddle_rect = pygame.Rect((PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))
paddle2_rect = pygame.Rect((PADDLE2_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))


# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
score = 0
score2 = 0

# Load the font for displaying the score
font = pygame.font.Font(None, 30)

# Game loop
while True:
	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
			pygame.quit()
		# Control the paddle with the mouse
		elif event.type == pygame.MOUSEMOTION:
			paddle_rect.centery = event.pos[1]
			# correct paddle position if it's going out of window
			if paddle_rect.top < 0:
				paddle_rect.top = 0
			elif paddle_rect.bottom >= SCREEN_HEIGHT:
				paddle_rect.bottom = SCREEN_HEIGHT

	# This test if up or down keys are pressed; if yes, move the paddle
	if pygame.key.get_pressed()[pygame.K_UP] and paddle2_rect.top > 0:
		paddle2_rect.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_DOWN] and paddle2_rect.bottom < SCREEN_HEIGHT:
		paddle2_rect.top += BALL_SPEED
	if pygame.key.get_pressed()[pygame.K_w] and paddle_rect.top > 0:
		paddle_rect.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_s] and paddle_rect.bottom < SCREEN_HEIGHT:
		paddle_rect.top += BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
		sys.exit(0)
		pygame.quit()
		
	# Update ball position
	ball_rect.left += ball_speed[0]
	ball_rect.top += ball_speed[1]

	# Ball collision with rails
	if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
		ball_speed[1] = -ball_speed[1]
	if ball_rect.right >= SCREEN_WIDTH:
		ball_speed[0] = -ball_speed[0]
		score += 1
		ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
	if ball_rect.left <= 0:
		ball_speed[0] = -ball_speed[0]
		score2 += 1
		ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))


	# Test if the ball is hit by the paddle; if yes reverse speed and add a point
	if paddle_rect.colliderect(ball_rect):
		ball_speed[0] = -ball_speed[0]
		sound.play()
	
	if paddle2_rect.colliderect(ball_rect):
		ball_speed[0] = -ball_speed[0]
		sound.play()
	
	# Clear screen
	screen.fill((255, 255, 255))

	# Render the ball, the paddle, and the score
	pygame.draw.rect(screen, (0, 0, 0), paddle_rect) # Your paddle
	pygame.draw.rect(screen, (0, 0, 0), paddle2_rect) # Your paddle
	pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((SCREEN_WIDTH/2, 0), (2, SCREEN_HEIGHT)))
	pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball
	score_text = font.render(str(score), True, (0, 0, 0))
	score_text2 = font.render(str(score2), True, (0, 0, 0))
	screen.blit(score_text, ((SCREEN_WIDTH / 4) - font.size(str(score))[0] / 2, 5)) # Your score
	screen.blit(score_text2, ((3*SCREEN_WIDTH / 4) - font.size(str(score2))[0] / 2, 5)) # Other score
	
	# Update screen and wait 20 milliseconds
	pygame.display.flip()
	pygame.time.delay(20)
	
	while score >= 11:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
				pygame.quit()
		
		if pygame.key.get_pressed()[pygame.K_n]:
			score = 0
			score2 = 0
			
		win_text = font.render("Player 1 wins!", True, (0,0,255))
		inst_text = font.render("Press 'n' to play a new game!", True, (255, 0, 100))
		screen.blit(win_text, ((SCREEN_WIDTH/2 - font.size("Player 1 wins!")[0]/2), 5))
		screen.blit(inst_text, ((SCREEN_WIDTH/2 - font.size("Press 'n' to play a new game!")[0]/2), 30))
		
		# Update screen and wait 20 milliseconds
		pygame.display.flip()
		pygame.time.delay(20)
	
	while score2 >= 11:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
				pygame.quit()
		
		if pygame.key.get_pressed()[pygame.K_n]:
			score = 0
			score2 = 0
			
		win_text = font.render("Player 2 wins!", True, (0,0,255))
		inst_text = font.render("Press 'n' to play a new game!", True, (255, 0, 100))
		screen.blit(win_text, ((SCREEN_WIDTH/2 - font.size("Player 2 wins!")[0]/2), 5))
		screen.blit(inst_text, ((SCREEN_WIDTH/2 - font.size("Press 'n' to play a new game!")[0]/2), 30))
		
		# Update screen and wait 20 milliseconds
		pygame.display.flip()
		pygame.time.delay(20)