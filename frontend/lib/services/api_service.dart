import '../models/task.dart';
import 'api_client.dart';

class ApiService {
  /// AI CLASSIFICATION
  static Future<Map<String, dynamic>> classifyTask(
    String title,
    String description,
  ) async {
    final res = await ApiClient.dio.post(
      '/classify',
      data: {"text": "$title $description"},
    );

    return res.data['analysis'];
  }

  /// FETCH TASKS
  static Future<List<Task>> fetchTasks() async {
    final res = await ApiClient.dio.get('/api/tasks');

    return (res.data as List)
        .map((e) => Task.fromJson(e))
        .toList();
  }

  /// CREATE TASK
  static Future<void> createTask(
    String title,
    String description,
    String category,
    String priority,
  ) async {
    await ApiClient.dio.post(
      '/api/tasks',
      data: {
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
      },
    );
  }
}
