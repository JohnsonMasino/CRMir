import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:web_socket_channel/io.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

import 'settings_page.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // hide debug banner
    return MaterialApp(
      home: const MyHomePage(),
      // make app bar back button color white
      theme: ThemeData(
        appBarTheme: const AppBarTheme(
          iconTheme: IconThemeData(
            color: Colors.white,
          ),
        ),
        // borders on all text fields
        inputDecorationTheme: const InputDecorationTheme(
          border: OutlineInputBorder(
            borderRadius: BorderRadius.all(
              Radius.circular(10),
            ),
          ),
        ),
        // all buttons shape are rounded
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            shape: const RoundedRectangleBorder(
              borderRadius: BorderRadius.all(
                Radius.circular(10),
              ),
            ),
            textStyle: const TextStyle(
              fontSize: 18,
            ),
          ),
        ),
      ),
      debugShowCheckedModeBanner: false,
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  static const platform = MethodChannel('smssender-kishea');
  final TextEditingController _messageController = TextEditingController();

  late WebSocketChannel _channel;
  // Change to late to allow initialization later

  // Default WebSocket URL
  String _serverIp = '192.168.161.226';
  String _serverPort = '5069';
  String _clientID = 'EXODUS-SMS-SENDER';

  // Boolean to track if the WebSocket connection is open
  bool _isConnected = false;

  @override
  void initState() {
    super.initState();
    var socketUrl = 'ws://$_serverIp:$_serverPort/smsws?clientid=$_clientID';
    debugPrint('Connecting to $socketUrl');
    var uri = Uri.parse(socketUrl);
    _channel = IOWebSocketChannel.connect(uri);
  }

  void _sendSMS(String message, String phoneNumber) async {
    try {
      bool hasPermission = await requestSmsPermission();
      if (hasPermission) {
        await platform.invokeMethod(
            'sendSMS', {'message': message, 'phoneNumber': phoneNumber});
      } else {
        // Handle permission not granted
        debugPrint('Permission not granted');
      }
    } on PlatformException catch (e) {
      // Handle exception
      debugPrint('Error: $e');
    }
  }

  Future<bool> requestSmsPermission() async {
    var status = await Permission.sms.status;
    if (status.isGranted) {
      return true;
    } else {
      var result = await Permission.sms.request();
      return result.isGranted;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      /// make blue background
      backgroundColor: Colors.blue[100],
      // blue appbar
      appBar: AppBar(
        title: const Text(
          'SMS Sender',
          style: TextStyle(color: Colors.white),
        ),
        backgroundColor: Colors.blue[900],
        actions: [
          // icon showing socket connection status
          IconButton(
            icon: Icon(
              _isConnected ? Icons.wifi : Icons.wifi_off,
              color: _isConnected ? Colors.green[100] : Colors.red[100],
            ),
            onPressed: () {
              setState(() {
                reconnect();
              });
            },
          ),
          IconButton(
            icon: const Icon(
              Icons.settings,
              color: Colors.white,
            ),
            onPressed: () async {
              final apiIpAddress = await Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const SettingsPage()),
              );

              if (apiIpAddress != null &&
                  apiIpAddress is String &&
                  apiIpAddress.isNotEmpty) {
                // check port not empty
                if (apiIpAddress.contains(':')) {
                  // split ip and port
                  var ipPort = apiIpAddress.split(':');
                  _serverIp = ipPort[0];
                  _serverPort = ipPort[1];
                  _clientID = ipPort[2];
                } else {
                  // set default port
                  _serverPort = '8080';
                  _clientID = 'EXODUS-SMS-SENDER';
                }
                // Update WebSocket channel with the new API URL
                setState(() {
                  _clientID = _clientID;
                  _serverIp = _serverIp;
                  _serverPort = _serverPort;
                });
              }
            },
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: StreamBuilder(
              stream: _channel.stream,
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  // Display WebSocket messages
                  List<dynamic> messages = snapshot.data as List<dynamic>;

                  return ListView.builder(
                    itemCount: messages.length,
                    itemBuilder: (context, index) {
                      return ListTile(
                        title: Text(messages[index].toString()),
                      );
                    },
                  );
                } else if (snapshot.hasError) {
                  return Center(
                    child: Text('Error: ${snapshot.error}'),
                  );
                } else {
                  return const Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text('Listening for incoming messages'),
                        SizedBox(height: 16),
                        CircularProgressIndicator(),
                      ],
                    ),
                  );
                }
              },
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _channel.sink.close();
    super.dispose();
  }

  void reconnect() {
    if (_isConnected) {
      _channel.sink.close();
      setState(() {
        _isConnected = false;
      });
    } else {
      var address = 'ws://$_serverIp:$_serverPort/smsws?clientid=$_clientID';
      debugPrint('Connecting to $address');
      var uri = Uri.parse(address);
      _channel = IOWebSocketChannel.connect(uri);
      // keep track of connection status
      setState(() {
        _isConnected = true;
      });
      // check if connection is closed
    }
  }
}
