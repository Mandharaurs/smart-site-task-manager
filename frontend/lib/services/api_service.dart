import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config.dart';
import '../models/task.dart';

class ApiService {
  // CLASSIFY TASK
  static Future<Map<String, dynamic>> classifyTask(
      String title, String description) async {
    final response = await http.post(
      Uri.parse("${AppConfig.baseUrl}/classify"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "text": "$title $description",
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body)["analysis"];
    } else {
      throw Exception("Failed to classify task");
    }
  }

  // CREATE TASK
  static Future<void> createTask(
      String title, String description) async {
    final response = await http.post(
      Uri.parse("${AppConfig.baseUrl}/api/tasks"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "title": title,
        "description": description,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception("Failed to create task");
    }
  }

  // FETCH TASKS
  static Future<List<Task>> fetchTasks() async {
    final response =
        await http.get(Uri.parse("${AppConfig.baseUrl}/api/tasks"));

    if (response.statusCode == 200) {
      final List data = jsonDecode(response.body);
      return data.map((e) => Task.fromJson(e)).toList();
    } else {
      throw Exception("Failed to fetch tasks");
    }
  }
}
