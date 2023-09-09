// Initialize CommandSender with the Raspberry Pi's IP address and port
val commandSender = CommandSender("RASPBERRY_PI_IP", 12345)

// Connect to the Raspberry Pi
commandSender.connect()

// Send commands (e.g., "F" for forward, "L" for left, "R" for right, "S" for stop)
commandSender.sendCommand("F")

// Disconnect when finished
commandSender.disconnect()
