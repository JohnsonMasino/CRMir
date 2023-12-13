import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  final TextEditingController _urlController = TextEditingController();
  final TextEditingController _portController = TextEditingController();
  String _clientID = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // set scaffold back button color to white
      backgroundColor: Colors.blue[100],
      appBar: AppBar(
        title: const Text(
          'Settings',
          style: TextStyle(
            color: Colors.white,
          ),
        ),
        backgroundColor: Colors.blue[900],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              // allow only numbers, dots and colons
              inputFormatters: [
                FilteringTextInputFormatter.allow(RegExp(r'[0-9.]')),
              ],
              // set the keyboard to show numbers by default
              keyboardType: TextInputType.number,
              controller: _urlController,
              decoration: const InputDecoration(
                  labelText: 'API ADDRESS', hintText: '192.168.0.10'),
              onChanged: (value) {
                setState(() {
                  _urlController.text = value;
                });
              },
            ),
            //
            const SizedBox(height: 16.0),
            // text field for port
            TextField(
                // allow only numbers
                inputFormatters: [
                  FilteringTextInputFormatter.allow(RegExp(r'[0-9]')),
                ],
                // set the keyboard to show numbers by default
                keyboardType: TextInputType.number,
                controller: _portController,
                decoration:
                    const InputDecoration(labelText: 'PORT', hintText: '8080'),
                onChanged: (value) {
                  setState(() {
                    _portController.text = value;
                  });
                }),
            const SizedBox(height: 16.0),
            // Dropdown of available clients to select from
            DropdownButton<String>(
              value: 'SMS-SENDER',
              icon: const Icon(Icons.arrow_downward),
              iconSize: 24,
              hint: const Text('Select Client ID'),
              elevation: 16,
              style: const TextStyle(color: Colors.blue),
              underline: Container(
                height: 2,
                color: Colors.blue,
              ),
              // add border
              borderRadius: BorderRadius.circular(10),
              onChanged: (String? newValue) {
                setState(() {
                  // concatinate the client id with the port
                  _clientID = '$newValue';
                });
              },
              items: <String>[
                'SMS-SENDER',
                'SMS-SENDER-1',
                'SMS-SENDER-2',
                'SMS-SENDER-3',
                'SMS-SENDER-4',
                'SMS-SENDER-5',
                'SMS-SENDER-6',
                'SMS-SENDER-7',
              ].map<DropdownMenuItem<String>>((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child:
                      Text(value, style: const TextStyle(color: Colors.blue)),
                );
              }).toList(),
            ),

            ElevatedButton(
              onPressed: () {
                // Save the API URL and navigate back to the home page
                // concatinate the ip address with the port and client id
                var apiUrl =
                    '${_urlController.text}:${_portController.text}:$_clientID';
                Navigator.pop(context, apiUrl);
              },
              child: const Text('Save'),
            ),
          ],
        ),
      ),
    );
  }
}
