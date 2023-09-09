import java.io.IOException
import java.io.OutputStream
import java.net.Socket

class CommandSender(private val ipAddress: String, private val port: Int) {
    private var socket: Socket? = null
    private var outputStream: OutputStream? = null

    fun connect() {
        try {
            socket = Socket(ipAddress, port)
            outputStream = socket?.getOutputStream()
        } catch (e: IOException) {
            e.printStackTrace()
        }
    }

    fun sendCommand(command: String) {
        try {
            outputStream?.write(command.toByteArray())
        } catch (e: IOException) {
            e.printStackTrace()
        }
    }

    fun disconnect() {
        try {
            outputStream?.close()
            socket?.close()
        } catch (e: IOException) {
            e.printStackTrace()
        }
    }
}
