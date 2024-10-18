import random
import pgzrun
import itertools

WIDTH=400
HEIGHT=400

BLOCK_POSITIONS = [(350, 50),
                   (350, 350),
                   (50, 350),
                   (50, 50)
]

block_positions=itertools.cycle(BLOCK_POSITIONS) #cycle funtions will lets us cycle through the positions forever

block = Actor("block", center=(50, 50))
player=Actor("player", center=(200, 200))

Red=(255, 0, 0)
def draw():
    screen.clear()
    screen.fill(Red)
    player.draw()
    block.draw()

def move_block():
    animate(block, "bounce_end", duration = 1, pos= next (block_positions))

move_block()
clock.schedule_interval(move_block, 2)

def next_ship_target():
    x=random.randint(100, 300)
    y=random.randint(100, 300)
    player.target = x, y

    target_angle=player.angle_to(player.target)

# Angles are tricky because 0 and 359 degrees are right next to each other.
    #
    # If we call animate(angle=target_angle) now, it wouldn't know about this,
    # and will simple adjust the value of angle from 359 down to 0, which means
    # that the ship spins nearly all the way round.
        #
    # We can always add multiples of 360 to target_angle to get the same angle.
    # 0 degrees = 360 degrees = 720 degrees = -360 degrees and so on. If the
    # ship is currently at 359 degrees, then having it animate to 360 degrees
    # is the animation we want.
  #
    # Here we calculate how many multiples we need to add so that any rotations
    # will be less than 180 degrees.

    target_angle += 360 * ((player.angle - target_angle + 180) // 360)

    animate(
        player,
        angle=target_angle,
        duration=0.3,
        on_finished=move_player,

    )

def move_player():
    anim=animate(
        player,
        tween='accel_decel',
        pos=player.target,
        duration=player.distance_to(player.target)/200,
        on_finished=next_ship_target
    )

next_ship_target()
pgzrun.go()